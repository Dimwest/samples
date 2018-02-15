#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as et
from googleads import adwords


def api_boot(credentials_path=None, credentials_string=None):
    """Function creating and returning the Adwords API client. Can use both LoadFromStorage and LoadFromString methods
    depending on which parameters are given. In case both are provided, LoadFromStorage method has the priority."""

    try:

        assert (credentials_path is not None or credentials_string is not None)

        if credentials_path is not None:
            adwords_client = adwords.AdWordsClient.LoadFromStorage(credentials_path)
            print("Adwords client loaded successfully.")
            return adwords_client
        else:
            adwords_client = adwords.AdWordsClient.LoadFromString(credentials_string)
            print("Adwords client loaded successfully.")
            return adwords_client

    except Exception as ex:
        print("Error during Adwords API initialization:\n" + ex + '\n' + type(ex) + '\n' + ex.args)


def get_report(client, account_ids, date_range, report_type,
               fields, report_name='REPORT'):
    """Function querying Adwords API for the list of account IDs provided and generating the selected report.
    By default, gets the daily costs for yesterday at city and ad group level. Returns report at XML
    Work In Progress: parsing should be separated from the generic function and only be present in the get_costs function."""

    for IDs in account_ids:
        client.SetClientCustomerId(IDs)

        report_downloader = client.GetReportDownloader(version='v201609')

        report = {
            'reportName': report_name,
            'dateRangeType': date_range,
            'reportType': report_type,
            'downloadFormat': 'XML',
            'selector': {
                'fields': fields
            }
        }

        report_xml = report_downloader.DownloadReportAsString(
            report, skip_report_header=True, skip_column_header=True,
            skip_report_summary=True)

        if report_xml != '':
            xml_report = et.fromstring(report_xml.encode('utf-8'))
    return xml_report


