from django.conf import settings
from twitter import Api, TwitterError

from twitterbot.models import Follower, RetweetUser
from utils.decorators import render_to


@render_to('twitterbot.html')
def index(request):
    exceeded_error = False
    if request.method == 'POST':
        api = Api(consumer_key=settings.CONSUMER_KEY, 
                  consumer_secret=settings.CONSUMER_SECRET,
                  access_token_key=settings.ACCESS_TOKEN_KEY, 
                  access_token_secret=settings.ACCESS_TOKEN_SECRET)

        account = request.POST.get('account')
        RetweetUser.objects.all().delete()
        RetweetUser.objects.create(screen_name=account)

        try:
            followers = api.GetFollowers(account)
            for follower in followers:
                follower_id = follower.GetId()
                Follower.objects.update_or_create(follower_id=follower_id, 
                    followers=follower.GetFollowersCount())

                api.CreateFriendship(follower_id)
        except TwitterError as e:
            if e.message[0]['code'] == 88:
                exceeded_error = True

    return {'followers': Follower.objects.all()[:20], 
        'exceeded_error': exceeded_error}

