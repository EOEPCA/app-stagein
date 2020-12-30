import os
from urllib.parse import urlparse
import requests
from requests.auth import HTTPBasicAuth
from pystac import STAC_IO
import boto3
from botocore.client import Config
from pprint import pprint
from botocore.exceptions import ClientError
from click import ClickException


class S3Error(ClickException):
    pass

def read_http_method(uri):

    # stagein password is not provided
    if os.environ.get('STAGEIN_PASSWORD') is None:
        return requests.get(uri).text

    # stagein password is provided
    else:
        return requests.get(uri, auth=HTTPBasicAuth(os.environ.get('STAGEIN_USERNAME'), os.environ.get('STAGEIN_PASSWORD'))).text


def read_s3_method(uri):

    parsed = urlparse(uri, allow_fragments=False)

    # example: https://s3.Region.amazonaws.com/bucket-name/key name
    # ParseResult(scheme='https', netloc='s3.Region.amazonaws.com', path='/bucket-name/key name', params='', query='', fragment='')
    bucket = parsed.netloc
    key = parsed.path.split("/",1)[1]
    S3_endpoint = os.environ.get('S3_ENDPOINT', parsed.netloc)
    myconfig = Config(
        signature_version='s3v4',
        s3={'addressing_style': 'path'})

    if S3_endpoint is None:
        raise S3Error(f"S3 endpoint not provided")

    S3_access_key_id = os.environ.get('STAGEIN_USERNAME', None)
    S3_secret_access_key = os.environ.get('STAGEIN_PASSWORD', None)
    S3_region_name = os.environ.get('S3_REGION_NAME', None)
    S3_signature_version = os.environ.get('S3_SIGNATURE_VERSION', None)

    s3 = boto3.resource('s3',
                        endpoint_url=S3_endpoint,
                        aws_access_key_id=S3_access_key_id,
                        aws_secret_access_key=S3_secret_access_key,
                        config=myconfig,
                        region_name=S3_region_name)

    try:
        obj = s3.Object(bucket, key)
        response = obj.get()['Body'].read().decode('utf-8')
    except ClientError as ex:
        if ex.response['Error']['Code'] == 'NoSuchKey':
            raise S3Error(f"S3 object with key \"{key}\" does not exist.")
        elif ex.response['Error']['Code'] == 'NoSuchBucket':
            raise S3Error(f"S3 bucket \"{bucket}\" does not exist.")
        else:
            raise ex

    return response


# general read method
def my_read_method(uri):

    # parsing the uri
    parsed = urlparse(uri)

    # initializing response
    response = None

    # url scheme
    if parsed.scheme == 's3':
        response = read_s3_method(uri)
    elif parsed.scheme == 'http' or parsed.scheme == 'https':
        response = read_http_method(uri)
    else:
        response = STAC_IO.default_read_text_method(uri)
    return response
