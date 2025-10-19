# Phase 1 Archive

## Purpose
This folder contains early Phase 1 development files that are **not needed for the demo** but may be useful reference for future phases.

## Archived Files

### `ml_corrective_deformer.py`
- **Status:** Incomplete Maya MPxDeformerNode plugin
- **Reason Archived:** 
  - Phase 1 uses blend shapes for simulation, not actual plugins
  - This is Phase 2/3 work (real deformer plugin development)
  - Contains placeholder ML code that doesn't function
- **Future Use:** Reference when building Phase 3 C++ plugin

### `install_deformer.py`
- **Status:** Incomplete plugin installer
- **Reason Archived:**
  - Depends on ml_corrective_deformer.py which is incomplete
  - Not needed for Phase 1 demo workflow
- **Future Use:** May adapt for Phase 2/3 installation

### `example_basic.py`
- **Status:** Examples that don't work without plugin
- **Reason Archived:**
  - Tries to use `cmds.deformer(type="mlCorrectiveDeformer")`
  - Requires ml_corrective_deformer.py plugin to be loaded
  - Not applicable to Phase 1 simulation approach
- **Future Use:** Examples for Phase 2/3 plugin usage

### `example_data_collection.py`
- **Status:** Broken - missing dependencies
- **Reason Archived:**
  - Imports `from utils.data_collector import DataCollector`
  - utils/ module doesn't exist
  - Won't run at all
- **Future Use:** May extract concepts for Phase 2 data pipeline

## Phase 1 is Complete With:

### Working Files (in parent directory):
- ✅ **`end_to_end_demo.py`** - Main 4-step workflow simulation
- ✅ **`demo_ui.py`** - User-friendly UI interface
- ✅ **`simple_demo.py`** - Early lattice-based prototype

### What Phase 1 Does:
- Simulates the complete ML workflow using blend shapes
- Uses MEL expressions to mimic neural network inference
- Demonstrates the concept end-to-end
- Creates demo videos for portfolio/LinkedIn

### What Phase 1 Does NOT Do:
- ❌ Real PyTorch training (simulated)
- ❌ Actual neural network inference (uses MEL)
- ❌ Maya deformer plugin (uses blend shapes)

## Next Steps

**Phase 2:** Implement real PyTorch training and inference
**Phase 3:** Build production C++ plugin with LibTorch

These archived files may provide useful reference when implementing those phases.

---

**Archive Created:** October 19, 2025  
**Reason:** Phase 1 cleanup - separating working demo from incomplete experiments
