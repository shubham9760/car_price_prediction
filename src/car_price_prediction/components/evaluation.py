import os
import pandas as pd
import joblib
from pathlib import Path
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from car_price_prediction.entity.config_entity import EvaluationConfig
from car_price_prediction.utils.common import save_json
from car_price_prediction import logger


class Evaluation:
    def __init__(self, config: EvaluationConfig):
        self.config = config
        self.model = None
        self.scaler = None
        self.label_encoders = None

    def load_model(self):
        """Load the trained model"""
        self.model = joblib.load(self.config.path_of_model)
        logger.info(f"Model loaded from {self.config.path_of_model}")

    def load_scaler(self):
        """Load the scaler used during training"""
        scaler_path = self.config.path_of_model.parent / "scaler.pkl"
        if os.path.exists(scaler_path):
            self.scaler = joblib.load(scaler_path)
            logger.info(f"Scaler loaded from {scaler_path}")
        else:
            logger.warning("Scaler not found, using unscaled data")

    def load_label_encoders(self):
        """Load the label encoders used during training"""
        encoders_path = self.config.path_of_model.parent / "label_encoders.pkl"
        if os.path.exists(encoders_path):
            self.label_encoders = joblib.load(encoders_path)
            logger.info(f"Label encoders loaded from {encoders_path}")
        else:
            logger.warning("Label encoders not found")

    def evaluate(self, X_test, y_test):
        """Evaluate the model on test data"""
        logger.info("Starting model evaluation")
        
        # Scale test data if scaler exists
        if self.scaler:
            X_test_scaled = self.scaler.transform(X_test)
        else:
            X_test_scaled = X_test
        
        # Make predictions
        y_pred = self.model.predict(X_test_scaled)
        
        # Calculate metrics
        mse = mean_squared_error(y_test, y_pred)
        rmse = mse ** 0.5
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        metrics = {
            "MSE": mse,
            "RMSE": rmse,
            "MAE": mae,
            "R2": r2
        }
        
        logger.info(f"Evaluation metrics: {metrics}")
        return metrics

    def save_score(self, scores: dict):
        """Save evaluation scores to json file"""
        scores_path = Path("scores.json")
        save_json(scores_path, scores)

