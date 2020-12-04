from app.models import AllPosts, FetchLog
from datetime import datetime
from app import db, getCreds
import os, requests, json, asyncio, aiohttp

def getCategory(caption):

    caption = caption.lower()

    if "#memoriannounce" in caption:
        return "Announcement"
    elif "memorivid" in caption:
        return "Video"
    elif "#voteformemori" in caption:
        return "Voting"
    elif "#askmemori" in caption:
        return "FAQ"
    elif "#memoriforyou" in caption:
        return "Photo"
    elif "#thanksforthememori" in caption:
        return "TY"
    elif "#memoridyk" in caption:
        return "DYK"
    elif "#memoriquote" in caption:
        return "Quote"
    elif "#memorigreets" in caption:
        return "Greetings"
    elif "#memoriteaser" in caption:
        return "Teaser"
    elif "#memoriworkshopdate" in caption:
        return "Workshop Date"
    elif "#mtwmemori" in caption:
        return "Mtw"
    elif "#memoriblog" in caption:
        return "Blog"
    elif "#mlegacyplanningtips" in caption:
        return "LP Tip"
    elif "#memoriwantsyou" in caption:
        return "Hiring"
    elif "#mind2care" in caption:
        return "M2C"
    elif "#lmno" in caption:
        return "LMNO"
    elif "#choice" in caption:
        return "Filler"
    elif "#tipsfrommemori" in caption:
        return "Tips"
    else:
        return "N/A"
        
params = getCreds()

recentpostsurl = "https://graph.facebook.com/" + params['graph_version'] + "/" + params['instagram_account_id'] + \
    "/media?fields=id,caption,media_type,media_url,permalink,timestamp,comments_count,like_count,thumbnail_url&limit=10&access_token=" + \
    params['access_token']

async def getRecentPosts(session):
    async with session.get(recentpostsurl) as response:
        json_response = await response.json()

        for post in json_response['data']:

            media_url = "N/A"
            thumbnail_url = "N/A"

            strdate = (post["timestamp"])[:10]
            strtime = (post["timestamp"])[11:19]
            strdatetime = strdate + " " + strtime
            dt = datetime.strptime(strdatetime, "%Y-%m-%d %H:%M:%S")

            post_id = post["id"]
            post_link = post["permalink"]
            post_type = post["media_type"]
            post_category = getCategory(post["caption"])
            num_likes = post["like_count"]
            num_comments = post["comments_count"]
            post_caption = post["caption"]

            thumbnailfetchurl = "https://graph.facebook.com/" + params['graph_version'] + "/instagram_oembed?url=" + post_link + "&maxwidth=320&fields=thumbnail_url%2Cauthor_name%2Cprovider_name%2Cprovider_url&access_token=" + params['access_token']
            async with session.get(thumbnailfetchurl) as response:
                json_response = await response.json()
                thumbnail_url= json_response["thumbnail_url"];

            if db.session.query(AllPosts).filter(AllPosts.post_id == post_id).count() == 0:
                data = AllPosts(post_id, dt, post_type, post_category, post_link,
                                num_comments, num_likes, 0, 0, 0, 0, 0, media_url, thumbnail_url, post_caption)
                db.session.add(data)
                db.session.commit()
            else:
                db.session.query(AllPosts).filter(AllPosts.post_id == post_id).update({
                    AllPosts.thumbnail_url: thumbnail_url,
                    AllPosts.count_comments: num_comments,
                    AllPosts.count_like: num_likes,
                    AllPosts.category: post_category,
                    AllPosts.caption: post_caption
                })
                db.session.commit()


async def getRecentPostsInsights(session):
    query = db.session.query(AllPosts.post_id, AllPosts.media_type).order_by(
        AllPosts.timestamp.desc()).limit(10).all()
    for post in query:
        params['latest_media_id'] = str(post[0])
        if post[1] == 'CAROUSEL_ALBUM':
            params['metric'] = 'carousel_album_engagement,carousel_album_impressions,carousel_album_reach,carousel_album_saved'
        elif post[1] == 'VIDEO':
            params['metric'] = 'engagement,impressions,reach,saved,video_views'
        else:
            params['metric'] = 'engagement,impressions,reach,saved'

        postinsighturl = "https://graph.facebook.com/" + \
            params['graph_version'] + "/" + params['latest_media_id'] + "/insights?metric=" + \
            params['metric'] + "&access_token=" + params['access_token']

        async with session.get(postinsighturl) as response:
            json_response = await response.json()
            db.session.query(AllPosts).filter(AllPosts.post_id == post[0]).update({
                AllPosts.count_engagement: json_response['data'][0]['values'][0]['value'],
                AllPosts.count_impressions: json_response['data'][1]['values'][0]['value'],
                AllPosts.count_reach: json_response['data'][2]['values'][0]['value'],
                AllPosts.count_saved: json_response['data'][3]['values'][0]['value']
            })
            db.session.commit()
            if post[1] == 'VIDEO':
                db.session.query(AllPosts).filter(AllPosts.post_id == post[0]).update({
                    AllPosts.count_video_views: json_response['data'][4]['values'][0]['value']
                })
                db.session.commit()
    
    log = FetchLog(datetime.utcnow(), "Recent Insights")
    db.session.add(log)
    db.session.commit()


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [getRecentPosts(session)]
        await asyncio.gather(*tasks)

    async with aiohttp.ClientSession() as session:
        tasks = [getRecentPostsInsights(session)]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())