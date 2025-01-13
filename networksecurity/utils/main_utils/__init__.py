import yaml
import os,sys
import pickle
from networksecurity.exception.exception import CustomException
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score


def read_yaml_file(file_path:str)->dict:
  try:
    with open(file_path, "rb") as yaml_file:
      return yaml.safe_load(yaml_file)
  except Exception as e:
    raise CustomException(e,sys)

def write_yaml_file(file_path:str, content: object, replace: bool = False) -> None:
  try:
    if replace:
      if os.path.exists(file_path):
        os.remove(file_path)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w") as file:
      yaml.dump(content, file)
  except Exception as e:
    raise CustomException(e,sys)
  
  '''
  save numpy array data to file
  file_path: str location of file to save
  array: np.array data to save
  '''
def save_numpy_array_data(file_path:str, array:np.array):
  try:
    dir_path = os.path.dirname(file_path)
    os.makedirs(dir_path,exist_ok=True)

    with open(file_path, "wb") as file_obj:
      np.save(file_obj, array)
  except Exception as e:
    raise CustomException(e,sys)
  
  '''
  load numpy array data file
  file_path: str location of file to save
  array: np.array data to save
  '''
def load_numpy_array_data(file_path:str) -> np.array:
  try:
    with open(file_path, "rb") as file_obj:
      return np.load(file_obj)
  except Exception as e:
    raise CustomException(e,sys)
    
def save_object(file_path:str, obj:object):
    try:
      dir_path = os.path.dirname(file_path)
      os.makedirs(dir_path,exist_ok=True)

      with open(file_path, "wb") as file_obj:
        pickle.dump(obj, file_obj)
    except Exception as e:
      raise CustomException(e,sys)
    
def load_object(file_path:str)-> object:
    try:
      if not os.path.exists(file_path):
        raise Exception(f"The file: {file_path} does not exists")

      with open(file_path, "rb") as file_obj:
        pickle.load(file_obj)
    except Exception as e:
      raise CustomException(e,sys)

def evaluate_models(X_train, y_train,X_test , y_test, models, params):
  report = {}
  fitted_models = {}
  try:
    for name, model in models.items():
      params = params.get(name, {})
      
      # Use GridSearchCV for hyperparameter tuning if parameters are provided
      if params:
          gs = GridSearchCV(model, params, cv=3, scoring="r2", n_jobs=-1)
          gs.fit(X_train, y_train)
          best_model = gs.best_estimator_
      else:
          # Directly fit the model if no params are provided
          model.fit(X_train, y_train)
          best_model = model

      # Store the fitted model
      fitted_models[name] = best_model

      # Evaluate on test data
      y_pred = best_model.predict(X_test)
      report[name] = r2_score(y_test, y_pred)

      return report, fitted_models
  except Exception as e:
    raise CustomException(e, sys)
