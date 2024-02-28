import json
from typing import Dict, List

class ReportResponse():
    "Agriwebb API Report Response"

    data : dict = {}
    type_value : str = ""
    tenant_type : str = ""
    tenant_id : str = ""
    reporting_period_start : int = 0
    reporting_period_end : int = 0
    report_id : str = ""
    status  : str = ""
    creation_date: int = 0
    last_modified_date : int = 0
    links : list = []
    download_link : str = ""

    def __init__(self, json_response) -> None:
        # Parse the JSON response
        try:
            parsed_response = json.loads(json_response)
        except:
            #Not json
            return

        # Extract variables
        self.data = parsed_response.get('data', {})
        self.type_value = self.data.get('type')
        self.tenant_type = self.data.get('tenantType')
        self.tenant_id = self.data.get('tenantId')
        self.reporting_period_start = self.data.get('reportingPeriodStart')
        self.reporting_period_end = self.data.get('reportingPeriodEnd')
        self.report_id = self.data.get('id')
        self.status = self.data.get('status')
        self.creation_date = self.data.get('creationDate')
        self.last_modified_date = self.data.get('lastModifiedDate')

        self.links = parsed_response.get('links', {})
        self.download_link = self.links.get('download')

    def __str__(self) -> str:
        return f'Type: {self.type_value}\nTenant Type: {self.tenant_type}\nTenant ID: {self.tenant_id}\nReporting Period Start: {self.reporting_period_start}\nReporting Period End: {self.reporting_period_end}\nReport ID: {self.report_id}\nStatus: {self.status}\nCreation Date: {self.creation_date}\nLast Modified Date: {self.last_modified_date}\nDownload Link: {self.download_link}'
