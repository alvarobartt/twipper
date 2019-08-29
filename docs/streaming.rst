Streaming
=========

Twitter offers a Streaming service to retrieve real-time tweets that match a given query or location. This service
uses an OAuth1 authentication method which requires both consumer (``consumer_key``, ``consumer_secret``) and access keys
(``access_token``, ``access_token_secret``) and those keys will be used to authenticate the Twitter App, and so on to access
the Streaming service via OAuth1.

As described below, for further details on Twitter Streaming insights please check the following diagram proposed by
Twitter on `Consuming Streaming Data <https://developer.twitter.com/en/docs/tutorials/consuming-streaming-data.html>`_.

.. image:: https://raw.githubusercontent.com/alvarob96/twipper/master/docs/twitter_streaming.png
    :align: center

So on, `twipper <https://github.com/alvarob96/twipper>`_ has been created in order to cover Twitter Streaming process
to retrieve real-time tweets. The sample usage of **twipper** when it comes to streaming data will be as it follows:

.. code-block:: python

    import twipper

    from twipper.streaming import stream_tweets

    cred = twipper.Twipper(consumer_key='consumer_key',
                           consumer_secret='consumer_secret',
                           access_token='access_token',
                           access_token_secret='access_token_secret')

    tweets = stream_tweets(access=cred,
                           query='cats',
                           language='en',
                           filter_retweets=True,
                           tweet_limit=100,
                           date_limit=None,
                           retry='no_limit')

    results = list()

    for index, tweet in enumerate(tweets, 1):
        print('Inserting tweet number ' + str(index))
        results.append(tweet)


The previous block of code retrieves up to 100 tweets written in English matching the word `cats` as specified on the
query, filtering out retweets and with an infinite number of tries if the retrieval process fails, until the objective
is reached. Later on, as the returned data from the function are ``yield`` values inserted into a generator, a for loop
is needed in order to store all the available retrieved data on a list. That list will contain a tweet formatted as a
JSON object as described by Twitter.

.. code-block:: json

    {
        "created_at": "Thu May 10 15:24:15 +0000 2018",
        "id_str": "850006245121695744",
        "text": "Here is the Tweet message.",
        "user": {

        },
        "place": {

        },
        "entities": {

        },
        "extended_entities": {

        }
    }

More JSON samples can be found at https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/intro-to-tweet-json.html.

.. note::
    For further ``twipper.streaming`` insights or information please use the streaming API Reference where functions
    are described and sorted out so to understand its usage and how the params should be formatted in order to execute
    useful queries and retrieve the desired information from Twitter.
