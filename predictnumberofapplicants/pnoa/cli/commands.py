import pickle
import pandas as pd

from collections import Counter
from itertools import chain, groupby

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression

from pnoa.cli import core 


TRAINING_FILE = 'data/training.csv'
REGRESSION_MODEL_FILE = 'data/regression_model.pckl'
CITIES_FILE = 'data/cities.pckl'
TEST_FILE = 'data/test.csv'
COLUMNS_TRAINING = ['job_type', 'hours', 'city', 'salary', 'applications']
COLUMNS_TEST = ['job_type', 'hours', 'city', 'salary']

@core.command
@core.argument('--file', default=TRAINING_FILE)
def train(args):
    try:
        df = pd.read_csv(
            TRAINING_FILE, index_col=False, header=0, usecols=COLUMNS_TRAINING)
    except IOError:
        raise ValueError('Please provide a correct file path')

    # get only necessary columns
    df = pd.read_csv(
        TRAINING_FILE, index_col=False, header=0, usecols=COLUMNS_TRAINING)

    # We need to find real city names to replace with a int identifier
    col_city = df[['city']]
    cities_iterator = chain(*col_city.values.tolist())
    city_count_mapping = Counter(cities_iterator)
    cities = city_count_mapping.keys()

    df = normalize_df(df, cities=cities)

    # split into two dataframe
    x = df.drop('applications', axis=1)
    y = df[['applications']]

    # split dataframes into two seperated set for traning and testing
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25,
                                                        random_state=1)
    # build predictive model
    regression_model = LinearRegression()
    regression_model.fit(x_train, y_train)

    # store predictive model in a file
    pickle.dump(regression_model, open(REGRESSION_MODEL_FILE, 'wb'))
    # store cities to get cty index for prediction calls
    pickle.dump(cities, open(CITIES_FILE, 'wb'))

    # information about the success of model
    regression_score = regression_model.score(x_test, y_test)
    print 'Regression model score: %s' % regression_score

    # find mean squared error comparing the predicted and original values
    y_predict = regression_model.predict(x_test)
    regression_model_mse = mean_squared_error(y_predict, y_test)
    print 'Regression model mean squared error: %s' % regression_model_mse


@core.command
@core.argument('--file', default=TEST_FILE)
def predict(args):
    try:
        regression_model = pickle.load(open(REGRESSION_MODEL_FILE, 'rb'))
    except IOError:
        raise ValueError(
            'Please make sure that regression_model is ready. `pnoa train`')

    test_file = args.file
    original_test_df = pd.read_csv(
        test_file, index_col=False, header=0, usecols=COLUMNS_TEST)
    test_df = normalize_df(original_test_df)

    # predict new values
    predicted_values = regression_model.predict(test_df)
    col_job_id = original_test_df[['job_id']]
    __import__('ipdb').set_trace()



def normalize_df(df, cities=None):
    if not cities:
        try:
            cities = pickle.load(open(CITIES_FILE, 'rb'))
        except IOError:
            raise ValueError(
                'Please make sure that cities is ready. `pnoa train`')

    df['city'] = df['city'].replace(
        {city: cities.index(city) for city in cities})
    return df
    __import__('ipdb').set_trace()


def load_commands():
    import commands

    attrs = set(dir(commands))
    return filter(
        lambda f: isinstance(f, core.Command), map(
            lambda attr: getattr(commands, attr), attrs))
