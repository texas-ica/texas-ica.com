import os

from slackclient import SlackClient


SLACK_LOG_CHANNEL = 'C5H4CMGE6'


# Configure Swiper
client = SlackClient(os.getenv('SLACK_API_KEY'))


def log_event(ip, category, event, data=None):
    """
    Logs event to the Slack #logs channel as Swiper

    Arguments:
        ip - IP address of request
        category - Category of request
        event - Actual event
        data - Context of the event
    """

    message = '{} - {} - {}'.format(ip, category, event)

    if data:
        message = '{} - {}'.format(message, data)

    if client.rtm_connect():
        client.api_call(
            'chat.postMessage',
            channel=SLACK_LOG_CHANNEL,
            text=message,
            as_user=True
        )
