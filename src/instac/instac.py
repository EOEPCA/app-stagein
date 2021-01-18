import os
import sys
import click
import logging
import requests
from pystac import Catalog, STAC_IO, CatalogType
import pystac
from .stac import my_read_method
from pprint import pprint

logging.basicConfig(stream=sys.stderr,
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%dT%H:%M:%S')


@click.command()
@click.option('--target', '-t', 'data_dir', help='target directory')
@click.option('--store_username', '-u', 'store_username', default=None, help='store username')
@click.option('--store_apikey', '-p', 'store_apikey', default=None, help='store username')
@click.option('--s3_endpoint', '-e', 's3_endpoint', default=None, help='S3 enpoint')
@click.option('--s3_region', '-r', 's3_region', default=None, help='S3 Region')
@click.option('--s3_signature_version', '-s', 's3_signature_version', default=None, help='S3 Signature Version')
@click.argument('input_references', nargs=-1, required=False)
def entry(data_dir, input_references, store_username, store_apikey,s3_endpoint,s3_region, s3_signature_version):
    main(data_dir, input_references, store_username, store_apikey,s3_endpoint,s3_region, s3_signature_version)


def main(data_dir, input_references, store_username, store_apikey,s3_endpoint,s3_region, s3_signature_version):

    # if target is not specified, the data will be staged in 
    # a folder called staged-data
    if data_dir is None:
        data_dir = "staged-data"

    # setting stagein username and password env variables
    if store_username is not None:
        os.environ['STAGEIN_USERNAME'] = store_username
        os.environ['STAGEIN_PASSWORD'] = store_apikey
    
    # setting S3 env variables
    if s3_endpoint is not None:
        os.environ['S3_ENDPOINT'] = s3_endpoint

    if s3_region is not None:
        os.environ['S3_REGION_NAME'] = s3_region

    if s3_signature_version is not None:
        os.environ['S3_SIGNATURE_VERSION'] = s3_signature_version


    STAC_IO.read_text_method = my_read_method

    items = []

    for input_reference in input_references:

        input_reference=input_reference.strip("/")
        thing = pystac.read_file(input_reference)

        print(f"reading file {input_reference}")
        if isinstance(thing, pystac.item.Item):
            items.append(thing)

        elif isinstance(thing, pystac.catalog.Catalog):
            for item in thing.get_items():
                items.append(item)

    # in order to make STAC_IO.read_text_method work with simple
    # http urls we are unsetting the S3 endpoint
    #del os.environ['S3_ENDPOINT']
    
    # create catalog
    catalog = Catalog(id='catalog',
                      description='staged STAC catalog')

    catalog.add_items(items)

    catalog.normalize_and_save(root_href="./",
                               catalog_type=CatalogType.RELATIVE_PUBLISHED)

    catalog.describe()


if __name__ == '__main__':
    entry()
