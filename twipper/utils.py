#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Alvaro Bartolome @ alvarob96 on GitHub'
__version__ = '0.0.3'

import json
import requests


def available_languages(api):
    """
    This function retrieves all the languages in which the language of a tweet can be detected,
    as they are the languages that Twitter works with. This function allows the system to check if
    the introduced language to a function is a valid one or not. API Reference:
    https://developer.twitter.com/en/docs/developer-utilities/supported-languages/api-reference/get-help-languages.html

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
        raise ConnectionError('connection to `api.twitter` could not be established.')

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

    bounding_box = ','.join(result)

    return bounding_box
