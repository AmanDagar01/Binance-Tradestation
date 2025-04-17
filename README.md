# Binance Trading Bot

This project is a Python application that interacts with the Binance API to manage trading operations. It allows users to create and cancel orders, view existing orders and positions, and subscribe to ticker updates for a specified duration.

## Features

- Create orders
- Cancel orders
- View orders
- View positions
- Subscribe to ticker updates

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/AmanDagar01/Binance-Tradestation.git
   cd binance-trading-bot
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python src/main.py
```

Follow the prompts to interact with the Binance API.

## Configuration

Before running the application, ensure that you have set up your API keys in the `src/utils/config.py` file.

### Creating Binance API Keys

1. Log in to your Binance account
2. Navigate to Profile → API Management
3. Click on [Create API]
4. Enter a label for your API key
5. Complete the security verification
6. Save your API Key and Secret Key immediately (you won't be able to see the Secret Key again)
7. Enable the following permissions:
   - Read Info
   - Spot & Margin Trading
   - Futures Trading (if needed)

### Setting Up API Keys in the Project

1. Locate the `src/utils/config.py` file
2. Replace the placeholder values with your actual API keys:
   ```python
   # src/utils/config.py
   API_KEY = "your_api_key_here"
   API_SECRET = "your_api_secret_here"
   ```
   
⚠️ **Security Notice**: 
- Never share your API keys with anyone
- Don't commit your actual API keys to version control
- Consider using environment variables for production use

## Running Tests

To run the unit tests for the BinanceClient class, use:
```
pytest tests/test_client.py
```
