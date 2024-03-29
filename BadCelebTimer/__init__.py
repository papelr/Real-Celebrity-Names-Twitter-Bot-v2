# Packages
import os
import sys
import datetime
import logging
import azure.functions as func
from SharedCode import name_utils as dc
from SharedCode import twitter_utils as tu
from SharedCode import slack_utils as su
from SharedCode import random_name_gen_bot
from SharedCode import table_store as ts


# TimerTriger Function ----
def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    if mytimer.past_due:
        logging.info('The timer is past due!')
    logging.info('Python timer trigger function ran at %s', utc_timestamp)


    # CLASS instantiation: handles / Twitter ops / Slack ----
    name_handle_instance = dc.NameHandle()
    twitter_ops_instance = tu.TwitterOperations()
    slack_notifications = su.SlackNotifications()
    table_insertion = ts.TweetStorage()

    # Call random name generator script ----
    random_gen = random_name_gen_bot.name_gen()
    print(random_gen)

    # Pull in randomly choosen celeb name and twitter handle + sentence ----
    celeb_tweet = name_handle_instance.name_and_handle(random_gen)
    print(celeb_tweet)

    # Pull the handle only ----
    bare_handle = name_handle_instance.handle_only()
    print(bare_handle)

    # Get latest Tweet ID/Test from bare handle ----
    latest_id = twitter_ops_instance.get_tweet_id(bare_handle)
    print(latest_id)

    latest_text = twitter_ops_instance.get_tweet_text(bare_handle)
    print(latest_text)

    # Create hashtags (make this a function..) ----
    celeb_tweet = celeb_tweet + ' |  #' + bare_handle.replace('@', '') 
    celeb_tweet = celeb_tweet + ' #' + 'RealCelebrityNames'
    print(celeb_tweet)

    # Put Bot Timer Tweet into table
    bot_type = 'BadCelebTimer'
    insert_magic = table_insertion.create_entity_and_push(
        bare_handle, latest_id, latest_text, celeb_tweet, bot_type)
    print(insert_magic)  

    # Call twitter push script (with error handling & notifs) ----
    try:
        twitter_ops_instance.twit_push(celeb_tweet)
        slack_notifications.timeline_post_win()
    except:
        slack_notifications.timeline_post_loss()

