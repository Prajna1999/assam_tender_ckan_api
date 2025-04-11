# update a specific field of an exisiting file in CKAN
import pandas as pd
import sys
import os
import ckanapi
import requests
import json
import pdb

APIKEY = "2ef8ee32-6bed-4246-aaef-d4e22cce9cce"

ckan = ckanapi.RemoteCKAN('http://15.207.1.169/', apikey=APIKEY)

def update_dataset(pkg_dict):
    pkg_name = pkg_dict['ocid'].replace(" ", "_").lower().replace("’", "").replace("–", '-').replace(',', "-").replace(":", "--").replace("?", "").replace("&amp;", "-").replace("(", "").replace(")", "").replace("&", "-").replace(".", "").replace("'", "")[:100]
    try:
        package = ckan.action.package_patch(id=pkg_name,statistics = pkg_dict['statistics'])   
        print(pkg_dict['ocid'])
    except Exception as e:
        print (e)

def clean_data(data):
    for key in data:
        if isinstance(data[key], dict) : 
            current_data = data[key]
            current_data = clean_data(current_data)
            current_data = [current_data]
    return data


def main(): 
    path = "/Users/shreyaagrawal/Downloads/tenders/jsons_v10_clean/"
    for root, _, files in os.walk(path):
        for index,file_name in enumerate(files):
            print(index)
            if file_name.endswith('.json'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r') as file:
                    try: 
                        json_data = json.load(file)
                        json_data = clean_data(json_data)
                        update_dataset(json_data)

                    except json.JSONDecodeError:
                        print(f"Error decoding JSON from file: {path}")


if __name__ == '__main__':
    main()
    

