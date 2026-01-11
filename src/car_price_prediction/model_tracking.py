import json
from pathlib import Path
from car_price_prediction import logger
import pandas as pd

# Try to import MLflow, but make it optional
try:
    import mlflow
    import mlflow.sklearn
    import mlflow.xgboost
    MLFLOW_AVAILABLE = True
except ImportError:
    MLFLOW_AVAILABLE = False
    logger.warning("MLflow not available - model tracking disabled")


class MLFlowTracker:
    """Track and manage models using MLflow (gracefully handles when MLflow is unavailable)"""
    
    def __init__(self, tracking_uri='http://localhost:5001', experiment_name='car_price_prediction'):
        """Initialize MLflow tracker
        
        Args:
            tracking_uri: MLflow server URI
            experiment_name: Experiment name
        """
        self.enabled = False
        
        if not MLFLOW_AVAILABLE:
            logger.warning("MLflow tracking disabled - library not available")
            return
            
        try:
            mlflow.set_tracking_uri(tracking_uri)
            mlflow.set_experiment(experiment_name)
            self.enabled = True
            logger.info(f"MLflow tracking initialized: {tracking_uri}")
        except Exception as e:
            logger.warning(f"Could not initialize MLflow: {e} - tracking disabled")
    
    def log_model(self, model, model_name, artifact_path="model"):
        """Log a model to MLflow
        
        Args:
            model: Trained model object
            model_name: Name of the model
            artifact_path: Path to save the model
        """
        if not self.enabled:
            return False
            
        try:
            # Log model based on type
            if 'xgboost' in str(type(model)).lower():
                mlflow.xgboost.log_model(model, artifact_path=artifact_path)
            else:
                mlflow.sklearn.log_model(model, artifact_path=artifact_path)
            
            logger.info(f"Model '{model_name}' logged to MLflow")
            return True
        except Exception as e:
            logger.debug(f"Could not log model to MLflow: {e}")
            return False
    
    def log_metrics(self, metrics, step=None):
        """Log metrics to MLflow
        
        Args:
            metrics: Dictionary of metric names and values
            step: Optional step number
        """
        if not self.enabled:
            return
            
        try:
            for metric_name, metric_value in metrics.items():
                mlflow.log_metric(metric_name, metric_value, step=step)
            logger.debug(f"Logged {len(metrics)} metrics to MLflow")
        except Exception as e:
            logger.debug(f"Could not log metrics to MLflow: {e}")
    
    def log_params(self, params):
        """Log parameters to MLflow
        
        Args:
            params: Dictionary of parameter names and values
        """
        if not self.enabled:
            return
            
        try:
            for param_name, param_value in params.items():
                mlflow.log_param(param_name, param_value)
            logger.debug(f"Logged {len(params)} parameters to MLflow")
        except Exception as e:
            logger.debug(f"Could not log parameters to MLflow: {e}")
    
    def log_artifact(self, local_path, artifact_path=None):
        """Log artifact to MLflow
        
        Args:
            local_path: Local file path
            artifact_path: Remote artifact path
        """
        if not self.enabled:
            return
            
        try:
            if artifact_path:
                mlflow.log_artifact(local_path, artifact_path=artifact_path)
            else:
                mlflow.log_artifact(local_path)
            logger.debug(f"Artifact logged to MLflow: {local_path}")
        except Exception as e:
            logger.debug(f"Could not log artifact to MLflow: {e}")
    
    def start_run(self, run_name=None, tags=None):
        """Start a new MLflow run
        
        Args:
            run_name: Name for the run
            tags: Dictionary of tags
        """
        if not self.enabled:
            return
            
        try:
            mlflow.start_run(run_name=run_name)
            if tags:
                for tag_name, tag_value in tags.items():
                    mlflow.set_tag(tag_name, tag_value)
            logger.debug(f"MLflow run started: {run_name}")
        except Exception as e:
            logger.debug(f"Could not start MLflow run: {e}")
    
    def end_run(self):
        """End the current MLflow run"""
        if not self.enabled:
            return
            
        try:
            mlflow.end_run()
            logger.debug("MLflow run ended")
        except Exception as e:
            logger.debug(f"Could not end MLflow run: {e}")
    
    def register_model(self, model_uri, model_name):
        """Register a model in the MLflow registry
        
        Args:
            model_uri: URI of the model to register
            model_name: Name for the registered model
        """
        try:
            mlflow.register_model(model_uri, model_name)
            logger.info(f"Model registered: {model_name}")
        except Exception as e:
            logger.error(f"Error registering model: {e}")
    
    def get_run_info(self):
        """Get information about the current run"""
        try:
            run = mlflow.active_run()
            if run:
                return {
                    'run_id': run.info.run_id,
                    'run_name': run.info.run_name,
                    'status': run.info.status,
                    'artifact_uri': run.info.artifact_uri
                }
            else:
                logger.warning("No active MLflow run")
                return None
        except Exception as e:
            logger.error(f"Error getting run info: {e}")
            return None


class ModelVersioning:
    """Manage model versions and metadata"""
    
    def __init__(self, version_dir='artifacts/model_versions'):
        self.version_dir = Path(version_dir)
        self.version_dir.mkdir(parents=True, exist_ok=True)
        self.versions = self._load_versions()
    
    def _load_versions(self):
        """Load version history from file"""
        version_file = self.version_dir / 'versions.json'
        if version_file.exists():
            with open(version_file, 'r') as f:
                return json.load(f)
        return []
    
    def _save_versions(self):
        """Save version history to file"""
        version_file = self.version_dir / 'versions.json'
        with open(version_file, 'w') as f:
            json.dump(self.versions, f, indent=4)
    
    def create_version(self, model_path, metrics, params, description=""):
        """Create a new model version
        
        Args:
            model_path: Path to the model file
            metrics: Dictionary of metrics
            params: Dictionary of parameters
            description: Version description
        
        Returns:
            Version info dictionary
        """
        try:
            version_num = len(self.versions) + 1
            version_info = {
                'version': version_num,
                'model_path': str(model_path),
                'metrics': metrics,
                'params': params,
                'description': description,
                'timestamp': pd.Timestamp.now().isoformat(),
                'status': 'active'
            }
            
            self.versions.append(version_info)
            self._save_versions()
            
            logger.info(f"Model version {version_num} created")
            return version_info
        except Exception as e:
            logger.error(f"Error creating model version: {e}")
            return None
    
    def get_latest_version(self):
        """Get the latest active model version"""
        active_versions = [v for v in self.versions if v.get('status') == 'active']
        if active_versions:
            return active_versions[-1]
        return None
    
    def get_version_history(self):
        """Get complete version history"""
        return self.versions
    
    def promote_version(self, version_num, status='production'):
        """Change the status of a model version
        
        Args:
            version_num: Version number to promote
            status: New status (e.g., 'production', 'staging', 'archived')
        """
        try:
            for version in self.versions:
                if version['version'] == version_num:
                    version['status'] = status
                    self._save_versions()
                    logger.info(f"Version {version_num} promoted to {status}")
                    return True
            logger.warning(f"Version {version_num} not found")
            return False
        except Exception as e:
            logger.error(f"Error promoting version: {e}")
            return False
    
    def get_comparison(self, version1, version2):
        """Compare two model versions
        
        Args:
            version1: First version number
            version2: Second version number
        
        Returns:
            Comparison dictionary
        """
        v1 = next((v for v in self.versions if v['version'] == version1), None)
        v2 = next((v for v in self.versions if v['version'] == version2), None)
        
        if not (v1 and v2):
            logger.warning(f"Could not find versions {version1} and {version2}")
            return None
        
        comparison = {
            'version1': v1['version'],
            'version2': v2['version'],
            'metrics_v1': v1['metrics'],
            'metrics_v2': v2['metrics'],
            'difference': {}
        }
        
        # Calculate differences
        for metric, value1 in v1['metrics'].items():
            value2 = v2['metrics'].get(metric)
            if value2:
                try:
                    comparison['difference'][metric] = float(value2) - float(value1)
                except:
                    pass
        
        return comparison
