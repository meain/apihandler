from apihandler import apihandler
import wolframalpha
from apikeys import *


class apiwolfram(apihandler):
    def __init__(self):
        self.client = wolframalpha.Client(key_wolfram.key)

    @property
    def cache_validity(self):
        return '5s'

    def call(self, data, mode):
        '''
        Data : string - 'wolfram query'
        '''
        data = self.client.query(data)
        return data
