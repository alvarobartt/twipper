#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Alvaro Bartolome @ alvarob96 on GitHub'
__version__ = '0.1'

import pytest

from twipper.credentials import Twipper


def test_credentials():
    credentials = Twipper(consumer_key='4mfeYj9SH1PXsff5HgZ5bTOzW',
                          consumer_secret='aiEfkE5tYCKcKEg42OcHbNgVvA2uikwwpRuBYwl5VmGSAm7N7e',
                          access_token='254490342-xIGPeyGYLDyD1uFIVgybDsd9ImUPaz467kowIoem',
                          access_token_secret='JrEuYnm1s44JR46AQDdoJagee3Uw9Ip0jxlp7z3XFcPDg')

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