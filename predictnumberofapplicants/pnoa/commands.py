import pickle
import pandas as pd

from collections import Counter
from itertools import chain, groupby

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression

from pnoa import core 
from pnoa import config

@core.command
@core.argument('--file', default=config.TRAINING_FILE)
def train(args):
    """
    build a regression model and store it in a file.
    """
    try:
        df = pd.read_csv(
            args.file, index_col=False,
            header=0, usecols=config.COLUMNS_TRAINING)
    except IOError:
        raise ValueError('Please provide a correct file path')

    # get only necessary columns
    df = pd.read_csv(
        args.file, index_col=False, header=0, usecols=config.COLUMNS_TRAINING)

    # We need to find the real city names to replace with a int identifier
    col_city = df[['city']]
    cities_iterator = chain(*col_city.values.tolist())
    city_count_mapping = Counter(cities_iterator)
    cities = city_count_mapping.keys()

    # all columns should be int, float etc.
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
    pickle.dump(regression_model, open(config.REGRESSION_MODEL_FILE, 'wb'))
    # store cities to get cty index for prediction calls
    pickle.dump(cities, open(config.CITIES_FILE, 'wb'))

    # information about the success of model
    regression_score = regression_model.score(x_test, y_test)
    print 'Regression model score: %s' % regression_score

    # find mean squared error comparing the predicted and original values
    y_predict = regression_model.predict(x_test)
    regression_model_mse = mean_squared_error(y_predict, y_test)
    print 'Regression model mean squared error: %s' % regression_model_mse


@core.command
@core.argument('--file', default=config.TEST_FILE)
def predict(args):
    try:
        regression_model = pickle.load(
            open(config.REGRESSION_MODEL_FILE, 'rb'))
    except IOError:
        raise ValueError(
            'Please make sure that regression_model is ready. `pnoa train`')

    test_df = pd.read_csv(args.file, index_col=False, header=0)
    # pop job_id column from the original test df for making pairs after
    # prediction
    col_job_id = test_df[['job_id']]
    test_df = test_df.drop('job_id', axis=1)
    test_df = normalize_df(test_df)

    # predict new values
    predicted_values_nparr = regression_model.predict(test_df)

    # write results into a csv
    write_prediction_results(col_job_id, predicted_values_nparr)



def normalize_df(df, cities=None):
    """
    use regarding index value instead of using city name
    """
    if not cities:
        try:
            cities = pickle.load(open(config.CITIES_FILE, 'rb'))
        except IOError:
            raise ValueError(
                'Please make sure that cities is ready. `pnoa train`')

    df['city'] = df['city'].replace(
        {city: cities.index(city) for city in cities})
    return df


def write_prediction_results(col_job_id, predicted_values_nparr):
    """
    chain and zip job_id column and predicted values
    """
    job_ids_nparr = col_job_id.values

    # keep them as an iterator to reduce memory usage
    # also normalize value casting integer
    predicted_values_iterator = (
        int(pv) for pv in chain(*predicted_values_nparr.tolist()))
    job_ids_iterator = chain(*job_ids_nparr.tolist())
    # zip job_id and the predicted result
    result = zip(job_ids_iterator, predicted_values_iterator)

    # make dataframe from result matrix
    df = pd.DataFrame.from_records(result, columns=['job_id', 'prediction'])
    df.to_csv(config.PREDICTION_RESULTS_FILE, sep=',', encoding='utf-8')


def load_commands():
    """
    load all functions at runtime and return all "Command" instances as list
    """
    import commands

    attrs = set(dir(commands))
    return filter(
        lambda f: isinstance(f, core.Command), map(
            lambda attr: getattr(commands, attr), attrs))
