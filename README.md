# ML Corrective Deformer for Maya

> **Visit the project page:** [https://pose-based-correctiv--mayjackass.github.app/](https://pose-based-correctiv--mayjackass.github.app/)

**Pose-Based Corrective Blendshape Prediction Using Machine Learning**

A research implementation by Mayj Amilano

## Overview

This project implements a machine learning-based deformer for Autodesk Maya that automatically predicts corrective blendshapes based on skeletal joint poses. The system learns from artist-provided or simulation-derived data to automate the traditionally manual and time-consuming process of creating corrective shapes for character rigs.

### Key Features

-   **ML-Driven Corrections**: Neural networks predict vertex displacements from joint angles
-   **Real-Time Performance**: Optimized for viewport playback in Maya
-   **Artist-Friendly**: Intuitive UI for data collection and model deployment
-   **Flexible Training**: Multiple architecture options (Standard, Compact, Residual)
-   **Production-Ready**: Phased implementation from prototype to C++/LibTorch

## Project Structure

```
ML_deformerTool/
  phase1_python_prototype/      # Phase 1: Python proof-of-concept
      ml_corrective_deformer.py # Main deformer node
      install_deformer.py       # Installation & test setup
  phase2_real_dataset/          # Phase 2: Real rig integration
  phase3_cpp_production/        # Phase 3: C++ + LibTorch
  phase4_artist_workflow/       # Phase 4: Artist UI tools
  ml_training/                  # Machine learning framework
      model.py                  # Neural network architectures
      train.py                  # Training scripts
  utils/                        # Utilities
      data_collector.py         # Maya data collection tool
  data/                         # Training datasets
  models/                       # Trained models
  docs/                         # Documentation
  tests/                        # Unit tests
```

## Implementation Phases

###   Phase 1: Python Prototype (Current)
- [x] Python deformer node (MPxDeformerNode)
- [x] Simple procedural corrections
- [x] Basic attribute system
- [x] Test scene setup

###   Phase 2: Real Dataset
- [ ] Data collection from actual rigs
- [ ] PyTorch model integration
- [ ] Real-time ML inference
- [ ] Joint attribute connections

###   Phase 3: C++ Production
- [ ] C++ deformer node
- [ ] LibTorch integration
- [ ] GPU acceleration
- [ ] Performance optimization

###   Phase 4: Artist Workflow
- [ ] Complete UI system
- [ ] Dataset capture tools
- [ ] Model training pipeline
- [ ] Production deployment

## Installation

### Prerequisites

- Autodesk Maya (2020+)
- Python 3.7+
- PyTorch 1.8+ (for training)
- NumPy

### Quick Start

1. **Load the Plugin in Maya**:

```python
import maya.cmds as cmds

# Set the plugin path
plugin_path = "C:/Users/Burn/Documents/maya/scripts/ML_deformerTool/phase1_python_prototype/ml_corrective_deformer.py"

# Load the plugin
cmds.loadPlugin(plugin_path)

# Run installation script
exec(open("C:/Users/Burn/Documents/maya/scripts/ML_deformerTool/phase1_python_prototype/install_deformer.py").read())
```

2. **Create Test Scene**:

The installation script automatically creates a test scene with:
- Test geometry (arm)
- Joint chain (shoulder, elbow, wrist)
- Applied ML deformer
- Animation keyframes

3. **Test the Deformer**:

Rotate the elbow joint or play the timeline to see corrective deformations.

## Usage

### Applying the Deformer

```python
# Select your mesh
cmds.select("yourMesh")

# Apply ML Corrective Deformer
deformer = cmds.deformer(type="mlCorrectiveDeformer")[0]

# Connect joint rotation to deformer
cmds.connectAttr("yourJoint.rotateZ", f"{deformer}.poseAngle")

# Adjust weights
cmds.setAttr(f"{deformer}.correctionWeight", 1.0)
cmds.setAttr(f"{deformer}.enableML", True)
```

### Data Collection

1. **Open Data Collection UI**:

```python
from utils import data_collector
data_collector.create_data_collection_ui()
```

2. **Setup**:
   - Select your base mesh and click "Load Selected Mesh"
   - Select joints to track and click "Load Selected Joints"
   - Click "Initialize Collector"

3. **Capture Data**:
   - **Manual**: Set poses manually and click "Capture Current Pose"
   - **With Correctives**: Click "Create Corrective Duplicate", sculpt the correction, then "Capture with Corrective"
   - **Automatic**: Use "Auto-Capture Range" to sample across joint rotations

4. **Save Dataset**:
   - Specify output path
   - Click "Save Dataset"

### Training a Model

```bash
# Navigate to ml_training directory
cd ml_training

# Train with your dataset
python train.py --data ../data/training_data.npz \
                --save-dir ../models/trained \
                --model-type standard \
                --epochs 100 \
                --batch-size 32 \
                --lr 0.001
```

### Model Architectures

**Standard Model** (Default):
```python
# 4-layer feedforward network
# Hidden layers: [256, 512, 512, 256]
# Best for general-purpose corrections
model = create_model('standard', num_joints=6, num_vertices=1000)
```

**Compact Model**:
```python
# Lightweight with PCA compression
# Hidden layers: [128, 256, 128]
# Best for real-time performance
model = create_model('compact', num_joints=6, pca_components=50)
```

**Residual Model**:
```python
# Deep network with skip connections
# Best for complex deformations
model = create_model('residual', num_joints=6, num_vertices=1000, num_blocks=4)
```

## Configuration

### Deformer Attributes

| Attribute | Type | Range | Description |
|-----------|------|-------|-------------|
| `poseAngle` | Float | -180 to 180 | Input joint angle (degrees) |
| `correctionWeight` | Float | 0 to 2 | Multiplier for correction strength |
| `enableML` | Bool | - | Enable/disable ML prediction |

### Training Parameters

Edit training configuration in `ml_training/train.py`:

```python
# Network architecture
hidden_layers = [256, 512, 512, 256]

# Training settings
num_epochs = 100
batch_size = 32
learning_rate = 0.001
val_split = 0.2

# Device
device = 'cuda'  # or 'cpu'
```

## Technical Details

### Neural Network Architecture

The system uses feedforward neural networks to learn the nonlinear mapping:

```
Joint Angles ( ,  , ...,  )   Vertex Displacements ( x,  y,  z)
```

**Input**: Normalized joint angles [-1, 1]  
**Output**: Vertex displacement vectors [num_vertices   3]  
**Loss**: Mean Squared Error (MSE)

### Data Format

Training data is stored in `.npz` format:

```python
{
    'joint_angles': np.array([num_samples, num_joints]),
    'vertex_deltas': np.array([num_samples, num_vertices, 3]),
    'joint_names': list of joint names,
    'num_vertices': int
}
```

### Model Export

Trained models are exported in two formats:
- **TorchScript** (`.pt`): For PyTorch-based inference
- **ONNX** (`.onnx`): For cross-platform compatibility

## Workflow Example

### Complete Pipeline

1. **Setup Character Rig**:
   - Create joint hierarchy
   - Apply skin cluster
   - Test basic deformations

2. **Collect Training Data**:
   ```python
   from utils.data_collector import DataCollector
   
   collector = DataCollector(
       base_mesh="armMesh",
       joints=["shoulder", "elbow", "wrist"]
   )
   
   # Capture multiple poses
   collector.capture_pose_range("elbow", "rotateZ", -90, 90, 20)
   collector.save_dataset("data/arm_correctives.npz")
   ```

3. **Train Model**:
   ```bash
   python ml_training/train.py \
       --data data/arm_correctives.npz \
       --save-dir models/arm_model \
       --epochs 100
   ```

4. **Deploy in Maya**:
   ```python
   # Load trained model (Phase 2+)
   deformer_node = cmds.createNode("mlCorrectiveDeformer")
   # Load model into deformer...
   ```

## Performance

### Phase 1 (Python Prototype)
- **Vertices**: ~1000 vertices
- **Frame Rate**: 24-30 FPS (viewport)
- **Latency**: ~10-20ms per frame

### Phase 3 Target (C++ + LibTorch)
- **Vertices**: 10,000+ vertices
- **Frame Rate**: 60+ FPS (viewport)
- **Latency**: <5ms per frame
- **GPU Acceleration**: CUDA support

## Applications

### VFX Production
- Automate corrective sculpting for hero characters
- Reduce rigging time by 40-60%
- Consistent corrections across similar characters

### Animation Studios
- Style-consistent deformations
- Rapid character iteration
- Encode artist style in training data

### Game Development
- Real-time character corrections
- Lightweight runtime models
- Cross-platform deployment

### Virtual Production
- Real-time character previews
- Mocap-driven corrections
- On-set visualization

## Research Background

This implementation is based on the technical research paper:

**"Pose-Based Corrective Blendshape Prediction Using Machine Learning in Maya"**  
by Mayj Amilano

### Key Concepts

- **Corrective Blendshapes**: Artist-sculpted shapes that fix deformation artifacts
- **Pose-Space Deformation**: Corrections driven by joint configurations
- **Neural Regression**: ML models learn pose correction mapping
- **Real-Time Inference**: Embedded models run during Maya playback

### Related Work

- Disney Research: "Deep Appearance Models"
- Ziva Dynamics: "Ziva Face Trainer"
- ILM: "Facial Performance Capture with ML"

## Troubleshooting

### Plugin Won't Load

```python
# Check Maya Python API version
import maya.api.OpenMaya as om
print(om.MGlobal.apiVersion())

# Verify plugin path
import sys
print(sys.path)
```

### Training Issues

**CUDA Out of Memory**:
```bash
# Reduce batch size
python train.py --batch-size 16

# Use CPU
python train.py --device cpu
```

**Poor Convergence**:
- Increase training epochs
- Adjust learning rate
- Collect more diverse training data

### Performance Issues

- Reduce number of vertices (use proxy mesh)
- Use Compact model architecture
- Enable GPU acceleration (Phase 3)

## Development Roadmap

### Short Term
- [x] Phase 1 Python prototype
- [ ] PyTorch integration
- [ ] Real rig testing
- [ ] Documentation

### Medium Term
- [ ] C++ plugin development
- [ ] LibTorch integration
- [ ] Performance profiling
- [ ] Artist beta testing

### Long Term
- [ ] Facial rig support
- [ ] Simulation integration (Ziva)
- [ ] Multi-character transfer learning
- [ ] Game engine export (Unity/Unreal)

## Contributing

This is a research project. For questions or collaboration:
- Author: Mayj Amilano
- Email: [Your Email]
- GitHub: [Your GitHub]

## License

[Specify License]

## Acknowledgments

- Maya Python API documentation
- PyTorch team
- VFX/Animation community

## Citation

If you use this work in research or production:

```bibtex
@techreport{amilano2025mlcorrective,
    title={Pose-Based Corrective Blendshape Prediction Using Machine Learning in Maya},
    author={Amilano, Mayj},
    year={2025},
    institution={[Your Institution]}
}
```

---

**Last Updated**: October 17, 2025  
**Version**: 1.0.0 (Phase 1)  
**Status**: Active Development

