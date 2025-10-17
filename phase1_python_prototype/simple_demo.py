"""
Simple ML Corrective Deformer Demo for Maya 2026
This creates a demo scene with a lattice-based deformer driven by joint rotation
"""

import maya.cmds as cmds
import math

def create_demo_scene():
    """
    Create a simple demo scene showing ML-style corrective deformation
    """
    # Clear scene
    cmds.file(new=True, force=True)
    
    # Create a cylinder (arm-like shape)
    cylinder = cmds.polyCylinder(name='arm_geo', radius=0.5, height=4, 
                                  subdivisionsX=20, subdivisionsY=20, 
                                  axis=[0, 1, 0])[0]
    cmds.move(0, 2, 0, cylinder)
    
    # Create joint chain
    cmds.select(clear=True)
    shoulder_joint = cmds.joint(name='shoulder', position=[0, 0, 0])
    elbow_joint = cmds.joint(name='elbow', position=[0, 2, 0])
    wrist_joint = cmds.joint(name='wrist', position=[0, 4, 0])
    cmds.joint(shoulder_joint, edit=True, orientJoint='xyz', secondaryAxisOrient='yup')
    
    # Bind skin
    cmds.select(cylinder, shoulder_joint, elbow_joint, wrist_joint)
    cmds.skinCluster(toSelectedBones=True, bindMethod=0, normalizeWeights=1)
    
    # Create a lattice for ML corrective simulation
    cmds.select(cylinder)
    lattice_deformer = cmds.lattice(divisions=[3, 5, 3], objectCentered=True, 
                                    ldivisions=[3, 5, 3])
    lattice_shape = lattice_deformer[1]
    lattice_base = lattice_deformer[2]
    
    # Create expression to simulate ML correction based on elbow rotation
    expression_code = """
// Simple ML-style corrective deformation
// This simulates what a trained neural network would predict

float $elbowRotZ = elbow.rotateZ;
float $bendAmount = $elbowRotZ / 90.0;  // Normalize to 0-1 range

// Apply corrective "bulge" when elbow bends
// This simulates muscle deformation

if ($bendAmount > 0) {
    // Outer lattice points bulge out (simulating bicep)
    ffd1Lattice.pt[0][2][1].xValue = $bendAmount * 0.3;
    ffd1Lattice.pt[2][2][1].xValue = -$bendAmount * 0.3;
    
    // Inner lattice points compress (simulating elbow collapse fix)
    ffd1Lattice.pt[1][1][1].xValue = -$bendAmount * 0.1;
    ffd1Lattice.pt[1][3][1].xValue = $bendAmount * 0.15;
}
"""
    
    cmds.expression(name='ML_Corrective_Expression', string=expression_code)
    
    # Set up scene
    cmds.setAttr('elbow.rotateZ', 0)
    cmds.viewFit(all=True)
    cmds.select(clear=True)
    
    # Create display text
    print("=" * 60)
    print("ML CORRECTIVE DEFORMER DEMO")
    print("=" * 60)
    print("This demonstrates ML-style corrective deformation.")
    print("")
    print("INSTRUCTIONS:")
    print("1. Select 'elbow' joint")
    print("2. Rotate Z-axis (Channel Box: Rotate Z)")
    print("3. Watch the corrective deformation activate")
    print("")
    print("The lattice simulates what a trained ML model would predict:")
    print("- Muscle bulge on the outside")
    print("- Elbow collapse correction on the inside")
    print("=" * 60)
    
    # Select elbow for easy manipulation
    cmds.select('elbow')
    
    return {
        'geometry': cylinder,
        'joints': [shoulder_joint, elbow_joint, wrist_joint],
        'lattice': lattice_deformer
    }

def animate_demo():
    """
    Create a simple animation of the demo
    """
    cmds.playbackOptions(min=1, max=120, animationStartTime=1, animationEndTime=120)
    
    # Animate elbow rotation
    cmds.setKeyframe('elbow', attribute='rotateZ', time=1, value=0)
    cmds.setKeyframe('elbow', attribute='rotateZ', time=60, value=90)
    cmds.setKeyframe('elbow', attribute='rotateZ', time=120, value=0)
    
    # Set tangents to smooth
    cmds.keyTangent('elbow', attribute='rotateZ', inTangentType='spline', outTangentType='spline')
    
    print("Animation created! Press Play to see the ML corrective in action.")

def toggle_corrective(enable=True):
    """
    Toggle the corrective deformation on/off for comparison
    """
    if cmds.objExists('ffd1'):
        # Instead of disabling expression, we'll adjust the lattice envelope
        cmds.setAttr('ffd1.envelope', 1 if enable else 0)
        state = "ENABLED" if enable else "DISABLED"
        print(f"ML Corrective: {state}")
    else:
        print("Demo scene not found. Run create_demo_scene() first.")

# Easy-to-use functions
def demo():
    """Quick setup - creates scene and animation"""
    create_demo_scene()
    animate_demo()
    print("\nDemo ready! Press PLAY or rotate the 'elbow' joint manually.")

def on():
    """Turn corrective ON"""
    toggle_corrective(True)

def off():
    """Turn corrective OFF for comparison"""
    toggle_corrective(False)

if __name__ == "__main__":
    print("ML Corrective Deformer Demo")
    print("Run: demo() to create the scene")
    print("Run: on() or off() to toggle the corrective")
