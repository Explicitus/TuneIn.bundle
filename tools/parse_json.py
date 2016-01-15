import urllib2, json

request = urllib2.Request(
        url = 'http://tunein.com/profile/follows/?identifier=u159012873/follows/stations&type=&offset=0',
        headers={'x-requested-with': 'XMLHttpRequest'}
       )
response = urllib2.urlopen(request)
text = response.read()

js = json.loads(text)

print(len(js['payload']['guideItemGroups']))
