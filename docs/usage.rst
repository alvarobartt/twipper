Usage
=====

As **twipper** is a Twitter Wrapper written in Python its main purpose is to wrap all the available endpoints listed on
the Twitter API for both versions (Free and Premium), so to use them from a simple function call. So on the main step is
to validate Twitter API credentials since they are mandatory in order to work with the Twitter API.

.. code-block:: python

    import twipper

    cred = twipper.Twipper(consumer_key='consumer_key',
                           consumer_secret='consumer_secret',
                           access_token='access_token',
                           access_token_secret='access_token_secret')

Now once the ``Twipper`` credentials object has been properly created we can use it in order to work with the Twitter
API using Python. In the case that we want to retrieve data from Twitter based on a query, e.g. we want to search `cat`
tweets to analyze its content to launch a cat campaign for our brand (random example because everybody loves cats).

.. code-block:: python

    tweets = twipper.batch.search_tweets(access=credentials,
                                         query='cats',
                                         page_count=1,
                                         filter_retweets=True,
                                         language='en',
                                         result_type='popular',
                                         count=10)

So on, using ``batch`` functions you can retrieve historical *tweets* from the last 7-9 days matching the introduced
query, in this case the query is `cats` due to our cat campaign, remember it. Anyways, params can be adjusted to our
desires and/or needs as described on the API Reference.

.. note::
    For further **twipper** functions insights check the API Reference.