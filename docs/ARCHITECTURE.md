# Project Architecture - ML Corrective Deformer

## System Overview

This document describes the technical architecture of the ML Corrective Deformer system for Autodesk Maya.

## High-Level Architecture

```
 
                          Maya Scene                           
                  
       Joints     ML Deformer     Geometry    
      (Input)               Node                (Output)    
                  
 
                               
                               
                     
                       Trained Model    
                       (.pt / .onnx)    
                     
                               
                               
 
                     Training Pipeline                          
                     
       Data        Neural    Model Export       
    Collection           Network            (TorchScript)     
                     
 
```

## Component Architecture

### 1. Maya Deformer Node (`ml_corrective_deformer.py`)

**Inheritance**: `MPxDeformerNode` (Maya Python API 2.0)

**Responsibilities**:
- Receive joint angle inputs
- Execute ML inference (or procedural fallback in Phase 1)
- Apply vertex corrections to geometry
- Manage deformer weights and attributes

**Key Methods**:
```python
class MLCorrectiveDeformer(MPxDeformerNode):
    def deform(dataBlock, geoIter, matrix, multiIndex)
        # Main deformation logic
    
    def load_ml_model(model_path)
        # Load trained PyTorch model
    
    def predict_corrections(joint_angles)
        # Run ML inference
```

**Attributes**:
- `poseAngle` (float): Input joint angle
- `correctionWeight` (float): Multiplier for correction strength
- `enableML` (bool): Toggle ML vs. procedural mode

### 2. Data Collection System (`data_collector.py`)

**Purpose**: Capture training data from Maya scenes

**Components**:

#### DataCollector Class
```python
class DataCollector:
    - base_mesh: Target geometry
    - joints: List of tracked joints
    - samples: Collected training samples
    
    Methods:
    - capture_sample(): Capture current pose + corrections
    - capture_pose_range(): Auto-sample across joint range
    - save_dataset(): Export to .npz format
```

#### CorrectiveSculptingTool Class
```python
class CorrectiveSculptingTool:
    - create_corrective_duplicate(): Create sculpt mesh
    - capture_corrective(): Capture sculpted correction
    - reset_corrective(): Reset for next pose
```

**Data Format**:
```python
{
    'joint_angles': np.array([N, num_joints]),     # Normalized [-1, 1]
    'vertex_deltas': np.array([N, num_verts, 3]), # World space deltas
    'joint_names': list,
    'num_vertices': int
}
```

### 3. Neural Network Models (`model.py`)

**Architecture Options**:

#### Standard Model (CorrectiveDeformerNet)
```
Input(num_joints)   FC(256)   ReLU   Dropout
                    FC(512)   ReLU   Dropout
                    FC(512)   ReLU   Dropout
                    FC(256)   ReLU   Dropout
                    FC(num_vertices * 3)
                    Reshape(num_vertices, 3)
```

**Parameters**: ~500K-1M (depends on vertex count)

#### Compact Model (CompactCorrectiveNet)
```
Input(num_joints)   FC(128)   ReLU
                    FC(256)   ReLU
                    FC(128)   ReLU
                    FC(pca_components)
                    PCA Reconstruction
                    Reshape(num_vertices, 3)
```

**Parameters**: ~50K-100K

#### Residual Model (ResidualCorrectiveNet)
```
Input(num_joints)   FC(hidden_size)
                    [ResBlock   N]
                    FC(num_vertices * 3)
                    Reshape(num_vertices, 3)

ResBlock:
    x   FC   ReLU   FC   ReLU   (+) x
```

**Parameters**: ~1M-2M

### 4. Training Pipeline (`train.py`)

**Components**:

#### Dataset Class
```python
class CorrectiveDeformerDataset(torch.utils.data.Dataset):
    - Loads .npz data
    - Returns (joint_angles, vertex_deltas) pairs
```

#### Trainer Class
```python
class Trainer:
    - model: Neural network
    - optimizer: Adam optimizer
    - scheduler: ReduceLROnPlateau
    - criterion: MSELoss
    
    Methods:
    - train_epoch(): One training epoch
    - validate(): Validation pass
    - train(): Full training loop
    - export_for_maya(): Export to TorchScript/ONNX
```

**Training Loop**:
```
for epoch in epochs:
    1. Forward pass: predictions = model(joint_angles)
    2. Loss computation: loss = MSE(predictions, targets)
    3. Backward pass: loss.backward()
    4. Optimizer step: optimizer.step()
    5. Validation
    6. Learning rate scheduling
    7. Checkpoint saving
```

## Data Flow

### Training Data Flow

```
Maya Scene   Data Collector   .npz Dataset   DataLoader
                                                   
Model   Optimizer   Loss   Forward Pass   Training Loop
   
TorchScript/ONNX Export   Deployed Model
```

### Runtime Data Flow (Phase 2+)

```
Joint Rotations   Maya Deformer Node   PyTorch Model
                                             
                                    Vertex Corrections
                                             
                                    Deformed Geometry
```

### Phase 1 Data Flow (Current)

```
Joint Rotations   Maya Deformer Node   Procedural Correction
                                             
                                    Deformed Geometry
```

## File Organization

```
ML_deformerTool/
  phase1_python_prototype/          # Phase 1 implementation
      ml_corrective_deformer.py    # Main deformer node
      install_deformer.py          # Installation script
      example_basic.py             # Basic usage examples
      example_data_collection.py   # Data collection examples
 
  ml_training/                      # ML training framework
      model.py                      # Network architectures
      train.py                      # Training pipeline
 
  utils/                            # Utility modules
      data_collector.py            # Data collection tools
 
  data/                             # Training datasets (.npz)
  models/                           # Trained models (.pt, .onnx)
  docs/                             # Documentation
  tests/                            # Unit tests
 
  README.md                         # Main documentation
  config.json                       # Configuration
  requirements.txt                  # Python dependencies
```

## Phase Progression

### Phase 1: Python Prototype   (Current)
- Python-based MPxDeformerNode
- Procedural corrections (no ML yet)
- Data collection tools
- Training framework setup

### Phase 2: ML Integration   (Next)
- Load PyTorch models in Maya
- Real-time ML inference
- Multiple joint inputs
- Model hot-reloading

### Phase 3: C++ Production  
- C++ MPxDeformerNode
- LibTorch integration
- GPU acceleration
- Optimized performance

### Phase 4: Artist Tools  
- Complete UI system
- Automated workflows
- Model management
- Production deployment

## Integration Points

### Maya API Integration

```python
# Plugin Registration
def initializePlugin(mobject):
    mplugin = om.MFnPlugin(mobject)
    mplugin.registerNode(
        MLCorrectiveDeformer.kPluginNodeName,
        MLCorrectiveDeformer.kPluginNodeId,
        MLCorrectiveDeformer.creator,
        MLCorrectiveDeformer.initialize,
        oma.MPxNode.kDeformerNode
    )
```

### PyTorch Integration (Phase 2)

```python
# Model Loading
self.model = torch.jit.load(model_path)
self.model.eval()

# Inference
with torch.no_grad():
    joint_tensor = torch.tensor(joint_angles).float()
    predictions = self.model(joint_tensor)
    vertex_deltas = predictions.numpy()
```

### ONNX Integration (Alternative)

```python
import onnxruntime as ort

session = ort.InferenceSession(model_path)
input_name = session.get_inputs()[0].name
predictions = session.run(None, {input_name: joint_angles})
```

## Performance Considerations

### Phase 1 Target
- **Vertices**: 1,000
- **FPS**: 24
- **Latency**: 20ms
- **Method**: Procedural (NumPy)

### Phase 3 Target
- **Vertices**: 10,000+
- **FPS**: 60+
- **Latency**: <5ms
- **Method**: LibTorch GPU

### Optimization Strategies

1. **Model Compression**:
   - PCA dimensionality reduction
   - Quantization (INT8)
   - Model pruning

2. **Runtime Optimization**:
   - Batch inference
   - GPU acceleration
   - Parallel processing

3. **Caching**:
   - Cache predictions for repeated poses
   - Interpolate between cached results

## Error Handling

```python
try:
    # Deformation logic
    predictions = self.predict_corrections(joint_angles)
except Exception as e:
    print(f"ML prediction failed: {e}")
    # Fallback to procedural
    predictions = self.procedural_fallback(joint_angles)
```

## Testing Strategy

### Unit Tests
- Model forward pass
- Data loading
- Attribute connections

### Integration Tests
- Full training pipeline
- Maya plugin loading
- Deformer application

### Visual Tests
- Compare with manual correctives
- Artifact detection
- Performance profiling

## Security & Validation

### Model Validation
- Check input dimensions
- Verify output ranges
- Validate model format

### Data Validation
- Joint angle normalization
- Vertex count matching
- NaN/Inf detection

## Future Extensions

### Temporal Coherence
- LSTM/GRU for animation smoothing
- Frame-to-frame consistency

### Multi-Character Transfer
- Train on multiple characters
- Style transfer between rigs

### Simulation Integration
- Ziva/Houdini data ingestion
- Physics-based corrections

### Real-Time Training
- Online learning from artist edits
- Active learning strategies

---

**Last Updated**: October 17, 2025  
**Version**: 1.0.0  
**Phase**: Phase 1 - Python Prototype

