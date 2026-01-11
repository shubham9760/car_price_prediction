import pandas as pd
import numpy as np
import json
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.inspection import permutation_importance
from sklearn.preprocessing import StandardScaler
from car_price_prediction import logger
import joblib


class FeatureImportanceAnalyzer:
    """Analyze and visualize feature importance"""
    
    def __init__(self, output_dir='artifacts/feature_importance'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.feature_importance = None
        self.feature_names = None
    
    def calculate_linear_coefficients(self, model, feature_names):
        """Calculate feature importance from linear model coefficients"""
        try:
            if hasattr(model, 'coef_'):
                coefficients = model.coef_
                
                # Calculate absolute importance
                importance = np.abs(coefficients)
                
                # Normalize to sum to 1
                importance = importance / importance.sum()
                
                # Create dataframe
                self.feature_importance = pd.DataFrame({
                    'feature': feature_names,
                    'importance': importance,
                    'coefficient': coefficients
                }).sort_values('importance', ascending=False)
                
                self.feature_names = feature_names
                logger.info("Linear coefficients calculated successfully")
                return self.feature_importance
            else:
                logger.warning("Model does not have coef_ attribute")
                return None
        except Exception as e:
            logger.error(f"Error calculating linear coefficients: {e}")
            return None
    
    def calculate_tree_feature_importance(self, model, feature_names):
        """Calculate feature importance from tree-based models"""
        try:
            if hasattr(model, 'feature_importances_'):
                importance = model.feature_importances_
                
                self.feature_importance = pd.DataFrame({
                    'feature': feature_names,
                    'importance': importance
                }).sort_values('importance', ascending=False)
                
                self.feature_names = feature_names
                logger.info("Tree feature importances calculated successfully")
                return self.feature_importance
            else:
                logger.warning("Model does not have feature_importances_ attribute")
                return None
        except Exception as e:
            logger.error(f"Error calculating tree feature importance: {e}")
            return None
    
    def calculate_permutation_importance(self, model, X_test, y_test, feature_names, n_repeats=10):
        """Calculate permutation importance"""
        try:
            perm_importance = permutation_importance(
                model, X_test, y_test,
                n_repeats=n_repeats,
                random_state=42,
                n_jobs=-1
            )
            
            self.feature_importance = pd.DataFrame({
                'feature': feature_names,
                'importance': perm_importance.importances_mean,
                'std': perm_importance.importances_std
            }).sort_values('importance', ascending=False)
            
            self.feature_names = feature_names
            logger.info("Permutation importance calculated successfully")
            return self.feature_importance
        except Exception as e:
            logger.error(f"Error calculating permutation importance: {e}")
            return None
    
    def plot_feature_importance(self, top_n=15, figsize=(12, 6)):
        """Plot feature importance"""
        if self.feature_importance is None:
            logger.warning("No feature importance data available")
            return None
        
        try:
            top_features = self.feature_importance.head(top_n)
            
            fig, ax = plt.subplots(figsize=figsize)
            ax.barh(range(len(top_features)), top_features['importance'])
            ax.set_yticks(range(len(top_features)))
            ax.set_yticklabels(top_features['feature'])
            ax.set_xlabel('Importance')
            ax.set_ylabel('Feature')
            ax.set_title(f'Top {top_n} Feature Importance')
            ax.invert_yaxis()
            
            plt.tight_layout()
            
            # Save plot
            plot_path = self.output_dir / 'feature_importance_plot.png'
            fig.savefig(plot_path, dpi=300, bbox_inches='tight')
            logger.info(f"Feature importance plot saved to {plot_path}")
            
            plt.close()
            return plot_path
        except Exception as e:
            logger.error(f"Error plotting feature importance: {e}")
            return None
    
    def save_importance(self):
        """Save feature importance to CSV and JSON"""
        if self.feature_importance is None:
            logger.warning("No feature importance data to save")
            return None
        
        try:
            # Save as CSV
            csv_path = self.output_dir / 'feature_importance.csv'
            self.feature_importance.to_csv(csv_path, index=False)
            logger.info(f"Feature importance saved to {csv_path}")
            
            # Save as JSON
            json_path = self.output_dir / 'feature_importance.json'
            importance_dict = self.feature_importance.to_dict('records')
            with open(json_path, 'w') as f:
                json.dump(importance_dict, f, indent=4)
            logger.info(f"Feature importance saved to {json_path}")
            
            return {'csv': csv_path, 'json': json_path}
        except Exception as e:
            logger.error(f"Error saving feature importance: {e}")
            return None
    
    def get_summary(self, top_n=10):
        """Get summary of feature importance"""
        if self.feature_importance is None:
            return None
        
        top_features = self.feature_importance.head(top_n)
        summary = {
            'top_features': top_features['feature'].tolist(),
            'importance_values': top_features['importance'].tolist(),
            'cumulative_importance': top_features['importance'].cumsum().tolist()
        }
        
        # Add coefficient info if available
        if 'coefficient' in self.feature_importance.columns:
            summary['coefficients'] = top_features['coefficient'].tolist()
        
        return summary
    
    def get_feature_stats(self):
        """Get statistics about feature importance"""
        if self.feature_importance is None:
            return None
        
        importance_vals = self.feature_importance['importance'].values
        
        return {
            'total_features': len(importance_vals),
            'mean_importance': float(np.mean(importance_vals)),
            'std_importance': float(np.std(importance_vals)),
            'min_importance': float(np.min(importance_vals)),
            'max_importance': float(np.max(importance_vals)),
            'top_5_cumulative_importance': float(self.feature_importance['importance'].head(5).sum())
        }


class FeatureAnalysisPipeline:
    """Complete pipeline for feature analysis"""
    
    def __init__(self, model, feature_names, output_dir='artifacts/feature_importance'):
        self.model = model
        self.feature_names = feature_names
        self.analyzer = FeatureImportanceAnalyzer(output_dir)
    
    def run_analysis(self, X_test=None, y_test=None):
        """Run complete feature analysis"""
        try:
            # Try different importance calculation methods
            if hasattr(self.model, 'coef_'):
                logger.info("Using linear model coefficients")
                self.analyzer.calculate_linear_coefficients(self.model, self.feature_names)
            elif hasattr(self.model, 'feature_importances_'):
                logger.info("Using tree-based feature importances")
                self.analyzer.calculate_tree_feature_importance(self.model, self.feature_names)
            
            # If test data provided, also calculate permutation importance
            if X_test is not None and y_test is not None:
                logger.info("Calculating permutation importance")
                self.analyzer.calculate_permutation_importance(
                    self.model, X_test, y_test, self.feature_names
                )
            
            # Save and visualize
            self.analyzer.save_importance()
            self.analyzer.plot_feature_importance()
            
            logger.info("Feature analysis completed successfully")
            return self.analyzer.feature_importance
        except Exception as e:
            logger.error(f"Error running feature analysis: {e}")
            return None
    
    def get_analysis_report(self):
        """Get complete analysis report"""
        report = {
            'feature_importance': self.analyzer.get_summary(),
            'statistics': self.analyzer.get_feature_stats(),
            'total_features': len(self.feature_names)
        }
        return report
