import json
import pdb
import os
def clean_data(data):
    for key in data:
        if isinstance(data[key], dict) : 
            current_data = data[key]
            clean_data(current_data)
            data[key] = [current_data]
        elif isinstance(data[key], list):
            for each in data[key]:
                if isinstance(each, dict):
                    clean_data(each)

def main(): 
    path = "/Users/shreyaagrawal/Documents/Cdl/assam-tender-scraper/scraped_recent_tenders/jsons-v10"
    path_clean_json = "/Users/shreyaagrawal/Downloads/jsons_v10_clean/"
    for root, _, files in os.walk(path):
        for file_name in files:
            if file_name.endswith('.json'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r') as file:
                    try: 
                        json_data = json.load(file)
                        clean_data(json_data)
                        updict = {"id" : 1}
                        if json_data["tender"][0]["communication"][0]:
                            json_data["tender"][0]["communication"][0] = {**updict, **json_data["tender"][0]["communication"][0]}
                        if "bids" in json_data:
                            json_data['bids'][0] = {**updict,**json_data['bids'][0]}
                        # json_data = json.dumps(json_data,indent=4)
                        with open(path_clean_json+ json_data['tender'][0]['id']+ ".json", 'w') as newfile:
                            json.dump(json_data,newfile, indent=4)

                    except json.JSONDecodeError:
                        print(f"Error decoding JSON from file: {path}")

if __name__ == '__main__':
    main()
    