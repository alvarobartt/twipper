#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Alvaro Bartolome @ alvarob96 on GitHub'
__version__ = '0.0.1'

import json
import oauth2

from twipper.utils import available_languages


def search_tweets(api, query, page_count=5, filter_retweets=False, language=None):
    """
    This function retrieves historical tweets on batch processing. These tweets contain the specified words on the
    query, which can use operators such as AND or OR, as specified on
    https://developer.twitter.com/en/docs/tweets/rules-and-filtering/overview/standard-operators. Additionally some
    extra arguments can be specified in order to particularize the tweet search, so on to retrieve the exact content
    the user is looking for.
    API Reference: https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets.html

    Args:
        api (:obj:`oauth2.Client`): valid Twitter API generated via `twipper.credentials.TwipperCredentials`.
        query (:obj:`str`): contains the query with the words to search along Twitter historic data.
        page_count (:obj:`int`, optional):
            specifies the amount of pages (100 tweets per page) to retrieve data from. Default value is 5.
        filter_retweets (:obj:`boolean`, optional):
            can be either `True` or `False`, to filter out retweets or not, respectively. Default value is `False`.
        language (:obj:`str`, optional): is the language on which the tweet has been written. Default value is `None`.

    Returns:
        :obj:`list` - tweets:
            Returns a :obj:`list` containing all the retrieved tweets from Twitter API, based on the search query
            previously specified on the function arguments.

    Raises:
        ValueError: raised if the introduced arguments do not match or errored.
    """

    if not isinstance(api, oauth2.Client):
        raise ValueError('specified api is not valid!')

    if api is None:
        raise ValueError('api is mandatory')

    if not isinstance(query, str):
        raise ValueError('query must be a string!')

    if query is None:
        raise ValueError('query is mandatory')

    if not isinstance(page_count, int):
        raise ValueError('page_count must be an integer!')

    if page_count is None:
        raise ValueError('page_count is mandatory')

    if not isinstance(language, str):
        raise ValueError('language must be a string!')

    if language is None:
        raise ValueError('language is mandatory')

    if not isinstance(filter_retweets, bool):
        raise ValueError('filter_retweets must be a boolean!')

    if filter_retweets is None:
        raise ValueError('filter_retweets is mandatory')

    url = 'https://api.twitter.com/1.1/search/tweets.json?q=' + query

    if filter_retweets:
        url += ' -filter:retweets'

    try:
        languages = available_languages(api)
    except (ConnectionError, json.decoder.JSONDecodeError, IndexError):
        raise RuntimeError('`twipper.utils.available_languages` function failed')

    if language:
        if language in languages:
            url += '&lang=' + language
        else:
            raise ValueError('the introduced language does not exist.')

    url += '&count=100'

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
            max_id = data['statuses'][-1]['id']
            tweets.append(data['statuses'])
        else:
            return tweets
    else:
        return tweets

    pages = page_count
    for _ in range(pages):
        response, content = api.request(url + '&since_id=' + str(max_id), method='GET')

        if response.status != 200:
            break

        try:
            data = json.loads(content.decode('utf-8'))
        except json.decoder.JSONDecodeError:
            raise RuntimeError('ERR#006: retrieved content could not be parsed.')

        if 'statuses' in data:
            if len(data['statuses']) > 0:
                max_id = data['statuses'][-1]['id']
                tweets.append(data['statuses'])
            else:
                break
        else:
            break

    if len(tweets) > 0:
        return tweets
    else:
        raise IndexError('no tweets could be retrieved.')


def search_user_tweets(api, screen_name, page_count=5, filter_retweets=False, language=None):
    """
    This function retrieves historical tweets from a Twitter user by their screen_name (@), whenever they grant the
    application access their tweets for commercial purposes on ReadOnly permission. Retrieved tweets are stored on a
    :obj:`list` which will be returned to the user.
    API Reference: https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets.html

    Args:
        api (:obj:`oauth2.Client`): valid Twitter API generated via `twipper.credentials.TwipperCredentials`.
        screen_name (:obj:`str`): contains the username of the user from which tweets are going to be retrieved.
        page_count (:obj:`int`, optional):
            specifies the amount of pages (100 tweets per page) to retrieve data from. Default value is 5.
        filter_retweets (:obj:`boolean`, optional):
            can be either `True` or `False`, to filter out retweets or not, respectively. Default value is `False`.
        language (:obj:`str`, optional): is the language on which the tweet has been written. Default value is `None`.

    Returns:
        tweets (:obj:`list`): description
            returns a `list` containing all the retrieved tweets from Twitter, which means all the available tweets from
            the user specified on the arguments of the function.

    Raises:
        ValueError: raised if the introduced arguments do not match or errored.
    """

    if not isinstance(api, oauth2.Client):
        raise ValueError('specified api is not valid!')

    if api is None:
        raise ValueError('api is mandatory')

    if not isinstance(screen_name, str):
        raise ValueError('screen_name must be a string!')

    if screen_name is None:
        raise ValueError('screen_name is mandatory')

    if not isinstance(page_count, int):
        raise ValueError('page_count must be an integer!')

    if page_count is None:
        raise ValueError('page_count is mandatory')

    if not isinstance(filter_retweets, bool):
        raise ValueError('filter_retweets must be a boolean!')

    if filter_retweets is None:
        raise ValueError('filter_retweets is mandatory')

    if language is not None and not isinstance(language, str):
        raise ValueError('language must be a string!')

    url = 'https://api.twitter.com/1.1/search/tweets.json?q=from:' + screen_name

    if filter_retweets:
        url += ' -filter:retweets'
    try:
        languages = available_languages(api)
    except (ConnectionError, json.decoder.JSONDecodeError, IndexError):
        raise RuntimeError('`twipper.utils.available_languages` function failed')

    if language:
        if language in languages:
            url += '&lang=' + language
        else:
            raise ValueError('the introduced language does not exist.')

    url += '&count=100'

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
            max_id = data['statuses'][-1]['id']
            tweets.append(data['statuses'])
        else:
            return tweets
    else:
        return tweets

    pages = page_count
    for _ in range(pages):
        response, content = api.request(url + '&since_id=' + str(max_id), method='GET')

        if response.status != 200:
            break

        try:
            data = json.loads(content.decode('utf-8'))
        except json.decoder.JSONDecodeError:
            raise RuntimeError('ERR#006: retrieved content could not be parsed.')

        if 'statuses' in data:
            if len(data['statuses']) > 0:
                max_id = data['statuses'][-1]['id']
                tweets.append(data['statuses'])
            else:
                break
        else:
            break

    if len(tweets) > 0:
        return tweets
    else:
        raise IndexError('no tweets could be retrieved.')
