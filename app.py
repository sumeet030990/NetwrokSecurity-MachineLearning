import os,sys
import pandas as pd
import certifi
from networksecurity.exception.exception import CustomException
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()

from networksecurity.utils.main_utils import load_object, save_object
from networksecurity.utils.ml_utils.models.estimator import NetworkModel

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse

from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.constants.training_pipeline import FINAL_DIR, PREPROCESSING_OBJECT_FILE_NAME, MODEL_FILE_NAME

app = FastAPI()
origin=["*"]

app.add_middleware(
  CORSMiddleware,
  allow_origins= origin,
  allow_credentials = True,
  allow_methods=["*"],
  allow_headers=["*"]
)

@app.get("/", tags=["authentication"])
async def index():
  return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
  try:
    train_pipeline = TrainingPipeline()
    train_pipeline.run_pipeline()

    return Response("Training is successful")
  except Exception as e:
    raise CustomException(e,sys)

@app.post("/predict")
async def predict(request:Request, file_obj: UploadFile=File(...)):
  try:
    df= pd.read_csv(file_obj.file)

    preprocessor_path = os.path.join(FINAL_DIR, PREPROCESSING_OBJECT_FILE_NAME)
    preprocessor = load_object(file_path=preprocessor_path)

    final_model_path = os.path.join(FINAL_DIR, MODEL_FILE_NAME)
    final_model = load_object(final_model_path)

    network_model = NetworkModel(preprocessor = preprocessor, model = final_model)
    y_pred = network_model.predict(df)

    df['predicted_column'] = y_pred

    df.to_csv('input_output/output.csv')

    return Response("Prediction completed: please check: input_output/result.csv")
  except Exception as e:
    raise CustomException(e,sys)
  

if __name__=="__main__":
  app_run(app,host="localhost", port=8000)   