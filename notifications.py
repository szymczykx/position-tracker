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
