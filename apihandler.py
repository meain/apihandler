from unqlite import UnQLite
import datetime
try:
    import pickle
except:
    import cPickle as pickle


class apihandler:
    '''
    This is the base call from which each api class will be derived.
    Caching will be taken care in here, only the api specific code needs to be written in
    the derived class
    '''

    '''
    Initialize cache db
    '''
    db = UnQLite('apihandlerdata')
    api_cache = db.collection('apicache')
    api_cache.create()

    def write_cache(self, data, mode, result):
        '''
        Write cache to db
        Pickling all data cuz ****
        '''
        self.api_cache.store({'data': pickle.dumps(data), 'mode': pickle.dumps(mode), 'result': pickle.dumps(result), 'time': pickle.dumps(datetime.datetime.now())})

    def read_cache(self, data, mode):
        '''
        Read data, blah blah...
        You know how it works...
        '''
        cache_data = self.api_cache.filter(lambda api: api['data']==pickle.dumps(data) and api['mode']==pickle.dumps(mode))
        # cached_data[-1] jsut because it might have old data, this will ensure it takes the last one
        if not cache_data or cache_data[-1]['result'] is None:
            return None
        else :
            return pickle.loads(cache_data[-1]['result'])

    def call(self, data, mode):
        '''
        This function will be redifined in the derived api class according to the api reqiured

        Parameters:
            data - Data for the api( json/text )
            mode - In case the api has different kinds of calls this can be used
        '''
        pass

    def __call__(self, data, mode='defaultapicall'):
        '''
        Caching happens here.
        We cache the call() function which will be defined for each api in the derived class
        NoSQL db is used as backend
        '''
        # Chcke db
        cached_data = self.read_cache(data, mode)
        if cached_data is None:
            # No cached data available
            result = self.call(data, mode)
            self.write_cache(data, mode, result)
            return result
        else:
            # Cached data available
            # TODO : Check time so as to limit use of old cache data
            result = cached_data
            return result
