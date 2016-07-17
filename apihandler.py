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

    @property
    def cache_validity(self):
        '''
        Default = '' = unlimited
        You could use s(second) m(minute) h(hour) d(day) m(month) y(year)
        *only one at a time*
        eg :
            5s
            30d
            10m
            1y
        '''
        return ''

    def write_cache(self, data, mode, result):
        '''
        Write cache to db
        Pickling all data cuz ****
        '''
        # Get class name
        class_name = self.__class__.__name__

        pickled_data = pickle.dumps(data)
        pickled_mode = pickle.dumps(mode)
        pickled_result = pickle.dumps(result)
        pickled_time = pickle.dumps(datetime.datetime.now().replace(microsecond=0))
        self.api_cache.store({'data': pickled_data, 'mode': pickled_mode, 'result': pickled_result, 'class_name': class_name, 'time': pickled_time})

    def read_cache(self, data, mode):
        '''
        Read data, blah blah...
        You know how it works...
        '''
        # Get class name
        class_name = self.__class__.__name__

        cache_data = self.api_cache.filter(lambda api: api['data'] == pickle.dumps(data) and \
                api['mode'] == pickle.dumps(mode) and api['class_name'] == class_name)
        if len(cache_data) > 0:
            cache_result = cache_data[-1]
            # Check validity of cache
            validity = self.cache_validity
            save_time = pickle.loads(cache_result['time'])
            current_time = datetime.datetime.now().replace(microsecond=0)
            time_difference = (current_time - save_time).total_seconds()
            # Get validity
            if len(validity) > 0:
                if validity[-1] == 's':
                    valid_seconds = int(validity[:-1])
                elif validity[-1] == 'm':
                    valid_seconds = int(validity[:-1]) * 60
                elif validity[-1] == 'h':
                    valid_seconds = int(validity[:-1]) * 60 * 60
                elif validity[-1] == 'd':
                    valid_seconds = int(validity[:-1]) * 24 * 60 * 60
                elif validity[-1] == 'm':
                    valid_seconds = int(validity[:-1]) * 30 * 24 * 60 * 60
                elif validity[-1] == 'y':
                    valid_seconds = int(validity[:-1]) * 12 * 30 * 24 * 60 * 60
            else:
                # Infinite validity
                valid_seconds = 0
                time_difference = 0
            # Remove if api data not valid anymore
            if valid_seconds < time_difference :
                cache_result = None
        else :
            cache_result = None

        # cached_data[-1] jsut because it might have old data, this will ensure it takes the last one
        if not cache_result or cache_result['result'] is None:
            return None
        else :
            return pickle.loads(cache_result['result'])

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
            result = cached_data
            return result
