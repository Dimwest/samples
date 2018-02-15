#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import urllib2
import json

def get_events_visits(date, account, access_token):
    """Simple get request to the Piwik API getting the events and visits data of the selected date and account."""

    get_request = """https://%s.piwik.pro/index.php?module=API&method=Live.getLastVisitsDetails&idSite=1&format=json&filter_limit=-1&period=day&date=%s&token_auth=%s""" % (
        account, date, access_token)
    api_response = urllib2.urlopen(get_request)
    json_data = json.load(api_response)
    return json_data