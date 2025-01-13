from networksecurity.exception.exception import CustomException
import os
import sys

from networksecurity.entity.config_entity import ModelTrainingConfig
from networksecurity.utils.main_utils import save_object, load_object, load_numpy_array_data, evaluate_models
from networksecurity.utils.ml_utils.metrics.classification_metric import get_classification_score
from networksecurity.entity.artifact_entity import ClassificationMetricArtifact
 
from networksecurity.utils.ml_utils.models.estimator import NetworkModel

from networksecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact

##Model Trainer
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier, RandomForestClassifier
import mlflow   


class ModelTrainer:
  def __init__(self, model_trainer_config: ModelTrainingConfig, data_transformation_artifact: DataTransformationArtifact):
    try:
      self.model_trainer_config = model_trainer_config
      self.data_transformation_artifact = data_transformation_artifact
    except Exception as e:
      raise CustomException(e, sys)
  
  def track_mlflow(self, best_model,classification_test_metrics:ClassificationMetricArtifact):
    try:
      with mlflow.start_run():
        f1_score = classification_test_metrics.f1_score
        precision_score = classification_test_metrics.precision_score
        recall_score = classification_test_metrics.recall_score

        mlflow.log_metric("f1_score", f1_score)
        mlflow.log_metric("precision_score", precision_score)
        mlflow.log_metric("recall_score", recall_score)
        mlflow.sklearn.log_model(best_model, "best_model")

    except Exception as e:
      raise CustomException(e, sys)
  
  def train_model(self, x_train, y_train, x_test, y_test)->ModelTrainerArtifact:
    models = {
      "RandomForestClassifier": RandomForestClassifier(verbose=1),
      "DecisionTreeClassifier": DecisionTreeClassifier(),
      "GradientBoostingClassifier": GradientBoostingClassifier(verbose=1),
      "LinearRegression": LinearRegression(),
      "AdaBoostClassifier": AdaBoostClassifier(),
    }

    params={
        "Random Forest":{
            # 'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
            # 'max_features':['sqrt','log2',None],
            'n_estimators': [8,16,32,64,128,256]
        },
        "Decision Tree": {
            'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
            # 'splitter':['best','random'],
            # 'max_features':['sqrt','log2'],
        },
        "Gradient Boosting":{
            # 'loss':['squared_error', 'huber', 'absolute_error', 'quantile'],
            'learning_rate':[.1,.01,.05,.001],
            'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
            # 'criterion':['squared_error', 'friedman_mse'],
            # 'max_features':['auto','sqrt','log2'],
            'n_estimators': [8,16,32,64,128,256]
        },
        "Linear Regression":{},
        "AdaBoost Regressor":{
            'learning_rate':[.1,.01,0.5,.001],
            # 'loss':['linear','square','exponential'],
            'n_estimators': [8,16,32,64,128,256]
        }
      }
    
    model_report, fitted_models  = evaluate_models(X_train=x_train, y_train=y_train,X_test = x_test, y_test= y_test, models=models, params=params)

    # to get the best model score
    best_model_score = max(model_report.values())

    # to get the best model name from dict
    best_model_name = max(model_report, key=model_report.get)
    print(f"best_model_name: {best_model_name}")
    print(f"best_model_score: {best_model_score}")
    best_model = fitted_models[best_model_name]
    y_train_pred = best_model.predict(x_train)

    classification_train_metrics = get_classification_score(y_true=y_train, y_pred=y_train_pred)

    y_test_pred = best_model.predict(x_test)

    classification_test_metrics = get_classification_score(y_true=y_test, y_pred=y_test_pred)
    

    ## track the mlflow
    self.track_mlflow(best_model,classification_test_metrics)

    preprocessor = load_object(file_path=self.data_transformation_artifact.tranformed_object_file_path)

    model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
    os.makedirs(model_dir_path,exist_ok=True)

    networkModel = NetworkModel(preprocessor=preprocessor, model=best_model)
    save_object(self.model_trainer_config.trained_model_file_path, obj=networkModel)

    # Model Trainer Artifact
    model_trainer_artifact =  ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path, train_metric_artifact=classification_train_metrics, test_metric_artifact= classification_test_metrics)

    return model_trainer_artifact

  def initiate_model_trainer(self)->ModelTrainerArtifact:
    try:
      train_file_path = self.data_transformation_artifact.tranformed_train_file_path
      test_file_path = self.data_transformation_artifact.tranformed_test_file_path

      ## Loading Training and Testing array
      train_arr = load_numpy_array_data(train_file_path)
      test_arr = load_numpy_array_data(test_file_path)

      ## Split X and y
      x_train, y_train, x_test, y_test = (
        train_arr[:,:-1],
        train_arr[:,-1],
        test_arr[:,:-1],
        test_arr[:,-1]
      )

      model_trainer_artifact = self.train_model(x_train, y_train, x_test, y_test)

      return model_trainer_artifact
    except Exception as e:
      raise CustomException(e, sys)

