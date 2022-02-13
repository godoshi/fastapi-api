
# Requirements

python 3.9.10

## Project setup
1. create virtual environment
```
python -m venv venv
```
2. activate virtual environment
```
source venv/bin/activate
```
3. install requirements
```
pip install -r api/requirements.txt
```
4. create `api/.env` using `api/.env.example`

## Run locally
1. start the api server
```
cd api
uvicorn main:app --reload
```

## API docs
API docs are available when running locally: http://127.0.0.1:8000/docs

## Infrastructure
*Make sure you stay in the same region!*
### AWS S3
Used to store files uploaded via the API and the lambda deployment package.
1. Create an S3 bucket

### AWS Lambda
Serverless deployment of our API.
1. Create new lambda function with Python 3.9 runtime
2. Upload deployment package from S3 (see Deployment)
3. Update lambda handler to `main.handler`
4. Add S3_BUCKET environment variable to the lambda configuration

### AWS API Gateway
1. Create new public REST API.
2. Create a new method for ANY action.
	* Select the Lambda Function integration type
	* Check "on" Use Lambda Proxy Integration
	* Set Lambda Function to the Lambda function name
	* Confirm that you are giving API Gateway permissions to invoke the Lambda function
3. Create a resource
	* Check "on" the option to Configure as proxy resource
	* Select the Lambda Function integration type
	* Set Lambda Function to the Lambda function name
	* Confirm that you are giving API Gateway permissions to invoke the Lambda function
4. Deploy API
	* Create new stage


## Deployment
*It's a manual process right now*
1. Zip up a deployment package for AWS Lambda.
```
source venv/bin/activate
rm -rf api.zip
cd ./venv/lib/python3.9/site-packages
zip -r9 ../../../../api.zip .
cd ../../../../api && zip -x .env -g ../api.zip -r .
```
2. Upload your zip file to your AWS S3 bucket.
3. Update lambda source code

## TODO
- containerize local dev environment
- debgging and logging tools
- review and organize code
- define branching structure
- authentication
- automate infrastructure creation
- automate deployments, CI/CD
- testing automation and tooling
- figure out how to deploy docs

## Helpful links
- [pyenv](https://github.com/pyenv/pyenv)
- [python virtual environments](https://docs.python.org/3/library/venv.html)
- [python csv](https://docs.python.org/3/library/csv.html)
- [geojson](https://pypi.org/project/geojson/)
- [fastapi](https://fastapi.tiangolo.com/)
- [uvicorn](https://www.uvicorn.org/)
- [python-multipart](https://andrew-d.github.io/python-multipart/])
- [magnum](https://pypi.org/project/mangum/)
