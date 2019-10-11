#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2018-2019 Alvaro Bartolome
# See LICENSE for details.

import pytest

import os

from twipper.credentials import Twipper
import twipper.batch as batch
import twipper.streaming as stream


def test_twipper():
    credentials = Twipper(consumer_key=os.environ['consumer_key'],
                          consumer_secret=os.environ['consumer_secret'],
                          access_token=os.environ['access_token'],
                          access_token_secret=os.environ['access_token_secret'])

    credentials.plan = 'fullarchive'
    credentials.label = 'research'

    try:
        batch.search_tweets(access=credentials,
                            query='futbol',
                            page_count=1,
                            filter_retweets=True,
                            language='es',
                            result_type='mixed',
                            count=10)

        batch.search_user_tweets(access=credentials,
                                 screen_name='realDonaldTrump',
                                 page_count=1,
                                 filter_retweets=True,
                                 language='en',
                                 result_type='mixed',
                                 count=10)

        stream.stream_tweets(access=credentials,
                             query='futbol',
                             language='es',
                             filter_retweets=False,
                             tweet_limit=10,
                             retry='no_limit')

        stream.stream_country_tweets(access=credentials,
                                     country='spain',
                                     language='es',
                                     filter_retweets=False,
                                     tweet_limit=10,
                                     retry='no_limit')

        # premium.search_tweets(access=credentials,
        #                       query='futbol',
        #                       page_count=1,
        #                       from_date='201901010000',
        #                       to_date='201901080000',
        #                       language='es')
        #
        # premium.search_user_tweets(access=credentials,
        #                            screen_name='realDonaldTrump',
        #                            page_count=1,
        #                            from_date='201901010000',
        #                            to_date='201901080000',
        #                            language='en')

    finally:
        credentials.close()


if __name__ == '__main__':
    test_twipper()
