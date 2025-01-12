from flask import Flask, request, jsonify

from networksecurity.components.push_data import NetworkDataExtract
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig

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


'''
Step2: data ingestion
'''
@app.route('/data-ingestion', methods=['GET'])
def data_ingestion():
  trainingPipelineConfig =TrainingPipelineConfig()
  dataIngestionConfig = DataIngestionConfig(trainingPipelineConfig)
  dataIngestion = DataIngestion(dataIngestionConfig)
  dataIngestion.initiate_data_ingestion()

  return jsonify({'result': 'done'})
  
if __name__=="__main__":
    app.run(host="0.0.0.0", debug=True)   