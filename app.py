from flask import Flask, request, jsonify

from networksecurity.components.push_data import NetworkDataExtract
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidationConfig,DataValidation
from networksecurity.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from networksecurity.components.data_transformation import DataTransformation, DataTransformationConfig
app = Flask(__name__)


COLLECTION_NAME = "phishingData"

'''
Step1: insert scv data in mongo db
'''
@app.route('/insert-data-to-mongo', methods=['GET'])
def insert_data_to_mongo():
  FILE_PATH = "Network_Data/dataset.csv"
  
  ob = NetworkDataExtract()
  records = ob.convert_csv_to_json(file_path=FILE_PATH)

  result = ob.insert_data_to_mongo_db(records=records, collection=COLLECTION_NAME)

  return jsonify({'result':result})

'''
Step1.1: delete all records from mongo db
'''
@app.route('/delete-all-records', methods=['DELETE'])
def delete_all_records():
  ob = NetworkDataExtract()
  result = ob.delete_data_from_mongo(collection=COLLECTION_NAME)
  return jsonify({'result':result.deleted_count})



@app.route('/process-data', methods=['GET'])
def data_ingestion():
  trainingPipelineConfig =TrainingPipelineConfig()
  # Step2: data ingestion
  dataIngestionConfig = DataIngestionConfig(trainingPipelineConfig)
  dataIngestion = DataIngestion(dataIngestionConfig)
  data_ingestion_artifact = dataIngestion.initiate_data_ingestion()

  # Step3: Data Validation
  data_validation_config = DataValidationConfig(trainingPipelineConfig)
  data_validation = DataValidation(data_ingestion_artifact, data_validation_config)

  data_validation_artifacts = data_validation.initate_data_validation()

  # Step4: data transformation
  data_transformation_config = DataTransformationConfig(trainingPipelineConfig)
  data_transformation = DataTransformation(data_validation_artifacts, data_transformation_config)
  data_transformation_artifact = data_transformation.initate_data_transformation()
  return jsonify({
     'data_validation_artifacts': data_validation_artifacts, 
     'data_transformation_artifact': data_transformation_artifact
  })

if __name__=="__main__":
    app.run(host="0.0.0.0", debug=True)   