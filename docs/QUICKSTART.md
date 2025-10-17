# Quick Start Guide - ML Corrective Deformer

## 5-Minute Tutorial

### Step 1: Install the Plugin

Open Maya's Script Editor and run:

```python
import maya.cmds as cmds

# Load the plugin
plugin_path = r"C:\Users\Burn\Documents\maya\scripts\ML_deformerTool\phase1_python_prototype\ml_corrective_deformer.py"
cmds.loadPlugin(plugin_path)

# Run installation script
exec(open(r"C:\Users\Burn\Documents\maya\scripts\ML_deformerTool\phase1_python_prototype\install_deformer.py").read())
```

This will:
- ✅ Load the ML Corrective Deformer plugin
- ✅ Create a shelf button for easy access
- ✅ Generate a test scene with an arm rig
- ✅ Open the ML Deformer UI

### Step 2: Test the Deformer

The test scene includes:
- An arm mesh (`testArm`)
- Three joints: `shoulder`, `elbow`, `wrist`
- An ML deformer already applied
- Animation from frame 1-100

**Try this:**
1. Select the `elbow` joint in the outliner
2. Rotate it on the Z-axis (try values from -90 to 90)
3. Watch the mesh deform with automatic corrections
4. Press Play to see the animation

### Step 3: Apply to Your Own Mesh

```python
# Select your mesh
cmds.select("yourMeshName")

# Apply the deformer
deformer = cmds.deformer(type="mlCorrectiveDeformer")[0]

# Connect a joint rotation
cmds.connectAttr("yourJoint.rotateZ", f"{deformer}.poseAngle")

# Adjust the strength
cmds.setAttr(f"{deformer}.correctionWeight", 1.0)
```

---

## Complete Workflow Example

### Scenario: Create Elbow Correctives

#### Part 1: Collect Training Data (10 minutes)

1. **Prepare your rig**:
   - Have a skinned arm mesh
   - Identify joints to track: `shoulder`, `elbow`, `wrist`

2. **Open Data Collection Tool**:
```python
import sys
sys.path.append(r"C:\Users\Burn\Documents\maya\scripts\ML_deformerTool")
from utils import data_collector
data_collector.create_data_collection_ui()
```

3. **Setup Collection**:
   - Select your arm mesh → Click "Load Selected Mesh"
   - Select the three joints → Click "Load Selected Joints"
   - Click "Initialize Collector"

4. **Capture Data**:

**Option A - Automatic (Recommended)**:
```
1. In "Auto-Capture Range" section:
   - Joint name: elbow
   - Axis: rotateZ
   - Start: -90, End: 90, Steps: 20
2. Click "Auto-Capture Range"
3. Wait ~30 seconds
```

**Option B - Manual with Correctives**:
```
1. Set elbow to specific angle (e.g., 45°)
2. Click "Create Corrective Duplicate"
3. Sculpt corrections on the duplicate mesh
4. Click "Capture with Corrective"
5. Repeat for multiple poses
```

5. **Save Dataset**:
   - Set path: `../data/elbow_correctives.npz`
   - Click "Save Dataset"

#### Part 2: Train the Model (15 minutes)

1. **Open PowerShell in the project directory**:
```powershell
cd "C:\Users\Burn\Documents\maya\scripts\ML_deformerTool\ml_training"
```

2. **Install dependencies** (first time only):
```powershell
pip install torch numpy tqdm
```

3. **Train the model**:
```powershell
python train.py --data ../data/elbow_correctives.npz `
                --save-dir ../models/elbow_model `
                --model-type standard `
                --epochs 100 `
                --batch-size 16
```

4. **Monitor training**:
```
Epoch [1/100] Train Loss: 0.045123 | Val Loss: 0.052341
Epoch [2/100] Train Loss: 0.038234 | Val Loss: 0.041232
...
✓ Saved best model (val_loss: 0.001234)
Training completed!
```

#### Part 3: Deploy (Phase 2 - Coming Soon)

In Phase 2, you'll be able to load trained models directly into the deformer:

```python
# Load your trained model
cmds.setAttr(f"{deformer}.modelPath", "../models/elbow_model/model_torchscript.pt")

# The deformer now uses ML predictions!
```

---

## Common Use Cases

### Use Case 1: Simple Elbow Correction

**Problem**: Elbow collapses when bent  
**Solution**: 20 samples across bend range

```python
collector = DataCollector("armMesh", ["shoulder", "elbow", "wrist"])
collector.capture_pose_range("elbow", "rotateZ", 0, 120, 20)
collector.save_dataset("data/elbow_fix.npz")
```

### Use Case 2: Shoulder Rotation

**Problem**: Shoulder collapses during rotation  
**Solution**: Sample multiple axes

```python
# Capture X-axis rotation
collector.capture_pose_range("shoulder", "rotateX", -45, 45, 10)

# Capture Y-axis rotation
collector.capture_pose_range("shoulder", "rotateY", -90, 90, 15)

# Capture Z-axis rotation
collector.capture_pose_range("shoulder", "rotateZ", -45, 45, 10)

collector.save_dataset("data/shoulder_fix.npz")
```

### Use Case 3: Multiple Joints

**Problem**: Complex deformation with shoulder + elbow interaction  
**Solution**: Capture combined poses

```python
# Manual capture at specific combined poses
cmds.setAttr("shoulder.rotateZ", 30)
cmds.setAttr("elbow.rotateZ", 45)
collector.capture_sample()

cmds.setAttr("shoulder.rotateZ", 60)
cmds.setAttr("elbow.rotateZ", 90)
collector.capture_sample()

# ... more combinations
collector.save_dataset("data/arm_complex.npz")
```

---

## Testing Your Setup

### Verify Plugin Load

```python
# Check if plugin is loaded
cmds.pluginInfo("ml_corrective_deformer.py", query=True, loaded=True)
# Should return: True

# List available deformer types
cmds.deformerType(query=True)
# Should include: 'mlCorrectiveDeformer'
```

### Test Data Collection

```python
# Create simple test
cmds.polyCube(name="testCube")
cmds.joint(name="testJoint")

from utils.data_collector import DataCollector
collector = DataCollector("testCube", ["testJoint"])
collector.capture_sample()
print(f"Samples: {len(collector.samples)}")
# Should print: Samples: 1
```

### Verify Model Training

```python
# In ml_training directory, test model creation
from model import create_model

model = create_model('standard', num_joints=3, num_vertices=100)
print(f"Model created with {sum(p.numel() for p in model.parameters())} parameters")
```

---

## Troubleshooting Quick Fixes

### "Plugin failed to load"
```python
# Check Python version
import sys
print(sys.version)
# Should be 3.7+

# Check Maya API
import maya.api.OpenMaya as om
print(om.MGlobal.apiVersion())
```

### "Module not found: torch"
```bash
# Install PyTorch (outside Maya)
pip install torch
```

### "No corrective visible"
```python
# Check deformer is enabled
cmds.getAttr("mlCorrectiveDeformer1.enableML")

# Check weight
cmds.getAttr("mlCorrectiveDeformer1.correctionWeight")

# Check connection
cmds.listConnections("mlCorrectiveDeformer1.poseAngle")
```

### "Training very slow"
```bash
# Use CPU if CUDA issues
python train.py --device cpu

# Reduce batch size
python train.py --batch-size 8

# Reduce network size
python train.py --model-type compact
```

---

## Next Steps

1. ✅ **Complete Phase 1**: Familiarize yourself with the prototype
2. 🔄 **Collect Real Data**: Use your production rigs
3. 🎯 **Train Models**: Experiment with different architectures
4. 📊 **Evaluate Results**: Compare with manual correctives
5. 🚀 **Phase 2**: Integrate PyTorch models into Maya

---

## Need Help?

- 📖 Read the full [README.md](README.md)
- 🔍 Check [config.json](config.json) for settings
- 💻 Review example scripts in `examples/`
- 📧 Contact: [Your Email]

---

**Happy Rigging! 🎨🤖**
