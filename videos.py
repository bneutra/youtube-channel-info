import os
import sys
import time

import googleapiclient.discovery
import googleapiclient.errors

# Note: Search results are constrained to a maximum of 500 videos if your request specifies
# a value for the channelId parameter and sets the type parameter value to video, 
# but it does not also set one of the forContentOwner, forDeveloper, or forMine filters.

# The request contains an invalid combination of search filters and/or restrictions. 
# Note that you must set the type parameter to video if you set either the forContentOwner or 
# forMine parameters to true.
# You must also set the type parameter to video if you set a value for the 
# eventType, videoCaption, videoCategoryId, videoDefinition, videoDimension, videoDuration, videoEmbeddable, videoLicense, videoSyndicated, or videoType parameters.


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
        print(f'iteration: {i}')
        request = youtube.search().list(
            part="snippet,id",
            # uncomment if you want to get your videos and they number more than 500
            #forMine=true,
            type='video',
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
            if not video_id:
                print(f'no video_id: {item}')
                continue
            # TODO: get more info?
            # https://developers.google.com/youtube/v3/docs/search#resource
            # is kind of lean, and the title and description are cut off
            this_record = [video_id]
            snippet = item.get('snippet')
            if not snippet:
                print(f'no snippit for video_id: {video_id}')
                continue
            if not snippet.get('title'):
                print(f'no title for video_id: {video_id}')
                continue

            for field in fields:
                this_record.append(snippet.get(field, ''))
            fh.write(','.join(this_record) + '\n')
        #breakpoint()
        if not next_page_token:
            print('done')
            fh.close()
            break

if __name__ == "__main__":
    api_key = os.environ.get('API_KEY')
    channel_id = sys.argv[1]
    main(channel_id, api_key)
