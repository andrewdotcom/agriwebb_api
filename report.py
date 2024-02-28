import datetime
import requests
from agriwebb import Agriwebb
from datetime import datetime
from enum import Enum
import logging

from report_response import ReportResponse

class ReportType(Enum):
    STOCK_REC = "livestock-reconciliation.v1"
    ANIMAL_LOAD_BY_PADDOCK = "animal-load-by-paddock.v1"

class Report(Agriwebb):
    "Agriwebb API report"

    reporting_period_start : int = 0
    reporting_period_end : int = 0
    tenant_type : str = "farm"
    type : str =""
    report_url : str = ""
    post_data : str = ""
    report_meta : ReportResponse

    def __init__(self, api_key="", endpoint="api.agriwebb.com", api_version="v2", reporting_period_start: str = "", reporting_period_end: str = "", type: Enum = ReportType.STOCK_REC, tenant_type: str = "farm" ) -> None:
        super().__init__(api_key, endpoint, api_version)

        self.report_url = f"{super().api_url}/report"
        self.type = type
        self.report_meta = ReportResponse('{}')

        if reporting_period_start != "" or None:
            self.reporting_period_start = super().date_to_utc(reporting_period_start)
        else:
            self.reporting_period_start = datetime.now().strftime('%Y-%m-%d')

        if reporting_period_end != "" or None:
            self.reporting_period_end = super().date_to_utc(reporting_period_end)
        else:
            self.reporting_period_end = datetime.now().strftime('%Y-%m-%d')

        self.post_data = {
            "type": self.type.value,
            "tenantType": self.tenant_type,
            "tenantId": self.tenant_id,
            "reportingPeriodStart": self.reporting_period_start,
            "reportingPeriodEnd": self.reporting_period_end,
        }

    def request(self) -> ReportResponse:
        try:
            response = requests.request("POST", self.report_url, headers=self.request_headers, json=self.post_data)
            response.raise_for_status()
            self.report_meta = ReportResponse(response.text)
            logging.info(self.report_meta)

        except requests.exceptions.RequestException as e:
            logging.warning(f"Request failed: {e}")
        except Exception as e:
            logging.error(e)

        return self.report_meta

    def get(self):
        self.request_headers = {
          'Content-Type': 'text/html',
          'Accept': 'text/csv',
          'x-api-key': self.api_key
        }

        try:
            response = requests.request("GET", self.report_meta.download_link, headers=self.request_headers)
        except:
            return None

        if response.status_code == 200:
            report_path="./report.csv"
            logging.info(f"Writing file {report_path}")
            with open(report_path, 'wb') as file:
                file.write(response.content)
        else:
            self.report_meta.status = 'pending'
        return None
