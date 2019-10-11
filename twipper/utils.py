#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2018-2019 Alvaro Bartolome
# See LICENSE for details.

import json
import requests
import re


def available_languages(api):
    """
    This function retrieves all the languages in which the language of a tweet can be detected,
    as they are the languages that Twitter works with. This function allows the system to check if
    the introduced language to a function is a valid one or not. API Reference:
    https://developer.twitter.com/en/docs/developer-utilities/supported-languages/api-reference/get-help-languages.html

    Args:
        api (:obj:`oauth2.Client`): api object with access to api.twitter

    Returns:
        :obj:`list` - languages:
            Returns a :obj:`list` containing all the available languages in which tweets are written,
            in order to check if the introduced language is a valid one or not.

    Raises:
        ConnectionError: raised when connection to api.twitter could not be established.
        RuntimeError: raised when response object could not be parsed.
        IndexError: raised if the retrieved languages `list` is empty.
    """

    url = 'https://api.twitter.com/1.1/help/languages.json'

    response, content = api.request(url, method='GET')

    if response.status != 200:
        raise ConnectionError('connection to `api.twitter` could not be established (HTTP Error ' +
                              str(response.status) + ').')

    try:
        data = json.loads(content.decode('utf-8'))
    except json.JSONDecodeError:
        raise RuntimeError('retrieved content could not be parsed.')

    languages = list()

    for value in data:
        if 'code' in value:
            languages.append(value['code'])
        else:
            continue

    if len(languages) > 0:
        return languages
    else:
        raise IndexError('`api.twitter` languages could not be retrieved.')


def country_to_bounding_box(country):
    """
    This function retrieves the bounding box coordinates of the specified country, as in order to retrieve tweets
    from an specific country or region from Twitter Streaming API the bounding box coordinates are needed. So on, the
    source where the bounding boxes are retrieved is https://nominatim.openstreetmap.org/, via HTTP GET request.

    Args:
        country (:obj:`str`): name of the country or region to get the bounding box coordinates from

    Returns:
        :obj:`str` - bounding_box:
            Returns a :obj:`str` containing all the bounding box coordinates for a specified country,
            in order to sent it as a param to the POST request for the Streaming API

    Raises:
        ConnectionError: raised when connection to http://nominatim.openstreetmap.org/ could not be established.
        ValueError: raised when arguments are not valid or json errored while loading.
        IndexError: raised if access to json object bounding box errored.
    """

    url = 'http://nominatim.openstreetmap.org/search?q=' + country + '&format=json'

    req = requests.get(url)

    if req.status_code != 200:
        raise ConnectionError('connection errored with code ' + str(req.status_code))

    try:
        result = json.loads(req.text)
    except ValueError:
        raise ValueError('error loading json from request')

    try:
        result = result[0]["boundingbox"]
    except IndexError:
        return IndexError('error accessing json object')

    coordinates = [2, 0, 3, 1]  # western, south, east, north

    result = [result[i] for i in coordinates]

    bounding_box = ','.join(result)

    return bounding_box


def standard_query(query):
    """
    This function converts the introduced query formatted as specified by twipper, so to make ease to use
    it as Twitter specifies different query formats for batch and streaming query. So on this function is intended
    to be used combined with any Twitter Wrapper to improve queries usability. API Reference:
    https://developer.twitter.com/en/docs/tweets/search/guides/standard-operators

    Args:
        query (:obj:`str`): query formatted as specified by twipper to be converted onto a Twitter Batch query

    Returns:
        :obj:`str` - formatted_query:
            Returns a :obj:`str` which is the query formatted as required by Twitter, so the twipper-format of the
            initial query is now converted to the required format.

    Raises:
        ValueError: raised if the introduced arguments do not match or errored.
        RuntimeError: raised if the resulting query is not valid.
    """

    if not query:
        raise ValueError('`query` parameter is mandatory and should be a str!')

    if query is not None and not isinstance(query, str):
        raise ValueError('`query` parameter is mandatory and should be a str!')

    query = ''.join(re.findall('[a-zA-Zá-üÁ-Ü0-9]+', query))

    query = query.replace('AND', ' ').replace('OR', ' OR ').replace('NOT', '-')

    if len(query) > 0:
        return query
    else:
        raise RuntimeError('`query formatting failed due to introduced query error')


def streaming_query(query):
    """
    This function converts the introduced query formatted as specified by twipper, so to make ease to use
    it as Twitter specifies different query formats for batch and streaming query. So on this function is intended
    to be used combined with any Twitter Wrapper to improve queries usability. API Reference:
    https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/basic-stream-parameters#track

    Args:
        query (:obj:`str`): query formatted as specified by twipper to be converted onto a Twitter Stream track query

    Returns:
        :obj:`str` - formatted_query:
            Returns a :obj:`str` which is the query formatted as required by Twitter, so the twipper-format of the
            initial query is now converted to the required format.

    Raises:
        ValueError: raised if the introduced arguments do not match or errored.
        RuntimeError: raised if the resulting query is not valid.
    """

    if not query:
        raise ValueError('`query` parameter is mandatory and should be a str!')

    if query is not None and not isinstance(query, str):
        raise ValueError('`query` parameter is mandatory and should be a str!')

    query = ''.join(re.findall('[a-zA-Zá-üÁ-Ü0-9]+', query))

    query = query.replace('AND', ' ').replace('OR', ',').replace('NOT', '-')

    if len(query) > 0:
        return query
    else:
        raise RuntimeError('`query formatting failed due to introduced query error')
