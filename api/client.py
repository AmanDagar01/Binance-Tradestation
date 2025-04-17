import time
import hmac
import hashlib
import requests
import logging
from urllib.parse import urlencode
from utils.config import BASE_URL, TIMEOUT
from requests.exceptions import RequestException, Timeout

logger = logging.getLogger(__name__)

class BinanceAPIError(Exception):
    pass

class BinanceClient:
    def __init__(self, api_key, api_secret):
        if not api_key or not api_secret:
            raise ValueError("API key and secret are required")
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = BASE_URL

    def _generate_signature(self, params):
        try:
            query_string = urlencode(params)
            signature = hmac.new(
                self.api_secret.encode('utf-8'),
                query_string.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            return signature
        except Exception as e:
            logger.error(f"Error generating signature: {str(e)}")
            raise BinanceAPIError("Failed to generate signature")

    def _send_signed_request(self, method, endpoint, params=None):
        try:
            if params is None:
                params = {}
                
            params['timestamp'] = int(time.time() * 1000)
            params['signature'] = self._generate_signature(params)
            
            headers = {
                'X-MBX-APIKEY': self.api_key
            }
            
            url = f"{self.base_url}{endpoint}"
            
            try:
                if method == "GET":
                    response = requests.get(url, headers=headers, params=params, timeout=TIMEOUT)
                elif method == "POST":
                    response = requests.post(url, headers=headers, params=params, timeout=TIMEOUT)
                elif method == "DELETE":
                    response = requests.delete(url, headers=headers, params=params, timeout=TIMEOUT)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                response.raise_for_status()
                return response.json()
                
            except Timeout:
                raise BinanceAPIError("Request timed out")
            except requests.exceptions.HTTPError as e:
                error_msg = response.json().get('msg', str(e))
                raise BinanceAPIError(f"HTTP error occurred: {error_msg}")
                
        except Exception as e:
            logger.error(f"Error in API request: {str(e)}")
            raise BinanceAPIError(f"API request failed: {str(e)}")

    def create_order(self, symbol, side, order_type, quantity, price):
        try:
            if not all([symbol, side, order_type, quantity, price]):
                raise ValueError("All order parameters are required")
            
            endpoint = '/api/v3/order'
            params = {
                'symbol': symbol,
                'side': side,
                'type': order_type,
                'quantity': quantity,
                'price': price,
                'timeInForce': 'GTC'
            }
            return self._send_signed_request('POST', endpoint, params)
        except Exception as e:
            logger.error(f"Error creating order: {str(e)}")
            raise BinanceAPIError(f"Failed to create order: {str(e)}")

    def cancel_order(self, symbol, order_id):
        try:
            if not all([symbol, order_id]):
                raise ValueError("Symbol and order ID are required")
            
            endpoint = '/api/v3/order'
            params = {
                'symbol': symbol,
                'orderId': order_id
            }
            return self._send_signed_request('DELETE', endpoint, params)
        except Exception as e:
            logger.error(f"Error canceling order: {str(e)}")
            raise BinanceAPIError(f"Failed to cancel order: {str(e)}")

    def view_orders(self, symbol):
        try:
            if not symbol:
                raise ValueError("Symbol is required")
            
            endpoint = '/api/v3/openOrders'
            params = {
                'symbol': symbol
            }
            return self._send_signed_request('GET', endpoint, params)
        except Exception as e:
            logger.error(f"Error viewing orders: {str(e)}")
            raise BinanceAPIError(f"Failed to view orders: {str(e)}")

    def view_positions(self):
        try:
            endpoint = '/api/v3/account'
            return self._send_signed_request('GET', endpoint)
        except Exception as e:
            logger.error(f"Error viewing positions: {str(e)}")
            raise BinanceAPIError(f"Failed to view positions: {str(e)}")