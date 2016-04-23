from celery import group
from django.conf import settings
from twitter import Api

from experience.celery import app
from twitterbot.models import Follower, RetweetUser


@app.task(bind=True)
def retweet(self):
    """ Retweet from twitter account provided earlier """
    api = Api(consumer_key=settings.CONSUMER_KEY, 
              consumer_secret=settings.CONSUMER_SECRET,
              access_token_key=settings.ACCESS_TOKEN_KEY, 
              access_token_secret=settings.ACCESS_TOKEN_SECRET)

    try:
        RetweetUser.objects.get()
    
        tweet = api.GetUserTimeline(screen_name='screen_name')[0]
        tweet.GetId()
        api.PostRetweet(tweet.GetId())
    except RetweetUser.DoesNotExist:
        pass
    except RetweetUser.MultipleObjectsReturned:
        pass


@app.task(bind=True)
def advertise(self):
    """ Create group with all tasks """
    followers = Follower.objects.all()
    tasks = [direct_message_follower.s(follower_id) for follower_id in followers]

    # create group with all tasks
    job = group(tasks)
    job.apply_async()


@app.task(bind=True)
def direct_message_follower(self, follower_id):
    """ Logs into api and post a direct tweet to the follower """
    api = Api(consumer_key=settings.CONSUMER_KEY, 
              consumer_secret=settings.CONSUMER_SECRET,
              access_token_key=settings.ACCESS_TOKEN_KEY, 
              access_token_secret=settings.ACCESS_TOKEN_SECRET)
    tweet = ('Time for some Java livestreams: https://www.livecoding.tv/username1, '
        'https://www.livecoding.tv/username2')
    
    api.PostDirectMessage(tweet, user_id=follower_id)

    return True