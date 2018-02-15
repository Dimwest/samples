#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import psycopg2, yaml

import xml.etree.ElementTree as ET
from googleads import adwords

def api_bootstrap(authentication_path="googleads.yaml"):

    #Setting up the API client by loading credentials and refresh token from the .yaml file located at the specified path
    adwords_client = adwords.AdWordsClient.LoadFromStorage(authentication_path)
    print "Adwords client loaded successfully."

    return adwords_client

def geo_performance_report(client, date_range="YESTERDAY", since=None, until=None):

    dataStock = []
    costs_data = []

    report_downloader = client.GetReportDownloader(version='v201710')

    # Create report definition. See https://developers.google.com/adwords/api/docs/guides/reporting and https://developers.google.com/adwords/api/docs/appendix/reports/campaign-performance-report#campaignname
    report = {
        'reportName': 'HISTORY_CAMPAIGN_PERF_REPORT',
        'dateRangeType': date_range,
        'reportType': 'GEO_PERFORMANCE_REPORT',
        'downloadFormat': 'XML',
        'selector': {
            'fields': ['Date', 'CountryCriteriaId', 'RegionCriteriaId', 'CityCriteriaId', 'AccountDescriptiveName', 'CampaignName', 'AdGroupName', 'Impressions', 'Clicks', 'Conversions', 'Cost']
        }
    }

    if date_range == "CUSTOM_DATE":
        report['selector']['dateRange'] = {'min': since.replace("-", ""), 'max': until.replace("-", "")}

    #Download the report as a string
    report_file = report_downloader.DownloadReportAsString(
        report, skip_report_header=True, skip_column_header=True,
        skip_report_summary=True)

    if report_file != '':
        root = ET.fromstring(report_file)
        for child in root:
            for rows in child:
                row_dict = rows.attrib
                costs_data.append([row_dict['day'].encode('utf-8'), row_dict['countryTerritory'].encode('utf-8'), row_dict['region'].encode('utf-8'), row_dict['city'].encode('utf-8'), row_dict['account'].encode('utf-8'), row_dict['campaign'].encode('utf-8'), row_dict['adGroup'].encode('utf-8'),
                    row_dict['impressions'].encode('utf-8'), row_dict['clicks'].encode('utf-8'), row_dict['conversions'].encode('utf-8'), row_dict['cost'].encode('utf-8')])

    return costs_data

def db_transfer(costs_data=[], creds_path="db_connect.yaml", date_range="YESTERDAY", since=None, until=None):

    try:

        with open(creds_path) as stream:
            db_creds = yaml.load(stream)

        conn = psycopg2.connect(database=db_creds['db_name'], host=db_creds['db_host'], user=db_creds['db_user'], password=db_creds['db_pw'])
        cur = conn.cursor()
        print("Successfully connected to target database.")

        range_dict = {'TODAY': """date::date = current_date;""",
                      'YESTERDAY': """date::date = (current_date - interval '1 day');""",
                      'LAST_7_DAYS': """date between current_date - interval '7 days' and current_date;""",
                      'LAST_14_DAYS': """date between current_date - interval '14 days' and current_date;""",
                      'LAST_30_DAYS': """date between current_date - interval '30 days' and current_date;""",
                      'THIS_MONTH': """(EXTRACT(MONTH FROM date) = EXTRACT(MONTH FROM current_date) AND EXTRACT(YEAR FROM date) = EXTRACT(YEAR FROM current_date))""",
                      'ALL_TIME': """date < current_date""",
                      'CUSTOM_DATE': """date >= '{0}'::date and date <= '{1}'::date""".format(since, until)}

        where_clause = range_dict[date_range]

        delete_query = "DELETE FROM external.adwords_city WHERE {0}".format(where_clause)
        cur.execute(delete_query)

        print("Existing data deleted for the selected time range.")

        for account_lists in costs_data:
            for row in account_lists:
                insert_query = """INSERT INTO external.adwords_city (date, country, region, city, account, campaign, ad_group, impressions, clicks, conversions, cost)
                    VALUES {0};""".format(tuple(row))
                cur.execute(insert_query)

    except Exception as e:
        conn.rollback()
        conn.close()
        print("Error during database transfer, rolled back changes and closed connection.")

    finally:
        if conn:
            conn.commit()
            conn.close()
            print("Transfer to database terminated, connection closed.")


def main(date_range="YESTERDAY", account_ids=[], since=None, until=None):

    try:
        assert date_range in ('TODAY', 'YESTERDAY', 'LAST_7_DAYS', 'LAST_14_DAYS', 'LAST_30_DAYS', 'THIS_MONTH', 'ALL_TIME', 'CUSTOM_DATE')

        if date_range == "CUSTOM_DATE":
            assert since is not None and until is not None

        client = api_bootstrap()
        data_storage = []

        for id in account_ids:
            status_text = "Getting report for account {0}".format(id)
            print(status_text)
            client.SetClientCustomerId(id)
            data_storage.append(geo_performance_report(client, date_range, since=since, until=until))

        print "Reports successfully downloaded and parsed."
        db_transfer(costs_data=data_storage, date_range=date_range, since=since, until=until)

    except AssertionError:
        print("""Assertion Error: time_range but be one of the following values: 'TODAY', 'YESTERDAY', 'LAST_7_DAYS', 'LAST_14_DAYS', 'LAST_30_DAYS', 'THIS_MONTH', 'ALL_TIME', 'CUSTOM_DATE'.
            If time_range == 'CUSTOM_DATE', since and until parameter must be filled in with the start and end date of the report.""")

if __name__ == '__main__':

    ACCOUNT_IDS = ['XXX-XXX-XXX'] # Should be loaded from a config file.

    main(date_range="CUSTOM_DATE", account_ids=ACCOUNT_IDS, since="2017-11-01", until="2018-01-31") # Example for custom date
    #main(date_range="YESTERDAY", account_ids=ACCOUNT_IDS)
