from car_price_prediction.config.configuration import ConfigurationManager
from car_price_prediction.components.evaluation import Evaluation
from car_price_prediction import logger
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

STAGE_NAME = "Evaluation Stage"

class EvaluationPipeline:
    def __init__(self):
        pass

    def preprocess_data(self, df: pd.DataFrame):
        """Preprocess the dataframe"""
        df = df.copy()
        
        # Replace '-' with NaN
        df = df.replace('-', pd.NA)
        
        # Handle categorical columns by label encoding
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].fillna('Unknown')
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))
        
        # Convert to numeric and fill NaN
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Fill remaining NaN with median
        df = df.fillna(df.median())
        
        return df

    def main(self):
        config = ConfigurationManager()
        eval_config = config.get_validation_config()
        prepare_base_model_config = config.get_prepare_base_model_config()
        
        # Load data
        logger.info("Loading data for evaluation")
        df = pd.read_csv(prepare_base_model_config.test_data_path)
        
        # Preprocess data
        logger.info("Preprocessing data for evaluation")
        df = self.preprocess_data(df)
        
        # Extract features and target
        X = df[prepare_base_model_config.feature_columns]
        y = df[prepare_base_model_config.target_column]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Initialize evaluation
        logger.info("Loading model for evaluation")
        evaluation = Evaluation(config=eval_config)
        evaluation.load_model()
        evaluation.load_scaler()
        
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
