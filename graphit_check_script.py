import requests


class State:
    __state = {0: 'OK', 1: 'Warning', 2: 'Critical', 3: 'Unknown'}

    def __init__(self, code=0):
        self.update_state_code(code)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.get_state())

    def get_state(self):
        return self.__state_code

    def get_state_message(self):
        return self.__state[self.get_state()]
    
    def update_state_code(self, code):
        if code in [0, 1, 2, 3]:
            self.__state_code = code
        else:
            self.__state_code = 3
    
    def check(self, low, high, value):
            if(value < low):
                self.update_state_code(0)
            elif (value < high):
                self.update_state_code(1)
            else:
                self.update_state_code(2)    

def main():
    try:
        url = "https://play.grafana.org/api/datasources/proxy/1/render?target=aliasByNode(movingAverage(scaleToSeconds(apps.fakesite.*.counters.requests.count,%201),%202),%202)&format=json&from=-5min"
        r = requests.get(url=url)
        datapoints = r.json()[0]['datapoints']
    except:
        print('Unkown')
        sys.exit()
        
    low = int(input('Enter Thereshhold Value: '))
    high = int(input('Enter Critical Thereshhold Value: '))
    for d in datapoints:
        state = State()
        try:
            state.check(low, high, d[0])
        except:
            state.update_state_code(3)
        print(state.get_state_message())

if __name__ == "__main__":
    main()
