"""
Example 2: Data Collection
Demonstrates how to collect training data from Maya
"""

import maya.cmds as cmds
import sys
import os

# Add project to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from utils.data_collector import DataCollector


def collect_simple_elbow_data():
    """
    Collect training data for a simple elbow correction
    """
    print("Creating test rig for data collection...")
    
    # Create arm mesh
    arm = cmds.polyCylinder(name="dataArm", radius=0.5, height=4, 
                            subdivisionsAxis=16, subdivisionsCaps=3)[0]
    cmds.move(0, 2, 0, arm)
    
    # Create joints
    cmds.select(clear=True)
    shoulder = cmds.joint(name="dataShoulder", position=[0, 0, 0])
    elbow = cmds.joint(name="dataElbow", position=[0, 2, 0])
    wrist = cmds.joint(name="dataWrist", position=[0, 4, 0])
    
    # Bind skin
    cmds.select(arm, shoulder)
    cmds.skinCluster(toSelectedBones=True)
    
    print("✓ Test rig created")
    
    # Initialize data collector
    joints_to_track = [shoulder, elbow, wrist]
    collector = DataCollector(arm, joints_to_track)
    
    # Collect data across elbow bend range
    print("\nCollecting training data...")
    collector.capture_pose_range(
        joint=elbow,
        axis="rotateZ",
        start=0,
        end=120,
        steps=15
    )
    
    # Save dataset
    save_path = os.path.join(project_root, "data", "example_elbow_data.npz")
    collector.save_dataset(save_path)
    
    print(f"\n✓ Data collection complete!")
    print(f"✓ Dataset saved to: {save_path}")
    
    return collector


def collect_with_corrective_sculpting():
    """
    Collect data with manually sculpted corrective shapes
    """
    print("Creating rig for corrective sculpting...")
    
    # Create test mesh
    mesh = cmds.polyCube(name="sculptMesh", sx=8, sy=8, sz=8)[0]
    
    # Create joint
    cmds.select(clear=True)
    joint = cmds.joint(name="sculptJoint", position=[0, 0, 0])
    
    # Initialize collector
    collector = DataCollector(mesh, [joint])
    
    # Create corrective duplicate
    corrective = cmds.duplicate(mesh, name=f"{mesh}_corrective")[0]
    cmds.move(5, 0, 0, corrective, relative=True)
    
    print("✓ Corrective mesh created")
    print("\nWorkflow:")
    print("1. Set joint to desired pose")
    print("2. Sculpt corrections on the duplicate mesh")
    print("3. Run collector.capture_sample(corrective_mesh='...')")
    print("4. Repeat for multiple poses")
    print("5. Save dataset")
    
    # Example: Capture at a specific pose
    cmds.setAttr(f"{joint}.rotateZ", 45)
    
    # In practice, artist would sculpt here
    # For demo, we'll just capture without sculpting
    collector.capture_sample()
    
    return collector, corrective


def collect_multi_axis_data():
    """
    Collect data across multiple rotation axes
    """
    print("Collecting multi-axis data...")
    
    # Create test setup
    mesh = cmds.polySphere(name="multiAxisMesh", radius=2, subdivisionsAxis=16, subdivisionsHeight=16)[0]
    
    cmds.select(clear=True)
    root = cmds.joint(name="multiRoot", position=[0, 0, 0])
    joint = cmds.joint(name="multiJoint", position=[0, 2, 0])
    
    cmds.select(mesh, root)
    cmds.skinCluster(toSelectedBones=True)
    
    # Initialize collector
    collector = DataCollector(mesh, [root, joint])
    
    # Collect data on X axis
    print("\nCapturing X-axis rotations...")
    collector.capture_pose_range(joint, "rotateX", -45, 45, 10)
    
    # Collect data on Y axis
    print("\nCapturing Y-axis rotations...")
    collector.capture_pose_range(joint, "rotateY", -45, 45, 10)
    
    # Collect data on Z axis
    print("\nCapturing Z-axis rotations...")
    collector.capture_pose_range(joint, "rotateZ", -45, 45, 10)
    
    # Save
    save_path = os.path.join(project_root, "data", "multi_axis_data.npz")
    collector.save_dataset(save_path)
    
    print(f"\n✓ Multi-axis data saved to: {save_path}")
    
    return collector


def demonstrate_data_collection_workflow():
    """
    Complete workflow demonstration
    """
    print("="*60)
    print("ML Corrective Deformer - Data Collection Examples")
    print("="*60)
    
    # Example 1: Simple elbow data
    print("\n" + "="*60)
    print("Example 1: Simple Elbow Correction Data")
    print("="*60)
    collector1 = collect_simple_elbow_data()
    
    # Example 2: With corrective sculpting (setup only)
    print("\n" + "="*60)
    print("Example 2: Corrective Sculpting Workflow")
    print("="*60)
    collector2, corrective = collect_with_corrective_sculpting()
    
    # Example 3: Multi-axis data
    print("\n" + "="*60)
    print("Example 3: Multi-Axis Data Collection")
    print("="*60)
    collector3 = collect_multi_axis_data()
    
    print("\n" + "="*60)
    print("Data Collection Examples Complete!")
    print("="*60)
    print("\nNext Steps:")
    print("1. Check the 'data' folder for generated datasets")
    print("2. Train models using: python ml_training/train.py")
    print("3. Deploy trained models in Maya (Phase 2)")


if __name__ == "__main__":
    demonstrate_data_collection_workflow()
