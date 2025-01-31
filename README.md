# Terabox Bot

A Telegram bot that allows users to save and watch Terabox videos through a Mini App interface.

## Features

- Save Terabox video URLs
- Watch videos through Telegram Mini App
- Track user statistics
- Admin commands for monitoring

## Tech Stack

- Python 3.9+
- python-telegram-bot
- MongoDB
- Flask (Mini App)

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/terabox-bot.git
cd terabox-bot
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Create a `.env` file with the following variables:
```env
BOT_TOKEN=your_telegram_bot_token
MONGODB_URI=your_mongodb_uri
MINI_APP_URL=your_mini_app_url
ADMIN_IDS=comma_separated_admin_ids
API_BASE=your_api_base_url
```

## Running the Bot

To start the bot:
```bash
python -m terabox_bot.main
```

## Deployment

### PythonAnywhere

1. Upload code to PythonAnywhere
2. Create a new virtual environment
3. Install dependencies
4. Set up environment variables
5. Create an "Always-on task" with the command:
```bash
python /path/to/terabox_bot/main.py
```

## Project Structure

```
terabox-bot/
├── README.md
├── requirements.txt
└── terabox_bot/
    ├── __init__.py
    ├── main.py
    ├── bot.py
    ├── config.py
    ├── database.py
    ├── handlers.py
    └── utils.py
```

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 