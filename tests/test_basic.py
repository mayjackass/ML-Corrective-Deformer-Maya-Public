"""
Test Suite for ML Corrective Deformer
Run basic tests to verify the installation and functionality
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from ml_training import model
        print("  ✓ ml_training.model")
    except ImportError as e:
        print(f"  ✗ ml_training.model: {e}")
        return False
    
    try:
        from ml_training import train
        print("  ✓ ml_training.train")
    except ImportError as e:
        print(f"  ✗ ml_training.train: {e}")
        return False
    
    # Note: Maya modules will fail outside Maya
    print("  ℹ Maya modules skipped (not in Maya environment)")
    
    return True


def test_model_creation():
    """Test neural network model creation"""
    print("\nTesting model creation...")
    
    try:
        from ml_training.model import create_model
        
        # Test standard model
        model = create_model('standard', num_joints=6, num_vertices=100)
        print("  ✓ Standard model created")
        
        # Test compact model
        model = create_model('compact', num_joints=6, pca_components=50)
        print("  ✓ Compact model created")
        
        # Test residual model
        model = create_model('residual', num_joints=6, num_vertices=100)
        print("  ✓ Residual model created")
        
        return True
    except Exception as e:
        print(f"  ✗ Model creation failed: {e}")
        return False


def test_model_forward_pass():
    """Test model forward pass"""
    print("\nTesting model forward pass...")
    
    try:
        import torch
        from ml_training.model import create_model
        
        model = create_model('standard', num_joints=6, num_vertices=100)
        
        # Create dummy input
        batch_size = 4
        num_joints = 6
        input_tensor = torch.randn(batch_size, num_joints)
        
        # Forward pass
        output = model(input_tensor)
        
        # Check output shape
        expected_shape = (batch_size, 100, 3)
        if output.shape == expected_shape:
            print(f"  ✓ Forward pass successful: {output.shape}")
            return True
        else:
            print(f"  ✗ Unexpected output shape: {output.shape} (expected {expected_shape})")
            return False
            
    except Exception as e:
        print(f"  ✗ Forward pass failed: {e}")
        return False


def test_config_file():
    """Test configuration file"""
    print("\nTesting configuration file...")
    
    try:
        import json
        config_path = os.path.join(project_root, "config.json")
        
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Check required sections
        required_sections = ['project', 'paths', 'deformer', 'training']
        for section in required_sections:
            if section in config:
                print(f"  ✓ Config section '{section}' found")
            else:
                print(f"  ✗ Config section '{section}' missing")
                return False
        
        return True
    except Exception as e:
        print(f"  ✗ Config test failed: {e}")
        return False


def test_project_structure():
    """Test that all required directories exist"""
    print("\nTesting project structure...")
    
    required_dirs = [
        'phase1_python_prototype',
        'ml_training',
        'utils',
        'data',
        'models',
        'docs',
        'tests'
    ]
    
    all_exist = True
    for dir_name in required_dirs:
        dir_path = os.path.join(project_root, dir_name)
        if os.path.isdir(dir_path):
            print(f"  ✓ {dir_name}/")
        else:
            print(f"  ✗ {dir_name}/ not found")
            all_exist = False
    
    return all_exist


def test_documentation():
    """Test that documentation files exist"""
    print("\nTesting documentation...")
    
    required_docs = [
        'README.md',
        'PROJECT_SUMMARY.md',
        'QUICK_REFERENCE.md',
        'docs/QUICKSTART.md',
        'docs/ARCHITECTURE.md',
        'config.json',
        'requirements.txt'
    ]
    
    all_exist = True
    for doc in required_docs:
        doc_path = os.path.join(project_root, doc)
        if os.path.isfile(doc_path):
            print(f"  ✓ {doc}")
        else:
            print(f"  ✗ {doc} not found")
            all_exist = False
    
    return all_exist


def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("ML Corrective Deformer - Test Suite")
    print("="*60)
    
    tests = [
        ("Project Structure", test_project_structure),
        ("Documentation", test_documentation),
        ("Configuration", test_config_file),
        ("Imports", test_imports),
        ("Model Creation", test_model_creation),
        ("Model Forward Pass", test_model_forward_pass),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Project is ready to use.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review errors above.")
    
    print("="*60)
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
