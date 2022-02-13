from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import boto3
import csv
import os
import json
from io import StringIO
from geojson import Feature, Point, FeatureCollection
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

origins = ["http://localhost", "http://localhost:8080", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET = os.getenv("S3_BUCKET")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


@app.get("/")
def root():
    return {"message": "You probably shouldn't be here..."}


@app.get("/files")
def get_files():
    try:
        files = s3_client.list_objects(Bucket=S3_BUCKET, Prefix="geojson")
        return files.get("Contents", [])
    except Exception as e:
        raise HTTPException(500, detail="error getting files from s3")


@app.get("/file")
def get_file(key: str = None):
    try:
        s3_object = s3_client.get_object(Bucket=S3_BUCKET, Key=key)
        s3_object_data = s3_object["Body"].read().decode("utf-8")
        return {
            "message": f"Returned contents of {key}",
            "data": json.loads(s3_object_data),
        }
    except Exception as e:
        raise HTTPException(500, detail=f"error getting {key} from s3")


@app.post("/files")
async def post_file(input_file: UploadFile = File(...)):
    if input_file.content_type not in ["text/csv"]:
        raise HTTPException(
            400,
            detail=f"Invalid file type: {input_file.content_type}. Only CSV accepted.",
        )
    try:
        # read csv input to create geojson
        contents = await input_file.read()
        decoded = contents.decode()
        csvfile = StringIO(decoded)

        # get csv headers from first line
        headers = [h.strip() for h in csvfile.readline().split(",")]
        # TODO: error if headers different than expected
        headers_expected = ["timestamp", "lon", "lat", "depth"]

        # loop through csv to create geojson feature collection
        geojson_features = []
        csv_reader = csv.DictReader(
            csvfile, fieldnames=headers_expected, quoting=csv.QUOTE_NONNUMERIC
        )
        for row in csv_reader:
            try:
                # TODO: validate data
                lat = row["lat"]
                lon = row["lon"]
                timestamp = row["timestamp"]
                depth = row["depth"]
                # create geojson feature
                point = Point((lon, lat))
                feature = Feature(
                    geometry=point, properties={"timestamp": timestamp, "depth": depth}
                )
                geojson_features.append(feature)
            except Exception as e:
                # skip invalid features
                continue
        if len(geojson_features) == 0:
            raise HTTPException(
                422,
                detail=f"File does not contain any valid data: {input_file.filename}",
            )
        geojson_feature_collection = FeatureCollection(geojson_features)
        # store geojson
        geojson_filename = os.path.basename(input_file.filename).split(".")[0]
        geojson_file_key = f"geojson/{geojson_filename}.geojson"
        s3_client.put_object(
            Body=json.dumps(geojson_feature_collection),
            Bucket=S3_BUCKET,
            Key=geojson_file_key,
        )
        # store original csv
        csv_file_key = f"csv/{input_file.filename}"
        s3_client.upload_fileobj(input_file.file, S3_BUCKET, csv_file_key)
    except Exception as e:
        raise HTTPException(500, detail="error uploading file to s3")
    # TODO: include number of valid/invalid rows in response
    return {
        "message": f"{input_file.filename} converted to geojson and uploaded.",
        "data": geojson_feature_collection,
    }
