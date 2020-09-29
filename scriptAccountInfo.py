from app.models import AccountInfo, FetchLog
from datetime import datetime
from app import db, getCreds
import os, requests, json, asyncio, aiohttp

params = getCreds()

bdurl = "https://graph.facebook.com/" + params['graph_version'] + "/" + params['instagram_account_id'] + \
        "?fields=business_discovery.username(" + params['ig_username'] + \
        "){username,website,name,ig_id,id,profile_picture_url,biography,follows_count,followers_count,media_count}&access_token=" + \
    params['access_token']

insighturl = "https://graph.facebook.com/" + \
    params['instagram_account_id'] + \
    "/insights?metric=follower_count,impressions,reach,profile_views&period=day&access_token=" + \
    params['access_token']
    
async def getAccountInfo(session):
    async with session.get(bdurl) as accountresponse:
        accountInfo = await accountresponse.json()

    async with session.get(insighturl) as insightresponse:
        dailyInsights = await insightresponse.json()

    now = datetime.utcnow()
    data = AccountInfo(now.date(), now.strftime("%H:%M:%S"), int(accountInfo['business_discovery']['follows_count']), int(accountInfo['business_discovery']['followers_count']), int(accountInfo['business_discovery']['media_count']), int(
        dailyInsights['data'][3]['values'][1]['value']), int(dailyInsights['data'][0]['values'][1]['value']), int(dailyInsights['data'][2]['values'][1]['value']), int(dailyInsights['data'][1]['values'][1]['value']), accountInfo['business_discovery']['profile_picture_url'], accountInfo['business_discovery']['biography'], accountInfo['business_discovery']['website'])

    db.session.add(data)
    db.session.commit()

    log = FetchLog(now, "Account Info")
    db.session.add(log)
    db.session.commit()

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [getAccountInfo(session)]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())