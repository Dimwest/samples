import argparse
import psycopg2
import ConfigParser
import os

import datetime
from datetime import timedelta

from facebookads.api import FacebookAdsApi
from facebookads.adobjects import adaccount, adsinsights


def api_boot(credentials):

    """Function initializing the API connection to Facebook Ads API."""

    application_id = credentials['facebook_ads']['app_id']
    secret = credentials['facebook_ads']['app_secret']
    token = credentials['facebook_ads']['access_token']

    FacebookAdsApi.init(application_id, secret, token)
    print("Facebook Ads API connection successfully initialized.")

def get_ads_report(account_ids, since=(datetime.datetime.now() - timedelta(1)).strftime('%Y-%m-%d'), until=(datetime.datetime.now() - timedelta(1)).strftime('%Y-%m-%d')):

    """Function querying Facebook Insights API in order to get costs data at ad level, per region,
    for all account IDs in the list variable account_ids and appending data rows as lists into the costs_data list. 
    Default start date is yesterday, default end date is yesterday."""

    costs_data = []
    for ids in account_ids:
        accounts = adaccount.AdAccount(ids)
        report_fields = [
            adsinsights.AdsInsights.Field.account_name,
            adsinsights.AdsInsights.Field.account_id,
            adsinsights.AdsInsights.Field.campaign_name,
            adsinsights.AdsInsights.Field.adset_name,
            adsinsights.AdsInsights.Field.ad_name,
            adsinsights.AdsInsights.Field.impressions,
            adsinsights.AdsInsights.Field.clicks,
            adsinsights.AdsInsights.Field.spend
        ]

        params = {'time_range': {'since': since, 'until': until},
                  'level': 'ad',
                  'breakdowns': ['region'],
                  'time_increment': 1
                  }

        insights = accounts.get_insights(fields=report_fields, params=params)
        # Querying the API on the defined fields and parameters

        for dataDict in insights:  # For all data dictionaries in the api response (= insights)
            report_data.append([dataDict['date_start'].encode('utf-8'), dataDict['date_stop'].encode('utf-8'),
                               dataDict['region'].encode('utf-8'), dataDict['account_name'].encode('utf-8'),
                               dataDict['account_id'].encode('utf-8'), dataDict['campaign_name'].encode('utf-8'),
                               dataDict['adset_name'].encode('utf-8'), dataDict['ad_name'].encode('utf-8'),
                               dataDict['impressions'].encode('utf-8'), dataDict['clicks'].encode('utf-8'),
                               dataDict['spend'].encode('utf-8')])

    print 'Facebook Ads Report successfully downloaded.'
    return report_data

def pg_transfer(db_name, db_user, db_pw, db_host, data_list, starting_date, schema, table):

    """Function connecting to Postgres, then deleting potentially existing data for the selected time range, then transferring the data previously collected.
    This function should be refactored."""
    
    with psycopg2.connect(database=db_name, user=db_user, password=db_pw, host=db_host) as connection_var:
        with connection_var.cursor() as cur:

            whereClause = str(""" date >= '%s'""") % starting_date

            cur.execute(
                """DELETE FROM {0}.{1} WHERE {2}""".format(schema, table, whereClause)
            )

            print 'Transferring Facebook Ads Report to DWH.'

            for stored_lists in data_list:

                cur.execute(
                """INSERT INTO {0}.{1} (date, region, ad_account, ad_id, campaign, ad_set, ad, impressions, clicks, spend)
                    VALUES ({2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11});""".format(
                    schema, table, stored_lists[0], stored_lists[2], stored_lists[3], stored_lists[4], stored_lists[5], stored_lists[6], stored_lists[7], stored_lists[8], stored_lists[9], stored_lists[10])
                )

    print 'Facebook Ads Report successfully transferred to DWH.'
