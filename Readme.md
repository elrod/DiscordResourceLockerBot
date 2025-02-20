# Resource Lock Bot

A Discord bot to manage shared resource locking and unlocking across multiple servers using slash commands.

## Features
- Add, remove, lock, and unlock resources.
- Track which user has locked a resource.
- Supports multiple servers with separate resource tracking.
- Uses JSON files for persistent storage.

## Installation

### 1. Clone the repository
```sh
git clone https://github.com/your-repo/resource-lock-bot.git
cd resource-lock-bot
```

### 2. Create a virtual environment and install dependencies
```sh
python -m venv .venv
source .venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Create an `.env` file
Create a `.env` file in the project root and add the following:
```
APP_TOKEN=your_discord_bot_token
RES_DIR=path_to_resource_directory
```
Replace `your_discord_bot_token` with your actual bot token and `path_to_resource_directory` with the folder where resource data should be stored.

## Setting Up the Bot on Discord

### 1. Create a Discord Application
- Go to [Discord Developer Portal](https://discord.com/developers/applications)
- Click "New Application" and give it a name
- Navigate to "Bot" section and click "Add Bot"
- Copy the bot token and add it to `.env` as `APP_TOKEN`

### 2. Invite the Bot to Your Server
- Navigate to "OAuth2" → "URL Generator"
- Under "Scopes", select `bot` and `applications.commands`
- Under "Bot Permissions", select:
  - `Read Messages`
  - `Send Messages`
  - `Use Slash Commands`
  - `Manage Messages` (optional)
- Copy the generated URL and open it in your browser to invite the bot.

## Running the Bot
```sh
python bot.py
```
The bot will sync slash commands and be ready to use.

## Usage
Use the following slash commands:

- `/res_list` - List all resources and their status.
- `/res_add <resource>` - Add a new resource.
- `/res_remove <resource>` - Remove a resource.
- `/res_lock <resource>` - Lock a resource if available.
- `/res_unlock <resource>` - Unlock a resource (only if you locked it).
- `/res_status <resource>` - Check the status of a resource.

## License
MIT License

