import json

ROOT_MENU = 'http://opml.radiotime.com/Browse.ashx?formats=mp3,aac'

ART    = 'art-default.jpg'
ICON   = 'icon-default.png'
ICON_MORE   = 'arrow-next-2-icon.png'

MY_STATIONS_PREFIX = 'mystations:'

RE_USER_ID = Regex('"HeroRibbon"\:\{"guideId"\:"(?P<userid>[^"]+)"')

USER_PAGE = "http://tunein.com/user/%s/"
STANTIONS_PAGE = "http://tunein.com/profile/follows/?identifier=%s/follows/stations&type=&offset=%s"
STATION_URL = 'http://opml.radiotime.com/Tune.ashx?id=%s&formats=mp3,aac'

####################################################################################################
def Start():

    ObjectContainer.title1 = 'TuneIn'
    HTTP.CacheTime = 300
    ObjectContainer.art = R(ART)
    DirectoryObject.art = R(ART)
    DirectoryObject.thumb = R(ICON)

####################################################################################################
def ValidatePrefs():

    return True

####################################################################################################
@handler('/music/tunein', 'TuneIn')
@route('/music/tunein/menu')
def Menu(url=ROOT_MENU, title='', outline_text=''):

    oc = ObjectContainer(title2=title)

    if url == ROOT_MENU:
        oc.add(MyStationsDirectory(L('My Stations'), 0))
        oc.add(PrefsObject(
                title   = L('Preferences...'),
            )
        )

    if (url.startswith(MY_STATIONS_PREFIX)):
        MakeMyStationsList(oc, url)
    else:
        MakeDefaultStationsList(oc, url, outline_text)

    return oc

####################################################################################################
def MyStationsDirectory(title, offset):

    return DirectoryObject(
                key = Callback(Menu, url=MY_STATIONS_PREFIX+str(offset), title=title, outline_text=title),
                title = title,
                thumb = R(ICON_MORE)
            )

####################################################################################################
def MakeMyStationsList(oc, url):

    if not Prefs['username']:
        oc.message = L('Please specify user name in the TuneIn preferences')
        return

    userid = GetUserId()
    offset = int(url.split(':')[1])

    Log.Debug("Requesting for stations. userid=%s, offset: %s" % (userid, offset))

    text = HTTP.Request(
                        STANTIONS_PAGE % (userid, offset),
                        headers={'x-requested-with': 'XMLHttpRequest'}
                        ).content

    js  = json.loads(text)

    counter = 0

    for station in js['payload']['guideItemGroups']:
        station_id = station['GuideId']

        track = TrackObject(
            url = STATION_URL % station_id,
            title = station['Title'],
            thumb = Resource.ContentsOfURLWithFallback(station['Image']),
            summary = station['Subtitle']
        )
        oc.add(track)

        counter += 1

    oc.add(MyStationsDirectory('More', offset+counter))

####################################################################################################
def MakeDefaultStationsList(oc, url, outline_text):

    root = XML.ElementFromURL(url).xpath('//body')[0]

    if len(root.xpath('./outline[@URL and not(@type="audio")]')) > 0:
        for item in root.xpath('./outline[@URL]'):

            oc.add(DirectoryObject(
                key = Callback(Menu, url=item.get('URL'), title=item.get('text')),
                title = item.get('text'),
                thumb = Resource.ContentsOfURLWithFallback('')
            ))

    if len(root.xpath('./outline[@text and not(@URL) and not(@key="related")]')) > 0 and outline_text == '':
        for item in root.xpath('./outline[@text and not(@URL) and not(@key="related")]'):

            if item.get('text') == 'This program is not available':
                continue

            oc.add(DirectoryObject(
                key = Callback(Menu, url=url, title=item.get('text'), outline_text=item.get('text')),
                title = item.get('text'),
                thumb = Resource.ContentsOfURLWithFallback('')
            ))

    if outline_text != '':
        for item in root.xpath('./outline[@text="%s"]/outline' % outline_text):

            if item.get('type') == 'link':

                oc.add(DirectoryObject(
                    key = Callback(Menu, url=item.get('URL'), title=item.get('text')),
                    title = item.get('text'),
                    thumb = Resource.ContentsOfURLWithFallback(item.get('image'))
                ))

            elif item.get('type') == 'audio':
                Log.Debug("Station XML: "+XML.StringFromElement(root))

                oc.add(TrackObject(
                    url = item.get('URL'),
                    title = item.get('text'),
                    thumb = Resource.ContentsOfURLWithFallback(item.get('image'))
                ))

####################################################################################################
def GetUserId():

    if Dict['username'] == Prefs['username']:
        return Dict['userid']

    content = HTTP.Request(USER_PAGE % Prefs['username']).content

    userid = RE_USER_ID.search(content).group('userid')

    Dict['username'] = Prefs['username']
    Dict['userid'] = userid

    return userid
