# Position Tracker

一个用于追踪币安期货跟单持仓信息的实时监控工具。支持多渠道通知，让您随时掌握仓位变化。

## 功能

- 实时监控指定交易员的持仓信息
- 自动检测新开仓位、平仓和仓位大小变化
- 支持Bark应用通知（iOS用户）
- 支持Telegram机器人通知

## 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/yourusername/position-tracker.git
cd position-tracker
```

2. 配置参数
```bash
cp config.py.example config.py
# 编辑config.py并填入您的配置信息
```

3. 运行程序
```bash
python position_tracker.py
```

## 使用manager.sh管理脚本

`manager.sh` 是一个方便的脚本，用于管理和运行Position Tracker。以下是一些常用的命令：

- 启动服务：
  ```bash
  ./manager.sh start
  ```

- 停止服务：
  ```bash
  ./manager.sh stop
  ```

- 查看服务状态：
  ```bash
  ./manager.sh status
  ```

- 查看日志：
  ```bash
  ./manager.sh logs
  ```

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
    # Bark配置
    'bark_key': 'YOUR_BARK_KEY',     # Bark推送密钥
    'bark_url': 'BARK_SERVER_URL',   # Bark服务器地址
    'group': 'GROUP_NAME',           # 消息分组
    'icon': 'ICON_URL',              # 通知图标URL
    
    # Telegram配置
    'telegram_bot_token': 'YOUR_TELEGRAM_BOT_TOKEN',  # 从BotFather获取的机器人Token
    'telegram_chat_id': 'YOUR_TELEGRAM_CHAT_ID'       # 频道ID或聊天ID
}

# 程序配置
APP_CONFIG = {
    'polling_interval': 2,           # 轮询间隔（秒）
    'max_retries': 3                 # 最大重试次数
}
```

## Telegram机器人设置

1. 在Telegram中搜索 [@BotFather](https://t.me/BotFather)
2. 发送 `/newbot` 指令创建一个新机器人
3. 按照提示设置机器人名称和用户名
4. 获取机器人Token并填入配置文件
5. 将机器人添加到您的群组或频道中
6. 获取聊天ID或频道ID并填入配置文件

## 通知类型

程序会在以下情况发送通知：

- **新建仓位**：当检测到新的交易仓位时
- **平仓**：当已有的仓位被平掉时
- **加仓/减仓**：当仓位大小发生变化时

## 许可证

MIT License