#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Set of tools to manage connections to slack"""

import configparser
from slackclient import SlackClient


def post_slack_msg(credentials,
                   text,
                   username='Airflow',
                   channel='#e-bi-airflow-notifs'):
    """
    Posts message on Slack
    :param credentials: path to credentials file
    :param text: text of the message
    :param username: slack username to be used by bot
    :param channel: slack channel e.g. #general
    """
    # Read credentials
    config = configparser.ConfigParser()
    config.read(credentials)

    sc = SlackClient(config.get('SLACK', 'token'))
    sc.api_call(
        'chat.postMessage',
        as_user=True,
        channel=channel,
        username=username,
        text=text
    )


