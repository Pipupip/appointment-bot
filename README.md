# Appointment Bot

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Aiogram-3.x-blueviolet?style=for-the-badge&logo=telegram" alt="Aiogram">
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite" alt="SQLite">
  <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" alt="License">
</p>

A Telegram bot for booking appointments in barbershops, tattoo studios, or any service-based business. Clients can choose a master, browse available time slots, and confirm reservations.

## Features

- Select a master and a specific service
- View free time slots in real time
- Confirm and manage bookings
- Automatic schedule updates
- Customer database with booking history
- FSM-based step-by-step booking flow

## Tech Stack

- **Python** 3.10+
- **Aiogram** 3.x
- **SQLite**
- **FSM** (Finite State Machine)

## Installation

```bash
git clone https://github.com/pipupip/appointment-bot
cd appointment-bot
pip install -r requirements.txt
```

## Configuration

Edit `config.py` and set your bot token and other parameters:

```python
BOT_TOKEN = "your-telegram-bot-token"
```

## Running

```bash
python bot.py
```

## Project Structure

```
bot_1_appointments/
├── bot.py              # Entry point
├── config.py           # Configuration
├── database.py         # Database layer
├── requirements.txt    # Dependencies
└── handlers/           # Bot message handlers
```

## Deployment

You can deploy the bot on any VPS or cloud platform (Railway, Render, etc.). Make sure to set the `BOT_TOKEN` environment variable in your deployment environment.

---

<p align="center">Built with ❤️ by <a href="https://github.com/pipupip">pipupip</a></p>
