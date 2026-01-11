import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor
from sklearn.model_selection import cross_val_score, cross_validate
from car_price_prediction import logger
import joblib
from pathlib import Path
import json


class ModelFactory:
    """Factory for creating and managing different ML models"""
    
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.models = {}
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize all available models"""
        self.models = {
            'linear_regression': LinearRegression(),
            'random_forest': RandomForestRegressor(
                n_estimators=100,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=self.random_state,
                n_jobs=-1
            ),
            'xgboost': XGBRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=self.random_state,
                n_jobs=-1
            ),
            'gradient_boosting': GradientBoostingRegressor(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                subsample=0.8,
                random_state=self.random_state
            )
        }
        logger.info(f"Initialized {len(self.models)} models: {list(self.models.keys())}")
    
    def get_model(self, model_name):
        """Get a specific model by name"""
        if model_name not in self.models:
            raise ValueError(f"Unknown model: {model_name}. Available: {list(self.models.keys())}")
        return self.models[model_name]
    
    def get_all_models(self):
        """Get all available models"""
        return self.models
    
    def train(self, X_train, y_train, model_name):
        """Train a specific model"""
        try:
            model = self.get_model(model_name)
            logger.info(f"Training {model_name}...")
            model.fit(X_train, y_train)
            logger.info(f"{model_name} trained successfully")
            return model
        except Exception as e:
            logger.error(f"Error training {model_name}: {e}")
            raise
    
    def compare_models(self, X_train, y_train, X_test, y_test, cv_folds=5):
        """Compare all models with cross-validation and test metrics"""
        from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
        
        results = {}
        
        for model_name, model in self.models.items():
            logger.info(f"Evaluating {model_name}...")
            
            try:
                # Cross-validation scores
                cv_scores = cross_val_score(
                    model, X_train, y_train,
                    cv=cv_folds,
                    scoring='r2',
                    n_jobs=-1
                )
                
                # Train on full training set and evaluate on test set
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                
                # Calculate metrics
                mse = mean_squared_error(y_test, y_pred)
                rmse = np.sqrt(mse)
                mae = mean_absolute_error(y_test, y_pred)
                r2 = r2_score(y_test, y_pred)
                
                results[model_name] = {
                    'cv_mean': float(cv_scores.mean()),
                    'cv_std': float(cv_scores.std()),
                    'test_r2': float(r2),
                    'test_rmse': float(rmse),
                    'test_mae': float(mae),
                    'test_mse': float(mse)
                }
                
                logger.info(
                    f"{model_name}: CV R² = {cv_scores.mean():.4f} ± {cv_scores.std():.4f}, "
                    f"Test R² = {r2:.4f}, RMSE = {rmse:.2f}"
                )
                
            except Exception as e:
                logger.error(f"Error evaluating {model_name}: {e}")
                results[model_name] = {'error': str(e)}
        
        return results


class ModelComparison:
    """Component for comparing models and selecting the best one"""
    
    def __init__(self, output_dir='artifacts/model_comparison'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.comparison_results = None
    
    def run_comparison(self, X_train, y_train, X_test, y_test, cv_folds=5):
        """Run model comparison"""
        factory = ModelFactory()
        self.comparison_results = factory.compare_models(
            X_train, y_train, X_test, y_test, cv_folds
        )
        return self.comparison_results
    
    def save_comparison(self):
        """Save comparison results to JSON"""
        if self.comparison_results:
            output_path = self.output_dir / 'model_comparison.json'
            with open(output_path, 'w') as f:
                json.dump(self.comparison_results, f, indent=4)
            logger.info(f"Comparison results saved to {output_path}")
            return output_path
        else:
            logger.warning("No comparison results to save")
            return None
    
    def get_best_model(self):
        """Get the best performing model"""
        if not self.comparison_results:
            logger.error("No comparison results available")
            return None
        
        best_model_name = max(
            self.comparison_results.items(),
            key=lambda x: x[1].get('test_r2', float('-inf')) if 'error' not in x[1] else float('-inf')
        )[0]
        
        logger.info(f"Best model: {best_model_name}")
        return best_model_name
    
    def get_comparison_summary(self):
        """Get a summary of the comparison"""
        if not self.comparison_results:
            return None
        
        summary = {}
        for model_name, metrics in self.comparison_results.items():
            if 'error' not in metrics:
                summary[model_name] = {
                    'cv_r2': f"{metrics['cv_mean']:.4f} ± {metrics['cv_std']:.4f}",
                    'test_r2': f"{metrics['test_r2']:.4f}",
                    'test_rmse': f"{metrics['test_rmse']:.2f}"
                }
        
        return summary
