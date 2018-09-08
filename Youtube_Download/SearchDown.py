# -*- coding: utf-8 -*-
#
import configparser
from tkinter import *
import configparser
import os

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import socks
import socket
from you_get import common




class Gui(object):
    def __init__(self):
        config = configparser.ConfigParser()
        config.readfp(open(os.path.join(os.path.dirname(__file__), "config.ini")))
        self.dev_key = config.get("YOUTUBE", "DEVELOPER_KEY")
        self.api_name = config.get("YOUTUBE", "YOUTUBE_API_SERVICE_NAME")
        self.api_version = config.get("YOUTUBE", "YOUTUBE_API_VERSION")
        self.proxy_host = config.get("YOUTUBE", "PROXY_HOST")
        self.proxy_port = int(config.get("YOUTUBE", "PROXY_PORT"))
        self.max_results = 2

    def down_result(self, TkWindow):
        print("getResult")

    def click_1(self):
        print("111")

    def click_2(self):
        print("22")

    def click_3(self):
        print("33")

    def initWindow(self):
        TkWindow = Tk()
        TkWindow.title("Search Youtube Video...")
        TkWindow.geometry('1280x720')

        # 添加一个label、entry、button和message到frame2
        TkFrame = Frame(TkWindow)
        TkFrame.pack()
        searchLabel = Label(TkFrame, text="请输入关键词")
        searchLabel.grid(row=0, column=0)
        searchInput = Entry(TkFrame)
        searchInput.grid(row=0, column=1)
        searchButton = Button(TkFrame, text="搜索",
                              command=lambda: self.show_result(TkWindow=TkWindow, searchWord=searchInput.get()))
        searchButton.grid(row=0, column=2)
        spLabel = Label(TkFrame, text="---------------------------------------------------------------------")
        spLabel.grid(row=1, column=0)
        return TkWindow, TkFrame

    def show_result(self, TkWindow, searchWord):
        # 多选框
        getData = self.youtube_search(searchWord)

        con_frame = Frame(TkWindow)
        con_frame.pack()
        # v = []
        i = 0
        for search_result in getData.get('items', []):
            print(search_result)
            if search_result['id']['kind'] == 'youtube#video':
                # v[i] = IntVar()
                ck = Checkbutton(con_frame, text=search_result['snippet']['title'],
                                 variable=search_result['id']['videoId'], command=self.click_1)
                ck.grid(row=i + 1, sticky=W)
                # videos.append('%s (%s)' % (search_result['snippet']['title'],
                #                            search_result['id']['videoId']))
                i = i + 1
            else:
                pass
        DownloadButton = Button(con_frame, text="下载所选", command=lambda: self.down_result(TkWindow=TkWindow))
        DownloadButton.grid(row=i + 1)

    def youtube_search(self, searchWord):
        socks.setdefaultproxy(socks.PROXY_TYPE_HTTP, self.proxy_host, self.proxy_port)
        socket.socket = socks.socksocket
        youtube = build(self.api_name, self.api_version,
                        developerKey=self.dev_key)
        # Call the search.list method to retrieve results matching the specified
        # query term.
        search_response = youtube.search().list(
            q=searchWord,
            part='id,snippet',
            maxResults=self.max_results
        ).execute()

        return search_response

        # videos = []
        # channels = []
        # playlists = []
        #
        # # Add each result to the appropriate list, and then display the lists of
        # # matching videos, channels, and playlists.
        # for search_result in search_response.get('items', []):
        #     # print search_result
        #     if search_result['id']['kind'] == 'youtube#video':
        #         videos.append('%s (%s)' % (search_result['snippet']['title'],
        #                                    search_result['id']['videoId']))
        #     elif search_result['id']['kind'] == 'youtube#channel':
        #         channels.append('%s (%s)' % (search_result['snippet']['title'],
        #                                      search_result['id']['channelId']))
        #     elif search_result['id']['kind'] == 'youtube#playlist':
        #         playlists.append('%s (%s)' % (search_result['snippet']['title'],
        #                                       search_result['id']['playlistId']))
        #
        # print('Videos:\n', '\n'.join(videos), '\n')
        # print('Channels:\n', '\n'.join(channels), '\n')
        # print('Playlists:\n', '\n'.join(playlists), '\n')

    def download(self,url,savepath):
        # common.any_download(url=url, stream_id='mp4', info_only=False, output_dir=r('%s' % savepath), merge=True)
        pass

if __name__ == '__main__':
    window, frame = Gui().initWindow()
    # Gui().show_result(frame)
    window.mainloop()


