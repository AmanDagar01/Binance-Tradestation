from api.client import BinanceClient
from api.websocket import WebSocketClient
from utils.config import API_KEY, API_SECRET
import logging
from requests.exceptions import RequestException
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number")

def main():
    try:
        # Initialize the Binance client
        client = BinanceClient(API_KEY, API_SECRET)
        
        while True:
            try:
                print("\n1. Create Order")
                print("2. Cancel Order")
                print("3. View Orders")
                print("4. View Positions")
                print("5. Subscribe to Ticker")
                print("6. Exit")
                
                choice = input("\nEnter your choice (1-6): ")
                
                if choice == '1':
                    try:
                        symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
                        side = input("Enter side (BUY/SELL): ").upper()
                        if side not in ['BUY', 'SELL']:
                            raise ValueError("Invalid side. Must be BUY or SELL")
                        quantity = get_float_input("Enter quantity: ")
                        price = get_float_input("Enter price: ")
                        
                        response = client.create_order(symbol, side, "LIMIT", quantity, price)
                        logger.info(f"Order created: {response}")
                    except (ValueError, RequestException) as e:
                        logger.error(f"Error creating order: {str(e)}")
                        
                elif choice == '2':
                    try:
                        symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
                        order_id = input("Enter order ID: ")
                        response = client.cancel_order(symbol, order_id)
                        logger.info(f"Order cancelled: {response}")
                    except RequestException as e:
                        logger.error(f"Error cancelling order: {str(e)}")
                        
                elif choice == '3':
                    try:
                        symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
                        orders = client.view_orders(symbol)
                        logger.info(f"Current orders: {orders}")
                    except RequestException as e:
                        logger.error(f"Error viewing orders: {str(e)}")
                        
                elif choice == '4':
                    try:
                        positions = client.view_positions()
                        logger.info(f"Current positions: {positions}")
                    except RequestException as e:
                        logger.error(f"Error viewing positions: {str(e)}")
                        
                elif choice == '5':
                    try:
                        symbol = input("Enter symbol (e.g., BTCUSDT): ").lower()
                        duration = int(input("Enter duration in seconds: "))
                        if duration <= 0:
                            raise ValueError("Duration must be positive")
                        
                        ws_url = f"wss://stream.binance.com:9443/ws/{symbol}@ticker"
                        ws_client = WebSocketClient(ws_url)
                        ws_client.subscribe_ticker(symbol, duration)
                    except (ValueError, ConnectionError) as e:
                        logger.error(f"Error in websocket connection: {str(e)}")
                        
                elif choice == '6':
                    logger.info("Exiting...")
                    break
                    
                else:
                    logger.warning("Invalid choice! Please try again.")
                    
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                
    except Exception as e:
        logger.critical(f"Critical error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()