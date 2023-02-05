import os
import sys
import time

import googleapiclient.discovery
import googleapiclient.errors


def main(channel_id, api_key):

    api_service_name = "youtube"
    api_version = "v3"
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version,developerKey=api_key)
    next_page_token = ""
    max_iterations = 100 # just to be safe
    i = 0
    fh = open('output.txt', 'w')
    while i < max_iterations or next_page_token is None:
        i+=1
        request = youtube.search().list(
            part="snippet,id",
            channelId=channel_id,
            order="date",
            pageToken=next_page_token,
            maxResults=50 # max allowed
        )
        response = request.execute()
        next_page_token=response.get('nextPageToken')
        
        fields = [
            'publishedAt',
            'title',
            'description'
        ]
        for item in response.get('items'):
            video_id = item.get('id').get('videoId')
            # TODO: get more info?
            # https://developers.google.com/youtube/v3/docs/search#resource
            # is kind of lean, and the title and description are cut off
            this_record = [video_id]
            snippet = item.get('snippet')
            for field in fields:
                this_record.append(snippet.get(field))
            fh.write(','.join(this_record) + '\n')
        #breakpoint()
        if not next_page_token:
            print('done')
            fh.close()
            breakpoint()
            break

if __name__ == "__main__":
    api_key = os.environ.get('API_KEY')
    channel_id = sys.argv[1]
    main(channel_id, api_key)
