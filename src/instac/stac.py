import os
from urllib.parse import urlparse
import requests
from requests.auth import HTTPBasicAuth
from pystac import STAC_IO

def my_read_method(uri):
    
    parsed = urlparse(uri)
    
    if parsed.scheme.startswith('http'):
    
        if os.environ.get('STAGEIN_PASSWORD') is None:
            
            return requests.get(uri).text
            
        else:
            
            return requests.get(uri, 
                                auth=HTTPBasicAuth(os.environ.get('STAGEIN_USERNAME'), 
                                                   os.environ.get('STAGEIN_PASSWORD'))
                               ).text
    else:
        return STAC_IO.default_read_text_method(uri)



