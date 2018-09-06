#!/usr/bin/python
# -*- coding: UTF-8 -*-

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import socks
import socket

DEVELOPER_KEY = 'AIzaSyC2D1q0RmS7zv1557sdddevG8qxXzLCt9k'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


def youtube_search(options):
    socks.setdefaultproxy(socks.PROXY_TYPE_HTTP, "127.0.0.1", 1087)
    socket.socket = socks.socksocket

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)
    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=options['q'],
        part='id,snippet',
        maxResults=options['max_results']
        ).execute()

    videos = []
    channels = []
    playlists = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get('items', []):
        print search_result
        if search_result['id']['kind'] == 'youtube#video':
          videos.append('%s (%s)' % (search_result['snippet']['title'],
                                     search_result['id']['videoId']))
        elif search_result['id']['kind'] == 'youtube#channel':
          channels.append('%s (%s)' % (search_result['snippet']['title'],
                                       search_result['id']['channelId']))
        elif search_result['id']['kind'] == 'youtube#playlist':
          playlists.append('%s (%s)' % (search_result['snippet']['title'],
                                        search_result['id']['playlistId']))

    print 'Videos:\n', '\n'.join(videos), '\n'
    print 'Channels:\n', '\n'.join(channels), '\n'
    print 'Playlists:\n', '\n'.join(playlists), '\n'


if __name__ == '__main__':
    args = {'q': '娱乐', 'max_results': 20}
    try:
        youtube_search(args)
    except HttpError, e:
        print 'An HTTP error %d occurred:\n%s' % (e.resp.status, e.content)