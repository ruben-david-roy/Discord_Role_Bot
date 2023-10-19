# Discord Role Bot

Discord Role Bot is a Discord bot that facilitates promoting and demoting users by manipulating roles. It is designed to be user-friendly and to do administrative tasks within a Discord server.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Bot Usage](#bot-usage)
- [License](#license)

## Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/DarkTwentyFive/Discord_Role_Bot.git
    cd Discord_Role_Bot
    ```

2. **Install the requirements**

   Before running the bot, make sure you've installed the necessary dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up `config.json`**

   Now, edit the `config.json` file to configure the `ROLE_ID`, `CHANNEL_ID`, and `PREFIX` according to your Discord server.

   <br>

   `ROLE_ID`: The role id of the Admins on the server.
   `CHANNEL_ID`: The channel id of the announcements channel where it will announce the promotions & demotions.
4. **Set up environment variables**

   Copy the provided `.env.example` to a new file named `.env`:
    ```bash
    cp .env.example .env
    ```

   Edit the `.env` file and replace `your_bot_token_here` with your actual bot token.
<br>
   NOTE: You don't need to wrap the token in quotes.

## Configuration

- **config.json**: Here you'll set the Discord-specific configurations.
  - `ROLE_ID`: The ID of the role required to use the promote/demote commands.
  - `CHANNEL_ID`: The ID of the channel where the bot will announce promotions/demotions.
  - `PREFIX`: The prefix for bot commands (e.g., `!`).

- **.env**: This file contains environment variables.
  - `BOT_TOKEN`: The token of your Discord bot. Remember, never share or expose this token.

## Bot Usage

1. **Run the bot**

   Execute the bot by running:
    ```bash
    python main.py
    ```

2. **Bot Commands**

   - `!promote`: This command allows users with the specified role to promote another user to a designated role. The bot will guide the user through the process via direct messages.
   
   - `!demote`: Similar to the `promote` command but demotes the user from a designated role.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for more information.

