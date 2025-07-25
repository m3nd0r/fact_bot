# Fact Bot

A Telegram bot that sends daily interesting facts with images. The bot uses OpenAI Assistant API to generate facts and Unsplash API to find relevant images.

## Features

- 🤖 Automated daily fact delivery via Telegram
- 🧠 AI-powered fact generation using OpenAI Assistant
- 🖼️ Automatic image search and attachment using Unsplash
- ⏰ Configurable sending time
- 📝 Structured fact format with title and content

## Prerequisites

Before running the bot, you need to:

1. **Create an OpenAI Assistant** - This is required for fact generation
2. **Set up a Telegram Bot** - For message delivery
3. **Get an Unsplash API Key** - For image search

## Environment Variables

1. Copy the example environment file:
   ```bash
   cp .example.env .env
   ```

2. Edit `.env` file and fill in your actual values:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
ASSISTANT_ID=your_assistant_id_here

# Telegram Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Unsplash Configuration
UNSPLASH_API_KEY=your_unsplash_api_key_here

# Sending Schedule (optional, defaults to 13:00)
SEND_TIME_HOUR=13
SEND_TIME_MINUTE=0
```

### Required Variables

- `OPENAI_API_KEY` - Your OpenAI API key
- `ASSISTANT_ID` - ID of your OpenAI Assistant (see setup instructions below)
- `TELEGRAM_BOT_TOKEN` - Token from your Telegram bot (get from @BotFather)
- `TELEGRAM_CHAT_ID` - Chat ID where facts will be sent
- `UNSPLASH_API_KEY` - Your Unsplash API key

> 💡 The `.example.env` file contains helpful comments with links to get each API key.

### Optional Variables

- `SEND_TIME_HOUR` - Hour to send facts (0-23, default: 13)
- `SEND_TIME_MINUTE` - Minute to send facts (0-59, default: 0)

## Setup Instructions

### 1. Create OpenAI Assistant

You need to create an OpenAI Assistant that can generate facts. The assistant should:

- Respond to the prompt "Интересный факт на сегодня"
- Return JSON in the format:
  ```json
  {
    "title": "Russian title of the fact",
    "fact": "Detailed fact description in Russian",
    "title_en": "English title for image search"
  }
  ```
> 💡 The `title_en` field is used to search for an image on Unsplash. By default this bot is working with Russian language, but naming the image in English is important for the image search to work.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd fact_bot
   ```

2. Copy the example environment file:
   ```bash
   cp .example.env .env
   ```

3. Edit `.env` file with your actual API keys and settings

4. Install dependencies:
   ```bash
   # Using pip
   pip install -e .

   # Or using uv (recommended)
   uv sync
   ```

## Usage

Run the bot:

```bash
python main.py
```

The bot will:
1. Start the scheduler
2. Send facts daily at the configured time
3. Include relevant images when available
4. Handle graceful shutdown on Ctrl+C

## Docker

You can also run the bot using Docker:

```bash
docker-compose up -d
```

## Project Structure

- `main.py` - Entry point and scheduler setup
- `jobs.py` - Daily fact job implementation
- `assistant.py` - OpenAI Assistant interaction
- `telegram.py` - Telegram bot messaging
- `unsplash.py` - Image search functionality
- `config.py` - Environment configuration
- `utils.py` - Utility functions
- `logger.py` - Logging setup

## License

This project is open source and available under the MIT License.
