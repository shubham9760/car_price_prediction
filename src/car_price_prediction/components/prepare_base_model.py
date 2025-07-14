import pandas as pd
from pathlib import Path
import joblib
from sklearn.linear_model import LinearRegression
from car_price_prediction.entity.config_entity import PrepareBaseModelConfig


class PrepareBaseModel:
    def __init__(self, config: PrepareBaseModelConfig):
        self.config = config
        self.model = None

    def get_base_model(self):
        """
        Initialize a base Linear Regression model and save it.
        """
        self.model = LinearRegression()
        self.save_model(self.config.base_model_path, self.model)
        print(f"✅ Base model saved at: {self.config.base_model_path}")

    def update_base_model(self):
        """
        Load dataset, train model on training data, and save updated model.
        """
        df = pd.read_csv(self.config.test_data_path)

        # Extract features and target
        X = df[self.config.feature_columns]
        y = df[self.config.target_column]

        # Train the model
        self.model.fit(X, y)

        # Save the trained model
        self.save_model(self.config.updated_base_model_path, self.model)
        print(f"✅ Trained model saved at: {self.config.updated_base_model_path}")

    @staticmethod
    def save_model(path: Path, model):
        """
        Save the model to a .pkl file using joblib.
        """
        joblib.dump(model, path)
