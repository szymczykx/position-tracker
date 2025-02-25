import json
import requests
import sqlite3
from datetime import datetime
import time
import logging
import os
from functools import wraps
from typing import List, Optional
from config import *
from models import Position

# 设置绝对路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'positions.db')

# 配置logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def retry_on_error(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    logger.warning(f"操作失败，{delay}秒后重试: {str(e)}")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_database()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_database(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS positions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                entry_price REAL,
                leverage INTEGER,
                position_side TEXT,
                break_even_price REAL,
                position_amount REAL,
                created_at TIMESTAMP
            )
            ''')
            conn.commit()

    @retry_on_error()
    def insert_positions(self, positions: List[Position]):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            for position in positions:
                data = position.to_dict()
                cursor.execute('''
                INSERT INTO positions (symbol, entry_price, leverage, position_side, 
                                    break_even_price, position_amount, created_at)
                VALUES (:symbol, :entry_price, :leverage, :position_side, 
                        :break_even_price, :position_amount, :created_at)
                ''', data)
            conn.commit()

    @retry_on_error()
    def get_active_positions(self) -> List[Position]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT * FROM positions WHERE position_amount != 0
            ORDER BY created_at DESC
            ''')
            rows = cursor.fetchall()
            positions = []
            for row in rows:
                row_dict = dict(zip([col[0] for col in cursor.description], row))
                if 'id' in row_dict:
                    del row_dict['id']
                positions.append(Position(**row_dict))
            return positions

    @retry_on_error()
    def close_position(self, symbol: str) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE positions SET position_amount = 0 WHERE symbol = ? AND position_amount != 0', (symbol,))
            affected = cursor.rowcount
            conn.commit()
            return affected
            
    @retry_on_error()
    def update_position_amount(self, symbol: str, position_amount: float) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE positions SET position_amount = ? WHERE symbol = ? AND position_amount != 0', 
                          (position_amount, symbol))
            affected = cursor.rowcount
            conn.commit()
            return affected

class PositionTracker:
    def __init__(self):
        self.db = DatabaseManager(DB_CONFIG['path'])
        self.url = f"{API_CONFIG['base_url']}?portfolioId={API_CONFIG['portfolio_id']}"

    @retry_on_error()
    def fetch_positions(self) -> List[Position]:
        response = requests.get(self.url, timeout=API_CONFIG['request_timeout'])
        logger.info(f"API请求状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            return [Position.from_api_data(pos) for pos in data['data'] if abs(float(pos['positionAmount'])) > 0]
        raise Exception(f"API请求失败: {response.status_code}")

    def send_notification(self, message: str):
        base_url = f"{NOTIFICATION_CONFIG['bark_url']}/{NOTIFICATION_CONFIG['bark_key']}/haywarPosition/"
        params = {
            "group": NOTIFICATION_CONFIG['group'],
            "icon": NOTIFICATION_CONFIG['icon'],
            "level": "critical",
            "volume": "5",
            "call": "1"
        }
        try:
            requests.get(base_url + message, params=params, timeout=5)
        except Exception as e:
            logger.error(f"发送通知失败: {str(e)}")

    def process_positions(self):
        try:
            current_positions = self.fetch_positions()
            active_positions = self.db.get_active_positions()
            
            # 构建当前持仓和活跃持仓的字典，方便比较
            current_positions_dict = {pos.symbol: pos for pos in current_positions}
            active_positions_dict = {pos.symbol: pos for pos in active_positions}
            
            # 处理已关闭的仓位
            current_symbols = set(current_positions_dict.keys())
            active_symbols = set(active_positions_dict.keys())
            
            for closed_symbol in active_symbols - current_symbols:
                self.db.close_position(closed_symbol)
                self.send_notification(
                    f"仓位已关闭：{closed_symbol}\n"
                    f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                )
            
            # 处理新开仓位
            new_positions = [pos for pos in current_positions 
                           if pos.symbol in (current_symbols - active_symbols)]
            
            if new_positions:
                self.db.insert_positions(new_positions)
                for pos in new_positions:
                    self.send_notification(
                        f"新建仓位\n"
                        f"交易对: {pos.symbol}\n"
                        f"开仓价格: {pos.entry_price}\n"
                        f"杠杆倍数: {pos.leverage}x\n"
                        f"方向: {pos.position_side}\n"
                        f"仓位大小: {pos.position_amount}\n"
                        f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    )
            
            # 处理仓位变动（加仓/减仓）
            for symbol in current_symbols & active_symbols:
                current_pos = current_positions_dict[symbol]
                active_pos = active_positions_dict[symbol]
                
                if abs(current_pos.position_amount) != abs(active_pos.position_amount):
                    old_amount = active_pos.position_amount
                    new_amount = current_pos.position_amount
                    change_type = "加仓" if abs(new_amount) > abs(old_amount) else "减仓"
                    
                    self.db.update_position_amount(symbol, new_amount)
                    self.send_notification(
                        f"{change_type}\n"
                        f"交易对: {symbol}\n"
                        f"变更前仓位: {old_amount}\n"
                        f"变更后仓位: {new_amount}\n"
                        f"开仓价格: {current_pos.entry_price}\n"
                        f"方向: {current_pos.position_side}\n"
                        f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    )
        
        except Exception as e:
            logger.error(f"处理持仓数据时出错: {str(e)}", exc_info=True)

def main():
    tracker = PositionTracker()
    logger.info("开始监控持仓数据...")
    
    while True:
        try:
            tracker.process_positions()
            time.sleep(APP_CONFIG['polling_interval'])
        except KeyboardInterrupt:
            logger.info("程序已停止")
            break
        except Exception as e:
            logger.error(f"发生错误: {str(e)}", exc_info=True)
            time.sleep(APP_CONFIG['polling_interval'])

if __name__ == "__main__":
    main()
