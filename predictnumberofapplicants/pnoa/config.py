import os


def find_data_root():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return current_dir.replace('pnoa', 'data')


DATA_ROOT = find_data_root() 
TRAINING_FILE = os.path.join(DATA_ROOT, 'training.csv')
TEST_FILE = os.path.join(DATA_ROOT, 'test.csv')
PREDICTION_RESULTS_FILE = os.path.join(DATA_ROOT, 'prediction_results.csv')
REGRESSION_MODEL_FILE = os.path.join(DATA_ROOT, 'regression_model.pckl')
CITIES_FILE = os.path.join(DATA_ROOT, 'cities.pckl')
COLUMNS_TRAINING = ['job_type', 'hours', 'city', 'salary', 'applications']
