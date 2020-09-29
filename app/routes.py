from flask import render_template, flash, redirect, request, Response, url_for
from app import app, db
from app.models import DailyFetch, AccountInfo, AllPosts, AllStories, Webhooks, FetchLog
from datetime import datetime, timedelta, date

import os, asyncio

import scriptAccountInfo as fetchInfo
import scriptRecentInsights as fetchRecentPosts
import scriptAllInsights as fetchAllPosts

today = date.today()
now = datetime.today().time()
dailyStatsCutoff = now.replace(hour=7, minute=00, second=00)
if (now < dailyStatsCutoff):
    yesterday = today - timedelta(days=2)
    print("two")
else:
    yesterday = today - timedelta(days=1)
    print("one")

@app.route('/')
@app.route('/index')
def index():

    latestInfo = AccountInfo.query.order_by(AccountInfo.date.desc(), AccountInfo.time.desc()).first()
    recentInsights = AllPosts.query.order_by(AllPosts.timestamp.desc()).limit(10).all()
    recentHooks = Webhooks.query.order_by(Webhooks.timestamp.desc()).limit(6).all()
    yesterdaystats = DailyFetch.query.filter(DailyFetch.date == yesterday).first()
        
    return render_template('index.html', 
        bd=latestInfo, 
        recentInsights=recentInsights,
        recentUpdates = recentHooks,
        yesterdayStats = yesterdaystats,
        message=request.args.get('message'), 
        alerttype=request.args.get('alerttype'),
        title='Home'
    )

@app.route('/allposts/')
def allposts():

        allPosts = AllPosts.query.order_by(AllPosts.timestamp.desc()).all()
        return render_template('allposts.html', 
            allPosts=allPosts,
            message=request.args.get('message'), 
            alerttype=request.args.get('alerttype'),
            title='Posts'
        )

@app.route('/allstory/')
def allstory():

    allStory = AllStories.query.order_by(AllStories.timestamp.desc()).all()
    return render_template('allstory.html', 
        allStory=allStory,
        title='Story'
    )

@app.route('/dailystats/')
def dailystats():

    dailyStats = DailyFetch.query.order_by(DailyFetch.date.desc(), DailyFetch.time.desc()).all()
    return render_template('dailystats.html', 
        daily=dailyStats,
        title='Daily Stats'
    )

messageAlert = ""
alertType = ""

@app.route('/fetchdata/')
def fetchdata():
    latestdaily = FetchLog.query.filter(FetchLog.fetch_type == 'Account Info').order_by(FetchLog.timestamp.desc()).first()
    latestrecent = FetchLog.query.filter(FetchLog.fetch_type == 'Recent Insights').order_by(FetchLog.timestamp.desc()).first()
    latestall = FetchLog.query.filter(FetchLog.fetch_type == 'All Insights').order_by(FetchLog.timestamp.desc()).first()
    return render_template('fetch.html',
        title='Fetch',
        latestdaily = latestdaily,
        latestrecent = latestrecent,
        latestall = latestall,
        message=request.args.get('message'), 
        alerttype=request.args.get('alerttype')
    )

@app.route('/fetch_account_info/')
def fetchaccountinfo():
    try:
        asyncio.run(fetchInfo.main())
        messageAlert = "Successfully fetched latest account information and daily insights."
        alertType = "success"
    except:
        messageAlert = "Failed to fetch."
        alertType = "warning"
        db.session.rollback()

    return redirect(url_for('fetchdata', message=messageAlert, alerttype=alertType))

@app.route('/fetch_recent/')
def fetchrecentinsights():
    try:
        asyncio.run(fetchRecentPosts.main())
        messageAlert = "Successfully fetched recent posts and their insights."
        alertType = "success"
    except:
        messageAlert = "Failed to fetch."
        alertType = "warning"
        db.session.rollback()

    return redirect(url_for('fetchdata', message=messageAlert, alerttype=alertType))

@app.route('/fetch_all/')
def fetchallinsights():
    try:
        asyncio.run(fetchAllPosts.main())
        messageAlert = "Successfully fetched all posts and their latest insights."
        alertType = "success"
    except:
        messageAlert = "Failed to fetch."
        alertType = "warning"
        db.session.rollback()

    return redirect(url_for('fetchdata', message=messageAlert, alerttype=alertType))

@app.route('/webhook', methods=['POST', 'GET'])
def respond():

    challenge = request.args.get('hub.challenge', '')
    if challenge:
        return challenge
    else:
        print('-----------')
        response = request.json
        for entry in response['entry']:
            time = datetime.utcnow()
            contentReceived = entry['changes'][0]['field']
            print(entry['changes'][0]['value'])

            if contentReceived == 'comments':
                comment_id = entry['changes'][0]['value']['id']
                text = entry['changes'][0]['value']['text']
                data = Webhooks(dt, "Comment", comment_id, text, 0,0)

                try:
                    db.session.add(data)
                    db.session.commit()
                    print('Successful webhook')
                except:
                    db.session.rollback()
                    print('Failed webhook')

            elif contentReceived == 'mentions':
                comment_id = entry['changes'][0]['value']['comment_id']
                media_id = entry['changes'][0]['value']['media_id']
                data = Webhooks(dt, "Mention", comment_id, "", media_id,0)

                try:
                    db.session.add(data)
                    db.session.commit()
                    print('Successful webhook')
                except:
                    db.session.rollback()
                    print('Failed webhook')

            elif contentReceived == 'story_insights':
                media_id = entry['changes'][0]['value']['media_id']
                impressions = entry['changes'][0]['value']['impressions']
                reach = entry['changes'][0]['value']['reach']
                taps_forward = entry['changes'][0]['value']['taps_forward']
                taps_back = entry['changes'][0]['value']['taps_back']
                exits = entry['changes'][0]['value']['exits']
                replies = entry['changes'][0]['value']['replies']
                
                try:
                    data = AllStories(media_id, dt, impressions, reach, taps_forward, taps_back,
                                exits, replies)  
                    db.session.add(data)
                    db.session.commit()
                    data = Webhooks(dt, "Story", 0, "", 0, media_id)
                    db.session.add(data)
                    db.session.commit()
                    print('Successful webhook')
                except:
                    db.session.rollback()
                    print('Failed webhook')                

            else:
                print("Unknown received.")

        print('-----------')
        return Response(status=200)
        
@app.errorhandler(404)
def errorpage(error):
    return render_template('error.html', title='404'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error.html', title='500'), 500