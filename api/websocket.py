import websocket
import json
import threading
import time
import logging

logger = logging.getLogger(__name__)

class WebSocketError(Exception):
    pass

class WebSocketClient:
    def __init__(self, url):
        if not url:
            raise ValueError("WebSocket URL is required")
        self.url = url
        self.ws = None
        self.keep_running = True

    def on_message(self, ws, message):
        try:
            data = json.loads(message)
            logger.info(f"Received message: {data}")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse message: {str(e)}")

    def on_error(self, ws, error):
        logger.error(f"WebSocket error: {str(error)}")
        self.keep_running = False

    def on_close(self, ws, close_status_code, close_msg):
        logger.info(f"WebSocket closed. Status code: {close_status_code}, Message: {close_msg}")
        self.keep_running = False

    def on_open(self, ws):
        logger.info("WebSocket connection opened")

    def subscribe_ticker(self, symbol, duration):
        if duration <= 0:
            raise ValueError("Duration must be positive")

        def run():
            try:
                websocket.enableTrace(True)
                self.ws = websocket.WebSocketApp(
                    self.url,
                    on_message=self.on_message,
                    on_error=self.on_error,
                    on_close=self.on_close
                )
                self.ws.on_open = self.on_open
                self.ws.run_forever()
            except Exception as e:
                logger.error(f"WebSocket connection failed: {str(e)}")
                raise WebSocketError(f"Failed to establish WebSocket connection: {str(e)}")

        try:
            thread = threading.Thread(target=run)
            thread.start()

            time.sleep(duration)
            self.keep_running = False
            if self.ws:
                self.ws.close()
            thread.join(timeout=5)  # Wait up to 5 seconds for thread to finish
            
            if thread.is_alive():
                logger.warning("WebSocket thread did not terminate properly")
                
        except Exception as e:
            logger.error(f"Error in WebSocket operation: {str(e)}")
            raise WebSocketError(f"WebSocket operation failed: {str(e)}")