"""
Training Script for Corrective Deformer Neural Network
Handles data loading, training loop, validation, and model export.
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split
import numpy as np
import json
import os
import sys
from datetime import datetime
from tqdm import tqdm

# Add current directory to path for local imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from model import create_model


class CorrectiveDeformerDataset(Dataset):
    """
    PyTorch Dataset for pose-to-correction training data.
    """
    
    def __init__(self, data_file):
        """
        Load dataset from file.
        
        Args:
            data_file (str): Path to dataset file (.npz format)
        """
        data = np.load(data_file)
        self.joint_angles = torch.FloatTensor(data['joint_angles'])
        self.vertex_deltas = torch.FloatTensor(data['vertex_deltas'])
        
        # Store metadata
        self.num_samples = len(self.joint_angles)
        self.num_joints = self.joint_angles.shape[1]
        self.num_vertices = self.vertex_deltas.shape[1]
        
        print(f"Loaded dataset: {self.num_samples} samples")
        print(f"  Joints: {self.num_joints}")
        print(f"  Vertices: {self.num_vertices}")
    
    def __len__(self):
        return self.num_samples
    
    def __getitem__(self, idx):
        return self.joint_angles[idx], self.vertex_deltas[idx]


class Trainer:
    """
    Training manager for the corrective deformer network.
    """
    
    def __init__(self, model, device='cuda', learning_rate=0.001):
        """
        Initialize trainer.
        
        Args:
            model (nn.Module): The neural network model
            device (str): Device to train on ('cuda' or 'cpu')
            learning_rate (float): Learning rate for optimizer
        """
        self.device = torch.device(device if torch.cuda.is_available() else 'cpu')
        self.model = model.to(self.device)
        
        self.criterion = nn.MSELoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        self.scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            self.optimizer, mode='min', factor=0.5, patience=10, verbose=True
        )
        
        self.train_losses = []
        self.val_losses = []
        self.best_val_loss = float('inf')
        
        print(f"Training on device: {self.device}")
    
    def train_epoch(self, train_loader):
        """
        Train for one epoch.
        
        Args:
            train_loader (DataLoader): Training data loader
        
        Returns:
            float: Average training loss
        """
        self.model.train()
        total_loss = 0.0
        
        for joint_angles, vertex_deltas in train_loader:
            joint_angles = joint_angles.to(self.device)
            vertex_deltas = vertex_deltas.to(self.device)
            
            # Forward pass
            self.optimizer.zero_grad()
            predictions = self.model(joint_angles)
            loss = self.criterion(predictions, vertex_deltas)
            
            # Backward pass
            loss.backward()
            self.optimizer.step()
            
            total_loss += loss.item()
        
        return total_loss / len(train_loader)
    
    def validate(self, val_loader):
        """
        Validate the model.
        
        Args:
            val_loader (DataLoader): Validation data loader
        
        Returns:
            float: Average validation loss
        """
        self.model.eval()
        total_loss = 0.0
        
        with torch.no_grad():
            for joint_angles, vertex_deltas in val_loader:
                joint_angles = joint_angles.to(self.device)
                vertex_deltas = vertex_deltas.to(self.device)
                
                predictions = self.model(joint_angles)
                loss = self.criterion(predictions, vertex_deltas)
                
                total_loss += loss.item()
        
        return total_loss / len(val_loader)
    
    def train(self, train_loader, val_loader, num_epochs, save_dir):
        """
        Full training loop.
        
        Args:
            train_loader (DataLoader): Training data loader
            val_loader (DataLoader): Validation data loader
            num_epochs (int): Number of epochs to train
            save_dir (str): Directory to save checkpoints
        """
        os.makedirs(save_dir, exist_ok=True)
        
        print(f"\nStarting training for {num_epochs} epochs...")
        
        for epoch in range(num_epochs):
            # Train
            train_loss = self.train_epoch(train_loader)
            self.train_losses.append(train_loss)
            
            # Validate
            val_loss = self.validate(val_loader)
            self.val_losses.append(val_loss)
            
            # Learning rate scheduling
            self.scheduler.step(val_loss)
            
            # Print progress
            print(f"Epoch [{epoch+1}/{num_epochs}] "
                  f"Train Loss: {train_loss:.6f} | "
                  f"Val Loss: {val_loss:.6f}")
            
            # Save best model
            if val_loss < self.best_val_loss:
                self.best_val_loss = val_loss
                self.save_checkpoint(save_dir, 'best_model.pth', epoch, val_loss)
                print(f"  ✓ Saved best model (val_loss: {val_loss:.6f})")
            
            # Save periodic checkpoint
            if (epoch + 1) % 10 == 0:
                self.save_checkpoint(save_dir, f'checkpoint_epoch_{epoch+1}.pth', epoch, val_loss)
        
        print("\nTraining completed!")
        print(f"Best validation loss: {self.best_val_loss:.6f}")
        
        # Export final model
        self.export_for_maya(save_dir)
    
    def save_checkpoint(self, save_dir, filename, epoch, val_loss):
        """Save model checkpoint."""
        checkpoint = {
            'epoch': epoch,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'val_loss': val_loss,
            'train_losses': self.train_losses,
            'val_losses': self.val_losses
        }
        torch.save(checkpoint, os.path.join(save_dir, filename))
    
    def export_for_maya(self, save_dir):
        """
        Export model in formats usable by Maya.
        Exports both TorchScript and ONNX formats.
        """
        self.model.eval()
        
        # Create example input for tracing
        num_joints = self.model.num_joints
        example_input = torch.randn(1, num_joints).to(self.device)
        
        # Export to TorchScript
        try:
            traced_model = torch.jit.trace(self.model, example_input)
            torchscript_path = os.path.join(save_dir, 'model_torchscript.pt')
            traced_model.save(torchscript_path)
            print(f"✓ Exported TorchScript model: {torchscript_path}")
        except Exception as e:
            print(f"✗ Failed to export TorchScript: {e}")
        
        # Export to ONNX
        try:
            onnx_path = os.path.join(save_dir, 'model.onnx')
            torch.onnx.export(
                self.model,
                example_input,
                onnx_path,
                export_params=True,
                opset_version=11,
                do_constant_folding=True,
                input_names=['joint_angles'],
                output_names=['vertex_deltas'],
                dynamic_axes={
                    'joint_angles': {0: 'batch_size'},
                    'vertex_deltas': {0: 'batch_size'}
                }
            )
            print(f"✓ Exported ONNX model: {onnx_path}")
        except Exception as e:
            print(f"✗ Failed to export ONNX: {e}")
        
        # Save model metadata
        metadata = {
            'num_joints': int(num_joints),
            'num_vertices': int(self.model.num_vertices),
            'best_val_loss': float(self.best_val_loss),
            'export_date': datetime.now().isoformat()
        }
        metadata_path = os.path.join(save_dir, 'model_metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"✓ Saved metadata: {metadata_path}")


def train_corrective_deformer(
    data_file,
    save_dir,
    model_type='standard',
    num_epochs=100,
    batch_size=32,
    learning_rate=0.001,
    val_split=0.2,
    device='cuda'
):
    """
    Main training function.
    
    Args:
        data_file (str): Path to training data (.npz file)
        save_dir (str): Directory to save trained models
        model_type (str): Type of model architecture
        num_epochs (int): Number of training epochs
        batch_size (int): Batch size for training
        learning_rate (float): Learning rate
        val_split (float): Validation split ratio
        device (str): Device to train on
    """
    print("="*60)
    print("ML Corrective Deformer Training")
    print("="*60)
    
    # Load dataset
    dataset = CorrectiveDeformerDataset(data_file)
    
    # Split into train/val
    val_size = int(len(dataset) * val_split)
    train_size = len(dataset) - val_size
    train_dataset, val_dataset = random_split(dataset, [train_size, val_size])
    
    # Create data loaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    
    print(f"\nDataset split: {train_size} train, {val_size} validation")
    
    # Create model
    model = create_model(
        model_type=model_type,
        num_joints=dataset.num_joints,
        num_vertices=dataset.num_vertices
    )
    
    # Create trainer and train
    trainer = Trainer(model, device=device, learning_rate=learning_rate)
    trainer.train(train_loader, val_loader, num_epochs, save_dir)
    
    return trainer


if __name__ == "__main__":
    # Example usage
    import argparse
    
    parser = argparse.ArgumentParser(description='Train corrective deformer model')
    parser.add_argument('--data', type=str, required=True, help='Path to training data')
    parser.add_argument('--save-dir', type=str, default='../models/trained', help='Save directory')
    parser.add_argument('--model-type', type=str, default='standard', 
                       choices=['standard', 'compact', 'residual'], help='Model architecture')
    parser.add_argument('--epochs', type=int, default=100, help='Number of epochs')
    parser.add_argument('--batch-size', type=int, default=32, help='Batch size')
    parser.add_argument('--lr', type=float, default=0.001, help='Learning rate')
    parser.add_argument('--device', type=str, default='cuda', help='Device (cuda/cpu)')
    
    args = parser.parse_args()
    
    trainer = train_corrective_deformer(
        data_file=args.data,
        save_dir=args.save_dir,
        model_type=args.model_type,
        num_epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.lr,
        device=args.device
    )
