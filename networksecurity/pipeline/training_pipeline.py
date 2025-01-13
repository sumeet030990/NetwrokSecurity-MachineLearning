import os,sys

from networksecurity.exception.exception import CustomException

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainingConfig

from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtifact

class TrainingPipeline:
  def __init__(self):
    self.trainingPipelineConfig = TrainingPipelineConfig()
  # Step2: data ingestion
  def start_data_ingestion(self)-> DataIngestionArtifact:
    try:
      self.dataIngestionConfig = DataIngestionConfig(self.trainingPipelineConfig)
      dataIngestion = DataIngestion(self.dataIngestionConfig)
      data_ingestion_artifact = dataIngestion.initiate_data_ingestion()

      return data_ingestion_artifact
    except Exception as e:
      raise CustomException(e,sys)

  # start Data validation
  def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
    try:
      data_validation_config = DataValidationConfig(self.trainingPipelineConfig)
      data_validation = DataValidation(data_ingestion_artifact, data_validation_config)

      data_validation_artifacts = data_validation.initate_data_validation()

      return data_validation_artifacts
    except Exception as e:
      raise CustomException(e,sys)
    
  # start Data Transformation
  def start_data_transformation(self,data_validation_artifacts: DataValidationArtifact) -> DataTransformationArtifact: 
    try:
      data_transformation_config = DataTransformationConfig(self.trainingPipelineConfig)
      data_transformation = DataTransformation(data_validation_artifacts, data_transformation_config)
      data_transformation_artifact = data_transformation.initate_data_transformation()

      return data_transformation_artifact
    except Exception as e:
      raise CustomException(e,sys)
 
  # start model training
  def start_model_training(self,data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact: 
    try:
      self.model_training_config:ModelTrainingConfig = ModelTrainingConfig(self.trainingPipelineConfig)
      model_trainer = ModelTrainer(self.model_training_config ,data_transformation_artifact)

      model_trainer_artifact = model_trainer.initiate_model_trainer()

      return model_trainer_artifact
    except Exception as e:
      raise CustomException(e,sys)
 
  # run all steps
  def run_pipeline(self): 
    try:
      data_ingestion_artifact =self.start_data_ingestion()
      data_validation_artifact =self.start_data_validation(data_ingestion_artifact)
      data_transformation_artifact = self.start_data_transformation(data_validation_artifact)
      model_trainer_artifact = self.start_model_training(data_transformation_artifact)
      
      return model_trainer_artifact
    except Exception as e:
      raise CustomException(e,sys)