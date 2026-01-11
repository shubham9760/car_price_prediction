import os
import pandas as pd
import joblib
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from car_price_prediction.entity.config_entity import TrainingConfig
from car_price_prediction import logger


class Training:
    def __init__(self, config: TrainingConfig):
        self.config = config
        self.model = None
        self.scaler = StandardScaler()

    def get_base_model(self):
        """Load the base model from the updated base model path"""
        self.model = joblib.load(self.config.updated_base_model_path)
        logger.info(f"Base model loaded from {self.config.updated_base_model_path}")

    def train_full_model(self, X_train, y_train):
        """Train the model on full training data"""
        logger.info("Training model on full dataset")
        
        # Ensure numeric types
        X_train = X_train.copy()
        y_train = y_train.copy()
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # Train model
        self.model.fit(X_train_scaled, y_train)
        
        logger.info("Model training completed")

    def save_model(self, path: Path):
        """Save the trained model"""
        joblib.dump(self.model, path)
        logger.info(f"Model saved at {path}")
        
    def save_scaler(self, path: Path):
        """Save the scaler for later use in predictions"""
        scaler_path = path.parent / "scaler.pkl"
        joblib.dump(self.scaler, scaler_path)
        logger.info(f"Scaler saved at {scaler_path}")
