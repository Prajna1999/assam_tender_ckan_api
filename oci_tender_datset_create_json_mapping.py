# uploads a new tender in json to CKAN
import pandas as pd
import sys
import os
import ckanapi
import requests
from glob import glob
import pdb
import json

APIKEY = "2ef8ee32-6bed-4246-aaef-d4e22cce9cce"

ckan = ckanapi.RemoteCKAN('http://15.207.1.169/', apikey=APIKEY)

def upload_dataset(pkg_dict):
    pkg_name = pkg_dict['ocid'].replace(" ", "_").lower().replace("’", "").replace("–", '-').replace(',', "-").replace(":", "--").replace("?", "").replace("&amp;", "-").replace("(", "").replace(")", "").replace("&", "-").replace(".", "").replace("'", "")[:100]
    org_name = pkg_dict['buyer'][0]['name'].split('|')[0]
    org_name = org_name.replace(" ", "_").lower().replace("’", "").replace("–", '-').replace(',', "-").replace(":", "--").replace("?", "").replace("&amp;", "-").replace("(", "").replace(")", "").replace("&", "-").replace(".", "").replace("'", "")[:100]
    # Create Package
    # print(type(pkg_dict['tender']['communication'][0]['documentAvailabilityPeriod']))
    try:

        package = ckan.action.package_create(name=pkg_name,owner_org=org_name, type='tender_dataset',
                    title=pkg_dict['tender'][0]['title'], ocid = pkg_dict['ocid'], id_ = pkg_dict['id'], date = pkg_dict['date'],
                    initiationType = pkg_dict['initiationType'],parties = pkg_dict['parties'] if "parties" in pkg_dict else [],
                    buyer = pkg_dict['buyer'] if "buyer" in pkg_dict else [] , tender = pkg_dict['tender'] if "tender" in pkg_dict else [],
                    bids = pkg_dict['bids'] if 'bids' in pkg_dict else [], awards = pkg_dict['awards'] if "awards" in pkg_dict else [],
                    statistics = pkg_dict['statistics'] if "statistics" in pkg_dict else [] )

        print (pkg_dict['tender'][0]['id'])
        print("")
        
    except Exception as error:
        print (error)
    # except ckanapi.ValidationError as e:
    #     print(e)
        # if (e.error_dict['__type'] == 'Validation Error' and
        #    e.error_dict['name'] == ['That URL is already in use.']):
        #     print ('package already exists')
        #     return
        # else:
        #     raise


def clean_data(data):
    for key in data:
        if isinstance(data[key], dict) : 
            current_data = data[key]
            current_data = clean_data(current_data)
            current_data = [current_data]
    return data

def main(): 
    # json file output from Jupyter notebook in the scraper.
    path = "/Users/shreyaagrawal/Downloads/jsons_v8_clean/" 
    for root, _, files in os.walk(path):
        for file_name in files:
            if file_name.endswith('.json'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r') as file:
                    try: 
                        json_data = json.load(file)
                        json_data = clean_data(json_data)
                        upload_dataset(json_data)

                    except json.JSONDecodeError:
                        print(f"Error decoding JSON from file: {path}")

# Example usage
    
    # for index, row in raw_data.iterrows():
    #     # if index < 6968:
    #     #     continue
    #     # if index > 10:
    #     #     break
    #     upload_dataset(row)
    #     print (index)


if __name__ == '__main__':
    main()
    

