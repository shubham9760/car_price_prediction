from car_price_prediction import logger
from car_price_prediction.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from car_price_prediction.pipeline.stage_02_prepare_base_model import PrepareBaseModelTrainingPipeline
from car_price_prediction.pipeline.stage_03_training import ModelTrainingPipeline
from car_price_prediction.pipeline.stage_03_advanced_training import AdvancedModelTrainingPipeline
from car_price_prediction.pipeline.stage_04_evaluation import EvaluationPipeline
import sys
import warnings
import os
import logging
from urllib3.connectionpool import log as urllib3_log

# Disable verbose logging for urllib3 and MLflow
urllib3_log.setLevel(logging.CRITICAL)
logging.getLogger('mlflow').setLevel(logging.CRITICAL)
logging.getLogger('connectionpool').setLevel(logging.CRITICAL)

# Suppress all warnings
warnings.filterwarnings('ignore')
os.environ['MLFLOW_TRACKING_URI'] = 'sqlite:///mlflow.db'
os.environ['MLFLOW_REGISTRY_STORE_URI'] = 'sqlite:///mlflow.db'


STAGE_NAME = "Data Ingestion stage"
try:
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
   data_ingestion = DataIngestionTrainingPipeline()
   data_ingestion.main()
   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logger.exception(e)
        raise e




STAGE_NAME = "Prepare base model"
try: 
   logger.info(f"*******************")
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
   prepare_base_model = PrepareBaseModelTrainingPipeline()
   prepare_base_model.main()
   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logger.exception(e)
        raise e




STAGE_NAME = "Training"
use_advanced = '--advanced' in sys.argv or True  # Use advanced training by default
try: 
   logger.info(f"*******************")
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
   
   if use_advanced:
      logger.info("Using ADVANCED training pipeline with model comparison and MLflow tracking")
      model_trainer = AdvancedModelTrainingPipeline()
   else:
      logger.info("Using BASIC training pipeline")
      model_trainer = ModelTrainingPipeline()
   
   model_trainer.main()
   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logger.exception(e)
        raise e






STAGE_NAME = "Evaluation stage"
try:
   logger.info(f"*******************")
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
   model_evalution = EvaluationPipeline()
   model_evalution.main()
   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")

except Exception as e:
        logger.exception(e)
        raise e




