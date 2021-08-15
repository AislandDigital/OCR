"""Serveless application to extract text from images with texts."""

import io
import os
import json
from typing import Dict
from base64 import b64decode, b64encode
import requests
import pytesseract
from PIL import Image



if os.getenv('AWS_EXECUTION_ENV') is not None:
    os.environ['DYLD_LIBRARY_PATH'] = '/opt/lib'
    os.environ['TESSDATA_PREFIX'] = '/opt/data/tessdata'


def get_as_base64(url: str):
    """Return as base64 a url image."""
    return b64encode(requests.get(url).content)

def cors_web_response(status_code: int, body: Dict[str, str]):
    """Create a response when dealing with CORS."""
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,X-Amz-Security-Token,Authorization,X-Api-Key,'
                                            'X-Requested-With,Accept,Access-Control-Allow-Methods,'
                                            'Access-Control-Allow-Origin,Access-Control-Allow-Headers',
            "Access-Control-Allow-Methods": 'OPTIONS,POST',
            'Access-Control-Allow-Origin': '*',
            'X-Requested-With': '*'
    },
        'body': json.dumps(body)
    }

def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    if event["httpMethod"] == "OPTIONS":
        body = {
            "message": "cors allowed"
        }

        return cors_web_response(200, body)

    request_body = json.loads(event['body'])
    config = ""
    lang = "por"

    #POST is the Default Method
    if 'config' in request_body.keys() and request_body['config']:
        config = request_body['config']

    if 'lang' in request_body.keys() and request_body['lang']:
        lang = request_body['lang']

    if 'image64' in request_body.keys() and request_body['image64']:
        image64 = request_body['image64']
    elif 'url_path' in request_body.keys() and request_body['url_path']:
        try:
            image64 = get_as_base64(request_body['url_path'])
        except ValueError:
            body = {
                "message": "Wrong url path."
            }

            return cors_web_response(400, body)
    else:
        body = {
            "message": "You must pass a least one of the arguments: url_pah or image64"
        }

        return cors_web_response(400, body)

    text = None

    if not text:
        try:
            image = io.BytesIO(b64decode(image64))
        except ValueError:
            body = {
                "message": "Not able to convert image64 string into image file. Wrong url path/wrong image64 bytes."
            }

            return cors_web_response(400, body)

        try:
            text = pytesseract.image_to_string(Image.open(image), lang=lang, config=config)
        except ValueError:
            body = {
                "message": "Not able to extract text from image"
            }

            return cors_web_response(400, body)

    body = {
        "message": text
    }

    return cors_web_response(200, body)
