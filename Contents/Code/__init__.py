ROOT_MENU = 'http://opml.radiotime.com/Browse.ashx?formats=mp3,aac'

ART    = 'art-default.jpg'
ICON   = 'icon-default.png'
ICON_MORE   = 'arrow-next-2-icon.png'

STATION_URL = 'http://tunein.com/radio/-%s/'
USER_URL = 'http://opml.radiotime.com/Browse.ashx?c=presets&partnerId=RadioTime&username=%s'
MY_STATIONS = 'tunein://mystations'

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
def Menu(url=ROOT_MENU, title='', xml = None):

    oc = ObjectContainer(title2=title)

    if url == ROOT_MENU:
        my_stations = L('My Stations')
        oc.add(DirectoryObject(
            key = Callback(Menu, url=MY_STATIONS, title=my_stations),
            title = my_stations
        ))
        oc.add(PrefsObject(
                title   = L('Preferences...'),
            )
        )

    if url == MY_STATIONS:
        username = Prefs['username']

        if not username:
            oc.message = L('Please specify user name in the TuneIn preferences')
            return oc

        url = USER_URL % username

    if xml:
        subitems = XML.ElementFromString(xml)
    else:
        subitems = XML.ElementFromURL(url).xpath('//body')[0]

    # Log.Debug('Subitems: '+str(subitems))
    Log.Debug('Subitems count: '+str(len(subitems)))

    for item in subitems:
        typ = item.get('type')
        local_url = item.get('URL')
        text = item.get('text')
        image = item.get('image')
        key = item.get('key')
        subtext = item.get('subtext')

        if key in ['unavailable', 'related']:
            continue

        if typ == 'audio':
            oc.add(TrackObject(
                url = local_url,
                title = text,
                summary = subtext,
                thumb = Resource.ContentsOfURLWithFallback(image)
            ))
        elif typ == 'link':
            oc.add(DirectoryObject(
                key = Callback(Menu, url=local_url, title=text),
                title = text,
                thumb = Resource.ContentsOfURLWithFallback('')
            ))
        else:
            # Log.Debug('Current item: '+str(item))
            oc.add(DirectoryObject(
                key = Callback(Menu, title=text, xml = XML.StringFromElement(item)),
                title = text,
                thumb = Resource.ContentsOfURLWithFallback('')
            ))

    return oc
