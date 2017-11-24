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
