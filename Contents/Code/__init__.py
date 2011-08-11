####################################################################################################

MUSIC_PREFIX = "/music/tunein"

NAME = "TuneIn"

ART = 'art-default.jpg'
ICON = 'icon-default.png'

ROOT_MENU = 'http://opml.radiotime.com/Browse.ashx'

####################################################################################################

# This function is initially called by the PMS framework to initialize the plugin. This includes
# setting up the Plugin static instance along with the displayed artwork.
def Start():
    
    # Initialize the plugin
    Plugin.AddPrefixHandler(MUSIC_PREFIX, MainMenu, "TuneIn", ICON, ART)
    Plugin.AddViewGroup("List", viewMode = "List", mediaType = "items")
    Plugin.AddViewGroup("Details", viewMode = "InfoList", mediaType = "items")
    
    # Setup the artwork associated with the plugin
    MediaContainer.art = R(ART)
    MediaContainer.title1 = NAME
    MediaContainer.viewGroup = "List"
    DirectoryItem.thumb = R(ICON)

####################################################################################################

def MainMenu():
    dir = MediaContainer(disabledViewModes=["Coverflow"], title1 = NAME)

    root = XML.ElementFromURL(ROOT_MENU)
    for item in root.xpath("//body/outline[@type='link']"):
        title = item.get('text')
        url = item.get('URL')
        dir.Append(Function(DirectoryItem(SubMenu, title = title), url = url))
    
    return dir

####################################################################################################

def SubMenu(sender, url, root = None, outline_index = 0):
    dir = MediaContainer(disabledViewModes=["Coverflow"], title1 = L('Title'), title2 = sender.itemTitle)

    index = 0
    navigator = "/"
    
    # If we are starting from the beginning, we need to make sure that we only match elements
    # we immediately proceed the main body element.
    if outline_index == 0:
        navigator = navigator + "/body"
    
    # Append the correct number 
    while(index <= outline_index):
        navigator = navigator + "/outline"
        index = index + 1
    
    # Obtain the appropriate root element to start from. If we have been given a specific one, we
    # can ignore the url and just construct the XML object from the given root.
    if root == None:
        root = XML.ElementFromURL(url)
    else:
        root = XML.ElementFromString(root)

    for item in root.xpath(navigator):
        
        type = item.get('type')
        title = item.get('text')

        # If we have found a linked item, it will contain a new page to navigate too.
        if type == 'link':

            url = item.get('URL')
            dir.Append(Function(DirectoryItem(SubMenu, title = title), url = url))

        # If we have actually found an audio stream, we should expect it to contain more
        # information about the available content.
        elif type == 'audio':

            # We should be able to access the subtext and thumb associated with the content.
            url = item.get('URL')
            subtitle = item.get('subtext')
            thumb = item.get('image')
            dir.Append(TrackItem(url, title = title, subtitle = subtitle, thumb = thumb))

        else:

            # We'll use the same url but navigate further down the available sub-items.
            dir.Append(Function(DirectoryItem(SubMenu, title = title), url = url, outline_index = outline_index + 1, root = XML.StringFromElement(item)))

    return dir