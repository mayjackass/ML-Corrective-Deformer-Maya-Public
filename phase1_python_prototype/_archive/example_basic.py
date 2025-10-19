"""
Example 1: Basic Deformer Application
Shows how to apply the ML corrective deformer to a mesh
"""

import maya.cmds as cmds

def apply_ml_deformer_basic():
    """
    Simple example of applying the ML corrective deformer
    """
    # Create test geometry
    mesh = cmds.polyCube(name="simpleCube", width=2, height=4, depth=2)[0]
    
    # Create a joint
    cmds.select(clear=True)
    joint = cmds.joint(name="bendJoint", position=[0, 0, 0])
    
    # Apply deformer to mesh
    cmds.select(mesh)
    deformer = cmds.deformer(type="mlCorrectiveDeformer")[0]
    
    # Connect joint rotation to deformer
    cmds.connectAttr(f"{joint}.rotateZ", f"{deformer}.poseAngle")
    
    # Set deformer attributes
    cmds.setAttr(f"{deformer}.correctionWeight", 1.0)
    cmds.setAttr(f"{deformer}.enableML", True)
    
    print(f"✓ Applied {deformer} to {mesh}")
    print(f"✓ Connected {joint}.rotateZ to {deformer}.poseAngle")
    print(f"\nRotate {joint} to see the corrective deformation!")
    
    return mesh, joint, deformer


def create_arm_rig():
    """
    Create a simple arm rig for testing
    """
    # Create arm geometry
    arm = cmds.polyCylinder(name="arm", radius=0.5, height=4, 
                            subdivisionsCaps=3, subdivisionsAxis=16)[0]
    cmds.move(0, 2, 0, arm)
    
    # Create joint chain
    cmds.select(clear=True)
    shoulder = cmds.joint(name="shoulder", position=[0, 0, 0])
    elbow = cmds.joint(name="elbow", position=[0, 2, 0])
    wrist = cmds.joint(name="wrist", position=[0, 4, 0])
    
    # Orient joints
    cmds.joint(shoulder, edit=True, orientJoint="xyz", secondaryAxisOrient="yup")
    
    # Bind skin
    cmds.select(arm, shoulder)
    skin_cluster = cmds.skinCluster(toSelectedBones=True)[0]
    
    # Apply ML deformer
    cmds.select(arm)
    deformer = cmds.deformer(type="mlCorrectiveDeformer")[0]
    
    # Connect elbow rotation
    cmds.connectAttr(f"{elbow}.rotateZ", f"{deformer}.poseAngle")
    
    # Add keyframes for testing
    cmds.setKeyframe(elbow, attribute="rotateZ", time=1, value=0)
    cmds.setKeyframe(elbow, attribute="rotateZ", time=50, value=90)
    cmds.setKeyframe(elbow, attribute="rotateZ", time=100, value=0)
    
    print(f"✓ Created arm rig with ML deformer")
    print(f"✓ Play timeline to see animation with corrections")
    
    return arm, [shoulder, elbow, wrist], deformer


def test_multiple_joints():
    """
    Example with multiple joints affecting the deformer
    """
    # Create mesh
    mesh = cmds.polyCube(name="multiJointMesh", sx=8, sy=8, sz=8)[0]
    
    # Create multiple joints
    joints = []
    for i in range(3):
        cmds.select(clear=True)
        joint = cmds.joint(name=f"joint_{i}", position=[i*2, 0, 0])
        joints.append(joint)
    
    # Apply deformer
    cmds.select(mesh)
    deformer = cmds.deformer(type="mlCorrectiveDeformer")[0]
    
    # For Phase 1, we can only connect one joint
    # In Phase 2, we'll support multiple joint inputs
    cmds.connectAttr(f"{joints[1]}.rotateZ", f"{deformer}.poseAngle")
    
    print(f"✓ Created multi-joint test setup")
    print(f"Note: Phase 1 supports single joint input")
    print(f"Phase 2 will support multiple joint inputs")
    
    return mesh, joints, deformer


if __name__ == "__main__":
    # Run examples
    print("="*60)
    print("ML Corrective Deformer - Basic Examples")
    print("="*60)
    
    # Example 1: Basic application
    print("\n1. Basic Deformer Application")
    mesh1, joint1, deformer1 = apply_ml_deformer_basic()
    
    # Example 2: Arm rig
    print("\n2. Arm Rig with Animation")
    arm, arm_joints, arm_deformer = create_arm_rig()
    
    print("\n" + "="*60)
    print("Examples created successfully!")
    print("="*60)
