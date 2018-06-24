# https://stackoverflow.com/questions/15512239/python-get-all-youtube-video-urls-of-a-channel
# modified the above to work in Python 3 with the following
# https://stackoverflow.com/questions/3969726/attributeerror-module-object-has-no-attribute-urlopen

# Before it only works with "channels"
# used https://stackoverflow.com/questions/23978328/how-to-retrieve-youtube-channel-id-based-on-user-url-api-v3-0
# so that it works for "users" as well
# (basically users got renamed to channels so it makes working with the YouTube API a little more complciated)

import urllib
import json
import subprocess
import sys
from urllib.request import urlopen

def get_all_video_in_channel(channel_id, value):
    """
    channel_id can be both a user or channel,
    i.e. youtube.com/user/______  or youtube.com/channel/_______

    value can either be "channel" or "user"

    If "user" is selected, a script will run to convert the user to
    the corresponding channel_id

    """

    api_key = sys.argv[1]
    value = sys.argv[3]
    if value == "user":

        tmp = "https://www.googleapis.com/youtube/v3/channels?part=id&forUsername={}&key={}".format(channel_id, api_key)
        inp = urlopen(tmp)
        resp = json.load(inp)
        channel_id = [x for x in resp['items']][0]['id']
        
    base_video_url = 'https://www.youtube.com/watch?v='
    base_search_url = 'https://www.googleapis.com/youtube/v3/search?'

    first_url = base_search_url+'key={}&channelId={}&part=snippet,id&order=date&maxResults=25'.format(api_key, channel_id)
    
    video_links = []
    url = first_url
    while True:
        inp = urlopen(url)
        resp = json.load(inp)

        for i in resp['items']:
            if i['id']['kind'] == "youtube#video":
                video_links.append(base_video_url + i['id']['videoId'])

        try:
            next_page_token = resp['nextPageToken']
            url = first_url + '&pageToken={}'.format(next_page_token)
        except:
            break
    return video_links


videos = get_all_video_in_channel(sys.argv[2], sys.argv[3])

for video in videos:    
    print(video)

