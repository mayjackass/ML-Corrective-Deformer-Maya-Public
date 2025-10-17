"""
Neural Network Model for Corrective Blendshape Prediction
This module defines the ML model architecture that learns the mapping from
joint poses to vertex corrections.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class CorrectiveDeformerNet(nn.Module):
    """
    Feedforward neural network for predicting vertex displacements
    from joint pose data.
    
    Architecture:
    - Input: Joint angles (normalized)
    - Hidden layers: Fully connected with ReLU activation
    - Output: Vertex displacements (x, y, z for each vertex)
    """
    
    def __init__(self, num_joints, num_vertices, hidden_layers=[256, 512, 512, 256]):
        """
        Initialize the network.
        
        Args:
            num_joints (int): Number of input joint angles
            num_vertices (int): Number of vertices in the mesh
            hidden_layers (list): List of hidden layer sizes
        """
        super(CorrectiveDeformerNet, self).__init__()
        
        self.num_joints = num_joints
        self.num_vertices = num_vertices
        self.output_size = num_vertices * 3  # x, y, z per vertex
        
        # Build layers dynamically
        layers = []
        input_size = num_joints
        
        for hidden_size in hidden_layers:
            layers.append(nn.Linear(input_size, hidden_size))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(0.1))  # Regularization
            input_size = hidden_size
        
        # Output layer
        layers.append(nn.Linear(input_size, self.output_size))
        
        self.network = nn.Sequential(*layers)
        
        # Initialize weights
        self._initialize_weights()
    
    def _initialize_weights(self):
        """Initialize network weights using Xavier initialization."""
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_normal_(m.weight)
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
    
    def forward(self, joint_angles):
        """
        Forward pass through the network.
        
        Args:
            joint_angles (torch.Tensor): Batch of joint angles [batch_size, num_joints]
        
        Returns:
            torch.Tensor: Predicted vertex displacements [batch_size, num_vertices, 3]
        """
        # Pass through network
        output = self.network(joint_angles)
        
        # Reshape to [batch_size, num_vertices, 3]
        batch_size = joint_angles.size(0)
        output = output.view(batch_size, self.num_vertices, 3)
        
        return output


class CompactCorrectiveNet(nn.Module):
    """
    Lighter version of the network for faster inference in Maya.
    Uses PCA-compressed outputs for efficiency.
    """
    
    def __init__(self, num_joints, pca_components, hidden_layers=[128, 256, 128]):
        """
        Initialize compact network with PCA compression.
        
        Args:
            num_joints (int): Number of input joint angles
            pca_components (int): Number of PCA components for output
            hidden_layers (list): List of hidden layer sizes
        """
        super(CompactCorrectiveNet, self).__init__()
        
        self.num_joints = num_joints
        self.pca_components = pca_components
        
        # Build layers
        layers = []
        input_size = num_joints
        
        for hidden_size in hidden_layers:
            layers.append(nn.Linear(input_size, hidden_size))
            layers.append(nn.ReLU())
            input_size = hidden_size
        
        # Output PCA coefficients
        layers.append(nn.Linear(input_size, pca_components))
        
        self.network = nn.Sequential(*layers)
        self._initialize_weights()
    
    def _initialize_weights(self):
        """Initialize network weights."""
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_normal_(m.weight)
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
    
    def forward(self, joint_angles):
        """
        Forward pass returning PCA coefficients.
        
        Args:
            joint_angles (torch.Tensor): Batch of joint angles [batch_size, num_joints]
        
        Returns:
            torch.Tensor: PCA coefficients [batch_size, pca_components]
        """
        return self.network(joint_angles)


class ResidualCorrectiveNet(nn.Module):
    """
    Advanced architecture with residual connections for deeper networks.
    Better for complex deformations.
    """
    
    def __init__(self, num_joints, num_vertices, hidden_size=512, num_blocks=4):
        """
        Initialize residual network.
        
        Args:
            num_joints (int): Number of input joint angles
            num_vertices (int): Number of vertices
            hidden_size (int): Size of hidden layers
            num_blocks (int): Number of residual blocks
        """
        super(ResidualCorrectiveNet, self).__init__()
        
        self.num_vertices = num_vertices
        self.output_size = num_vertices * 3
        
        # Input projection
        self.input_proj = nn.Linear(num_joints, hidden_size)
        
        # Residual blocks
        self.blocks = nn.ModuleList([
            self._make_residual_block(hidden_size)
            for _ in range(num_blocks)
        ])
        
        # Output projection
        self.output_proj = nn.Linear(hidden_size, self.output_size)
        
        self._initialize_weights()
    
    def _make_residual_block(self, hidden_size):
        """Create a residual block."""
        return nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU()
        )
    
    def _initialize_weights(self):
        """Initialize weights."""
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_normal_(m.weight)
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
    
    def forward(self, joint_angles):
        """
        Forward pass with residual connections.
        
        Args:
            joint_angles (torch.Tensor): Batch of joint angles [batch_size, num_joints]
        
        Returns:
            torch.Tensor: Predicted vertex displacements [batch_size, num_vertices, 3]
        """
        # Project input
        x = self.input_proj(joint_angles)
        
        # Residual blocks
        for block in self.blocks:
            residual = x
            x = block(x)
            x = x + residual  # Residual connection
        
        # Output projection
        output = self.output_proj(x)
        
        # Reshape
        batch_size = joint_angles.size(0)
        output = output.view(batch_size, self.num_vertices, 3)
        
        return output


def count_parameters(model):
    """
    Count trainable parameters in the model.
    
    Args:
        model (nn.Module): PyTorch model
    
    Returns:
        int: Number of trainable parameters
    """
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


# Model factory function
def create_model(model_type='standard', num_joints=6, num_vertices=100, **kwargs):
    """
    Factory function to create different model architectures.
    
    Args:
        model_type (str): Type of model ('standard', 'compact', 'residual')
        num_joints (int): Number of input joints
        num_vertices (int): Number of vertices
        **kwargs: Additional arguments for specific models
    
    Returns:
        nn.Module: Instantiated model
    """
    if model_type == 'standard':
        hidden_layers = kwargs.get('hidden_layers', [256, 512, 512, 256])
        model = CorrectiveDeformerNet(num_joints, num_vertices, hidden_layers)
    
    elif model_type == 'compact':
        pca_components = kwargs.get('pca_components', 50)
        hidden_layers = kwargs.get('hidden_layers', [128, 256, 128])
        model = CompactCorrectiveNet(num_joints, pca_components, hidden_layers)
    
    elif model_type == 'residual':
        hidden_size = kwargs.get('hidden_size', 512)
        num_blocks = kwargs.get('num_blocks', 4)
        model = ResidualCorrectiveNet(num_joints, num_vertices, hidden_size, num_blocks)
    
    else:
        raise ValueError(f"Unknown model type: {model_type}")
    
    print(f"Created {model_type} model with {count_parameters(model):,} parameters")
    return model


if __name__ == "__main__":
    # Test model creation
    print("Testing model architectures...\n")
    
    # Test standard model
    model1 = create_model('standard', num_joints=6, num_vertices=100)
    test_input = torch.randn(2, 6)  # Batch of 2 samples
    output1 = model1(test_input)
    print(f"Standard model output shape: {output1.shape}\n")
    
    # Test compact model
    model2 = create_model('compact', num_joints=6, pca_components=50)
    output2 = model2(test_input)
    print(f"Compact model output shape: {output2.shape}\n")
    
    # Test residual model
    model3 = create_model('residual', num_joints=6, num_vertices=100)
    output3 = model3(test_input)
    print(f"Residual model output shape: {output3.shape}\n")
