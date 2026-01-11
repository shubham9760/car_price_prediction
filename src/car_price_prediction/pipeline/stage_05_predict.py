import joblib
import pandas as pd
from pathlib import Path
from car_price_prediction.config.configuration import ConfigurationManager
from car_price_prediction import logger

class PredictionPipeline:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.config = ConfigurationManager()

    def load_model(self):
        """Load the trained model"""
        model_path = Path("artifacts/training/model.pkl")
        if model_path.exists():
            self.model = joblib.load(model_path)
            logger.info(f"Model loaded from {model_path}")
        else:
            raise FileNotFoundError(f"Model not found at {model_path}")

    def load_scaler(self):
        """Load the scaler"""
        scaler_path = Path("artifacts/training/scaler.pkl")
        if scaler_path.exists():
            self.scaler = joblib.load(scaler_path)
            logger.info(f"Scaler loaded from {scaler_path}")
        else:
            logger.warning("Scaler not found, predictions will use unscaled features")

    def predict(self, data):
        """
        Make predictions on new data
        
        Args:
            data: pandas DataFrame with features
            
        Returns:
            predictions: numpy array of predictions
        """
        if self.model is None:
            self.load_model()
        
        if self.scaler is None:
            self.load_scaler()
        
        # Scale data if scaler exists
        if self.scaler:
            data_scaled = self.scaler.transform(data)
        else:
            data_scaled = data
        
        # Make predictions
        predictions = self.model.predict(data_scaled)
        logger.info(f"Predictions made for {len(data)} samples")
        
        return predictions

if __name__ == '__main__':
    try:
        logger.info(">>>>>> Prediction Pipeline started <<<<<<")
        
        # Example usage
        pipeline = PredictionPipeline()
        
        # Load sample data
        sample_data = pd.read_csv("artifacts/data_ingestion/car_price_prediction.csv").head(5)
        prepare_base_model_config = pipeline.config.get_prepare_base_model_config()
        
        # Select only feature columns
        X_sample = sample_data[prepare_base_model_config.feature_columns]
        
        # Make predictions
        predictions = pipeline.predict(X_sample)
        print(f"Predictions: {predictions}")
        
        logger.info(">>>>>> Prediction Pipeline completed <<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e
