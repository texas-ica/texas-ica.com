import os
import logging

from slackclient import SlackClient


SLACK_LOG_CHANNEL = 'C5H4CMGE6'


# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_path = os.path.join(parent, 'logger', 'ica.log')

handler = logging.FileHandler(log_path)
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)

logger.addHandler(handler)

# Configure Swiper
client = SlackClient(os.getenv('SLACK_API_KEY'))


def log_event(ip, category, event, data=None):
    message = '{} - {} - {}'.format(ip, category, event)

    if data:
        message = '{} - {}'.format(message, data)

    logger.info(message)

    """
    if client.rtm_connect():
        client.api_call(
            'chat.postMessage',
            channel=SLACK_LOG_CHANNEL,
            text=message,
            as_user=True
        )
    """
