
# Packages
import json
import sys
import os
import requests
from BadCelebTimer.all_keys import slackhook

# Twitter Post SUCCESS notification function ----
def post_worked():

    # slack hook set-up
    url = slackhook
    # message = ("Twitter Notification Bot")
    title = ("Tweet Posted Successfully!")

    # data sent to slack hook
    slack_data = {
        # "username": "Twitter Post SUCCESS",
        'icon_emoji' : ':thumbsup:',
        #"channel" : "#somerandomcahnnel",
        "attachments": [
            {
                "color": "#3DFB00", #color: bright green
                "fields": [
                    {
                        "title": title,
                        # "value": message,
                        "short": "false",
                    }

                    ]}]}

    # posting to slack
    byte_length = str(sys.getsizeof(slack_data))
    headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
    response = requests.post(url, data=json.dumps(slack_data), headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)

# Twitter Post FAILURE notification function ----
def post_failed():

    # slack hook set-up
    url = slackhook
    # message = ("Twitter Notification Bot")
    title = ("Tweet Post Failed!")

    # data sent to slack hook
    slack_data = {
        # "username": "Twitter Post SUCCESS",
        'icon_emoji' : ':thumbsdown:',
        #"channel" : "#somerandomcahnnel",
        "attachments": [
            {
                "color": "#FB1B00", #color: bright red
                "fields": [
                    {
                        "title": title,
                        # "value": message,
                        "short": "false",
                    }

                    ]}]}

    # posting to slack
    byte_length = str(sys.getsizeof(slack_data))
    headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
    response = requests.post(url, data=json.dumps(slack_data), headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)

# Main function ----
if __name__ == '__main__':
    post_worked()
    post_failed()




