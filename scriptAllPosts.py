from app.models import AllPosts
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

allpostsurl = "https://graph.facebook.com/" + params['graph_version'] + "/" + params['instagram_account_id'] + \
    "/media?fields=id,caption,media_type,media_url,permalink,timestamp,comments_count,like_count,thumbnail_url&limit=500&access_token=" + \
    params['access_token']

async def getAllPosts(session):
    async with session.get(allpostsurl) as response:
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

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [getAllPosts(session)]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())