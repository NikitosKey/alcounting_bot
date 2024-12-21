[![code-quality](https://github.com/NikitosKey/alcounting_bot/actions/workflows/python-poetry-code-quality.yml/badge.svg)](https://github.com/NikitosKey/alcounting_bot/actions/workflows/python-poetry-code-quality.yml)

# Alcounting Telegram Bot

A bot designed to help manage parties and prevent organizers from going into the red.

## Table of Contents

- [Description](#description)
- [Guide](#Guide)
- [Documentation](#documentation)
- [Contributing](#contributing)

## Description

This bot is written in Python using the `python-telegram-bot` library.  
It offers a simple interface with buttons and a few commands.
Key features include:
- Ordering drinks, viewing the menu, and checking order statuses.
- Role-based access levels: Administrator, Bartender, and Customer.
- SQLite3 database integration.

## Guide
### How to install and run
#### Step 1: Create a Telegram Bot and Get the Token from @BotFather

1. Open the Telegram app and search for `@BotFather`.
2. Start a chat with `@BotFather` by clicking the "Start" button.
3. Use the command `/newbot` to create a new bot.
4. Follow the instructions to choose a name and username for your bot.
5. After successfully creating the bot, `@BotFather` will provide you with a token. This token is required to authenticate your bot and should be kept secure.

Example of the token provided by `@BotFather`:
```
123456789:ABCdefGhIJKlmNoPQRstuVWXyz
```

Save this token as you will need it to configure your bot in the next steps.

> **Note:** The token is sensitive information and should not be shared publicly.
#### Step 2: Set Up the Bot
First, you need to get repository on your local machine. You can do it by cloning the repository or downloading the zip file.
```shell
# Clone the repository


# Install Git from https://git-scm.com/downloads if you haven't already.
git clone git@github.com:NikitosKey/alcounting_bot.git
cd alcounting_bot
```
And get a token from the `@BotFather` in Telegram.

TODO: Add the instruction how to get the token.

##### Local Installation Native Method

```shell
# Install Python 3.13 if you haven't already.
# Visit https://www.python.org/downloads/ to download the latest version of Python.
# Or use your package manager to install it:

# Ubuntu
sudo apt-get install python3.13 

# macOS
# Install Homebrew from https://brew.sh/ if you haven't already.
brew install python3.13

# Windows
# Install Chocolatey from https://chocolatey.org/ if you haven't already.
choco install python3.13

# Install SQLite3 if you haven't already from https://www.sqlite.org/download.html or use your package manager:
# Ubuntu
sudo apt-get install sqlite3

# macOS
brew install sqlite3

# Windows
choco install sqlite3

# Install Poetry
# install pip if you haven't already from https://pip.pypa.io/en/stable/installation/.
pip install poetry
# This is sufficient to install dependencies, but for contributions,
# it's recommended to visit https://python-poetry.org/docs/ and follow their setup instructions.

# Install dependencies using Poetry (recommended for contributors)
poetry install

# Install dependencies using pip (alternative to Poetry)
# Create a virtual environment
python3.13 -m venv venv
# Activate the virtual environment
source venv/bin/activate
pip install -r requirements.txt

# Create an environment variable BOT_TOKEN and set it to your bot's token.
export BOT_TOKEN=your_token

# Run the bot
poetry run python bot/__main__.py

# For convenience, you can use screen or tmux to keep the bot running in the background:

# Using screen
screen -S alcounting_bot
poetry run python bot/__main__.py

# Using tmux
tmux new -s alcounting_bot
poetry run python bot/__main__.py
```

That's it!  
The bot will now run in the background, processing user requests.  
To stop the bot, press `Ctrl+C`.

##### Local Installation Docker-Compose Method
```shell
# Install Docker and Docker Compose from https://docs.docker.com/get-docker/ and https://docs.docker.com/compose/install/ if you haven't already.
docker-compose up --build
```

> To host the bot remotely instead of running it locally, you'll need to set up a hosting environment.

### How to use 
#### Step 1: Start the Bot
1. Open the Telegram app.
2. Search for your bot by its username.
3. Start a chat with the bot by clicking the "Start" button.

After receiving `/start` bot creates a database and sends a welcome message and your automatically get the role of the 
customer.

To use all the features of the bot, you need to change your role to administrator. To do this your need to install the 
SQLite browser and change the role in the database.

#### Step 2: Use the Bot
The bot supports the following commands:
1. `/start` - restart the bot.
2. `/help` - Display the help message.
3. `/menu` - Display the menu.

Menu consists of the following buttons:

TODO: Add the photos and the description of the buttons.

## Documentation

### Project Structure

- `bot/` - Bot folder
  - `handlers/` - Command handlers
  - `database/` - Database interactions
  - `users/` - User management
  - `__main__.py` - Bot entry point
- `data/` - Folder for the database
- `logs/` - Folder for logs
- `res/` - Folder for resources
- `startup_script/` - Scripts for starting the bot
- `tests/` - Folder for tests
- `.gitignore` - Ignored files
- `poetry.lock` - Poetry dependency lock file
- `pyproject.toml` - Poetry project configuration file
- `requirements.txt` - Dependencies for pip
- `README.md` - Project description

---

### Access Levels (+ Checklist)

#### **Customer**
Basic functionalities:
- [x] View the menu
- [x] Place orders
- [x] View their own orders
- [ ] Statistics

#### **Bartender**
Includes all Customer functionalities plus:
- [x] View the order queue
- [x] Confirm orders

#### **Administrator**
Includes all Bartender functionalities plus:
- [ ] Assign roles (Customer or Bartender)
- [ ] View logs
- [ ] Access various statistics
- [ ] Modify and edit the database
- [ ] Manage users

---

### Database

The database is located in `data/database.db` (git-ignored to prevent user data leaks) and is stored locally on the host.  

It uses SQLite and is managed through the `database.py` file.  

The database contains the following tables:
1. **Users**: Tracks user information and roles.
2. **Menu**: Contains bar items and pricing.
3. **Orders**: Tracks customer orders (used to generate the bartender's queue).

---

#### **Order Data**
Table structure:
- Order number (optional; currently using date and time instead)
- Product name (from the menu)
- Customer ID
- Bartender ID
- Order status
- Status change timestamps (optional, as there are only two statuses for now)

#### **Menu**
Table structure:
- Item name
- Description
- Price
- Tags (optional, for categorization if the menu becomes too large)

#### **User Data**
Table structure:
- User ID
- Username
- Access level (role)
- ...

---

### Party Management System (+ Checklist)

This feature will be implemented later. It is expected to include:
- [ ] Creating parties
- [ ] Inviting users
- [ ] Managing access to parties
- [ ] Joining an existing party

## Contributing
You can contribute to this project by creating a pull request or opening an issue. 
Also you can fork this repository and make your own version of the bot.


All contributions are welcome!
