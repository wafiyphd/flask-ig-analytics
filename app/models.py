from app import db

class DailyFetch(db.Model):
    __tablename__ = 'DailyFetch'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, index=True)
    time = db.Column(db.Time, index=True)
    numFollowing = db.Column(db.Integer)
    numFollowers = db.Column(db.Integer)
    numPosts = db.Column(db.Integer)
    numDailyVisits = db.Column(db.Integer)
    numDailyFollowers = db.Column(db.Integer)
    numDailyReach = db.Column(db.Integer)
    numDailyImpressions = db.Column(db.Integer)

    def __init__(self, date, time, numFollowing, numFollowers, numPosts, numDailyVisits, numDailyFollowers, numDailyReach, numDailyImpressions):
        self.date = date
        self.time = time
        self.numFollowing = numFollowing
        self.numFollowers = numFollowers
        self.numPosts = numPosts
        self.numDailyVisits = numDailyVisits
        self.numDailyFollowers = numDailyFollowers
        self.numDailyReach = numDailyReach
        self.numDailyImpressions = numDailyImpressions
    
    def __repr__(self):
        return '<DailyFetch {}>'.format(str(self.id))
        
class AccountInfo(db.Model):
    __tablename__ = 'AccountInfo'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, index=True)
    time = db.Column(db.Time, index=True)
    numFollowing = db.Column(db.Integer)
    numFollowers = db.Column(db.Integer)
    numPosts = db.Column(db.Integer)
    numDailyVisits = db.Column(db.Integer)
    numDailyFollowers = db.Column(db.Integer)
    numDailyReach = db.Column(db.Integer)
    numDailyImpressions = db.Column(db.Integer)
    profilePictureUrl = db.Column(db.Text())
    biography = db.Column(db.Text())
    website = db.Column(db.String(50))

    def __init__(self, date, time, numFollowing, numFollowers, numPosts, numDailyVisits, numDailyFollowers, numDailyReach, numDailyImpressions, picurl, biography, website):
        self.date = date
        self.time = time
        self.numFollowing = numFollowing
        self.numFollowers = numFollowers
        self.numPosts = numPosts
        self.numDailyVisits = numDailyVisits
        self.numDailyFollowers = numDailyFollowers
        self.numDailyReach = numDailyReach
        self.numDailyImpressions = numDailyImpressions
        self.profilePictureUrl = picurl
        self.biography = biography
        self.website = website

    def __repr__(self):
        return '<AccountInfo {}>'.format(str(self.id))

class AllPosts(db.Model):
    __tablename__ = 'AllPosts'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Numeric(30,0), index=True, unique=True)
    timestamp = db.Column(db.DateTime, index=True)
    media_type = db.Column(db.String(20))
    category = db.Column(db.String(20))
    permalink = db.Column(db.String(100))
    count_comments = db.Column(db.Integer)
    count_like = db.Column(db.Integer)
    count_engagement = db.Column(db.Integer)
    count_impressions = db.Column(db.Integer)
    count_reach = db.Column(db.Integer)
    count_saved = db.Column(db.Integer)
    count_video_views = db.Column(db.Integer)
    media_url = db.Column(db.Text())
    thumbnail_url = db.Column(db.Text())
    caption = db.Column(db.Text())

    def __init__(self, postid, timestamp, mediatype, category, permalink, numcomment, numlike, numengagement, numimpression, numreach, numsaved, numvideoviews, mediaurl, thumbnailurl, caption):
        self.post_id = postid
        self.timestamp = timestamp
        self.media_type = mediatype
        self.category = category
        self.permalink = permalink
        self.count_comments = numcomment
        self.count_like = numlike
        self.count_engagement = numengagement
        self.count_impressions = numimpression
        self.count_reach = numreach
        self.count_saved = numsaved
        self.count_video_views = numvideoviews
        self.media_url = mediaurl
        self.thumbnail_url = thumbnailurl
        self.caption = caption

    def __repr__(self):
        return '<AllPosts {}>'.format(str(self.post_id))

class AllStories(db.Model):
    __tablename__ = 'AllStories'
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Numeric(30,0), index=True)
    timestamp = db.Column(db.DateTime, index=True)
    count_impressions = db.Column(db.Integer)
    count_reach = db.Column(db.Integer)
    count_tapsforward = db.Column(db.Integer)
    count_tapsback = db.Column(db.Integer)
    count_exits = db.Column(db.Integer)
    count_replies = db.Column(db.Integer)

    def __init__(self, storyid, timestamp, impressions, reach, tapsforward, tapsback, exits, replies):
        self.story_id = storyid
        self.timestamp = timestamp
        self.count_impressions = impressions
        self.count_reach = reach
        self.count_tapsforward = tapsforward
        self.count_tapsback = tapsback
        self.count_exits = exits
        self.count_replies = replies

    def __repr__(self):
        return '<AllPosts {}>'.format(str(self.story_id))

class Webhooks(db.Model):
    __tablename__ = 'Webhooks'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True)
    hook_type = db.Column(db.String(20))
    comment_id = db.Column(db.Numeric(30,0))
    comment_text = db.Column(db.Text())
    media_id = db.Column(db.Numeric(30,0))
    story_id = db.Column(db.Numeric(30,0))

    def __init__(self, timestamp, hooktype, commentid, commenttext, mediaid, storyid):
        self.timestamp = timestamp
        self.hook_type = hooktype
        self.comment_id = commentid
        self.comment_text = commenttext
        self.media_id = mediaid
        self.story_id = storyid

    def __repr__(self):
        return '<Webhooks {}>'.format(self.hook_type)

class FetchLog(db.Model):
    __tablename__ = 'FetchLog'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True)
    fetch_type = db.Column(db.String(20))

    def __init__(self, timestamp, fetchtype):
        self.timestamp = timestamp
        self.fetch_type = fetchtype

    def __repr__(self):
        return '<LatestFetch {}>'.format(str(self.id))