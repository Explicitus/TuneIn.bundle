ROOT_MENU = 'http://opml.radiotime.com/Browse.ashx?formats=mp3,aac'

####################################################################################################
def Start():

    ObjectContainer.title1 = 'TuneIn'
    HTTP.CacheTime = 300

####################################################################################################
@handler('/music/tunein', 'TuneIn')
@route('/music/tunein/menu')
def Menu(url=ROOT_MENU, title='', outline_text=''):

    oc = ObjectContainer(title2=title)
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

                oc.add(TrackObject(
                    url = item.get('URL'),
                    title = item.get('text'),
                    thumb = Resource.ContentsOfURLWithFallback(item.get('image'))
                ))

    return oc
