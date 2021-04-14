from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

import uvicorn


from com_ineuron_firensmoke.com_ineuron_utils.utils import decodeImage
from com_ineuron_firensmoke.predictor_yolo_detector.detector_test import Detector
from pymongo import MongoClient
import datetime
import os
import logging

import boto3
from botocore.exceptions import NoCredentialsError


import sys
sys.path.insert(0, './com_ineuron_firensmoke')

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')


#CORS(app)

# Below is for docker
#dbConn = MongoClient('mongodb://db:27017/dockerdemo')

# Beloww is for local windows
dbConn = MongoClient("mongodb://localhost:27017/")

db = dbConn.appdb

logging.basicConfig(filename="test.log",level =logging.DEBUG,format='%(asctime)s:%(levelname)s:%(message)s')

# @cross_origin()
class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"
        #modelPath = 'research/ssd_mobilenet_v1_coco_2017_11_17'
        self.objectDetection = Detector(self.filename)


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



@app.post("/predict")
#@cross_origin()
async def predictRoute(request: Request):
    try:
        start = datetime.datetime.now()
        json_param = await request.json()

        enco = json_param['image']
        decodeImage(enco, clApp.filename)
        result = clApp.objectDetection.detect_action()
        logging.debug('Was able to return the labeled image succesfuly')
        resultct =db.appdb.find({})
        i =0
        i = resultct.count() + 1
        output = result[0]['image']
        my_row = {'Serial No': i,
                  'Input Image': enco,
                  'Output Image': output,
                  'last_modified': datetime.datetime.utcnow()
                  }

        db.appdb.insert_one(my_row)
        logging.debug("Saved to db succesfuly with record no :%d",i)
        end = datetime.datetime.now()
        elapsed = end - start
        print("Time taken for the predict is ",elapsed)
        #logging.debug(" %t   :  %t ",elapsed.seconds, elapsed.microseconds)
        #uploaded = upload_to_aws('output.jpg', 'imageupload9', 'output2.jpg')


    except ValueError as val:
        logging.error(val)
        return Response("Value not found inside  json data")
    except KeyError:
        return Response("Key value error incorrect key passed")
    except Exception as e:
        logging.error(e)
        result = "Invalid input"

    return jsonable_encoder(result)


clApp = ClientApp()

ACCESS_KEY = ''
SECRET_KEY = ''
def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False



