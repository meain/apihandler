# Apihandler

Handles api request caching and other "stuff". This module is used to cache api data without much boilerplate code.
All you have to add is to import the base class which deals with all the caching part for you.

* Uses NoSQL database
* Can set cache data validity
* Very little boilerplate code

## Structure

Below is an example definition for the wolfram alpha api.
``` python 
from apihandler.apihandler import apihandler
import wolframalpha
from apikeys import *


class apiwolfram(apihandler):
    def __init__(self):
        self.client = wolframalpha.Client(key_wolfram.key)

    @property
    def cache_validity(self):
        return '1h'

    def call(self, data, mode):
        '''
        Data : string - 'wolfram query'
        '''
        data = self.client.query(data)
        return data
```
The `apihandler` class can is used as the base class for the new wolfram alpha class with caching.
You can add all the key setting  and creating object part in the `init` method.

The `cahe_validy` can be used to set the validity of the cache in the db.

The base class has a empty `call` function you can override in the derived class.
How the caching works is by caching the result from the `call` function.

### Defining the `call` function.

Input parameters

* `data` : `json/string` - the data that will be passed to the actual api as arguments
* `mode` : `string` - used so that if an api has multiple kind of output modes

After taking the input send the over to the api object and return the result as the function result.
