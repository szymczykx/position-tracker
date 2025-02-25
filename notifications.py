import requests
import logging
from config import NOTIFICATION_CONFIG

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def send_bark_notification(title, content):
    """发送通知到Bark应用"""
    try:
        bark_key = NOTIFICATION_CONFIG['bark_key']
        bark_url = NOTIFICATION_CONFIG['bark_url']
        group = NOTIFICATION_CONFIG['group']
        icon = NOTIFICATION_CONFIG['icon']
        
        url = f"{bark_url}/{bark_key}/{title}/{content}"
        params = {
            "group": group,
            "icon": icon
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            logger.info("成功发送Bark通知")
            return True
        else:
            logger.error(f"发送Bark通知失败: {response.status_code}, {response.text}")
            return False
    except Exception as e:
        logger.error(f"发送Bark通知时出错: {str(e)}")
        return False

def send_telegram_message(message):
    """发送消息到Telegram频道"""
    try:
        bot_token = NOTIFICATION_CONFIG.get('telegram_bot_token')
        chat_id = NOTIFICATION_CONFIG.get('telegram_chat_id')
        
        if not bot_token or not chat_id or bot_token == 'YOUR_BOT_TOKEN':
            logger.error("Telegram配置不完整，无法发送消息")
            return False
            
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        response = requests.post(url, data=data)
        if response.status_code == 200:
            logger.info("成功发送Telegram消息")
            return True
        else:
            logger.error(f"发送Telegram消息失败: {response.status_code}, {response.text}")
            return False
    except Exception as e:
        logger.error(f"发送Telegram消息时出错: {str(e)}")
        return False
