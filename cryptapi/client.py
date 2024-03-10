from typing import Any, Optional, cast
import aiohttp

from cryptapi.enums import TransactionPriority
from cryptapi.types import GeneralDict, GenerateWalletDetails


class CryptAPIClient:
    def __init__(self) -> None:
        self.base_url = "https://api.cryptapi.io"
        self._session = aiohttp.ClientSession()

    def _params_to_str(self, params: GeneralDict) -> str:
        q: str = ""
        for k, v in params.items():
            if not q:
                q = f"{k}={v}"
                continue
            q = f"{q}&{k}={v}"

        return q

    async def _request(
        self, path: str, query_params: dict[str, Any], method: str = "GET"
    ) -> dict[str, Any]:
        url = self.base_url + path + f"?{self._params_to_str(query_params)}"
        async with self._session.request(method=method, url=url) as resp:
            await resp.read()

        return await resp.json()

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()

    async def generate_wallet(
        self,
        ticker: str,
        forward_to_wallet: str,
        callback_url: str,
        email: Optional[str] = None,
        post: int = 0,
        confirmations: int = 3,
        multi_token: int = 0,
        multi_chain: int = 0,
        convert: int = 0,
        priority: str = TransactionPriority.DEFAULT,
    ) -> GenerateWalletDetails:
        path = f"/{ticker}/create"
        query = {
            "callback": callback_url,
            "address": forward_to_wallet,
            "pending": "0",
            "confirmations": confirmations,
            "email": email,
            "post": post,
            "priority": priority,
            "multi_token": multi_token,
            "multi_chain": multi_chain,
            "convert": convert,
        }
        resp = await self._request(path, query)
        return cast(GenerateWalletDetails, resp)
