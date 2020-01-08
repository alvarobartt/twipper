#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2018-2019 Alvaro Bartolome
# See LICENSE for details.

import datetime
import json

import oauth2
import requests
import requests_oauthlib

from twipper.utils import country_to_bounding_box
# from twipper.utils import available_languages
from twipper.credentials import Twipper


def stream_tweets(access, query, language=None, filter_retweets=False,
                  tweet_limit=None, date_limit=None, retry=5):
    """
    This function retrieves streaming tweets matching the given query, so on, this function will open a stream to
    the Twitter Streaming API to retrieve real-time tweets. By the time these tweets are retrieved, they are handled
    and returned as a :obj:`list`.
    API Reference: https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/basic-stream-parameters.html

    Args:
        access (:obj:`twipper.credentials.Twipper`): object containing all the credentials needed to access api.twitter
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
            Yields a :obj:`list` containing all the retrieved tweets from Twitter, which means all the available tweets
            from the user specified on the arguments of the function.

    Raises:
        ValueError: raised if the introduced arguments do not match or errored.
    """

    if not access or not isinstance(access, Twipper):
        raise ValueError('access object to api.twitter is not valid!')

    api = access.api

    if not isinstance(api, oauth2.Client):
        raise ValueError('api is not valid!')

    oauth = access.oauth

    if not isinstance(oauth, requests_oauthlib.OAuth1):
        raise ValueError('auth is not valid!')

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

    if language:
        # try:
        #     languages = available_languages(api)
        # except (ConnectionError, json.decoder.JSONDecodeError, IndexError):
        #     raise RuntimeError('`twipper.utils.available_languages` function failed')

        languages = [
            'fr', 'en', 'ar', 'ja', 'es', 'de', 'it', 'id', 'pt', 'ko', 
            'tr', 'ru', 'nl', 'fil', 'msa', 'zh-tw', 'zh-cn', 'hi', 'no', 
            'sv', 'fi', 'da', 'pl', 'hu', 'fa', 'he', 'ur', 'th', 'uk', 
            'ca', 'ga', 'el', 'eu', 'cs', 'gl', 'ro', 'hr', 'en-gb', 'vi', 
            'bn', 'bg', 'sr', 'sk', 'gu', 'mr', 'ta', 'kn'
        ]

        if language in languages:
            params = {
                'track': query,
                'language': language
            }
        else:
            raise ValueError('the introduced language does not exist.')
    else:
        params = {
            'track': query
        }

    headers = {
        'Content-Type': 'application/json',
    }

    if isinstance(retry, str) and retry == 'no_limit':
        retries = -1
    else:
        retries = retry

    flag = False

    if tweet_limit:
        tweet_counter = 0

        while flag is False:
            response = requests.post(url, auth=oauth, headers=headers, params=params, stream=True)

            if response.status_code != 200:
                raise ConnectionError('connection errored with code ' + str(response.status_code) + '.')

            for line in response.iter_lines():
                if not line:
                    break

                if tweet_limit == tweet_counter:
                    flag = True
                    break

                if retries == 0:
                    flag = True
                    break

                try:
                    tweet = json.loads(line.decode('utf-8'))
                except json.decoder.JSONDecodeError:
                    retries -= 1
                    continue

                if filter_retweets:
                    if 'retweeted_status' not in tweet:
                        yield tweet
                        tweet_counter += 1
                else:
                    yield tweet
                    tweet_counter += 1

    elif date_limit is not None:
        while flag is False:
            response = requests.post(url, auth=oauth, headers=headers, params=params, stream=True)

            if response.status_code != 200:
                raise ConnectionError('connection errored with code ' + str(response.status_code) + '.')

            for line in response.iter_lines():
                if not line:
                    break

                current_date = datetime.datetime.now().strftime('%Y%m%d%H%M')
                if current_date >= date_limit:
                    flag = True
                    break

                if retries == 0:
                    flag = True
                    break

                try:
                    tweet = json.loads(line.decode('utf-8'))
                except json.decoder.JSONDecodeError:
                    retries -= 1
                    continue

                if filter_retweets:
                    if 'retweeted_status' not in tweet:
                        yield tweet
                else:
                    yield tweet

    else:
        tweet_limit = 1000
        tweet_counter = 0

        while flag is False:
            response = requests.post(url, auth=oauth, headers=headers, params=params, stream=True)

            if response.status_code != 200:
                raise ConnectionError('connection errored with code ' + str(response.status_code) + '.')

            for line in response.iter_lines():
                if not line:
                    break

                if tweet_limit == tweet_counter:
                    flag = True
                    break

                if retries == 0:
                    flag = True
                    break

                try:
                    tweet = json.loads(line.decode('utf-8'))
                except json.decoder.JSONDecodeError:
                    retries -= 1
                    continue

                if filter_retweets:
                    if 'retweeted_status' not in tweet:
                        yield tweet
                        tweet_counter += 1
                else:
                    yield tweet
                    tweet_counter += 1


def stream_country_tweets(access, country, language=None, filter_retweets=False,
                          tweet_limit=None, date_limit=None, retry=5):
    """
    This function retrieves streaming tweets matching the given query, so on, this function will open a stream to
    the Twitter Streaming API to retrieve real-time tweets. By the time these tweets are retrieved, they are handled
    and returned as a :obj:`list`.
    API Reference: https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/basic-stream-parameters.html

    Args:
        access (:obj:`twipper.credentials.Twipper`): object containing all the credentials needed to access api.twitter
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
            Yields a :obj:`list` containing all the retrieved tweets from Twitter, which means all the available tweets
            from the user specified on the arguments of the function.

    Raises:
        ValueError: raised if the introduced arguments do not match or errored.
    """

    if not access or not isinstance(access, Twipper):
        raise ValueError('access object to api.twitter is not valid!')

    api = access.api

    if not isinstance(api, oauth2.Client):
        raise ValueError('api is not valid!')

    oauth = access.oauth

    if not isinstance(oauth, requests_oauthlib.OAuth1):
        raise ValueError('auth is not valid!')

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

    if language:
        # try:
        #     languages = available_languages(api)
        # except (ConnectionError, json.decoder.JSONDecodeError, IndexError):
        #     raise RuntimeError('`twipper.utils.available_languages` function failed')

        languages = [
            'fr', 'en', 'ar', 'ja', 'es', 'de', 'it', 'id', 'pt', 'ko', 
            'tr', 'ru', 'nl', 'fil', 'msa', 'zh-tw', 'zh-cn', 'hi', 'no', 
            'sv', 'fi', 'da', 'pl', 'hu', 'fa', 'he', 'ur', 'th', 'uk', 
            'ca', 'ga', 'el', 'eu', 'cs', 'gl', 'ro', 'hr', 'en-gb', 'vi', 
            'bn', 'bg', 'sr', 'sk', 'gu', 'mr', 'ta', 'kn'
        ]

        if language in languages:
            params = {
                'language': language,
                'locations': str(bounding_box)
            }
        else:
            raise ValueError('the introduced language does not exist.')
    else:
        params = {
            'locations': str(bounding_box)
        }

    headers = {
        'Content-Type': 'application/json',
    }

    if isinstance(retry, str) and retry == 'no_limit':
        retries = -1
    else:
        retries = retry

    flag = False

    if tweet_limit:
        tweet_counter = 0

        while flag is False:
            response = requests.post(url, auth=oauth, headers=headers, params=params, stream=True)

            if response.status_code != 200:
                raise ConnectionError('connection errored with code ' + str(response.status_code))

            for line in response.iter_lines():
                if not line:
                    break

                if tweet_limit == tweet_counter:
                    flag = True
                    break

                if retries == 0:
                    flag = True
                    break

                try:
                    tweet = json.loads(line.decode('utf-8'))
                except json.decoder.JSONDecodeError:
                    retries -= 1
                    continue

                if filter_retweets:
                    if 'retweeted_status' not in tweet:
                        yield tweet
                        tweet_counter += 1
                else:
                    yield tweet
                    tweet_counter += 1

    elif date_limit is not None:

        while flag is False:
            response = requests.post(url, auth=oauth, headers=headers, params=params, stream=True)

            if response.status_code != 200:
                raise ConnectionError('connection errored with code ' + str(response.status_code))

            for line in response.iter_lines():
                if not line:
                    break

                current_date = datetime.datetime.now().strftime('%Y%m%d%H%M')
                if current_date >= date_limit:
                    flag = True
                    break

                if retries == 0:
                    flag = True
                    break

                try:
                    tweet = json.loads(line.decode('utf-8'))
                except json.decoder.JSONDecodeError:
                    retries -= 1
                    continue

                if filter_retweets:
                    if 'retweeted_status' not in tweet:
                        yield tweet
                else:
                    yield tweet

    else:
        tweet_limit = 1000
        tweet_counter = 0

        while flag is False:
            response = requests.post(url, auth=oauth, headers=headers, params=params, stream=True)

            if response.status_code != 200:
                raise ConnectionError('connection errored with code ' + str(response.status_code))

            for line in response.iter_lines():
                if not line:
                    break

                if tweet_limit == tweet_counter:
                    flag = True
                    break

                if retries == 0:
                    flag = True
                    break

                try:
                    tweet = json.loads(line.decode('utf-8'))
                except json.decoder.JSONDecodeError:
                    retries -= 1
                    continue

                if filter_retweets:
                    if 'retweeted_status' not in tweet:
                        yield tweet
                        tweet_counter += 1
                else:
                    yield tweet
                    tweet_counter += 1
