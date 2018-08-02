## Exposing model as Flask API

To run the flask application follow the following steps -

- Open a python 3 environment and cd to this folder
- Run "python main.py"
- To see if the application is running correctly use  section 6 of "Flask - Classification.ipynb" notebook in training folder

To deploy it on google cloud(app.yml needed) -
- Just open google sdk and cd to this folder
- Run "gcloud app deploy" which will then initiate a docker image on a kubernetes cluster with elastic environment