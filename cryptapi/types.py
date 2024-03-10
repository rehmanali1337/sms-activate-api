from typing import Any, TypeAlias, Callable, Coroutine, TypedDict


GeneralDict: TypeAlias = dict[str, Any]


class PaymentDetails(TypedDict):
    uuid: str
    address_in: str
    address_out: str
    txid_in: str
    txid_out: str
    confirmations: int
    value_coin: float
    value_coin_convert: dict[str, str]
    value_forwarded_coin_convert: dict[str, str]
    fee_coin: float
    coin: str
    price: float
    pending: int
    user_id: str
    fee: float
    value: float
    value_forwarded: float
    value_forwarded_coin: float
    result: str


class GenerateWalletDetails(TypedDict):
    status: str
    address_in: str
    address_out: str
    callback_url: str
    minimum_transaction_coin: str
    priority: str


PaymentReceivedCallback: TypeAlias = Callable[
    [PaymentDetails], Coroutine[Any, Any, None]
]
