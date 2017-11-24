# Predict Number Of Applications Using Existing Data

pnoa: means -Predict Number Of Applicants-. pnoa will be used also for CLI tool

## Installation
```
make
```
This will create a virtualenv with "venv" name, install pnoa package 
in editable mode(now pnoa can be called under this virtualenv as cli) 
and execute train function to be able to store regression_model.pckl under data/
 
## Predict
```
make predict
```
This will generate prediction_results.csv under data/

## Also can be called
```
pnoa train --file=<path to training file>
```

```
pnoa predict --file=<path to test file>
```

## How to scale?

### Celery (Distributed Task Queue)
* All created new jobs will be pushed a queue.
* I would calculate CPU resource and give regarding process count to regarding worker
* I would call prediction function for each job and create/update prediction_results.csv
* I would also consider race condition for the file in write status (maybe mutex can be used)
* I would keep regression_model in memory for each process, so while celery is upping, i would read and deserialize regression_model into a field and make process faster.
* Result is nearly real-time.
* Also i would update training file for the closed jobs eventually and keep it up-to-date to increase performance of regresion model

### PredictionIO (Spark - MLlib - ElasticSearch/HBase)
* I would provide data(jobs which no longer active) from original storage to PredictionIO Event Server(Data Storage) batch or real time.
* PredictionIo Engine will be generating the best preditive model in its own engine.
* So when the predictive model was created once, engine will be deployed as a web service.
* We can call it for prediction through REST API in real-time.
