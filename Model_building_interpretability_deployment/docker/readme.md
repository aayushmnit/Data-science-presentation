## Exposing model as Flask API

To run the flask application through docker follow the following steps -

### Creating a docker image
- Open docker quickstart terminal and go to this "docker" folder
- To create a docker image run "docker build -t flaskexample" , where flaskexample will be the name of docker image
- After image is created run this command - "docker run -p 4000:80 flaskexample" to run a container with our app
- To see if the application is running correctly use  section 6 of "Flask - Classification.ipynb" notebook in training folder to see if the flask application within the docker is running successfully

** Note - The IP address of flask API will depend on the OS of your machine. I was using windows and that's why the IP address was http://192.168.99.100:4000/, for linux users it will be http://localhost:4000/. For more info refer to this [docker tutorial](https://docs.docker.com/get-started/part2/#run-the-app).