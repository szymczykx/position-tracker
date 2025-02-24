# Position Tracker

一个用于追踪币安期货跟单持仓信息的工具。

## 功能特点

- 实时监控指定交易员的持仓信息
- 数据本地存储，支持持久化
- 通过Bark进行消息推送通知
- 支持自动重试和错误处理

## 配置说明

在使用前，需要在`config.py`中设置以下配置：

```python
# 数据库配置
DB_CONFIG = {
    'path': 'positions.db',          # 数据库文件路径
    'retry_attempts': 3,             # 数据库操作重试次数
    'retry_delay': 1                 # 重试延迟（秒）
}

# API配置
API_CONFIG = {
    'base_url': 'API_BASE_URL',      # API基础URL
    'portfolio_id': 'YOUR_PORTFOLIO_ID',  # 投资组合ID
    'request_timeout': 10            # 请求超时时间（秒）
}

# 通知配置
NOTIFICATION_CONFIG = {
    'bark_key': 'YOUR_BARK_KEY',     # Bark推送密钥
    'bark_url': 'BARK_SERVER_URL',   # Bark服务器地址
    'group': 'GROUP_NAME',           # 消息分组
    'icon': 'ICON_URL'               # 通知图标URL
}

# 程序配置
APP_CONFIG = {
    'polling_interval': 2,           # 轮询间隔（秒）
    'max_retries': 3                 # 最大重试次数
}
```

## 使用方法

1. 安装依赖
```bash
pip install -r requirements.txt
```

2. 配置参数
复制 `config.py.example` 为 `config.py`，并填入你的配置信息。

3. 运行程序
```bash
python position_tracker.py
```

## 注意事项

- 请确保妥善保管API密钥等敏感信息
- 建议定期备份数据库文件
- 可以通过调整轮询间隔来控制请求频率