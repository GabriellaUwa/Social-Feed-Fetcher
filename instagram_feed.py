"""
Fetches instagram feed using instagram_private_api library
"""
from datetime import datetime
from instagram_web_api import Client

def instagram_feed(user_handle=None, user_id=None):

    ret = []
    user_id = user_id #TODO:generate user_id given a user_handle
    web_api = Client(auto_patch=True, drop_incompat_keys=False)
    user_feed_info = web_api.user_feed(user_id, count=50) #gets fifty user feeds

    for feeds in user_feed_info:
        try:
            raw_item = feeds["node"]
            date = datetime.fromtimestamp(int(raw_item.get('taken_at_timestamp')))
            feed_info = {
                "provider": "instagram",
                "provider_handle": user_handle or '',
                "link": raw_item["link"] or '',
                "likes": raw_item["likes"]["count"] or 0,
                "media": [],
                "video_views": raw_item.get('video_view_count') or 0,
                "title": raw_item["edge_media_to_caption"]["edges"][0]["node"]["text"] or '',
                "description": raw_item["edge_media_to_caption"]["edges"][0]["node"]["text"] or '',
            }

            feed_info['pubDate'] = date.strftime('%a, %d %b %Y %H:%M:%S') + ' GMT'
            img_link = raw_item.get('display_src') or raw_item.get('thumbnail_src')
            if img_link:
                feed_info['media'].append(img_link)
            if raw_item["is_video"]:
                feed_info["videos"] = raw_item["display_url"]
                vid_link = feed_info["videos"]
                if vid_link:
                    feed_info['media'].append(vid_link)

            ret.append(feed_info)
        except:
            raise ("Could not get instagram feed or Feed does not exist")

    return ret

#TODO: give a more nicer output rather than print
id = 1067259270
user_handle="google"
print(instagram_feed(user_handle, id))
