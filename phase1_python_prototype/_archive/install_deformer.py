"""
Maya Installation and Setup Script for ML Corrective Deformer
Run this script in Maya's Script Editor to install and test the deformer.
"""

import maya.cmds as cmds
import maya.mel as mel
import sys
import os

def install_ml_deformer():
    """
    Install the ML Corrective Deformer plugin and set up the test environment.
    """
    # Get the plugin path
    script_dir = os.path.dirname(__file__)
    plugin_path = os.path.join(script_dir, "ml_corrective_deformer.py")
    
    # Load the plugin
    try:
        cmds.loadPlugin(plugin_path)
        print("✓ ML Corrective Deformer plugin loaded successfully")
    except Exception as e:
        print(f"✗ Failed to load plugin: {e}")
        return False
    
    # Create shelf button
    create_shelf_button()
    
    # Create test setup
    create_test_scene()
    
    return True

def create_shelf_button():
    """
    Create a shelf button for easy access to the deformer.
    """
    # Get the current shelf
    current_shelf = cmds.tabLayout("ShelfLayout", query=True, selectTab=True)
    
    # Shelf button command
    button_command = '''
import maya.cmds as cmds

# Apply ML Corrective Deformer to selected objects
selected = cmds.ls(selection=True)
if selected:
    for obj in selected:
        cmds.select(obj)
        deformer = cmds.deformer(type="mlCorrectiveDeformer")[0]
        print(f"Applied ML Corrective Deformer to {obj}: {deformer}")
else:
    print("Please select an object to apply the ML Corrective Deformer")
'''
    
    # Create the shelf button
    try:
        cmds.shelfButton(
            parent=current_shelf,
            image="polyBevel.png",  # Use a built-in Maya icon
            command=button_command,
            annotation="Apply ML Corrective Deformer to selected objects",
            label="ML Deformer"
        )
        print("✓ Shelf button created")
    except Exception as e:
        print(f"✗ Failed to create shelf button: {e}")

def create_test_scene():
    """
    Create a test scene with geometry and joints for testing the deformer.
    """
    # Clear the scene
    cmds.file(new=True, force=True)
    
    # Create test geometry - an arm-like shape
    arm_curve = cmds.curve(
        degree=1,
        point=[(0, 0, 0), (0, 4, 0), (0, 6, 1), (0, 8, 0)],
        name="armCurve"
    )
    
    # Extrude to create arm geometry
    arm_surface = cmds.extrude(
        arm_curve,
        constructionHistory=True,
        range=True,
        polygon=True,
        extrudeType=2,
        fixedPath=True,
        useComponentPivot=1,
        centerPivot=True,
        direction=(1, 0, 0),
        pivot=(0, 0, 0),
        scale=1,
        length=0.5
    )[0]
    
    cmds.rename(arm_surface, "testArm")
    
    # Create joint chain
    cmds.select(clear=True)
    shoulder_joint = cmds.joint(name="shoulder", position=[0, 0, 0])
    elbow_joint = cmds.joint(name="elbow", position=[0, 4, 0])
    wrist_joint = cmds.joint(name="wrist", position=[0, 8, 0])
    
    # Orient joints
    cmds.joint(shoulder_joint, edit=True, orientJoint="xyz", secondaryAxisOrient="yup", children=True)
    cmds.joint(wrist_joint, edit=True, orientJoint="none")
    
    # Bind skin
    cmds.select("testArm", shoulder_joint)
    skin_cluster = cmds.skinCluster(
        toSelectedBones=True,
        bindMethod=0,
        skinMethod=0,
        normalizeWeights=1
    )[0]
    
    # Apply ML deformer
    cmds.select("testArm")
    ml_deformer = cmds.deformer(type="mlCorrectiveDeformer")[0]
    
    # Connect elbow rotation to ML deformer
    cmds.connectAttr(f"{elbow_joint}.rotateZ", f"{ml_deformer}.poseAngle")
    
    # Set up initial pose
    cmds.setAttr(f"{elbow_joint}.rotateZ", 0)
    cmds.setAttr(f"{ml_deformer}.correctionWeight", 1.0)
    cmds.setAttr(f"{ml_deformer}.enableML", True)
    
    # Create animation for testing
    cmds.setKeyframe(elbow_joint, attribute="rotateZ", time=1, value=0)
    cmds.setKeyframe(elbow_joint, attribute="rotateZ", time=50, value=90)
    cmds.setKeyframe(elbow_joint, attribute="rotateZ", time=100, value=0)
    
    # Select the elbow for easy testing
    cmds.select(elbow_joint)
    
    print("✓ Test scene created with arm geometry and joints")
    print(f"  - Test geometry: testArm")
    print(f"  - Joints: {shoulder_joint}, {elbow_joint}, {wrist_joint}")
    print(f"  - ML Deformer: {ml_deformer}")
    print(f"  - Rotate '{elbow_joint}' Z-axis to see corrective deformation")
    print(f"  - Animation: Play timeline to see automatic correction")

def create_ui_window():
    """
    Create a simple UI window for the ML Corrective Deformer.
    """
    window_name = "mlCorrectiveDeformerWindow"
    
    # Delete existing window
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)
    
    # Create new window
    window = cmds.window(
        window_name,
        title="ML Corrective Deformer - Phase 1",
        widthHeight=(300, 200),
        resizeToFitChildren=True
    )
    
    # Main layout
    main_layout = cmds.columnLayout(adjustableColumn=True, marginWidth=10, marginHeight=10)
    
    cmds.text(label="ML Corrective Deformer Tool", font="boldLabelFont")
    cmds.separator(height=10)
    
    # Buttons
    cmds.button(
        label="Apply to Selected",
        command=lambda x: apply_to_selected(),
        height=30,
        backgroundColor=[0.4, 0.6, 0.4]
    )
    
    cmds.separator(height=5)
    
    cmds.button(
        label="Create Test Scene",
        command=lambda x: create_test_scene(),
        height=25
    )
    
    cmds.button(
        label="Load Model (Placeholder)",
        command=lambda x: load_model_dialog(),
        height=25
    )
    
    cmds.separator(height=10)
    cmds.text(label="Phase 1: Python Prototype", font="smallPlainLabelFont")
    
    cmds.showWindow(window)

def apply_to_selected():
    """
    Apply the ML deformer to selected objects.
    """
    selected = cmds.ls(selection=True)
    if not selected:
        cmds.warning("Please select an object to apply the ML Corrective Deformer")
        return
    
    for obj in selected:
        cmds.select(obj)
        deformer = cmds.deformer(type="mlCorrectiveDeformer")[0]
        print(f"Applied ML Corrective Deformer to {obj}: {deformer}")

def load_model_dialog():
    """
    Placeholder for model loading dialog.
    """
    cmds.confirmDialog(
        title="Load ML Model",
        message="Model loading will be implemented in Phase 2\nwith PyTorch integration.",
        button=["OK"]
    )

# Main execution
if __name__ == "__main__":
    print("Installing ML Corrective Deformer...")
    if install_ml_deformer():
        print("✓ Installation completed successfully!")
        create_ui_window()
    else:
        print("✗ Installation failed!")