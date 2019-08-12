#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2018-2019 Alvaro Bartolome
# See LICENSE for details.

import json

import oauth2
import requests
from requests_oauthlib import OAuth1


class Twipper(object):
    """
    Twipper is a class that contains the constructor (`__init__`) of the Twitter API credentials in order to
    get access to it via validating the credentials of the application previously created by the user on
    https://developer.twitter.com/.
    """

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        """
        This function is the constructor of :obj:`twipper.credentials.Twipper` class,
        which will instantiate the class and initialize it with the respective arguments specified.

        Args:
           consumer_key (:obj:`str`): Twitter API Consumer Key.
           consumer_secret (:obj:`str`): Twitter API Consumer Key Secret.
           access_token (:obj:`str`): Twitter API Access Token.
           access_token_secret (:obj:`str`): Twitter API Access Token Secret.
        """

        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

        self.api = self.__get_api()
        self.oauth = self.__get_oauth()
        self.oauth_token = self.__get_oauth_token()

        self.plan = ''
        self.label = ''

    @property
    def plan(self):
        return self._plan

    @plan.setter
    def plan(self, premium_plan):
        if isinstance(premium_plan, str):
            self._plan = premium_plan
        else:
            raise Exception('invalid value for premium plan.')

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, premium_label):
        if isinstance(premium_label, str):
            self._label = premium_label
        else:
            raise Exception('invalid value for dev environment label.')

    def __get_api(self):
        """
        This function validates the credentials of the Twitter API, by validating the token with oauth2 as it is the
        default authentication method implemented by the Twitter API (even though oauth1 authentication can be used). So
        on, once the credentials have been validated the function returns the client (API), which will later be used to
        send both GET and POST requests to https://api.twitter.com/1.1/

        Returns:
            :obj:`oauth2.Client` - api:
                Returns the oauth2 validated client to send both GET and POST requests to the Twitter API.

        Raises:
            ValueError: raised if the consumer, token or client are not valid.
        """

        try:
            try:
                consumer = oauth2.Consumer(key=self.consumer_key,
                                           secret=self.consumer_secret)
            except ValueError as e:
                print(e) # Invalid consumer
                return None

            try:
                token = oauth2.Token(key=self.access_token,
                                     secret=self.access_token_secret)
            except ValueError as e:
                print(e) # Invalid token
                return None

            api = oauth2.Client(consumer, token)

            return api
        except ValueError as e:
            print(e) # Invalid client
            return None

    def __get_oauth(self):
        """
        This function gets the `requests_oauthlib.OAuth1` authentication object with the OAuth1 method in order to
        generate the `auth` object that will be sent inside a request header.

        Returns:
            :obj:`requests_oauthlib.OAuth1` - oauth:
                Returns the oauth1 object containing the credentials to access Twitter API endpoints for Streaming.
        """

        oauth = OAuth1(self.consumer_key, self.consumer_secret,
                       self.access_token, self.access_token_secret)

        return oauth

    def __get_oauth_token(self):
        """
        This function provides the Bearer token which will grant us the access to the Twitter Premium API in order
        to send both GET and POST requests. The Bearer token is generated via Twitter API which implements an OAuth2
        authentication protocol, so on, it will be included on the Authorization field of the headers of every request.
        API Reference: https://developer.twitter.com/en/docs/basics/authentication/api-reference/token

        Returns:
            :obj:`str` - access_token:
                Returns the Bearer token provided by Twitter OAuth2 for API Premium access.
        """

        base_url = 'https://api.twitter.com/oauth2/token'

        data = {
            'grant_type': 'client_credentials',
            'client_id': self.consumer_key,
            'client_secret': self.consumer_secret,
        }

        response = requests.post(base_url,
                                 auth=(self.consumer_key, self.consumer_secret),
                                 data=data)

        if response.status_code != 200:
            return None

        parsed = response.json()

        if 'access_token' in parsed:
            oauth_token = parsed['access_token']

            return oauth_token
        else:
            return None

    def close(self):
        """
        This function invalidates the specified access_token as Twitter API generates one access_token per application,
        so whenever the current access_token is not needed anymore it should be invalidated in order to be able to
        generate another one in future requests. The Bearer token should be revoked by the end of its use.
        API Reference: https://developer.twitter.com/en/docs/basics/authentication/api-reference/invalidate_bearer_token

        Returns:
            :obj:`boolean` - state:
                Returns a :obj:`boolean` which is either `True` if the access_token was properly revoked or
                `False` if the function errored at any point.
        """

        base_url = 'https://api.twitter.com/oauth2/invalidate_token'

        headers = {
            'Authorization': 'Bearer ' + self.oauth_token,
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            'access_token': self.oauth_token,
        }

        data = json.dumps(data)

        response = requests.post(base_url,
                                 headers=headers,
                                 data=data)

        if response.status_code != 200:
            return False
        else:
            return True
