import os
from pathlib import Path
from car_price_prediction.entity.config_entity import PrepareCallbacksConfig
from car_price_prediction import logger


class PrepareCallbacks:
    def __init__(self, config: PrepareCallbacksConfig):
        self.config = config

    def get_tb_callback(self):
        """
        Get TensorBoard callback for monitoring training (if using TensorFlow)
        This is a placeholder for future TensorFlow implementation
        """
        logger.info(f"TensorBoard logs will be saved at: {self.config.tensorboard_root_log_dir}")
        return None

    def get_checkpoint_callback(self):
        """
        Get model checkpoint callback
        This is a placeholder for future model checkpointing
        """
        logger.info(f"Model checkpoints will be saved at: {self.config.checkpoint_model_filepath}")
        return None
