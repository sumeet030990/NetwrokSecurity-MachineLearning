import pymongo
import sys
from dotenv import load_dotenv
import os
import certifi
import pandas as pd
import json
from networksecurity.logging import logger
from networksecurity.exception.exception import CustomException

load_dotenv()
DB_NAME=os.getenv('DB_NAME')
MONGO_DB_URL=os.getenv('MONGO_DB_URL')

'''
ca = Trusted certificate authorities. 
This is used for SSL or TLS connections to verify that, the server you're connecting has a trusted certificate
'''

ca = certifi.where()

class NetworkDataExtract():
  def __init__(self):
    try:
      self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
      self.database = self.mongo_client[DB_NAME]

    except Exception as e:
        raise CustomException(e,sys)
    
  def convert_csv_to_json(self,file_path:str):
    try:
      df = pd.read_csv(file_path)
      df.drop(['index'], axis=1, inplace=True)
      df.reset_index(drop=True, inplace=True)

      json_data = df.T.to_json()

      records = list(json.loads(json_data).values())
      return records

    except Exception as e:
      raise CustomException(e, sys)
  
  def insert_data_to_mongo_db(self, records,collection):
    
    mongo_collection = self.database[collection]
    mongo_collection.insert_many(records)

    return (len(records))
  
  def delete_data_from_mongo(self,collection):
    try:
      mongo_collection = self.database[collection]
      result = mongo_collection.delete_many({})

      return result
    except Exception as e:
      print(e)
      raise CustomException(e,sys)



# if __name__ == '__main__':
#   FILE_PATH = "Network_Data/Phishing_Legitimate_full.csv"
#   COLLECTION_NAME = "phishingData"
#   ob = NetworkDataExtract()
#   records = ob.convert_csv_to_json(file_path=FILE_PATH)

#   result = ob.insert_data_to_mongo_db(records=records,database=DB_NAME, collection=COLLECTION_NAME)
#   print(result)

