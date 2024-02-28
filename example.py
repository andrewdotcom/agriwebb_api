from report import Report, ReportType
import logging
import configparser

#Set up
logging.basicConfig(filename='/tmp/report_log.log', encoding='utf-8', level=logging.INFO)
config = configparser.ConfigParser()
config.read('config.ini')

#Initialise the report
stock_rec = Report(api_key=config.get('General', 'api_key'),
    reporting_period_start="01/01/2024",
    reporting_period_end="01/02/2024",
    type=ReportType.STOCK_REC)

#Get the report
report_req = stock_rec.request()
report_csv = stock_rec.get()
