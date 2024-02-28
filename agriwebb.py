import requests
from datetime import datetime
import json
import os
import logging

class Agriwebb():
    " Agriwebb API Class for working with the Agriwebb API "

    api_protocol = "https"
    api_key = None
    api_version = "v2"
    api_endpoint = "api.agriwebb.com"
    api_url = f"{api_protocol}://{api_endpoint}/{api_version}"
    tenant_id = ""
    request_headers = {}

    def __init__(self, api_key: str, endpoint="api.agriwebb.com", api_version="v2") -> None:
        self.api_key = api_key
        self.api_endpoint = endpoint
        self.api_version = api_version

        if api_key == None:
            logging.error("No API Key Provided")
            return
        else:
            self.request_headers = {
              'Content-Type': 'application/json',
              'Accept': 'application/json',
              'x-api-key': api_key
            }

            self.get_tenant_id()

    def get_tenant_id(self):
        graph_ql = {
            'query': 'query tenent_id {\n  farms {\n    id\n  }\n}'
        }
        response = requests.post(self.api_url, headers=self.request_headers, json=graph_ql)
        if response.status_code == 200:
            json_response = response.json()
            farms = json_response.get('data', {}).get('farms', [])
            if farms:
                self.tenant_id = farms[0].get('id')
            else:
                logging.info('No tenants found in the response.')
        else:
            logging.error(f'Request failed with code: {response.status_code}')

    def date_to_utc(self,text_date: str = "") -> int:
        if text_date == "" or None:
                date_object = datetime.now()
        else:
            try:
                date_object = datetime.strptime(text_date, '%d/%m/%Y')
            except:
                #not sure if the best thing to do is return today on error
                return int(datetime.now().timestamp())
        timestamp_seconds = int(date_object.timestamp())
        timestamp_milliseconds = timestamp_seconds * 1000 + 62135596800000
        return timestamp_milliseconds

if __name__ == "__main__":
    api_key = ""
    api = Agriwebb(api_key)
