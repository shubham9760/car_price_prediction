import pandas as pd
from pathlib import Path
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from car_price_prediction.entity.config_entity import PrepareBaseModelConfig
from car_price_prediction import logger


class PrepareBaseModel:
    def __init__(self, config: PrepareBaseModelConfig):
        self.config = config
        self.model = None
        self.label_encoders = {}

    def preprocess_data(self, df: pd.DataFrame):
        """
        Preprocess the dataframe: handle missing values, encode categorical features
        """
        df = df.copy()
        
        # Replace '-' with NaN
        df = df.replace('-', pd.NA)
        
        # Drop rows with missing target
        df = df.dropna(subset=[self.config.target_column])
        
        # Handle categorical columns by label encoding
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if col in self.config.feature_columns:
                df[col] = df[col].fillna('Unknown')
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))
                self.label_encoders[col] = le
        
        # Fill remaining numeric NaN with median
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            if df[col].isna().any():
                df[col].fillna(df[col].median(), inplace=True)
        
        return df

    def get_base_model(self):
        """
        Initialize a base Linear Regression model and save it.
        """
        self.model = LinearRegression()
        self.save_model(self.config.base_model_path, self.model)
        logger.info(f"✅ Base model saved at: {self.config.base_model_path}")

    def update_base_model(self):
        """
        Load dataset, train model on training data, and save updated model.
        """
        df = pd.read_csv(self.config.test_data_path)
        
        # Preprocess data
        df = self.preprocess_data(df)

        # Extract features and target
        X = df[self.config.feature_columns]
        y = df[self.config.target_column]
        
        # Ensure numeric types
        y = pd.to_numeric(y, errors='coerce').dropna()
        X = X.loc[y.index]

        # Train the model
        self.model.fit(X, y)

        # Save the trained model
        self.save_model(self.config.updated_base_model_path, self.model)
        logger.info(f"✅ Trained model saved at: {self.config.updated_base_model_path}")

    @staticmethod
    def save_model(path: Path, model):
        """
        Save the model to a .pkl file using joblib.
        """
        joblib.dump(model, path)
