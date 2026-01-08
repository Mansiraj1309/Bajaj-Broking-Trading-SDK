from fastapi import FastAPI, HTTPException
from models import OrderRequest
from storage import instruments, orders, trades, portfolio
import uuid

app = FastAPI(title="Bajaj Broking Trading SDK")

USER_ID = "USER_1"


@app.get("/api/v1/instruments")
def get_instruments():
    return instruments


@app.post("/api/v1/orders")
def place_order(order: OrderRequest):

    if order.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")

    instrument = next((i for i in instruments if i["symbol"] == order.symbol), None)
    if not instrument:
        raise HTTPException(status_code=404, detail="Instrument not found")

    if order.orderStyle == "LIMIT" and order.price is None:
        raise HTTPException(status_code=400, detail="Price required for LIMIT order")

    order_id = str(uuid.uuid4())

    orders[order_id] = {
        "orderId": order_id,
        "symbol": order.symbol,
        "quantity": order.quantity,
        "orderType": order.orderType,
        "status": "EXECUTED"
    }

    trade_price = instrument["lastTradedPrice"]
    trade_id = str(uuid.uuid4())

    trades.append({
        "tradeId": trade_id,
        "orderId": order_id,
        "symbol": order.symbol,
        "price": trade_price,
        "quantity": order.quantity
    })

    # Update portfolio
    holding = portfolio.get(order.symbol, {
        "symbol": order.symbol,
        "quantity": 0,
        "averagePrice": 0
    })

    total_qty = holding["quantity"] + order.quantity
    holding["averagePrice"] = (
        (holding["averagePrice"] * holding["quantity"]) +
        (trade_price * order.quantity)
    ) / total_qty

    holding["quantity"] = total_qty
    portfolio[order.symbol] = holding

    return {"orderId": order_id, "status": "EXECUTED"}


@app.get("/api/v1/orders/{order_id}")
def get_order(order_id: str):
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders[order_id]


@app.get("/api/v1/trades")
def get_trades():
    return trades


@app.get("/api/v1/portfolio")
def get_portfolio():
    result = []
    for symbol, data in portfolio.items():
        instrument = next(i for i in instruments if i["symbol"] == symbol)
        current_value = data["quantity"] * instrument["lastTradedPrice"]

        result.append({
            "symbol": symbol,
            "quantity": data["quantity"],
            "averagePrice": data["averagePrice"],
            "currentValue": current_value
        })
    return result

@app.get("/")
def health():
    return {"status": "Trading SDK is running"}
