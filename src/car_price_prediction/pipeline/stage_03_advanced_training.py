from car_price_prediction.config.configuration import ConfigurationManager
from car_price_prediction.components.training import Training
from car_price_prediction.components.model_comparison import ModelFactory, ModelComparison
from car_price_prediction.components.feature_importance import FeatureAnalysisPipeline
from car_price_prediction.components.advanced_preprocessing import AdvancedPreprocessor
from car_price_prediction import logger
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib
import warnings
import os

# Suppress warnings and disable MLflow by default
warnings.filterwarnings('ignore', category=UserWarning)
os.environ['MLFLOW_TRACKING_URI'] = 'sqlite:///mlflow.db'

# Import MLflow components only if needed
try:
    from car_price_prediction.model_tracking import MLFlowTracker, ModelVersioning
except Exception as e:
    logger.warning(f"MLflow import failed: {e}")
    MLFlowTracker = None
    ModelVersioning = None

STAGE_NAME = "Advanced Training Stage"


class AdvancedModelTrainingPipeline:
    """Advanced training pipeline with multiple models, cross-validation, and tracking"""
    
    def __init__(self):
        self.config = ConfigurationManager()
        self.tracker = None
        self.versioning = None
        
        # Try to initialize MLflow only if available
        if MLFlowTracker:
            try:
                self.tracker = MLFlowTracker()
            except Exception as e:
                logger.debug(f"MLflow initialization failed: {e}")
        
        if ModelVersioning:
            try:
                self.versioning = ModelVersioning()
            except Exception as e:
                logger.debug(f"Model versioning initialization failed: {e}")
        
        self.best_model = None
        self.best_model_name = None
        self.scaler = None
        self.label_encoders = {}
        self.preprocessor = AdvancedPreprocessor()
    
    def preprocess_data(self, df: pd.DataFrame):
        """Preprocess the dataframe using advanced preprocessing"""
        # Use the advanced preprocessor
        X, y = self.preprocessor.preprocess(df, target_col='Price', fit=True)
        
        # Save preprocessor state for later use
        self.scaler = self.preprocessor.scaler
        self.label_encoders = self.preprocessor.label_encoders
        
        return X, y
    
    def train_with_comparison(self, X_train, y_train, X_test, y_test):
        """Train and compare multiple models"""
        logger.info("Starting model comparison")
        
        # Create model comparison instance
        comparison = ModelComparison()
        results = comparison.run_comparison(X_train, y_train, X_test, y_test, cv_folds=5)
        
        # Save comparison results
        comparison.save_comparison()
        
        # Get best model name
        self.best_model_name = comparison.get_best_model()
        logger.info(f"Best model selected: {self.best_model_name}")
        
        # Train and return the best model
        factory = ModelFactory()
        self.best_model = factory.train(X_train, y_train, self.best_model_name)
        
        return results
    
    def apply_feature_scaling(self, X_train, X_test):
        """Apply feature scaling using StandardScaler"""
        logger.info("Applying feature scaling")
        
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        return X_train_scaled, X_test_scaled
    
    def analyze_features(self, X_test, y_test, feature_names):
        """Analyze feature importance"""
        logger.info("Analyzing feature importance")
        
        pipeline = FeatureAnalysisPipeline(self.best_model, feature_names)
        pipeline.run_analysis(X_test, y_test)
        
        return pipeline.get_analysis_report()
    
    def track_experiment(self, metrics, params):
        """Track experiment with MLflow"""
        if not self.tracker:
            logger.debug("MLflow tracking not available")
            return
            
        logger.debug("Tracking experiment with MLflow")
        
        try:
            self.tracker.start_run(
                run_name=f"training_{self.best_model_name}",
                tags={'model': self.best_model_name, 'stage': 'advanced_training'}
            )
            
            self.tracker.log_params(params)
            self.tracker.log_metrics(metrics)
            
            self.tracker.end_run()
            logger.debug("Experiment tracked successfully")
        except Exception as e:
            logger.debug(f"Could not track to MLflow: {e}")
    
    def version_model(self, metrics, params, description=""):
        """Version the trained model"""
        logger.info("Versioning model")
        
        model_path = Path("artifacts/training/model.pkl")
        version_info = self.versioning.create_version(
            model_path, metrics, params, description
        )
    
    def save_artifacts(self, training_config):
        """Save model and scaler artifacts"""
        logger.info("Saving artifacts")
        
        # Create directory (trained_model_path is the file path, so use its parent)
        model_path = Path(training_config.trained_model_path)
        model_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save model
        joblib.dump(self.best_model, model_path)
        logger.info(f"Model saved to {model_path}")
        
        # Save scaler
        scaler_path = model_path.parent / "scaler.pkl"
        joblib.dump(self.scaler, scaler_path)
        logger.info(f"Scaler saved to {scaler_path}")
        
        # Save label encoders
        encoders_path = model_path.parent / "label_encoders.pkl"
        joblib.dump(self.label_encoders, encoders_path)
        logger.info(f"Label encoders saved to {encoders_path}")
    
    def main(self):
        """Run the advanced training pipeline"""
        try:
            training_config = self.config.get_training_config()
            prepare_base_model_config = self.config.get_prepare_base_model_config()
            
            # Load and preprocess data
            logger.info("Loading training data")
            df = pd.read_csv(prepare_base_model_config.test_data_path)
            
            logger.info("Preprocessing data")
            X, y = self.preprocess_data(df)
            
            # Prepare features and target - already done in preprocess_data
            
            # Split data with train/test split
            logger.info("Splitting data into train/test sets")
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Apply feature scaling
            X_train_scaled, X_test_scaled = self.apply_feature_scaling(X_train, X_test)
            
            # Compare and train models
            logger.info("Comparing different models")
            comparison_results = self.train_with_comparison(
                X_train_scaled, y_train, X_test_scaled, y_test
            )
            
            # Analyze feature importance
            logger.info("Analyzing feature importance")
            feature_analysis = self.analyze_features(
                X_test_scaled, y_test, list(X.columns)
            )
            
            # Prepare metrics and parameters for tracking
            from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
            y_pred = self.best_model.predict(X_test_scaled)
            
            metrics = {
                'mse': float(mean_squared_error(y_test, y_pred)),
                'rmse': float(np.sqrt(mean_squared_error(y_test, y_pred))),
                'mae': float(mean_absolute_error(y_test, y_pred)),
                'r2': float(r2_score(y_test, y_pred))
            }
            
            params = {
                'model': self.best_model_name,
                'test_size': 0.2,
                'random_state': 42,
                'scaler': 'StandardScaler'
            }
            
            # Track experiment
            self.track_experiment(metrics, params)
            
            # Version model
            version_info = self.version_model(metrics, params, f"Model: {self.best_model_name}")
            
            # Save artifacts
            self.save_artifacts(training_config)
            
            # Log final results
            logger.info("=" * 50)
            logger.info("TRAINING COMPLETED SUCCESSFULLY")
            logger.info("=" * 50)
            logger.info(f"Best Model: {self.best_model_name}")
            logger.info(f"R² Score: {metrics['r2']:.4f}")
            logger.info(f"RMSE: ${metrics['rmse']:.2f}")
            logger.info(f"MAE: ${metrics['mae']:.2f}")
            if version_info:
                logger.info(f"Model Version: {version_info['version']}")
            logger.info("=" * 50)
            
            return {
                'model': self.best_model_name,
                'metrics': metrics,
                'feature_analysis': feature_analysis,
                'version_info': version_info
            }
        
        except Exception as e:
            logger.exception(f"Error in advanced training pipeline: {e}")
            raise e


if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        pipeline = AdvancedModelTrainingPipeline()
        results = pipeline.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
