#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Alvaro Bartolome @ alvarob96 on GitHub'
__version__ = '0.1'

import pytest
import os

from twipper.credentials import Twipper


def test_credentials():
    credentials = Twipper(consumer_key=os.environ['consumer_key'],
                          consumer_secret=os.environ['consumer_secret'],
                          access_token=os.environ['access_token'],
                          access_token_secret=os.environ['access_token_secret'])

    print(os.environ['consumer_key'], os.environ['access_token'])

    credentials.plan = 'fullarchive'
    print(credentials.plan)
    credentials.label = 'research'
    print(credentials.label)

    credentials.close()

    # api = credentials.get_api()
    # auth = credentials.get_oauth()
    #
    # try:
    #     tweets = stream_country_tweets(api=api,
    #                                    auth=auth,
    #                                    country='spain',
    #                                    language='es',
    #                                    filter_retweets=False,
    #                                    tweet_limit=10,
    #                                    retry='no_limit')  # after cleaning maybe some are empty or invalid
    # except:
    #     credentials.close()
    #
    # credentials.close()
    #
    # for tweet in tweets:
    #     print(tweet)


if __name__ == '__main__':
    test_credentials()