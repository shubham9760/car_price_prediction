from car_price_prediction.config.configuration import ConfigurationManager
from car_price_prediction.components.evaluation import Evaluation
from car_price_prediction.components.advanced_preprocessing import AdvancedPreprocessor
from car_price_prediction import logger
import pandas as pd
from sklearn.model_selection import train_test_split
import joblib
from pathlib import Path

STAGE_NAME = "Evaluation Stage"

class EvaluationPipeline:
    def __init__(self):
        self.preprocessor = AdvancedPreprocessor()
        self.label_encoders = None
        self.scaler = None

    def load_preprocessor_state(self):
        """Load the fitted preprocessor state from training"""
        training_dir = Path("artifacts/training")
        
        # Load label encoders
        encoders_path = training_dir / "label_encoders.pkl"
        if encoders_path.exists():
            self.label_encoders = joblib.load(encoders_path)
            self.preprocessor.label_encoders = self.label_encoders
            logger.info(f"Label encoders loaded from {encoders_path}")
        else:
            logger.warning("Label encoders not found, using new instance")
        
        # Load scaler
        scaler_path = training_dir / "scaler.pkl"
        if scaler_path.exists():
            self.scaler = joblib.load(scaler_path)
            self.preprocessor.scaler = self.scaler
            logger.info(f"Scaler loaded from {scaler_path}")
        else:
            logger.warning("Scaler not found, using new instance")

    def main(self):
        config = ConfigurationManager()
        eval_config = config.get_validation_config()
        prepare_base_model_config = config.get_prepare_base_model_config()
        
        # Load preprocessor state from training
        self.load_preprocessor_state()
        
        # Load data
        logger.info("Loading data for evaluation")
        df = pd.read_csv(prepare_base_model_config.test_data_path)
        
        # Preprocess data using advanced preprocessing with fitted state
        logger.info("Preprocessing data for evaluation")
        X, y = self.preprocessor.preprocess(df, target_col='Price', fit=False)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Initialize evaluation
        logger.info("Loading model for evaluation")
        evaluation = Evaluation(config=eval_config)
        evaluation.load_model()
        evaluation.load_scaler()
        evaluation.load_label_encoders()
        
        # Evaluate model
        logger.info("Evaluating model")
        scores = evaluation.evaluate(X_test, y_test)
        
        # Save scores
        evaluation.save_score(scores)
        logger.info(f"Evaluation completed. Scores: {scores}")

if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = EvaluationPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
