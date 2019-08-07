#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Alvaro Bartolome @ alvarob96 on GitHub'
__version__ = '0.0.5'

import datetime
import json

import requests
import requests_oauthlib

from twipper.utils import country_to_bounding_box


def stream_tweets(auth, query, language=None, filter_retweets=False,
                  tweet_limit=None, date_limit=None, retry=5):
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
        retry (:obj:`int` or :obj:`str`, optional):
            value to set the number of retries if connection to api.twitter fails, it can either be an :obj:`int` or
            a :obj:`str` which can just be the value `no_limit` in the case that no retry limits want to be set. Default
            value is 5 retries whenever connection fails, until function finishes.

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

    if not isinstance(retry, int) and not isinstance(retry, str):
        raise ValueError('retry value is not valid as it is not a str or int value!')

    if isinstance(retry, str) and retry != 'no_limit':
        raise ValueError('retry value is not valid as it is not `no_limit`!')

    if isinstance(retry, int) and retry < 0:
        raise ValueError('retry value is not valid as it is below 0!')

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

    if isinstance(retry, str) and retry == 'no_limit':
        retries = -1
    else:
        retries = retry

    if tweet_limit is not None:
        tweet_counter = 0

        for line in response.iter_lines():
            if tweet_limit == tweet_counter:
                break

            if retries == 0:
                break

            try:
                tweet = json.loads(line.decode('utf-8'))
            except json.decoder.JSONDecodeError:
                retries -= 1
                continue

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

            if retries == 0:
                break

            try:
                tweet = json.loads(line.decode('utf-8'))
            except json.decoder.JSONDecodeError:
                retries -= 1
                continue

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

            if retries == 0:
                break

            try:
                tweet = json.loads(line.decode('utf-8'))
            except json.decoder.JSONDecodeError:
                retries -= 1
                continue

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


def stream_generic_tweets(auth, country, language=None, filter_retweets=False,
                          tweet_limit=None, date_limit=None, retry=5):
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
        retry (:obj:`int` or :obj:`str`, optional):
            value to set the number of retries if connection to api.twitter fails, it can either be an :obj:`int` or
            a :obj:`str` which can just be the value `no_limit` in the case that no retry limits want to be set. Default
            value is 5 retries whenever connection fails, until function finishes.

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

    if not isinstance(language, str) or language is None:
        raise ValueError('language must be a string!')

    if not isinstance(filter_retweets, bool) or filter_retweets is None:
        raise ValueError('filter_retweets must be a boolean!')

    if tweet_limit is not None and not isinstance(tweet_limit, int):
        raise ValueError('tweet_limit value is not valid')

    if date_limit is not None and isinstance(date_limit, str):
        try:
            datetime.datetime.strptime(date_limit, '%Y%m%d%H%M')
        except ValueError:
            raise ValueError("incorrect date format, it should be 'yyyymmddhhmm'.")

    if not isinstance(retry, int) and not isinstance(retry, str):
        raise ValueError('retry value is not valid as it is not a str or int value!')

    if isinstance(retry, str) and retry != 'no_limit':
        raise ValueError('retry value is not valid as it is not `no_limit`!')

    if isinstance(retry, int) and retry < 0:
        raise ValueError('retry value is not valid as it is below 0!')

    try:
        bounding_box = country_to_bounding_box(country)
    except (ConnectionError, ValueError, IndexError):
        raise RuntimeError('introduced country bounding_box was unavailable or unable to retrieve')

    url = 'https://stream.twitter.com/1.1/statuses/filter.json'

    params = {
        'language': language,
        'locations': str(bounding_box)
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
        raise ConnectionError('connection errored with code ' + str(response.status_code))

    tweets = list()

    if isinstance(retry, str) and retry == 'no_limit':
        retries = -1
    else:
        retries = retry

    if tweet_limit is not None:
        tweet_counter = 0

        for line in response.iter_lines():
            if tweet_limit == tweet_counter:
                break

            if retries == 0:
                break

            try:
                tweet = json.loads(line.decode('utf-8'))
            except json.decoder.JSONDecodeError:
                retries -= 1
                continue

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

            if retries == 0:
                break

            try:
                tweet = json.loads(line.decode('utf-8'))
            except json.decoder.JSONDecodeError:
                retries -= 1
                continue

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

            if retries == 0:
                break

            try:
                tweet = json.loads(line.decode('utf-8'))
            except json.decoder.JSONDecodeError:
                retries -= 1
                continue

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
