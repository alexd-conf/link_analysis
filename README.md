# Link Analysis
The purpose of this application is to provide a tool which people can use to gather information about a hyperlink, most likely to check if they want to visit that hyperlink.<br>
Please refer to the 'backend' and 'frontend' directories for instructions on how to run the application locally for development.<br>
## Docker Instructions
### Build a Docker image
Navigate to the root directory for the project.<br>
<code>docker-compose build</code><br>
### Run the Docker container
Navigate to the root directory for the projecct.<br>
<code>docker-compose up</code><br>
### Run Docker test containers (normally done in a pipeline, but can be done locally)
#### For the Backend
Navigate to the 'backend' directory.<br>
<code>docker-compose -f docker-compose.test.yml build</code><br>
<code>docker-compose -f docker-compose.text.yml up</code><br>
#### For the Frontend
Navigate to the 'frontend' directory.<br>
<code>docker-compose -f docker-compose.test.yml build</code><br>
<code>docker-compose -f docker-compose.text.yml up</code><br>
