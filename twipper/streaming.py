#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Alvaro Bartolome @ alvarob96 on GitHub'
__version__ = '0.0.2'

import datetime
import json

import requests
import requests_oauthlib

from twipper.utils import country_to_bounding_box


def stream_tweets(auth, query, language=None, filter_retweets=False, tweet_limit=None, date_limit=None):
    """
    This function retrieves streaming tweets matching the given query, so on, this function will open a stream to
    the Twitter Streaming API to retrieve real-time tweets. By the time these tweets are retrieved, they are handled
    and returned as a :obj:`list`.
    API Reference: https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/basic-stream-parameters.html

    Args:
        auth (:obj:`requests_oauthlib.OAuth1`):
            valid Twitter Auth object generated via `twipper.credentials.TwipperCredentials`.
        query (:obj:`str`): contains the query with the words to search along the Twitter Streaming.
        language (:obj:`str`, optional): is the language on which the tweet has been written, default is `None`.
        filter_retweets (:obj:`boolean`, optional):
            can be either `True` or `False`, to filter out retweets or not, respectively.
        tweet_limit (:obj:`int`, optional):
            specifies the amount of tweets to be retrieved on streaming, default is 10k tweets.
        date_limit (:obj:`str`, optional):
            specifies the date (format `yyyymmddhhmm`) where the stream will stop, default is `None`

    Returns:
        :obj:`list` - tweets:
            Returns a :obj:`list` containing all the retrieved tweets from Twitter, which means all the available tweets
            from the user specified on the arguments of the function.

    Raises:
        ValueError: raised if the introduced arguments do not match or errored.
    """

    if not isinstance(auth, requests_oauthlib.OAuth1):
        raise ValueError('specified auth is not valid!')

    if auth is None:
        raise ValueError('auth is mandatory')

    if not isinstance(query, str):
        raise ValueError('query must be a string!')

    if query is None:
        raise ValueError('query is mandatory')

    if not isinstance(language, str):
        raise ValueError('language must be a string!')

    if language is None:
        raise ValueError('language is mandatory')

    if not isinstance(filter_retweets, bool):
        raise ValueError('filter_retweets must be a boolean!')

    if filter_retweets is None:
        raise ValueError('filter_retweets is mandatory')

    if tweet_limit is not None and not isinstance(tweet_limit, int):
        raise ValueError('tweet_limit value is not valid')

    if date_limit is not None and isinstance(date_limit, str):
        try:
            datetime.datetime.strptime(date_limit, '%Y%m%d%H%M')
        except ValueError:
            raise ValueError("incorrect date format, it should be 'yyyymmddhhmm'.")

    url = 'https://stream.twitter.com/1.1/statuses/filter.json'

    params = {
        'track': query,
        'language': language,
    }

    headers = {
        'Content-Type': 'application/json',
    }

    response = requests.post(url,
                             auth=auth,
                             headers=headers,
                             params=params,
                             stream=True)

    if response.status_code != 200:
        raise ConnectionError('connection errored with code ' + str(response.status_code) + '.')

    tweets = list()

    if tweet_limit is not None:
        tweet_counter = 0

        for line in response.iter_lines():
            if tweet_limit == tweet_counter:
                break

            tweet = json.loads(line.decode('utf-8'))

            if filter_retweets:
                if 'retweeted_status' not in tweet:
                    tweets.append(tweet)
                    tweet_counter += 1
            else:
                tweets.append(tweet)
                tweet_counter += 1

    elif date_limit is not None:

        for line in response.iter_lines():
            current_date = datetime.datetime.now().strftime('%Y%m%d%H%M')
            if current_date >= date_limit:
                break

            tweet = json.loads(line.decode('utf-8'))

            if filter_retweets:
                if 'retweeted_status' not in tweet:
                    tweets.append(tweet)
            else:
                tweets.append(tweet)

    else:
        tweet_limit = 1000
        tweet_counter = 0

        for line in response.iter_lines():
            if tweet_limit == tweet_counter:
                break

            tweet = json.loads(line.decode('utf-8'))

            if filter_retweets:
                if 'retweeted_status' not in tweet:
                    tweets.append(tweet)
                    tweet_counter += 1
            else:
                tweets.append(tweet)
                tweet_counter += 1

    if len(tweets) > 0:
        return tweets
    else:
        raise IndexError('no tweets could be retrieved.')


def stream_generic_tweets(auth, country, language=None, filter_retweets=False, tweet_limit=None, date_limit=None):
    """
    This function retrieves streaming tweets matching the given query, so on, this function will open a stream to
    the Twitter Streaming API to retrieve real-time tweets. By the time these tweets are retrieved, they are handled
    and returned as a :obj:`list`.
    API Reference: https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/basic-stream-parameters.html

    Args:
        auth (:obj:`requests_oauthlib.OAuth1`):
            valid Twitter Auth object generated via `twipper.credentials.TwipperCredentials`.
        country (:obj:`str`): contains the country name from where generic tweets will be retrieved.
        language (:obj:`str`, optional): is the language on which the tweet has been written, default is `None`.
        filter_retweets (:obj:`boolean`, optional):
            can be either `True` or `False`, to filter out retweets or not, respectively.
        tweet_limit (:obj:`int`, optional):
            specifies the amount of tweets to be retrieved on streaming, default is 10k tweets.
        date_limit (:obj:`str`, optional):
            specifies the date (format `yyyymmddhhmm`) where the stream will stop, default is `None`

    Returns:
        :obj:`list` - tweets:
            Returns a :obj:`list` containing all the retrieved tweets from Twitter, which means all the available tweets
            from the user specified on the arguments of the function.

    Raises:
        ValueError: raised if the introduced arguments do not match or errored.
    """

    if not isinstance(auth, requests_oauthlib.OAuth1):
        raise ValueError('specified auth is not valid!')

    if auth is None:
        raise ValueError('auth is mandatory')

    if not isinstance(country, str):
        raise ValueError('query must be a string!')

    if country is None:
        raise ValueError('query is mandatory')

    if not isinstance(language, str):
        raise ValueError('language must be a string!')

    if language is None:
        raise ValueError('language is mandatory')

    if not isinstance(filter_retweets, bool):
        raise ValueError('filter_retweets must be a boolean!')

    if filter_retweets is None:
        raise ValueError('filter_retweets is mandatory')

    if tweet_limit is not None and not isinstance(tweet_limit, int):
        raise ValueError('tweet_limit value is not valid')

    if date_limit is not None and isinstance(date_limit, str):
        try:
            datetime.datetime.strptime(date_limit, '%Y%m%d%H%M')
        except ValueError:
            raise ValueError("incorrect date format, it should be 'yyyymmddhhmm'.")

    try:
        bounding_box = country_to_bounding_box(country)
    except (ConnectionError, ValueError, IndexError):
        raise RuntimeError('introduced country bounding_box was unavailable or unable to retrieve')

    url = 'https://stream.twitter.com/1.1/statuses/filter.json'

    params = {
        'language': language,
        'locations': bounding_box
    }

    headers = {
        'Content-Type': 'application/json',
    }

    response = requests.post(url,
                             auth=auth,
                             headers=headers,
                             params=params,
                             stream=True)

    if response.status_code != 200:
        raise ConnectionError('connection errored with code ' + str(response.status_code) + '.')

    tweets = list()

    if tweet_limit is not None:
        tweet_counter = 0

        for line in response.iter_lines():
            if tweet_limit == tweet_counter:
                break

            tweet = json.loads(line.decode('utf-8'))

            if filter_retweets:
                if 'retweeted_status' not in tweet:
                    tweets.append(tweet)
                    tweet_counter += 1
            else:
                tweets.append(tweet)
                tweet_counter += 1

    elif date_limit is not None:

        for line in response.iter_lines():
            current_date = datetime.datetime.now().strftime('%Y%m%d%H%M')
            if current_date >= date_limit:
                break

            tweet = json.loads(line.decode('utf-8'))

            if filter_retweets:
                if 'retweeted_status' not in tweet:
                    tweets.append(tweet)
            else:
                tweets.append(tweet)

    else:
        tweet_limit = 1000
        tweet_counter = 0

        for line in response.iter_lines():
            if tweet_limit == tweet_counter:
                break

            tweet = json.loads(line.decode('utf-8'))

            if filter_retweets:
                if 'retweeted_status' not in tweet:
                    tweets.append(tweet)
                    tweet_counter += 1
            else:
                tweets.append(tweet)
                tweet_counter += 1

    if len(tweets) > 0:
        return tweets
    else:
        raise IndexError('no tweets could be retrieved.')