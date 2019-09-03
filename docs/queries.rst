Queries
=======

Since the Twitter querying system is a little bit confusing due to some differences between Standard and Streaming queries,
some additional functions have been created by `twipper <https://github.com/alvarob96/twipper>`_ in order to fix this
minor issue when it comes to data retrieval from Twitter via its API, using either **twipper** or any other Twitter
Wrapper for Python.

So on, a simple keyword based queries format has been created in order to convert every traditional query using logical
operators to the standard query required by Twitter on its Standard or Streaming search. The created queries have the
following operators:

- **AND**: logical operator that implies that the tweets-to-search match both of the introduced keywords, but not on the specified order.
- **OR**: logical operator that means that the tweets-to-search will match every tweet containing either one word or another, can be applied for N keywords.
- **NOT**: operator that means that the tweets-to-search do not contain the introduced keyword.

.. warning::
    Note that the NOT operator will only work for standard queries since it is not supported by Twitter Streaming

Once the basics have been explained a simple example on its usage is proposed. Suppose that you want to search tweets
containing either the word dog or cat, and you want to filter out the ones that even matching the previous condition
also have the word frog. So on the query will look like: ``DOG AND CAT AND NOT frog``, then, the twipper querying
formatter will convert that query to either a standard or a streaming query.

Then, twipper should be used the following way in order to convert the previous query into a standard twitter query:

.. code-block:: python

    from twipper.utils import standard_query

    query = "dog OR cat AND NOT frog"
    standard = standard_query(query)

    print(standard)
    >>> "dog OR cat -frog"


As already said before, the NOT operator just works for the standard search as it is not supported for streaming tweets,
if we wanted to filter out tweets containing certain words we should do it while the tweets are being retrieved. Anyways
the basic usage for streaming queries should be like:

.. code-block:: python

    from twipper.utils import streaming_query

    query = "dog OR cat"
    streaming = streaming_query()

    print(streaming)
    >>> "dog,cat"

For further help you can either check the API Reference.
