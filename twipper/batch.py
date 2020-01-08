#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2018-2019 Alvaro Bartolome
# See LICENSE for details.

import json
import oauth2
from twipper.credentials import Twipper

# from twipper.utils import available_languages


def search_tweets(access, query, page_count=1, filter_retweets=False, verified_account=False,
                  language=None, result_type='mixed', count=100):
    """
    This function retrieves historical tweets on batch processing. These tweets contain the specified words on the
    query, which can use operators such as AND or OR, as specified on
    https://developer.twitter.com/en/docs/tweets/rules-and-filtering/overview/standard-operators. Additionally some
    extra arguments can be specified in order to particularize the tweet search, so on to retrieve the exact content
    the user is looking for.
    API Reference: https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets.html

    Args:
        access (:obj:`twipper.credentials.Twipper`): object containing all the credentials needed to access api.twitter
        query (:obj:`str`): contains the query with the words to search along Twitter historic data.
        page_count (:obj:`int`, optional):
            specifies the amount of pages (100 tweets per page) to retrieve data from, default value is 1.
        filter_retweets (:obj:`boolean`, optional):
            can be either `True` or `False`, to filter out retweets or not, respectively, default value is `False`.
        verified_account (:obj:`boolean`, optional):
            can either be True or False to retrieve tweets just from verified accounts or from any account type,
            respectively.
        language (:obj:`str`, optional): is the language on which the tweet has been written, default value is `None`.
        result_type (:obj:`str`, optional):
            value to indicate which type of tweets want to be retrieved, it can either be `mixed`, `popular` or `recent`
        count (:obj:`int`, optional): number of tweets per requests to retrieve (default and max is 100).

    Returns:
        :obj:`list` - tweets:
            Returns a :obj:`list` containing all the retrieved tweets from Twitter API, based on the search query
            previously specified on the function arguments.

    Raises:
        ValueError: raised if the introduced arguments do not match or errored.
    """

    if not access or not isinstance(access, Twipper):
        raise ValueError('access object to api.twitter is not valid!')

    api = access.api

    if not isinstance(api, oauth2.Client):
        raise ValueError('api is not valid!')

    if not isinstance(query, str):
        raise ValueError('query must be a string!')

    if query is None:
        raise ValueError('query is mandatory')

    if not isinstance(page_count, int) or not page_count:
        raise ValueError('page_count must be an `int` equal or higher than 1!')

    if isinstance(page_count, int) and page_count < 1:
        raise ValueError('page_count must be an `int` equal or higher than 1!')

    if not isinstance(language, str):
        raise ValueError('language must be a `str`!')

    if not isinstance(filter_retweets, bool):
        raise ValueError('filter_retweets must be a `boolean`!')

    if not isinstance(verified_account, bool):
        raise ValueError('verified_account must be a `boolean`!')

    if not isinstance(result_type, str):
        raise ValueError('result_type must be a `str`')

    if result_type not in ['mixed', 'popular', 'recent']:
        raise ValueError('result_type can just be `mixed`, `popular` or `recent`')

    if not isinstance(count, int):
        raise ValueError('count must be an `int` between 1 and 100!')

    if verified_account:
        query += " filter:verified"

    url = 'https://api.twitter.com/1.1/search/tweets.json?q=' + query

    if filter_retweets:
        url += ' -filter:retweets'

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

    if language:
        if language in languages:
            url += '&lang=' + language
        else:
            raise ValueError('the introduced language does not exist.')

    if isinstance(count, int) and 0 < count <= 100:
        url += '&count=' + str(count)
    else:
        url += '&count=100'

    if isinstance(result_type, str) and result_type in ['mixed', 'popular', 'recent']:
        url += '&result_type=' + result_type
    else:
        url += '&result_type=mixed'

    url += '&tweet_mode=extended'

    response, content = api.request(url, method='GET')

    if response.status != 200:
        raise ConnectionError('connection errored with code ' + str(response.status) + '.')

    tweets = list()

    try:
        data = json.loads(content.decode('utf-8'))
    except json.decoder.JSONDecodeError:
        raise RuntimeError('retrieved content could not be parsed.')

    if 'statuses' in data:
        if len(data['statuses']) > 0:
            tweets += data['statuses']

            if 'search_metadata' in data:
                if 'next_results' in data['search_metadata']:
                    next_url = data['search_metadata']['next_results']
                else:
                    return tweets
            else:
                return tweets
        else:
            raise IndexError('no tweets could be retrieved.')
    else:
        raise IndexError('no tweets could be retrieved.')

    base_url = 'https://api.twitter.com/1.1/search/tweets.json'

    if page_count > 1:
        for _ in range(page_count - 1):
            response, content = api.request(base_url + next_url, method='GET')

            if response.status != 200:
                break

            try:
                data = json.loads(content.decode('utf-8'))
            except json.decoder.JSONDecodeError:
                break

            if 'statuses' in data:
                if len(data['statuses']) > 0:
                    tweets += data['statuses']

                    if 'search_metadata' in data:
                        if 'next_results' in data['search_metadata']:
                            next_url = data['search_metadata']['next_results']
                        else:
                            break
                    else:
                        break
                else:
                    break
            else:
                break

    if len(tweets) > 0:
        return tweets
    else:
        raise IndexError('no tweets could be retrieved.')


def search_user_tweets(access, screen_name, page_count=1, filter_retweets=False,
                       language=None, result_type='mixed', count=100):
    """
    This function retrieves historical tweets from a Twitter user by their screen_name (@), whenever they grant the
    application access their tweets for commercial purposes on ReadOnly permission. Retrieved tweets are stored on a
    :obj:`list` which will be returned to the user.
    API Reference: https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets.html

    Args:
        access (:obj:`twipper.credentials.Twipper`): object containing all the credentials needed to access api.twitter
        screen_name (:obj:`str`): contains the username of the user from which tweets are going to be retrieved.
        page_count (:obj:`int`, optional):
            specifies the amount of pages (100 tweets per page) to retrieve data from, default value is 1.
        filter_retweets (:obj:`boolean`, optional):
            can be either `True` or `False`, to filter out retweets or not, respectively, default value is `False`.
        language (:obj:`str`, optional): is the language on which the tweet has been written, default value is `None`.
        result_type (:obj:`str`, optional):
            value to indicate which type of tweets want to be retrieved, it can either be `mixed`, `popular` or `recent`
        count (:obj:`int`, optional): number of tweets per requests to retrieve (default and max is 100).

    Returns:
        :obj:`list` - tweets:
            Returns a `list` containing all the retrieved tweets from Twitter, which means all the available tweets from
            the user specified on the arguments of the function.

    Raises:
        ValueError: raised if the introduced arguments do not match or errored.
    """

    if not access or not isinstance(access, Twipper):
        raise ValueError('access object to api.twitter is not valid!')

    api = access.api

    if not isinstance(api, oauth2.Client):
        raise ValueError('api is not valid!')

    if not isinstance(screen_name, str):
        raise ValueError('screen_name must be a string!')

    if screen_name is None:
        raise ValueError('screen_name is mandatory')

    if not isinstance(page_count, int) or not page_count:
        raise ValueError('page_count must be an `int` equal or higher than 1!')

    if isinstance(page_count, int) and page_count < 1:
        raise ValueError('page_count must be an `int` equal or higher than 1!')

    if not isinstance(language, str):
        raise ValueError('language must be a `str`!')

    if not isinstance(filter_retweets, bool):
        raise ValueError('filter_retweets must be a `boolean`!')

    if not isinstance(result_type, str):
        raise ValueError('result_type must be a `str`')

    if result_type not in ['mixed', 'popular', 'recent']:
        raise ValueError('result_type can just be `mixed`, `popular` or `recent`')

    if not isinstance(count, int):
        raise ValueError('count must be an `int` between 1 and 100!')

    url = 'https://api.twitter.com/1.1/search/tweets.json?q=from:' + screen_name

    if filter_retweets:
        url += ' -filter:retweets'

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

    if language:
        if language in languages:
            url += '&lang=' + language
        else:
            raise ValueError('the introduced language does not exist.')

    if isinstance(count, int) and 0 < count <= 100:
        url += '&count=' + str(count)
    else:
        url += '&count=100'

    if isinstance(result_type, str) and result_type in ['mixed', 'popular', 'recent']:
        url += '&result_type=' + result_type
    else:
        url += '&result_type=mixed'

    url += '&tweet_mode=extended'

    response, content = api.request(url, method='GET')

    if response.status != 200:
        raise ConnectionError('connection errored with code ' + str(response.status))

    tweets = list()

    try:
        data = json.loads(content.decode('utf-8'))
    except json.decoder.JSONDecodeError:
        raise RuntimeError('retrieved content could not be parsed.')

    if 'statuses' in data:
        if len(data['statuses']) > 0:
            tweets += data['statuses']

            if 'search_metadata' in data:
                if 'next_results' in data['search_metadata']:
                    next_url = data['search_metadata']['next_results']
                else:
                    return tweets
            else:
                return tweets
        else:
            raise IndexError('no tweets could be retrieved.')
    else:
        raise IndexError('no tweets could be retrieved.')

    base_url = 'https://api.twitter.com/1.1/search/tweets.json'

    if page_count > 1:
        for _ in range(page_count - 1):
            response, content = api.request(base_url + next_url, method='GET')

            if response.status != 200:
                break

            try:
                data = json.loads(content.decode('utf-8'))
            except json.decoder.JSONDecodeError:
                break

            if 'statuses' in data:
                if len(data['statuses']) > 0:
                    tweets += data['statuses']

                    if 'search_metadata' in data:
                        if 'next_results' in data['search_metadata']:
                            next_url = data['search_metadata']['next_results']
                        else:
                            break
                    else:
                        break
                else:
                    break
            else:
                break

    if len(tweets) > 0:
        return tweets
    else:
        raise IndexError('no tweets could be retrieved.')
