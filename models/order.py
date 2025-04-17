class Order:
    def __init__(self, order_id, symbol, quantity, price):
        self.order_id = order_id
        self.symbol = symbol
        self.quantity = quantity
        self.price = price

    def __repr__(self):
        return f"Order(order_id={self.order_id}, symbol={self.symbol}, quantity={self.quantity}, price={self.price})"