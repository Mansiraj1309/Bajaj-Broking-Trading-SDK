# Bajaj Broking Trading SDK (Simulation)

## Overview
This project implements a simplified trading backend SDK simulating
core trading workflows like placing orders, viewing trades and portfolio.

## Tech Stack
- Python
- FastAPI
- In-memory storage

## Setup
pip install -r requirements.txt  
uvicorn app:app --reload

## APIs
- GET /api/v1/instruments
- POST /api/v1/orders
- GET /api/v1/orders/{orderId}
- GET /api/v1/trades
- GET /api/v1/portfolio

## Assumptions
- Single user system
- Market orders execute immediately
- One trade per order
- No real market integration

Swagger UI available at: http://127.0.0.1:8000/docs

<img width="1467" height="880" alt="image" src="https://github.com/user-attachments/assets/14cfa8f2-11f0-43b7-84f0-082ae1653437" />


