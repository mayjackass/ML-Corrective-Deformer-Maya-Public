# Quick Reference Card - ML Corrective Deformer

## 🚀 Installation (Run in Maya Script Editor)

```python
import maya.cmds as cmds

# Load plugin
plugin_path = r"C:\Users\Burn\Documents\maya\scripts\ML_deformerTool\phase1_python_prototype\ml_corrective_deformer.py"
cmds.loadPlugin(plugin_path)

# Run installation & create test scene
exec(open(r"C:\Users\Burn\Documents\maya\scripts\ML_deformerTool\phase1_python_prototype\install_deformer.py").read())
```

## 🎨 Apply Deformer

```python
# Select mesh and apply
cmds.select("yourMesh")
deformer = cmds.deformer(type="mlCorrectiveDeformer")[0]

# Connect joint rotation
cmds.connectAttr("yourJoint.rotateZ", f"{deformer}.poseAngle")

# Set parameters
cmds.setAttr(f"{deformer}.correctionWeight", 1.0)
cmds.setAttr(f"{deformer}.enableML", True)
```

## 📊 Data Collection

```python
# Open UI
import sys
sys.path.append(r"C:\Users\Burn\Documents\maya\scripts\ML_deformerTool")
from utils import data_collector
data_collector.create_data_collection_ui()

# Or use Python API
from utils.data_collector import DataCollector

collector = DataCollector("meshName", ["joint1", "joint2"])
collector.capture_pose_range("joint1", "rotateZ", -90, 90, 20)
collector.save_dataset("../data/my_data.npz")
```

## 🧠 Train Model (PowerShell)

```powershell
cd "C:\Users\Burn\Documents\maya\scripts\ML_deformerTool\ml_training"

# Install dependencies (first time)
pip install torch numpy tqdm onnx

# Train
python train.py --data ../data/my_data.npz `
                --save-dir ../models/my_model `
                --model-type standard `
                --epochs 100 `
                --batch-size 32
```

## 📦 Model Architectures

```bash
# Standard (default) - best for general use
python train.py --model-type standard --data data.npz

# Compact - faster inference
python train.py --model-type compact --data data.npz

# Residual - complex deformations
python train.py --model-type residual --data data.npz
```

## 🔧 Common Tasks

### Check Plugin Status
```python
cmds.pluginInfo("ml_corrective_deformer.py", query=True, loaded=True)
```

### List Deformers on Object
```python
cmds.listHistory("yourMesh", type="mlCorrectiveDeformer")
```

### Get Deformer Attributes
```python
cmds.getAttr("mlCorrectiveDeformer1.poseAngle")
cmds.getAttr("mlCorrectiveDeformer1.correctionWeight")
```

### Delete Deformer
```python
cmds.delete("mlCorrectiveDeformer1")
```

## 📁 File Locations

| File | Location |
|------|----------|
| Plugin | `phase1_python_prototype/ml_corrective_deformer.py` |
| Data Collector | `utils/data_collector.py` |
| Training Script | `ml_training/train.py` |
| Models | `ml_training/model.py` |
| Config | `config.json` |
| Datasets | `data/*.npz` |
| Trained Models | `models/*.pt` |

## 🎯 Attributes

| Attribute | Type | Range | Default |
|-----------|------|-------|---------|
| `poseAngle` | float | -180 to 180 | 0.0 |
| `correctionWeight` | float | 0 to 2 | 1.0 |
| `enableML` | bool | - | True |

## 💡 Tips & Tricks

### Animate Corrections
```python
# Keyframe the weight
cmds.setKeyframe(deformer, attribute="correctionWeight", time=1, value=0)
cmds.setKeyframe(deformer, attribute="correctionWeight", time=50, value=1)
```

### Multiple Deformers
```python
# Apply different deformers for different joint ranges
deformer1 = cmds.deformer(type="mlCorrectiveDeformer")[0]
cmds.connectAttr("elbow.rotateZ", f"{deformer1}.poseAngle")

deformer2 = cmds.deformer(type="mlCorrectiveDeformer")[0]
cmds.connectAttr("shoulder.rotateX", f"{deformer2}.poseAngle")
```

### Blend with Blendshapes
```python
# ML deformer works with existing blendshapes
# Apply order: SkinCluster → Blendshape → MLDeformer
```

## 🐛 Troubleshooting

### Plugin Won't Load
```python
# Check Maya version
import maya
print(maya.cmds.about(version=True))  # Should be 2020+

# Check Python version
import sys
print(sys.version)  # Should be 3.7+
```

### No Deformation Visible
```python
# Check deformer envelope
cmds.getAttr("mlCorrectiveDeformer1.envelope")
cmds.setAttr("mlCorrectiveDeformer1.envelope", 1.0)

# Check if enabled
cmds.setAttr("mlCorrectiveDeformer1.enableML", True)
```

### Training Errors
```powershell
# Use CPU if CUDA issues
python train.py --device cpu --data data.npz

# Reduce batch size if out of memory
python train.py --batch-size 8 --data data.npz
```

## 📖 Documentation

- **Full Guide**: `README.md`
- **Quick Start**: `docs/QUICKSTART.md`
- **Architecture**: `docs/ARCHITECTURE.md`
- **Project Summary**: `PROJECT_SUMMARY.md`

## 🔗 Workflow Summary

```
1. Create/Load Rig → 2. Collect Data → 3. Train Model → 4. Deploy
        ↓                    ↓                ↓            ↓
   (in Maya)        (Data Collection)   (Python)    (Phase 2)
                         UI
```

## 🎓 Example Workflow

```python
# 1. Apply deformer
cmds.select("armMesh")
deformer = cmds.deformer(type="mlCorrectiveDeformer")[0]
cmds.connectAttr("elbow.rotateZ", f"{deformer}.poseAngle")

# 2. Collect data
from utils.data_collector import DataCollector
collector = DataCollector("armMesh", ["shoulder", "elbow", "wrist"])
collector.capture_pose_range("elbow", "rotateZ", -90, 90, 20)
collector.save_dataset("data/elbow.npz")

# 3. Train (in PowerShell)
# python ml_training/train.py --data data/elbow.npz --epochs 100

# 4. Deploy (Phase 2)
# cmds.setAttr(f"{deformer}.modelPath", "models/elbow/model.pt")
```

---

**Save this file for quick reference!**

*ML Corrective Deformer v1.0.0 - Phase 1*
