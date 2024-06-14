# Wrong Bot

Wrong Bot is a Discord bot designed to manage leveling and rewards within a Discord server. It allows users to gain experience points (XP) and level up by participating in server activities. Upon reaching certain levels, users are awarded roles and level-up messages are sent to a specific channel.

## Features

- **Leveling System:** Users gain XP by sending messages. XP is capped to prevent spamming.
- **Role Rewards:** Users are assigned roles when they reach certain levels.
- **Daily Rewards:** Users can claim daily XP rewards.
- **Level-Up Messages:** Level-up messages are sent to a specific channel.
- **Leaderboard:** Displays the top users by XP.

## Requirements

- Python 3.8+
- discord.py
- aiosqlite

## Setup

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/wrong-bot.git
    cd wrong-bot
    ```

2. **Install dependencies:**

    ```sh
    pip install discord.py aiosqlite
    ```

3. **Configure the bot:**

    Replace the placeholders in `bot.py` with your own values:
    - `YOUR_BOT_TOKEN` with your Discord bot token.
    - `ROLE_ID_1`, `ROLE_ID_2`, etc. with the role IDs for level rewards.
    - `YOUR_CHANNEL_ID` with the channel ID for level-up messages.

4. **Run the bot:**

    ```sh
    python bot.py
    ```

## Usage

### Commands

- `!level [@member]`: Check the level and XP of yourself or another member.
- `!leaderboard`: Display the top users by XP.
- `!daily`: Claim your daily XP reward.

### Example

1. **Check your level:**

    ```sh
    !level
    ```

    Output:
    ```
    @User is at level 3 with 250 XP.
    ```

2. **Check another member's level:**

    ```sh
    !level @AnotherUser
    ```

    Output:
    ```
    @AnotherUser is at level 5 with 600 XP.
    ```

3. **View the leaderboard:**

    ```sh
    !leaderboard
    ```

    Output:
    ```
    **Leaderboard:**
    1. @TopUser: Level 10, 1500 XP
    2. @SecondUser: Level 9, 1300 XP
    ...
    ```

4. **Claim your daily reward:**

    ```sh
    !daily
    ```

    Output:
    ```
    @User, you have claimed your daily reward of 50 XP!
    ```

## Contributing

1. **Fork the repository.**
2. **Create a new branch:**

    ```sh
    git checkout -b my-feature
    ```

3. **Make your changes.**
4. **Commit your changes:**

    ```sh
    git commit -am 'Add new feature'
    ```

5. **Push to the branch:**

    ```sh
    git push origin my-feature
    ```

6. **Create a new Pull Request.**

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
