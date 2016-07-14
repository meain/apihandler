from apihandler import apihandler
import wolframalpha
from apikeys import *


class apiwolfram(apihandler):
    def __init__(self):
        self.client = wolframalpha.Client(key_wolfram.key)

    def call(self, data, mode):
        '''
        Here data is a string 'the wolfram querry'
        '''
        data = self.client.query(data)
        return data


