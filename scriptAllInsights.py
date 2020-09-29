from app.models import AllPosts, FetchLog
from datetime import datetime
from app import db, getCreds
import os, requests, json, asyncio, aiohttp

params = getCreds()

async def getAllInsights(session):
    query = db.session.query(
        AllPosts.post_id, AllPosts.media_type).order_by(AllPosts.id).all()
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

    log = FetchLog(datetime.utcnow(), "All Insights")
    db.session.add(log)
    db.session.commit()

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [getAllInsights(session)]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())