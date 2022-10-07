# Overview
Having seen that the serialised model is able to be loaded from a pickled file, we now pull the model from S3 instead. This means that we can function independent of MLFlow's tracking server. The model is loaded only ONCE when the `predict.py` is run, reducing the need to pull from S3 many times.

Activate the pipenv shell and start the flask app.
```
pipenv shell
python predict.py
```

Then send a test request to the locally running flask app.
```
pipenv run python test.py
```
OR
```
pipenv shell
python test.py
```