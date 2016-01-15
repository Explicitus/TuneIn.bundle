License
-------

If the software submitted to this repository accesses or calls any software provided by Plex (“Interfacing Software”), then as a condition for receiving services from Plex in response to such accesses or calls, you agree to grant and do hereby grant to Plex and its affiliates worldwide a worldwide, nonexclusive, and royalty-free right and license to use (including testing, hosting and linking to), copy, publicly perform, publicly display, reproduce in copies for distribution, and distribute the copies of any Interfacing Software made by you or with your assistance; provided, however, that you may notify Plex at legal@plex.tv if you do not wish for Plex to use, distribute, copy, publicly perform, publicly display, reproduce in copies for distribution, or distribute copies of an Interfacing Software that was created by you, and Plex will reasonable efforts to comply with such a request within a reasonable time.

# Installation

Follow the Manual Installation Instructions from [here](https://support.plex.tv/hc/en-us/articles/201187656-How-do-I-manually-install-a-channel-).
Such username can be found if you open a web page of a tunein user, for [this](http://tunein.com/user/adamchuk2168/) example the username is `adamchuk2168`.

# Listing of a user following stations

'My Stations' sections shows radio stations following by a user. You need to specify username in preferences to use this feature.

# Information for developer
* Requesting for a json with all station for a user: `curl 'http://tunein.com/profile/follows/?identifier=u159012873/follows/stations&type=&offset=20' -H 'x-requested-with: XMLHttpRequest'`
* [Example of a user profile page](http://tunein.com/user/adamchuk2168/)
* [Setting header to HTTP Request](http://thingsinjars.com/post/297/writing-a-plex-plugin-part-i/)
* [Persisting channel information](http://forums.plex.tv/discussion/88179/storing-user-data-in-dict)
