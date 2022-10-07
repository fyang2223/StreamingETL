# Overview
First, manually move the `pipe.bin` serialised pipeline model into this directory from the first directory. The `predict.py` file will take a locally stored serialised model and serve it with flask. When the flask app is started, whenever a request is sent to the url, the code in `predict_endpoint()` is executed, loading and unserialising the model, then using it to generate features from the json object, then outputting a prediction.

Since we used SKLearn 0.24.2 to create the model in Jupyter, we setup the virtual environment with:
```
pipenv install scikit-learn==0.24.2 flask requests --python=3.9
```

Start the flask app in `predict.py` and then send a test request with the following (make sure to be in the pipenv environment):
```
python predict.py 
python test.py
```

An alternative to running the flask app locally is to do so through a Docker container. We copy the flask application `predict.py` and serialised model `pipe.bin` to a docker container running a python image. We then send a test request (use the pipenv env).
```
docker build -t bike-prediction:v1 .
docker run -it --rm -p 9696:9696 bike-prediction:v1
python test.py
```

# Notes
If you `EXPOSE` a port, the service in the container is not accessible from outside Docker, but from inside other Docker containers. So this is good for inter-container communication. If you `EXPOSE` and `-p` a port, the service in the container is accessible from anywhere, even outside Docker.

# Links
https://stackoverflow.com/questions/22111060/what-is-the-difference-between-expose-and-publish-in-docker