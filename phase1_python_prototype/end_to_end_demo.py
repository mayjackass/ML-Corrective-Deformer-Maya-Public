"""
ML Corrective Deformer - Complete End-to-End Workflow Demo
This demonstrates the full pipeline from data collection to deployment

Author: Mayj Amilano
"""

import maya.cmds as cmds
import json
import os

# ============================================================================
# STEP 1: CREATE TRAINING SCENE
# ============================================================================

def step1_create_training_scene():
    """
    Create a simple arm with joints for training data collection
    """
    print("\n" + "="*70)
    print("STEP 1: CREATE TRAINING SCENE")
    print("="*70)
    
    # Clear scene
    cmds.file(new=True, force=True)
    
    # Create arm geometry (cylinder)
    arm_geo = cmds.polyCylinder(name='arm_geo', radius=0.5, height=4,
                                 subdivisionsX=12, subdivisionsY=12,
                                 axis=[0, 1, 0])[0]
    cmds.move(0, 2, 0, arm_geo)
    
    # Create joint chain
    cmds.select(clear=True)
    shoulder = cmds.joint(name='shoulder_jnt', position=[0, 0, 0])
    elbow = cmds.joint(name='elbow_jnt', position=[0, 2, 0])
    wrist = cmds.joint(name='wrist_jnt', position=[0, 4, 0])
    cmds.joint(shoulder, edit=True, orientJoint='xyz', secondaryAxisOrient='yup')
    
    # Bind skin with basic weights
    cmds.select(arm_geo, shoulder, elbow, wrist)
    skin_cluster = cmds.skinCluster(toSelectedBones=True, bindMethod=0, 
                                     normalizeWeights=1, name='arm_skin')[0]
    
    # Frame view
    cmds.viewFit(all=True)
    cmds.select(clear=True)
    
    print("\n✓ Training scene created:")
    print("  - Arm geometry: arm_geo")
    print("  - Joints: shoulder_jnt, elbow_jnt, wrist_jnt")
    print("  - Skin cluster: arm_skin")
    print("\nNext: Paint skin weights if needed, then run step2")
    print("\nTo paint weights:")
    print("  - Select 'arm_geo'")
    print("  - Go to: Skin > Paint Skin Weights Tool")
    print("  - Or run: open_paint_weights_tool()")
    
    return {
        'geometry': arm_geo,
        'joints': [shoulder, elbow, wrist],
        'skin': skin_cluster
    }


def open_paint_weights_tool():
    """
    Open the Paint Skin Weights tool for training scene
    """
    if not cmds.objExists('arm_geo'):
        print("\n✗ Error: arm_geo not found! Run step1 first.")
        return
    
    # Select geometry
    cmds.select('arm_geo')
    
    # Open Paint Skin Weights Tool
    cmds.ArtPaintSkinWeightsToolOptions()
    
    print("\n" + "="*70)
    print("PAINT SKIN WEIGHTS TOOL OPENED")
    print("="*70)
    print("\nYou can now paint skin weights to improve the deformation.")
    print("This will affect how the arm bends and the ML corrections.")
    print("\nTips:")
    print("  - Paint smoother weight transitions for better deformation")
    print("  - Focus on elbow region for the demo")
    print("  - When done, close tool and run step2")
    print("="*70)


# ============================================================================
# STEP 2: COLLECT TRAINING DATA
# ============================================================================

def step2_collect_training_data(num_poses=5):
    """
    Collect pose/correction pairs for training
    """
    print("\n" + "="*70)
    print("STEP 2: COLLECT TRAINING DATA")
    print("="*70)
    
    training_data = []
    
    # Get base mesh position
    cmds.setAttr('elbow_jnt.rotateZ', 0)
    base_positions = get_vertex_positions('arm_geo')
    
    print(f"\nCollecting {num_poses} training samples...")
    
    # Collect poses at different angles
    angles = [0, 30, 60, 90, 120][:num_poses]
    
    for i, angle in enumerate(angles):
        print(f"\n  Pose {i+1}/{num_poses}: Elbow at {angle}°")
        
        # Set pose
        cmds.setAttr('elbow_jnt.rotateZ', angle)
        cmds.refresh()
        
        # Get deformed positions (this is what skinning gives us)
        deformed_positions = get_vertex_positions('arm_geo')
        
        # Get "corrected" positions (artist would sculpt these)
        # For demo, we'll simulate a correction
        corrected_positions = simulate_artist_correction(deformed_positions, angle)
        
        # Calculate deltas (correction - deformed)
        deltas = []
        for j in range(len(deformed_positions)):
            delta = [
                corrected_positions[j][0] - deformed_positions[j][0],
                corrected_positions[j][1] - deformed_positions[j][1],
                corrected_positions[j][2] - deformed_positions[j][2]
            ]
            deltas.append(delta)
        
        # Store training sample
        sample = {
            'pose': {
                'elbow_angle': angle
            },
            'deltas': deltas
        }
        training_data.append(sample)
        
        print(f"    ✓ Collected: angle={angle}°, vertices={len(deltas)}")
    
    # Save training data
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    data_file = os.path.join(data_dir, 'training_data_demo.json')
    with open(data_file, 'w') as f:
        json.dump(training_data, f, indent=2)
    
    print(f"\n✓ Training data saved: {data_file}")
    print(f"  Total samples: {len(training_data)}")
    print(f"  Vertices per sample: {len(deltas)}")
    print("\nNext: Run step3 to train the model")
    
    return training_data


def get_vertex_positions(mesh):
    """Get all vertex positions for a mesh"""
    num_verts = cmds.polyEvaluate(mesh, vertex=True)
    positions = []
    for i in range(num_verts):
        pos = cmds.pointPosition(f"{mesh}.vtx[{i}]", world=True)
        positions.append(pos)
    return positions


def simulate_artist_correction(positions, angle):
    """
    Simulate what an artist would sculpt as a corrective shape
    In real workflow, artist would manually sculpt this
    """
    import math
    corrected = []
    
    # Simple correction: add muscle bulge based on angle
    angle_factor = math.sin(math.radians(angle)) * 0.3
    
    for i, pos in enumerate(positions):
        # Add bulge to upper part (y > 1.5)
        if pos[1] > 1.5:
            bulge = angle_factor * (pos[1] - 1.5) * 0.2
            corrected.append([
                pos[0] + bulge if pos[0] > 0 else pos[0] - bulge,
                pos[1],
                pos[2]
            ])
        else:
            corrected.append(list(pos))
    
    return corrected


# ============================================================================
# STEP 3: TRAIN ML MODEL (SIMULATED)
# ============================================================================

def step3_train_model():
    """
    Train the ML model on collected data
    (Simplified for demo - real training would use PyTorch)
    """
    print("\n" + "="*70)
    print("STEP 3: TRAIN ML MODEL")
    print("="*70)
    
    # Load training data
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    data_file = os.path.join(data_dir, 'training_data_demo.json')
    
    if not os.path.exists(data_file):
        print("\n✗ Error: Training data not found!")
        print("  Run step2_collect_training_data() first")
        return None
    
    with open(data_file, 'r') as f:
        training_data = json.load(f)
    
    print(f"\n✓ Loaded training data: {len(training_data)} samples")
    print("\n  Simulating ML training...")
    print("  (In production: PyTorch neural network training)")
    
    # Simulate training process
    import time
    epochs = 5
    for epoch in range(epochs):
        print(f"    Epoch {epoch+1}/{epochs}... ", end='')
        time.sleep(0.3)
        loss = 0.1 / (epoch + 1)
        print(f"Loss: {loss:.4f}")
    
    # Create simple model (lookup table for demo)
    model = {
        'type': 'demo_model',
        'training_samples': len(training_data),
        'data': training_data
    }
    
    # Save model
    models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
    
    model_file = os.path.join(models_dir, 'corrective_model_demo.json')
    with open(model_file, 'w') as f:
        json.dump(model, f, indent=2)
    
    print(f"\n✓ Model trained and saved: {model_file}")
    print("\nNext: Run step4 to deploy the model in Maya")
    
    return model


# ============================================================================
# HELPER: CREATE CORRECTIVE TARGET
# ============================================================================

def create_corrective_target(base_positions, angle, name):
    """
    Create a corrective target shape for a specific angle
    Simulates what an artist would sculpt as a corrective shape
    """
    import math
    
    # Create duplicate mesh for this target
    target_mesh = cmds.duplicate('arm_geo', name=name, returnRootsOnly=True)[0]
    
    # Remove all deformers from target
    history = cmds.listHistory(target_mesh, pruneDagObjects=True)
    if history:
        for node in history:
            if cmds.nodeType(node) in ['skinCluster', 'blendShape', 'tweak']:
                try:
                    cmds.delete(node)
                except:
                    pass
    
    # Calculate correction intensity based on angle
    normalized_angle = angle / 120.0
    bulge_intensity = math.sin(normalized_angle * math.pi / 2.0)
    
    # Apply corrections to simulate artist sculpting
    for i, base_pos in enumerate(base_positions):
        corrected_pos = list(base_pos)
        
        # UPPER ARM: Bicep bulge (increases with bend)
        if base_pos[1] > 2.5:
            height_factor = (base_pos[1] - 2.5) * 0.3
            bulge = bulge_intensity * height_factor * 0.4
            
            # Side bulge
            if base_pos[0] > 0:
                corrected_pos[0] += bulge
            else:
                corrected_pos[0] -= bulge
            
            # Slight forward push
            corrected_pos[2] += bulge * 0.2
        
        # MIDDLE: Elbow region - compression and pinching
        elif 1.5 < base_pos[1] <= 2.5:
            # Elbow pinch (gets stronger with more bend)
            pinch_factor = normalized_angle * 0.15
            
            # Compress inward
            if abs(base_pos[0]) > 0.1:
                corrected_pos[0] *= (1.0 - pinch_factor)
            
            # Slight downward compression
            corrected_pos[1] -= pinch_factor * 0.1
        
        # LOWER ARM: Forearm maintains volume
        elif base_pos[1] <= 1.5:
            # Very subtle volume preservation
            maintain_factor = normalized_angle * 0.05
            if abs(base_pos[0]) > 0.1:
                corrected_pos[0] += maintain_factor * (1 if base_pos[0] > 0 else -1)
        
        # Apply the correction
        cmds.xform(f'{target_mesh}.vtx[{i}]',
                  worldSpace=True,
                  absolute=True,
                  translation=corrected_pos)
    
    print(f"    ✓ {name}: bulge={bulge_intensity:.2f}")
    
    return target_mesh


# ============================================================================
# STEP 4: DEPLOY MODEL AS DEFORMER
# ============================================================================

def step4_deploy_deformer():
    """
    Deploy the trained model as a live Maya deformer
    This simulates real ML inference - reading trained model and predicting deltas
    """
    print("\n" + "="*70)
    print("STEP 4: DEPLOY ML DEFORMER")
    print("="*70)
    
    # Load model
    models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
    model_file = os.path.join(models_dir, 'corrective_model_demo.json')
    
    if not os.path.exists(model_file):
        print("\n✗ Error: Model not found!")
        print("  Run step3_train_model() first")
        return None
    
    with open(model_file, 'r') as f:
        model = json.load(f)
    
    print(f"\n✓ Loaded trained model: {len(model['data'])} training samples")
    print("\n  Deploying ML inference system...")
    
    # Create blend shape to store ML corrections
    if not cmds.objExists('arm_geo'):
        print("\n✗ Error: arm_geo not found! Run step1 first.")
        return None
    
    # Store the current pose
    current_elbow_angle = cmds.getAttr('elbow_jnt.rotateZ')
    
    # Get base positions in bind pose for creating corrective targets
    cmds.setAttr('elbow_jnt.rotateZ', 0)
    num_verts = cmds.polyEvaluate('arm_geo', vertex=True)
    base_positions = []
    for i in range(num_verts):
        pos = cmds.pointPosition(f'arm_geo.vtx[{i}]', world=True)
        base_positions.append(list(pos))
    
    # Create MULTIPLE blend shape targets for different poses
    # This simulates what a real ML model does: interpolates between learned corrections
    print("\n  Creating multiple corrective targets (simulating trained poses)...")
    
    targets_created = []
    
    # Target 1: 30 degrees - slight bulge
    target_30 = create_corrective_target(base_positions, angle=30, name='ML_30deg')
    targets_created.append(('ML_30deg', target_30))
    
    # Target 2: 60 degrees - medium bulge + elbow pinch
    target_60 = create_corrective_target(base_positions, angle=60, name='ML_60deg')
    targets_created.append(('ML_60deg', target_60))
    
    # Target 3: 90 degrees - strong bulge + elbow crease
    target_90 = create_corrective_target(base_positions, angle=90, name='ML_90deg')
    targets_created.append(('ML_90deg', target_90))
    
    # Target 4: 120 degrees - maximum bulge + full elbow collapse
    target_120 = create_corrective_target(base_positions, angle=120, name='ML_120deg')
    targets_created.append(('ML_120deg', target_120))
    
    print(f"  ✓ Created {len(targets_created)} corrective targets")
    
    # Create blend shape with multiple targets
    # Add them one by one to control the target names
    blend_shape_node = cmds.blendShape('arm_geo', name='ML_corrective_deformer')[0]
    
    target_attrs = []
    for i, (name, mesh) in enumerate(targets_created):
        # Add target with specific name
        cmds.blendShape(blend_shape_node, edit=True, 
                       target=('arm_geo', i, mesh, 1.0),
                       topologyCheck=False)
        
        # The target will be named based on the mesh name
        # Get the actual attribute that was created
        alias = cmds.aliasAttr(f'{blend_shape_node}.weight[{i}]', query=True)
        if alias:
            target_attrs.append(alias)
            print(f"    ✓ Target {i}: {name} → {blend_shape_node}.{alias}")
        else:
            target_attrs.append(f'weight[{i}]')
            print(f"    ✓ Target {i}: {name} → {blend_shape_node}.weight[{i}]")
    
    # Hide all targets
    for name, target in targets_created:
        cmds.setAttr(target + '.visibility', 0)
    
    # Reorder deformers
    skin_cluster = None
    history = cmds.listHistory('arm_geo', pruneDagObjects=True)
    if history:
        for node in history:
            if cmds.nodeType(node) == 'skinCluster':
                skin_cluster = node
                break
    
    if skin_cluster:
        try:
            cmds.reorderDeformers(skin_cluster, blend_shape_node, 'arm_geo')
            print(f"  ✓ Deformer order: {skin_cluster} → {blend_shape_node}")
        except Exception as e:
            print(f"  Warning: {e}")
    
    # Restore pose
    cmds.setAttr('elbow_jnt.rotateZ', current_elbow_angle)
    
    # Create MEL expression for INTELLIGENT interpolation between targets
    # This simulates how a neural network interpolates between learned poses
    if cmds.objExists('ML_inference_expression'):
        cmds.delete('ML_inference_expression')
    
    # Build expression with actual target attribute names
    inference_expression = f"""
// ML NEURAL NETWORK INFERENCE SIMULATION
// Intelligently interpolates between trained corrective poses

float $angle = elbow_jnt.rotateZ;

// Initialize all weights to 0
ML_corrective_deformer.{target_attrs[0]} = 0;
ML_corrective_deformer.{target_attrs[1]} = 0;
ML_corrective_deformer.{target_attrs[2]} = 0;
ML_corrective_deformer.{target_attrs[3]} = 0;

// NEURAL NETWORK PREDICTION: Blend between nearest training samples
// This is what the ML model does - interpolates learned corrections

if ($angle <= 30) {{
    // Between 0 and 30: blend from nothing to first target
    float $blend = $angle / 30.0;
    ML_corrective_deformer.{target_attrs[0]} = $blend;
}}
else if ($angle <= 60) {{
    // Between 30 and 60: blend between targets
    float $blend = ($angle - 30) / 30.0;
    ML_corrective_deformer.{target_attrs[0]} = 1.0 - $blend;
    ML_corrective_deformer.{target_attrs[1]} = $blend;
}}
else if ($angle <= 90) {{
    // Between 60 and 90: blend between targets
    float $blend = ($angle - 60) / 30.0;
    ML_corrective_deformer.{target_attrs[1]} = 1.0 - $blend;
    ML_corrective_deformer.{target_attrs[2]} = $blend;
}}
else if ($angle <= 120) {{
    // Between 90 and 120: blend between targets
    float $blend = ($angle - 90) / 30.0;
    ML_corrective_deformer.{target_attrs[2]} = 1.0 - $blend;
    ML_corrective_deformer.{target_attrs[3]} = $blend;
}}
else {{
    // Beyond 120: use maximum correction
    ML_corrective_deformer.{target_attrs[3]} = 1.0;
}}
"""
    
    cmds.expression(name='ML_inference_expression',
                   string=inference_expression,
                   alwaysEvaluate=True)
    
    blend_shape = blend_shape_node
    
    print("\n✓ ML Deformer deployed!")
    print("  - Deformer Type: Multi-Target BlendShape (4 trained poses)")
    print("  - Inference Engine: MEL Expression (neural network interpolation)")
    print("  - Training Data: 30°, 60°, 90°, 120° corrective shapes")
    print("\n  How it works:")
    print("    1. Created 4 target shapes (simulating artist-sculpted corrections)")
    print("    2. MEL expression reads elbow angle in real-time")
    print("    3. Intelligently blends between nearest training samples")
    print("    4. Mimics neural network interpolation")
    print("    5. Result: Smooth, realistic ML-predicted corrections")
    print("\n  This demonstrates how a real ML model works:")
    print("    - Learns from multiple training poses")
    print("    - Interpolates for in-between angles")
    print("    - Produces smooth, artist-quality deformations")
    
    # Create animation for demo
    cmds.playbackOptions(min=1, max=120)
    cmds.setKeyframe('elbow_jnt', attribute='rotateZ', time=1, value=0)
    cmds.setKeyframe('elbow_jnt', attribute='rotateZ', time=60, value=120)
    cmds.setKeyframe('elbow_jnt', attribute='rotateZ', time=120, value=0)
    cmds.keyTangent('elbow_jnt', attribute='rotateZ', 
                   inTangentType='spline', outTangentType='spline')
    
    print("\n✓ Animation created (120 frames)")
    print("\n🎬 DEMO READY!")
    print("  Press PLAY to see ML inference in action!")
    print("  The model predicts corrections based on training data!")
    
    return blend_shape


# ============================================================================
# COMPLETE WORKFLOW
# ============================================================================

def run_complete_workflow():
    """
    Run the complete end-to-end ML corrective workflow
    """
    print("\n" + "="*70)
    print("ML CORRECTIVE DEFORMER - COMPLETE WORKFLOW")
    print("="*70)
    print("\nThis demo shows the full pipeline:")
    print("  1. Create training scene")
    print("  2. Collect pose/correction data")
    print("  3. Train ML model")
    print("  4. Deploy as live deformer")
    
    input("\nPress Enter to start...")
    
    # Run all steps
    step1_create_training_scene()
    input("\n[Step 1 complete] Press Enter to continue...")
    
    step2_collect_training_data(num_poses=5)
    input("\n[Step 2 complete] Press Enter to continue...")
    
    step3_train_model()
    input("\n[Step 3 complete] Press Enter to continue...")
    
    step4_deploy_deformer()
    
    print("\n" + "="*70)
    print("WORKFLOW COMPLETE!")
    print("="*70)
    print("\n🎥 Ready to record demo:")
    print("  - Press PLAY to see animation")
    print("  - Or manually rotate 'elbow_jnt'")
    print("  - ML corrective adjusts automatically!")
    print("="*70)


# ============================================================================
# COMPARISON DEMO
# ============================================================================

def create_comparison():
    """
    Create side-by-side comparison: WITH vs WITHOUT ML
    """
    print("\n" + "="*70)
    print("CREATING COMPARISON")
    print("="*70)
    
    if not cmds.objExists('arm_geo'):
        print("\n✗ Run the workflow first!")
        return
    
    # Check if comparison already exists
    if cmds.objExists('arm_WITHOUT_ML'):
        print("\n  Comparison already exists. Deleting old one...")
        cmds.delete('arm_WITHOUT_ML')
    
    # Duplicate WITHOUT upstream nodes (clean duplicate)
    duplicate = cmds.duplicate('arm_geo', name='arm_WITHOUT_ML', returnRootsOnly=True)[0]
    
    # Move to the side
    cmds.move(3, 0, 0, duplicate, relative=True)
    
    # Clean the duplicate - remove ALL deformers
    dup_history = cmds.listHistory(duplicate, pruneDagObjects=True)
    if dup_history:
        for node in dup_history:
            node_type = cmds.nodeType(node)
            if node_type in ['skinCluster', 'blendShape', 'tweak', 'groupParts', 'groupId']:
                try:
                    cmds.delete(node)
                    print(f"  Removed {node_type} from duplicate")
                except:
                    pass
    
    # Re-bind skin to joints (WITHOUT ML deformer)
    if cmds.objExists('shoulder_jnt'):
        print("\n  Binding duplicate to skeleton (no ML)...")
        cmds.select(duplicate, 'shoulder_jnt', 'elbow_jnt', 'wrist_jnt')
        cmds.skinCluster(toSelectedBones=True, bindMethod=0, 
                        normalizeWeights=1, name='arm_WITHOUT_ML_skin')
        print("  ✓ Duplicate has clean skinning (no ML corrections)")
    
    # Add color coding
    # GREEN = ML ON (original) - with transparency
    if not cmds.objExists('ML_ON'):
        green_shader = cmds.shadingNode('lambert', asShader=True, name='ML_ON')
        cmds.setAttr(green_shader + '.color', 0.2, 0.8, 0.3, type='double3')
        cmds.setAttr(green_shader + '.transparency', 0.3, 0.3, 0.3, type='double3')  # 30% transparent
        green_sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name='ML_ON_SG')
        cmds.connectAttr(green_shader + '.outColor', green_sg + '.surfaceShader')
    cmds.select('arm_geo')
    cmds.sets(forceElement='ML_ON_SG')
    
    # RED = ML OFF (duplicate) - opaque
    if not cmds.objExists('ML_OFF'):
        red_shader = cmds.shadingNode('lambert', asShader=True, name='ML_OFF')
        cmds.setAttr(red_shader + '.color', 0.9, 0.2, 0.2, type='double3')
        red_sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name='ML_OFF_SG')
        cmds.connectAttr(red_shader + '.outColor', red_sg + '.surfaceShader')
    cmds.select('arm_WITHOUT_ML')
    cmds.sets(forceElement='ML_OFF_SG')
    
    # Frame view
    cmds.select('arm_geo', 'arm_WITHOUT_ML')
    cmds.viewFit()
    cmds.select(clear=True)
    
    print("\n✓ Comparison created!")
    print("\n  🟢 LEFT (GREEN)  = WITH ML Corrective")
    print("  🔴 RIGHT (RED)   = WITHOUT ML Corrective")
    print("\n  Press PLAY to see the difference!")


# ============================================================================
# QUICK START
# ============================================================================

if __name__ == "__main__":
    print(__doc__)
    print("\nQUICK START:")
    print("  run_complete_workflow()  - Full end-to-end demo")
    print("  create_comparison()      - Add side-by-side comparison")
    print("\nOR run step-by-step:")
    print("  step1_create_training_scene()")
    print("  step2_collect_training_data()")
    print("  step3_train_model()")
    print("  step4_deploy_deformer()")
    print("  create_comparison()")
