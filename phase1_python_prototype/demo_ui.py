"""
ML Corrective Deformer - Demo UI
Simple interface for demonstrating the end-to-end workflow

Author: Mayj Amilano
"""

import maya.cmds as cmds
from functools import partial
import end_to_end_demo

# UI Window Name
WINDOW_NAME = "mlCorrectiveDemoUI"

def create_demo_ui():
    """
    Create the main demo UI window
    """
    # Delete existing window if it exists
    if cmds.window(WINDOW_NAME, exists=True):
        cmds.deleteUI(WINDOW_NAME)
    
    # Create window
    window = cmds.window(WINDOW_NAME, 
                        title="ML Corrective Deformer - Demo Tool",
                        widthHeight=(420, 750),
                        sizeable=True)
    
    # Scroll layout to contain everything
    scroll_layout = cmds.scrollLayout(horizontalScrollBarThickness=0,
                                     verticalScrollBarThickness=16)
    
    # Main layout
    main_layout = cmds.columnLayout(adjustableColumn=True, rowSpacing=5, columnOffset=['both', 10])
    
    # Header
    cmds.separator(height=10, style='none')
    cmds.text(label="ML Corrective Deformer Workflow", 
             font='boldLabelFont', height=30)
    cmds.text(label="Complete End-to-End Pipeline Demo", 
             font='smallPlainLabelFont')
    cmds.separator(height=10, style='in')
    
    # Step 1: Create Training Scene
    cmds.separator(height=10, style='none')
    cmds.frameLayout(label="Step 1: Create Training Scene", 
                    collapsable=False, borderStyle='etchedIn',
                    backgroundColor=[0.2, 0.3, 0.4])
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5, columnOffset=['both', 10])
    cmds.separator(height=5, style='none')
    cmds.text(label="Creates arm geometry with joint chain", align='left')
    cmds.button(label="1. Create Scene", 
               height=35,
               backgroundColor=[0.3, 0.5, 0.3],
               command=partial(run_step, 1))
    cmds.separator(height=3, style='none')
    cmds.button(label="Paint Skin Weights (Optional)", 
               height=25,
               backgroundColor=[0.35, 0.45, 0.35],
               command=partial(open_paint_tool))
    cmds.separator(height=5, style='none')
    cmds.setParent('..')
    cmds.setParent('..')
    
    # Step 2: Collect Training Data
    cmds.separator(height=5, style='none')
    cmds.frameLayout(label="Step 2: Collect Training Data", 
                    collapsable=False, borderStyle='etchedIn',
                    backgroundColor=[0.2, 0.3, 0.4])
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5, columnOffset=['both', 10])
    cmds.separator(height=5, style='none')
    cmds.text(label="Gather pose/correction pairs for ML training", align='left')
    cmds.rowLayout(numberOfColumns=2, columnWidth2=[200, 180], 
                  columnAttach2=['both', 'both'], columnOffset2=[0, 5])
    cmds.text(label="Number of training poses:", align='left')
    pose_field = cmds.intField('numPosesField', value=5, minValue=3, maxValue=10, width=60)
    cmds.setParent('..')
    cmds.button(label="2. Collect Data", 
               height=35,
               backgroundColor=[0.3, 0.5, 0.3],
               command=partial(run_step, 2))
    cmds.separator(height=5, style='none')
    cmds.setParent('..')
    cmds.setParent('..')
    
    # Step 3: Train Model
    cmds.separator(height=5, style='none')
    cmds.frameLayout(label="Step 3: Train ML Model", 
                    collapsable=False, borderStyle='etchedIn',
                    backgroundColor=[0.2, 0.3, 0.4])
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5, columnOffset=['both', 10])
    cmds.separator(height=5, style='none')
    cmds.text(label="Train neural network on collected data", align='left')
    cmds.button(label="3. Train Model", 
               height=35,
               backgroundColor=[0.3, 0.5, 0.3],
               command=partial(run_step, 3))
    cmds.separator(height=5, style='none')
    cmds.setParent('..')
    cmds.setParent('..')
    
    # Step 4: Deploy Deformer
    cmds.separator(height=5, style='none')
    cmds.frameLayout(label="Step 4: Deploy ML Deformer", 
                    collapsable=False, borderStyle='etchedIn',
                    backgroundColor=[0.2, 0.3, 0.4])
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5, columnOffset=['both', 10])
    cmds.separator(height=5, style='none')
    cmds.text(label="Deploy trained model as live Maya deformer", align='left')
    cmds.button(label="4. Deploy Deformer", 
               height=35,
               backgroundColor=[0.3, 0.5, 0.3],
               command=partial(run_step, 4))
    cmds.separator(height=5, style='none')
    cmds.setParent('..')
    cmds.setParent('..')
    
    # Visualization
    cmds.separator(height=5, style='none')
    cmds.frameLayout(label="Visualization Tools", 
                    collapsable=False, borderStyle='etchedIn',
                    backgroundColor=[0.25, 0.25, 0.35])
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5, columnOffset=['both', 10])
    cmds.separator(height=5, style='none')
    cmds.text(label="Create side-by-side comparison for demo", align='left')
    cmds.button(label="Create Comparison (WITH vs WITHOUT ML)", 
               height=35,
               backgroundColor=[0.4, 0.5, 0.6],
               command=partial(run_comparison))
    cmds.separator(height=5, style='none')
    cmds.text(label="Toggle visibility to compare:", align='left')
    cmds.rowLayout(numberOfColumns=2, columnWidth2=[195, 195], 
                  columnAttach2=['both', 'both'], columnOffset2=[0, 5])
    cmds.button(label="Show WITH ML (Green)", 
               height=30,
               backgroundColor=[0.2, 0.5, 0.3],
               command=partial(toggle_visibility, 'with'))
    cmds.button(label="Show WITHOUT ML (Red)", 
               height=30,
               backgroundColor=[0.5, 0.2, 0.2],
               command=partial(toggle_visibility, 'without'))
    cmds.setParent('..')
    cmds.button(label="Show Both", 
               height=25,
               backgroundColor=[0.4, 0.4, 0.5],
               command=partial(toggle_visibility, 'both'))
    cmds.separator(height=5, style='none')
    cmds.setParent('..')
    cmds.setParent('..')
    
    # Quick Actions
    cmds.separator(height=10, style='in')
    cmds.frameLayout(label="Quick Actions", 
                    collapsable=False, borderStyle='etchedIn',
                    backgroundColor=[0.35, 0.25, 0.25])
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5, columnOffset=['both', 10])
    cmds.separator(height=5, style='none')
    cmds.button(label="RUN ALL STEPS (Complete Workflow)", 
               height=40,
               backgroundColor=[0.5, 0.3, 0.3],
               command=partial(run_all_steps))
    cmds.separator(height=3, style='none')
    cmds.button(label="Play Animation", 
               height=30,
               backgroundColor=[0.3, 0.4, 0.5],
               command=partial(play_animation))
    cmds.separator(height=3, style='none')
    cmds.button(label="Reset Scene", 
               height=25,
               backgroundColor=[0.4, 0.4, 0.4],
               command=partial(reset_scene))
    cmds.separator(height=5, style='none')
    cmds.setParent('..')
    cmds.setParent('..')
    
    # Footer
    cmds.separator(height=10, style='in')
    cmds.text(label="ML Corrective Deformer Prototype", 
             font='smallPlainLabelFont', height=20)
    cmds.text(label="© 2024 Mayj Amilano", 
             font='smallPlainLabelFont', height=20)
    cmds.separator(height=5, style='none')
    
    # Show window
    cmds.showWindow(window)
    
    print("\n" + "="*70)
    print("ML Corrective Deformer Demo UI Loaded")
    print("="*70)
    print("\nQuick Start:")
    print("  1. Click 'RUN ALL STEPS' for complete demo")
    print("  2. Or click each step button in order (1-4)")
    print("  3. Click 'Create Comparison' for side-by-side view")
    print("  4. Click 'Play Animation' to see it in action!")
    print("="*70)


def run_step(step, *args):
    """
    Run a specific workflow step
    """
    print("\n" + "="*70)
    
    if step == 1:
        print("Running Step 1: Create Training Scene...")
        end_to_end_demo.step1_create_training_scene()
        cmds.confirmDialog(title='Step 1 Complete', 
                          message='Training scene created!\n\nArm geometry and joints ready.',
                          button=['OK'], defaultButton='OK')
    
    elif step == 2:
        print("Running Step 2: Collect Training Data...")
        num_poses = cmds.intField('numPosesField', query=True, value=True)
        end_to_end_demo.step2_collect_training_data(num_poses=num_poses)
        cmds.confirmDialog(title='Step 2 Complete', 
                          message=f'Training data collected!\n\n{num_poses} pose samples saved.',
                          button=['OK'], defaultButton='OK')
    
    elif step == 3:
        print("Running Step 3: Train ML Model...")
        end_to_end_demo.step3_train_model()
        cmds.confirmDialog(title='Step 3 Complete', 
                          message='Model trained successfully!\n\nReady for deployment.',
                          button=['OK'], defaultButton='OK')
    
    elif step == 4:
        print("Running Step 4: Deploy Deformer...")
        end_to_end_demo.step4_deploy_deformer()
        cmds.confirmDialog(title='Step 4 Complete', 
                          message='ML Deformer deployed!\n\nPress Play to see animation.',
                          button=['OK'], defaultButton='OK')
    
    print("="*70)


def run_comparison(*args):
    """
    Create side-by-side comparison
    """
    print("\n" + "="*70)
    print("Creating Comparison View...")
    end_to_end_demo.create_comparison()
    cmds.confirmDialog(title='Comparison Created', 
                      message='Side-by-side comparison ready!\n\nGREEN = WITH ML\nRED = WITHOUT ML\n\nPress Play to see the difference!',
                      button=['OK'], defaultButton='OK')
    print("="*70)


def run_all_steps(*args):
    """
    Run the complete workflow
    """
    result = cmds.confirmDialog(
        title='Run Complete Workflow',
        message='This will run all 4 steps automatically:\n\n1. Create Scene\n2. Collect Data\n3. Train Model\n4. Deploy Deformer\n\nContinue?',
        button=['Yes', 'Cancel'],
        defaultButton='Yes',
        cancelButton='Cancel',
        dismissString='Cancel'
    )
    
    if result == 'Yes':
        print("\n" + "="*70)
        print("RUNNING COMPLETE WORKFLOW")
        print("="*70)
        
        # Get number of poses
        num_poses = cmds.intField('numPosesField', query=True, value=True)
        
        # Run all steps
        print("\nStep 1/4: Creating Scene...")
        end_to_end_demo.step1_create_training_scene()
        
        print("\nStep 2/4: Collecting Data...")
        end_to_end_demo.step2_collect_training_data(num_poses=num_poses)
        
        print("\nStep 3/4: Training Model...")
        end_to_end_demo.step3_train_model()
        
        print("\nStep 4/4: Deploying Deformer...")
        end_to_end_demo.step4_deploy_deformer()
        
        print("\n" + "="*70)
        print("WORKFLOW COMPLETE!")
        print("="*70)
        
        cmds.confirmDialog(
            title='Workflow Complete',
            message='All steps completed successfully!\n\nML Deformer is now active.\n\nPress Play to see the animation!',
            button=['OK'],
            defaultButton='OK'
        )


def play_animation(*args):
    """
    Play the timeline animation
    """
    if cmds.objExists('elbow_jnt'):
        cmds.playbackOptions(min=1, max=120)
        cmds.currentTime(1)
        cmds.play(forward=True)
    else:
        cmds.confirmDialog(
            title='No Animation',
            message='Please run the workflow first!',
            button=['OK'],
            defaultButton='OK'
        )


def reset_scene(*args):
    """
    Reset to a clean scene
    """
    result = cmds.confirmDialog(
        title='Reset Scene',
        message='This will clear the current scene.\n\nAre you sure?',
        button=['Yes', 'Cancel'],
        defaultButton='Cancel',
        cancelButton='Cancel',
        dismissString='Cancel'
    )
    
    if result == 'Yes':
        cmds.file(new=True, force=True)
        print("\nScene reset. Ready for new demo.")


def open_paint_tool(*args):
    """
    Open paint skin weights tool
    """
    end_to_end_demo.open_paint_weights_tool()


def toggle_visibility(mode, *args):
    """
    Toggle visibility between WITH ML and WITHOUT ML meshes
    """
    with_ml = 'arm_geo'
    without_ml = 'arm_WITHOUT_ML'
    
    if mode == 'with':
        # Show only WITH ML (green)
        if cmds.objExists(with_ml):
            cmds.setAttr(with_ml + '.visibility', 1)
            print("\n✓ Showing WITH ML (green) - ML corrective enabled")
        if cmds.objExists(without_ml):
            cmds.setAttr(without_ml + '.visibility', 0)
            
    elif mode == 'without':
        # Show only WITHOUT ML (red)
        if cmds.objExists(with_ml):
            cmds.setAttr(with_ml + '.visibility', 0)
        if cmds.objExists(without_ml):
            cmds.setAttr(without_ml + '.visibility', 1)
            print("\n✓ Showing WITHOUT ML (red) - skinning only")
            
    elif mode == 'both':
        # Show both side-by-side
        if cmds.objExists(with_ml):
            cmds.setAttr(with_ml + '.visibility', 1)
        if cmds.objExists(without_ml):
            cmds.setAttr(without_ml + '.visibility', 1)
            print("\n✓ Showing both - side-by-side comparison")
    
    # Frame view
    if mode == 'with' and cmds.objExists(with_ml):
        cmds.select(with_ml)
        cmds.viewFit()
        cmds.select(clear=True)
    elif mode == 'without' and cmds.objExists(without_ml):
        cmds.select(without_ml)
        cmds.viewFit()
        cmds.select(clear=True)
    elif mode == 'both':
        if cmds.objExists(with_ml) and cmds.objExists(without_ml):
            cmds.select(with_ml, without_ml)
            cmds.viewFit()
            cmds.select(clear=True)


# Launch UI when script is run
if __name__ == "__main__":
    create_demo_ui()
