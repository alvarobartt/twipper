#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Alvaro Bartolome @ alvarob96 on GitHub'
__version__ = '0.0.1'

import json


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
