"""
Data Collection Tool for ML Corrective Deformer
Captures pose data and corrective shapes from Maya for training.
"""

import maya.cmds as cmds
import maya.api.OpenMaya as om
import numpy as np
import json
import os
from datetime import datetime


class DataCollector:
    """
    Collects training data from Maya rigs and corrective blendshapes.
    """
    
    def __init__(self, base_mesh, joints, corrective_mesh=None):
        """
        Initialize data collector.
        
        Args:
            base_mesh (str): Name of the base mesh (with skinning)
            joints (list): List of joint names to track
            corrective_mesh (str): Optional corrective target mesh
        """
        self.base_mesh = base_mesh
        self.joints = joints
        self.corrective_mesh = corrective_mesh
        
        self.samples = []
        self.num_vertices = self._get_vertex_count(base_mesh)
        
        print(f"DataCollector initialized:")
        print(f"  Base mesh: {base_mesh} ({self.num_vertices} vertices)")
        print(f"  Tracking {len(joints)} joints: {', '.join(joints)}")
    
    def _get_vertex_count(self, mesh):
        """Get number of vertices in mesh."""
        return cmds.polyEvaluate(mesh, vertex=True)
    
    def _get_joint_angles(self):
        """
        Get current rotation angles for all tracked joints.
        
        Returns:
            list: List of joint angles [rx, ry, rz] for each joint
        """
        angles = []
        for joint in self.joints:
            rx = cmds.getAttr(f"{joint}.rotateX")
            ry = cmds.getAttr(f"{joint}.rotateY")
            rz = cmds.getAttr(f"{joint}.rotateZ")
            angles.extend([rx, ry, rz])
        return angles
    
    def _get_vertex_positions(self, mesh):
        """
        Get vertex positions for a mesh.
        
        Returns:
            np.array: Vertex positions [num_vertices, 3]
        """
        # Get mesh as MObject
        sel_list = om.MSelectionList()
        sel_list.add(mesh)
        dag_path = sel_list.getDagPath(0)
        
        # Get vertex positions
        mesh_fn = om.MFnMesh(dag_path)
        points = mesh_fn.getPoints(om.MSpace.kWorld)
        
        # Convert to numpy array
        positions = np.array([[p.x, p.y, p.z] for p in points])
        return positions
    
    def _calculate_vertex_deltas(self, base_positions, corrective_positions):
        """
        Calculate vertex displacement deltas.
        
        Args:
            base_positions (np.array): Base mesh positions
            corrective_positions (np.array): Corrected mesh positions
        
        Returns:
            np.array: Vertex deltas [num_vertices, 3]
        """
        return corrective_positions - base_positions
    
    def capture_sample(self, corrective_mesh=None):
        """
        Capture a single training sample at the current pose.
        
        Args:
            corrective_mesh (str): Optional override for corrective mesh
        
        Returns:
            dict: Sample data
        """
        # Get current joint angles
        joint_angles = self._get_joint_angles()
        
        # Get base mesh positions
        base_positions = self._get_vertex_positions(self.base_mesh)
        
        # Get corrective mesh positions (if provided)
        target_mesh = corrective_mesh or self.corrective_mesh
        if target_mesh and cmds.objExists(target_mesh):
            corrective_positions = self._get_vertex_positions(target_mesh)
            vertex_deltas = self._calculate_vertex_deltas(base_positions, corrective_positions)
        else:
            # No corrective mesh - deltas are zero
            vertex_deltas = np.zeros_like(base_positions)
        
        sample = {
            'joint_angles': joint_angles,
            'vertex_deltas': vertex_deltas,
            'timestamp': datetime.now().isoformat()
        }
        
        self.samples.append(sample)
        print(f"Captured sample #{len(self.samples)} "
              f"(joint angles: {len(joint_angles)}, "
              f"vertices: {len(vertex_deltas)})")
        
        return sample
    
    def capture_pose_range(self, joint, axis='rotateZ', start=-90, end=90, steps=10):
        """
        Automatically capture samples across a range of poses.
        
        Args:
            joint (str): Joint to rotate
            axis (str): Rotation axis (rotateX, rotateY, or rotateZ)
            start (float): Start angle
            end (float): End angle
            steps (int): Number of samples to capture
        """
        print(f"\nCapturing pose range for {joint}.{axis}:")
        print(f"  Range: {start}° to {end}° ({steps} steps)")
        
        # Store original value
        original_value = cmds.getAttr(f"{joint}.{axis}")
        
        # Capture samples
        angles = np.linspace(start, end, steps)
        for i, angle in enumerate(angles):
            cmds.setAttr(f"{joint}.{axis}", angle)
            cmds.refresh()  # Update viewport
            self.capture_sample()
            print(f"  Progress: {i+1}/{steps} ({angle:.1f}°)")
        
        # Restore original value
        cmds.setAttr(f"{joint}.{axis}", original_value)
        
        print(f"✓ Captured {steps} samples")
    
    def save_dataset(self, filepath):
        """
        Save collected samples to file.
        
        Args:
            filepath (str): Path to save dataset (.npz format)
        """
        if not self.samples:
            print("No samples to save!")
            return
        
        # Convert to numpy arrays
        joint_angles = np.array([s['joint_angles'] for s in self.samples])
        vertex_deltas = np.array([s['vertex_deltas'] for s in self.samples])
        
        # Normalize joint angles to [-1, 1] range
        joint_angles_normalized = np.deg2rad(joint_angles)  # Convert to radians
        joint_angles_normalized = joint_angles_normalized / np.pi  # Normalize to [-1, 1]
        
        # Save as npz
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        np.savez_compressed(
            filepath,
            joint_angles=joint_angles_normalized,
            vertex_deltas=vertex_deltas,
            joint_names=self.joints,
            num_vertices=self.num_vertices
        )
        
        print(f"\n✓ Dataset saved: {filepath}")
        print(f"  Samples: {len(self.samples)}")
        print(f"  Joint angles shape: {joint_angles_normalized.shape}")
        print(f"  Vertex deltas shape: {vertex_deltas.shape}")
        
        # Save metadata
        metadata = {
            'num_samples': len(self.samples),
            'num_joints': len(self.joints),
            'joint_names': self.joints,
            'num_vertices': self.num_vertices,
            'base_mesh': self.base_mesh,
            'creation_date': datetime.now().isoformat()
        }
        
        metadata_path = filepath.replace('.npz', '_metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✓ Metadata saved: {metadata_path}")
    
    def clear_samples(self):
        """Clear all collected samples."""
        self.samples = []
        print("Cleared all samples")


class CorrectiveSculptingTool:
    """
    Interactive tool for sculpting corrective shapes and capturing data.
    """
    
    def __init__(self, base_mesh, joints):
        """
        Initialize sculpting tool.
        
        Args:
            base_mesh (str): Base mesh name
            joints (list): List of joint names
        """
        self.base_mesh = base_mesh
        self.joints = joints
        self.current_corrective = None
        self.collector = DataCollector(base_mesh, joints)
    
    def create_corrective_duplicate(self):
        """
        Create a duplicate of the base mesh for sculpting corrections.
        
        Returns:
            str: Name of corrective mesh
        """
        # Duplicate base mesh
        corrective = cmds.duplicate(self.base_mesh, name=f"{self.base_mesh}_corrective")[0]
        
        # Remove skin cluster from duplicate
        skin_cluster = self._get_skin_cluster(corrective)
        if skin_cluster:
            cmds.delete(skin_cluster)
        
        # Offset slightly for visibility
        cmds.move(5, 0, 0, corrective, relative=True)
        
        self.current_corrective = corrective
        self.collector.corrective_mesh = corrective
        
        print(f"Created corrective mesh: {corrective}")
        print("Sculpt this mesh to create the corrective shape")
        
        return corrective
    
    def _get_skin_cluster(self, mesh):
        """Get skin cluster attached to mesh."""
        history = cmds.listHistory(mesh, pruneDagObjects=True)
        skin_clusters = cmds.ls(history, type='skinCluster')
        return skin_clusters[0] if skin_clusters else None
    
    def capture_corrective(self):
        """Capture the current sculpted corrective."""
        if not self.current_corrective:
            print("No corrective mesh created!")
            return
        
        self.collector.capture_sample(self.current_corrective)
    
    def reset_corrective(self):
        """Delete corrective mesh and create a fresh one."""
        if self.current_corrective and cmds.objExists(self.current_corrective):
            cmds.delete(self.current_corrective)
        self.create_corrective_duplicate()
    
    def save_dataset(self, filepath):
        """Save collected corrective data."""
        self.collector.save_dataset(filepath)


# UI Functions
def create_data_collection_ui():
    """
    Create Maya UI for data collection.
    """
    window_name = "mlDataCollectionWindow"
    
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)
    
    window = cmds.window(
        window_name,
        title="ML Data Collection Tool",
        widthHeight=(400, 500),
        resizeToFitChildren=True
    )
    
    main_layout = cmds.columnLayout(adjustableColumn=True, marginWidth=10, marginHeight=10)
    
    # Header
    cmds.text(label="ML Corrective Deformer", font="boldLabelFont")
    cmds.text(label="Data Collection Tool", font="smallPlainLabelFont")
    cmds.separator(height=15)
    
    # Setup section
    cmds.frameLayout(label="1. Setup", collapsable=True, collapse=False)
    cmds.columnLayout(adjustableColumn=True)
    
    cmds.text(label="Base Mesh:", align='left')
    base_mesh_field = cmds.textField(placeholderText="Select mesh and click 'Load'")
    cmds.button(label="Load Selected Mesh", command=lambda x: load_selected_mesh(base_mesh_field))
    
    cmds.separator(height=5)
    cmds.text(label="Joints (comma-separated):", align='left')
    joints_field = cmds.textField(placeholderText="e.g., shoulder, elbow, wrist")
    cmds.button(label="Load Selected Joints", command=lambda x: load_selected_joints(joints_field))
    
    cmds.setParent('..')
    cmds.setParent('..')
    
    # Capture section
    cmds.frameLayout(label="2. Capture Data", collapsable=True, collapse=False)
    cmds.columnLayout(adjustableColumn=True)
    
    cmds.button(
        label="Initialize Collector",
        height=30,
        backgroundColor=[0.4, 0.6, 0.4],
        command=lambda x: init_collector(base_mesh_field, joints_field)
    )
    
    cmds.separator(height=10)
    cmds.button(label="Capture Current Pose", command=lambda x: capture_current())
    cmds.button(label="Create Corrective Duplicate", command=lambda x: create_corrective())
    cmds.button(label="Capture with Corrective", command=lambda x: capture_corrective())
    
    cmds.separator(height=10)
    cmds.text(label="Auto-Capture Range:", align='left')
    cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, 195), (2, 195)])
    joint_field = cmds.textField(placeholderText="Joint name")
    axis_field = cmds.optionMenu(label="Axis")
    cmds.menuItem(label="rotateX")
    cmds.menuItem(label="rotateY")
    cmds.menuItem(label="rotateZ")
    cmds.setParent('..')
    
    cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[(1, 130), (2, 130), (3, 130)])
    start_field = cmds.intField(value=-90)
    end_field = cmds.intField(value=90)
    steps_field = cmds.intField(value=10)
    cmds.setParent('..')
    
    cmds.button(
        label="Auto-Capture Range",
        command=lambda x: auto_capture_range(joint_field, axis_field, start_field, end_field, steps_field)
    )
    
    cmds.setParent('..')
    cmds.setParent('..')
    
    # Save section
    cmds.frameLayout(label="3. Save Dataset", collapsable=True, collapse=False)
    cmds.columnLayout(adjustableColumn=True)
    
    cmds.text(label="Samples Collected: 0", name="sampleCountText")
    cmds.separator(height=5)
    
    save_path_field = cmds.textField(text="../data/training_data.npz")
    cmds.button(label="Save Dataset", command=lambda x: save_dataset(save_path_field))
    cmds.button(label="Clear Samples", command=lambda x: clear_samples())
    
    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.showWindow(window)
    
    return window


# Global collector instance
_collector = None
_sculpting_tool = None


def load_selected_mesh(text_field):
    """Load selected mesh into text field."""
    sel = cmds.ls(selection=True, type='transform')
    if sel:
        cmds.textField(text_field, edit=True, text=sel[0])
        print(f"Loaded mesh: {sel[0]}")


def load_selected_joints(text_field):
    """Load selected joints into text field."""
    sel = cmds.ls(selection=True, type='joint')
    if sel:
        joints_str = ', '.join(sel)
        cmds.textField(text_field, edit=True, text=joints_str)
        print(f"Loaded joints: {joints_str}")


def init_collector(base_mesh_field, joints_field):
    """Initialize the data collector."""
    global _collector, _sculpting_tool
    
    base_mesh = cmds.textField(base_mesh_field, query=True, text=True)
    joints_str = cmds.textField(joints_field, query=True, text=True)
    joints = [j.strip() for j in joints_str.split(',')]
    
    if not base_mesh or not joints:
        cmds.warning("Please specify base mesh and joints")
        return
    
    _collector = DataCollector(base_mesh, joints)
    _sculpting_tool = CorrectiveSculptingTool(base_mesh, joints)
    print("✓ Collector initialized")


def capture_current():
    """Capture current pose."""
    if _collector:
        _collector.capture_sample()
        update_sample_count()


def create_corrective():
    """Create corrective duplicate."""
    if _sculpting_tool:
        _sculpting_tool.create_corrective_duplicate()


def capture_corrective():
    """Capture with corrective."""
    if _sculpting_tool:
        _sculpting_tool.capture_corrective()
        update_sample_count()


def auto_capture_range(joint_field, axis_field, start_field, end_field, steps_field):
    """Auto-capture pose range."""
    if not _collector:
        cmds.warning("Please initialize collector first")
        return
    
    joint = cmds.textField(joint_field, query=True, text=True)
    axis = cmds.optionMenu(axis_field, query=True, value=True)
    start = cmds.intField(start_field, query=True, value=True)
    end = cmds.intField(end_field, query=True, value=True)
    steps = cmds.intField(steps_field, query=True, value=True)
    
    _collector.capture_pose_range(joint, axis, start, end, steps)
    update_sample_count()


def save_dataset(save_path_field):
    """Save the dataset."""
    if _collector:
        filepath = cmds.textField(save_path_field, query=True, text=True)
        _collector.save_dataset(filepath)


def clear_samples():
    """Clear all samples."""
    if _collector:
        _collector.clear_samples()
        update_sample_count()


def update_sample_count():
    """Update sample count in UI."""
    if _collector and cmds.text("sampleCountText", exists=True):
        count = len(_collector.samples)
        cmds.text("sampleCountText", edit=True, label=f"Samples Collected: {count}")


if __name__ == "__main__":
    create_data_collection_ui()
