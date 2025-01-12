import os


'''
Constants related to Data Ingestion
'''
DATA_INGESTION_DATABASE_NAME:str="network-security"
DATA_INGESTION_COLLECTION_NAME:str="phishingData"
DATA_INGESTION_DIR_NAME:str="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str="feature_store"
DATA_INGESTION_INGESTED_DIR:str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float= 0.2

'''
defining common constant variable for training pipeline
'''
TARGET_COLUMN = "Result"
PIPELINE_NAME="NetworkSecurity"
ARTIFACT_DIR="Artifacts"
FILE_NAME="dataset.csv"

TRAIN_FILE_NAME="train.csv"
TEST_FILE_NAME="test.csv"

SCHEMA_FILE_PATH = os.path.join("data_schema", "schema.yaml")

'''
Constants related to Data Validation
'''
DATA_VALIDATION_DIR_NAME:str="data_validation"
DATA_VALIDATION_VALIDATED_DIR:str="validated"
DATA_VALIDATION_INVALIDATED_DIR:str="invalidated"
DATA_VALIDATION_DRIFT_REPORT_DIR:str="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str= "report.yaml"