# Phase 1: Python Prototype & Workflow Simulation

## Status: ✅ COMPLETE

Phase 1 demonstrates the complete ML corrective deformer workflow using Maya's built-in tools (blend shapes + MEL expressions) to simulate what a real ML model would do.

Demo video created and posted. Workflow validated end-to-end.

---

## Quick Start

### Option 1: UI-Based Demo (Recommended)
```python
# In Maya Script Editor (Python):
import sys
sys.path.append(r'C:\Users\Burn\Documents\maya\scripts\ML_deformerTool\phase1_python_prototype')

import demo_ui
demo_ui.create_demo_ui()
```

Then click through the steps in the UI!

### Option 2: Direct Script Execution
```python
# In Maya Script Editor (Python):
import sys
sys.path.append(r'C:\Users\Burn\Documents\maya\scripts\ML_deformerTool\phase1_python_prototype')

import end_to_end_demo

# Run complete workflow
end_to_end_demo.run_complete_workflow()

# Or run step-by-step:
end_to_end_demo.step1_create_training_scene()
end_to_end_demo.step2_collect_training_data(num_poses=5)
end_to_end_demo.step3_train_model()
end_to_end_demo.step4_deploy_deformer()

# Create side-by-side comparison
end_to_end_demo.create_comparison()
```

### Option 3: Simple Lattice Demo
```python
# In Maya Script Editor (Python):
import sys
sys.path.append(r'C:\Users\Burn\Documents\maya\scripts\ML_deformerTool\phase1_python_prototype')

import simple_demo
simple_demo.demo()  # Creates scene and animation
```

---

## Files

### Core Working Files

#### `end_to_end_demo.py` ⭐ Main Demo
**Complete 4-step ML workflow simulation**

**Functions:**
- `step1_create_training_scene()` - Creates arm geometry with skeleton
- `step2_collect_training_data(num_poses=5)` - Simulates data collection
- `step3_train_model()` - Simulates PyTorch training
- `step4_deploy_deformer()` - Deploys blend shape with MEL inference
- `create_comparison()` - Side-by-side WITH vs WITHOUT ML
- `run_complete_workflow()` - Runs all steps automatically

**Key Features:**
- Multi-target blend shape (30°, 60°, 90°, 120° training poses)
- MEL expression simulating neural network interpolation
- Realistic corrective shapes (bicep bulge, elbow pinch, volume preservation)
- Color-coded comparison (green WITH ML, red WITHOUT ML)

#### `demo_ui.py` ⭐ UI Interface
**User-friendly interface for running the demo**

**Features:**
- Step-by-step workflow buttons
- Optional paint skin weights integration
- Visualization tools (show WITH/WITHOUT/Both)
- Quick actions (Run All, Play, Reset)
- Status messages and confirmations

**Launch:** `demo_ui.create_demo_ui()`

#### `simple_demo.py` ⭐ Early Prototype
**Original lattice-based demonstration**

**Functions:**
- `demo()` - Quick setup with lattice deformer
- `on()` / `off()` - Toggle corrective on/off

**Purpose:**
- Shows early exploration with lattice approach
- Good for understanding basic concepts
- Simple one-line demo setup

---

## What Phase 1 Demonstrates

### ✅ Complete Workflow Simulation
1. **Scene Setup** - Character geometry + skeleton
2. **Data Collection** - Pose/correction pairs (simulated)
3. **Training** - Neural network learning (simulated)
4. **Deployment** - Real-time inference (MEL expression)

### ✅ Key Concepts Validated
- Pose-driven corrective deformations
- Multi-target interpolation
- Artist-sculpted training data workflow
- Real-time inference simulation
- Side-by-side comparison visualization

### ✅ Demo-Ready Features
- Professional UI with step-by-step flow
- Visual comparison (WITH vs WITHOUT ML)
- Animation playback
- Color coding (green = ML, red = no ML)
- Transparency for clear comparison

---

## What Phase 1 Does NOT Include

❌ **Real PyTorch Training**
- Training is simulated (prints fake progress)
- No actual neural network

❌ **Actual ML Inference**
- Uses MEL expression to interpolate blend shapes
- Mimics what a neural network would do

❌ **Maya Deformer Plugin**
- Uses standard blend shapes
- No MPxDeformerNode implementation

**These will be implemented in Phase 2 and Phase 3.**

---

## Technical Approach

### How the Simulation Works:

```
Simulated ML Pipeline:

1. Data Collection (step2)
   └─ Saves pose angles and dummy deltas to JSON
   
2. Training (step3)
   └─ Prints fake epoch/loss progress
   └─ Saves "model" (just the training data)
   
3. Deployment (step4)
   └─ Creates 4 blend shape targets (30°, 60°, 90°, 120°)
   └─ MEL expression reads joint angle
   └─ Blends between nearest targets
   └─ Result: smooth corrections like a real ML model
```

### Key Insight:
The blend shape interpolation **behaves identically** to how a neural network would interpolate between learned training samples. This makes it a perfect simulation for demonstrating the concept!

---

## Folder Structure

```
phase1_python_prototype/
├── README.md                   ← You are here
├── end_to_end_demo.py          ← Main demo (use this!)
├── demo_ui.py                  ← UI wrapper
├── simple_demo.py              ← Early prototype
└── _archive/                   ← Old/incomplete experiments
    ├── README.md
    ├── ml_corrective_deformer.py
    ├── install_deformer.py
    ├── example_basic.py
    └── example_data_collection.py
```

---

## Demo Video

The simulation demo video has been recorded and posted to LinkedIn, showing:
- Complete 4-step workflow
- Side-by-side comparison
- Real-time animation with ML corrections
- Professional UI demonstration

---

## Next Steps → Phase 2

**Phase 2 Goals:**
1. Implement **real PyTorch training**
   - Load JSON training data
   - Build simple neural network
   - Train and save model weights

2. Implement **real inference in Maya**
   - Load PyTorch model
   - Run forward pass per frame
   - Replace MEL expression with actual NN

3. Add **richer input features**
   - Multiple joint angles
   - Distance measurements
   - Strain vectors
   - (As suggested by Charles Looker from EA)

**See:** `../phase2_real_training/` (to be created)

---

## Troubleshooting

### "Module not found" errors
Make sure to add the path to sys.path:
```python
import sys
sys.path.append(r'C:\Users\Burn\Documents\maya\scripts\ML_deformerTool\phase1_python_prototype')
```

### Blend shape not working
Make sure you run the steps in order:
1. Step 1 (create scene)
2. Step 2 (collect data)
3. Step 3 (train model)
4. Step 4 (deploy deformer)

### Expression errors
The expression should auto-fix in the latest version. If issues persist, check that blend shape targets were created successfully.

---

## Credits

**Author:** Mayj Amilano  
**Project:** ML Corrective Deformer for Maya  
**Phase 1 Completed:** October 2025  

**LinkedIn:** [Your LinkedIn]  
**GitHub:** https://github.com/mayjackass/ML-Corrective-Deformer-Maya-Public  
**Documentation:** https://mayjackass.github.io/ML-Corrective-Deformer-Maya-Public/

---

## License

See main project LICENSE file.
