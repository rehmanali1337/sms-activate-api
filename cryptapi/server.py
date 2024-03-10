import asyncio
import json
from typing import Optional
from fastapi import FastAPI, Response
import uvicorn
from cryptapi.types import PaymentDetails, PaymentReceivedCallback


class PaymentServer:

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        on_payment_received: PaymentReceivedCallback,
        payment_pending_callback: Optional[PaymentReceivedCallback] = None,
    ) -> None:
        self.loop = loop
        self.app = FastAPI()
        """Setup the server"""
        self.on_payment_received = on_payment_received
        self.app.add_api_route("/payment_received", self.payment_received)

    async def payment_received(
        self,
        user_id: str,
        address_in: str,
        address_out: str,
        uuid: str,
        confirmations: int,
        txid_in: str,
        txid_out: str,
        fee: float,
        fee_coin: float,
        value: float,
        value_coin: float,
        value_forwarded: float,
        value_forwarded_coin: float,
        coin: str,
        price: float,
        result: str,
        pending: int,
        value_coin_convert: str,
        value_forwarded_coin_convert: str,
    ) -> Response:
        print("Payment received callback is being called ...")
        payment_details: PaymentDetails = {
            "address_in": address_in,
            "address_out": address_out,
            "coin": coin,
            "confirmations": confirmations,
            "fee_coin": fee_coin,
            "pending": pending,
            "price": price,
            "txid_in": txid_in,
            "txid_out": txid_out,
            "uuid": uuid,
            "value_coin": value_coin,
            "fee": fee,
            "result": result,
            "user_id": user_id,
            "value": value,
            "value_forwarded": value_forwarded,
            "value_forwarded_coin": value_forwarded_coin,
            "value_coin_convert": json.loads(value_coin_convert),
            "value_forwarded_coin_convert": json.loads(value_forwarded_coin_convert),
        }
        self.loop.create_task(self.on_payment_received(payment_details))
        return Response(content=json.dumps({"message": "success"}))

    async def run(self, host: str = "0.0.0.0", port: int = 9000) -> None:
        def _run() -> None:
            print("Running the payment callback server ...")
            uvicorn.run(self.app, host=host, port=port)

        await self.loop.run_in_executor(None, lambda: _run())
