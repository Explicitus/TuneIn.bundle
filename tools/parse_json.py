import urllib2, json
from pprint import pprint

URL_STATION = 'http://tunein.com/radio/-%s/'

####################################################################################################
def GetJson(url):

    print ("Requesting "+url)
    request = urllib2.Request(
        url = url,
        headers={
            'x-requested-with': 'XMLHttpRequest',
            'Accept: application/json': 'text/javascript, */*; q=0.01'}
       )
    response = urllib2.urlopen(request)
    text = response.read()

    # print ("The response: "+text)

    return json.loads(text)

####################################################################################################
class TuneInStation:

    def __init__(self, id='', url=''):
        if not id:
            id = GetStationId(url)

        self.js = GetJson(URL_STATION % id)['payload']['Station']
        self.broadcast = self.js['broadcast']
        self.echo = self.broadcast['EchoData']

        # Log.Debug('Station id: %s, json: %s' % (id, self.__js))
        # print('Station id: %s, json: %s' % (id, self.js))

    @property
    def id(self):
        return self.echo['targetGuideId']

    @property
    def title(self):
        return self.broadcast['Title']

    @property
    def description(self):
        return self.js['description']

    @property
    def image_url(self):
        return self.broadcast['Logo']

    @property
    def summary(self):
        return self.echo['subtitle']

    @property
    def playing(self):
        return self.broadcast['SongPlayingTitle']

    @property
    def stream_url(self):
        return self.broadcast['StreamUrl']

station = TuneInStation('s119801')
print (station.stream_url)
