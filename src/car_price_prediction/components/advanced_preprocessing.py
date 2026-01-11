"""
Advanced preprocessing and feature engineering for car price prediction
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from car_price_prediction import logger
import warnings
warnings.filterwarnings('ignore')


class AdvancedPreprocessor:
    """Advanced data preprocessing with feature engineering"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_stats = {}
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and prepare raw data"""
        df = df.copy()
        
        # Remove ID column (not useful for prediction)
        if 'ID' in df.columns:
            df = df.drop('ID', axis=1)
        
        # Clean numeric columns with object type
        # Robust parsing for Engine volume (e.g. '2.0 Turbo') and Mileage (e.g. '186005 km')
        if 'Engine volume' in df.columns:
            eng = df['Engine volume'].astype(str).str.replace(',', '.')
            eng_num = eng.str.extract(r'([0-9]+(?:\.[0-9]+)?)', expand=False)
            df['Engine volume'] = pd.to_numeric(eng_num, errors='coerce')

        if 'Mileage' in df.columns:
            mile = df['Mileage'].astype(str).str.replace('[^0-9]', '', regex=True)
            mile = mile.replace('', '0')
            df['Mileage'] = pd.to_numeric(mile, errors='coerce')
        
        # Handle Levy column (convert to numeric)
        if 'Levy' in df.columns:
            df['Levy'] = df['Levy'].replace('-', '0').astype(str)
            df['Levy'] = pd.to_numeric(df['Levy'], errors='coerce').fillna(0)

        # Only drop rows missing Price (target); fill other numeric NaNs with median
        if 'Price' in df.columns:
            df = df.dropna(subset=['Price'])

        # Fill remaining numeric missing values with median
        try:
            df = df.fillna(df.median(numeric_only=True))
        except Exception:
            # fallback: fill numeric columns individually
            num_cols = df.select_dtypes(include=[float, int]).columns
            for c in num_cols:
                df[c] = df[c].fillna(df[c].median())
        
        logger.info(f"Data cleaned: {df.shape[0]} rows, {df.shape[1]} columns")
        return df
    
    def create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create engineered features from raw features"""
        df = df.copy()
        
        # Age of vehicle
        df['Vehicle_Age'] = 2020 - df['Prod. year']
        
        # Engine size categories
        df['Engine_Size_Category'] = pd.cut(df['Engine volume'], 
                                             bins=[0, 1.5, 2.5, 3.5, float('inf')],
                                             labels=['Small', 'Medium', 'Large', 'XLarge'])
        
        # Mileage categories
        df['Mileage_Category'] = pd.cut(df['Mileage'], 
                                        bins=[0, 50000, 100000, 150000, float('inf')],
                                        labels=['Low', 'Medium', 'High', 'Very_High'])
        
        # Price per year
        df['Price_per_Year'] = df['Price'] / (df['Vehicle_Age'] + 1)
        
        # Interaction features
        df['Engine_Cylinders'] = df['Engine volume'] * df['Cylinders']
        df['Mileage_Age_Interaction'] = df['Mileage'] * df['Vehicle_Age']
        
        # Premium indicators
        df['Premium_Leather'] = (df['Leather interior'] == 'Yes').astype(int)
        df['Premium_Airbags'] = (df['Airbags'] > 6).astype(int)
        
        logger.info(f"Features created: {df.shape[1]} features total")
        return df
    
    def encode_categorical(self, df: pd.DataFrame, fit=True) -> pd.DataFrame:
        """Encode categorical variables"""
        df = df.copy()
        
        categorical_cols = df.select_dtypes(include='object').columns.tolist()
        
        for col in categorical_cols:
            if col not in ['Engine_Size_Category', 'Mileage_Category']:  # Skip already encoded
                if fit:
                    le = LabelEncoder()
                    df[col] = le.fit_transform(df[col].astype(str))
                    self.label_encoders[col] = le
                else:
                    if col in self.label_encoders:
                        le = self.label_encoders[col]
                        df[col] = le.transform(df[col].astype(str))
        
        # Handle categorical features we created
        for col in ['Engine_Size_Category', 'Mileage_Category']:
            if col in df.columns:
                df[col] = pd.factorize(df[col])[0]
        
        logger.info(f"Categorical variables encoded: {len(categorical_cols)} columns")
        return df
    
    def remove_outliers(self, df: pd.DataFrame, target_col='Price', iqr_multiplier=1.5) -> pd.DataFrame:
        """Remove outliers using IQR method"""
        df = df.copy()
        
        # Calculate IQR for price
        if df.empty:
            logger.warning("remove_outliers called with empty dataframe")
            return df

        Q1 = df[target_col].quantile(0.25)
        Q3 = df[target_col].quantile(0.75)
        IQR = Q3 - Q1

        # Define bounds
        lower_bound = Q1 - (iqr_multiplier * IQR)
        upper_bound = Q3 + (iqr_multiplier * IQR)

        # Filter data
        initial_rows = len(df)
        df = df[(df[target_col] >= lower_bound) & (df[target_col] <= upper_bound)]

        removed = initial_rows - len(df)
        pct = (removed / initial_rows * 100) if initial_rows > 0 else 0.0
        logger.info(f"Outliers removed: {removed} rows ({pct:.1f}%)")
        return df
    
    def normalize_features(self, X, fit=True):
        """Normalize numeric features"""
        if fit:
            X_scaled = self.scaler.fit_transform(X)
        else:
            X_scaled = self.scaler.transform(X)
        
        return X_scaled
    
    def preprocess(self, df: pd.DataFrame, target_col='Price', fit=True) -> tuple:
        """Complete preprocessing pipeline"""
        # Clean data
        df = self.clean_data(df)
        
        # Remove outliers
        df = self.remove_outliers(df, target_col=target_col)
        
        # Create features
        df = self.create_features(df)
        
        # Encode categorical
        df = self.encode_categorical(df, fit=fit)
        
        # Separate features and target
        X = df.drop(target_col, axis=1)
        y = df[target_col]
        
        # Normalize features
        X_scaled = self.normalize_features(X, fit=fit)
        X_scaled = pd.DataFrame(X_scaled, columns=X.columns)
        
        logger.info(f"Preprocessing complete: X shape {X_scaled.shape}, y shape {y.shape}")
        return X_scaled, y
