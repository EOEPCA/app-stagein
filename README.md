# app-stagein

[![Build Status](https://travis-ci.com/EOEPCA/app-stagein.svg?branch=main)](https://travis-ci.com/EOEPCA/app-stagein)

This application takes one or more STAC item references and does a simple stage-in creating a local STAC catalog with the item(s). The assets href remain untouched (not staged-in)

This application is a stub for supporting the EOEPCA processing scenarios using catalog references as input defined as the CWL Directory type in the Application Package.

## Example

Prepare a YAML file with:

instac.yml
```yaml
store_username: ''
store_apikey: ''
input_reference:
- https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a-cogs/items/S2B_36RTT_20191205_0_L2A 
- https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a-cogs/items/S2B_36RTT_20191215_0_L2A
```

Run the stage-in with:

```console
cwltool instac.cwl instac.yml
```

## Using this application to stage data

Check the output for the catalog.json location. Use such basepath(s) as the values for the Directory input parameter values in the EOEPCA reference applications.



