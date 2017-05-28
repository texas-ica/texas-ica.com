import os
import datetime

from slackclient import SlackClient


SLACK_LOG_CHANNEL = 'C5H4CMGE6'


# Configure Swiper
client = SlackClient(os.getenv('SLACK_API_KEY'))


def log_event(ip, message):
    """
    Logs event to the Slack #logs channel as Swiper

    Arguments:
        ip - IP address of request
        message - Description of event
    """

    time = datetime.datetime.now().strftime('%m/%d %H:%M')
    text = '{} - {} - {}'.format(ip, time, message)

    if client.rtm_connect():
        client.api_call(
            'chat.postMessage',
            channel=SLACK_LOG_CHANNEL,
            text=text,
            as_user=True
        )
