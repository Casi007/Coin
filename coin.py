import sys
import typing
from dataclasses import dataclass, field, fields
from functools import wraps

from pycoingecko import CoinGeckoAPI

MARKET_INFO = typing.List[typing.Dict[str, typing.Any]]


@dataclass
class Coin:
    id: str = field()
    name: str = field()
    current_price: int = field()
    high_24h: int = field()
    symbol: str = field()
    price_change_24h: float = field()
    price_change_percentage_24h: float = field()


def print_try_wrapper(
    start_msg: str,
    exc_msg: str,
):
    """
    Wraps around a callable to print fancy progress texts before the call,
    and bubbles up wrapped exceptions.
    """

    def wrapper(func):
        @wraps(func)
        def runner(*args, **kwargs):
            print(start_msg + "... ", end="")
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                print("FAIL")
                raise Exception(exc_msg) from exc
            finally:
                print("OK")

        return runner

    return wrapper


@print_try_wrapper(
    start_msg="Checking connection to CoinGecko API",
    exc_msg="Failed to connect to Coin Gecko API",
)
def check_api(gecko: CoinGeckoAPI) -> None:
    """
    Verifies we have a connection to Gecko API
    """
    gecko.ping()


@print_try_wrapper(
    start_msg="Getting list of known coins", exc_msg="Failed to get list of known coins"
)
def get_coin_ids(
    gecko: CoinGeckoAPI, coins_to_retrieve: typing.List[str]
) -> typing.Dict[str, str]:
    """
    Returns static coin info.

    Note: this call could be avoided entirely.
    """
    return {
        coin["symbol"]: coin["id"]
        for coin in gecko.get_coins_list()
        if coin["symbol"] in coins_to_retrieve
    }


@print_try_wrapper(start_msg="Getting market info", exc_msg="Failed to get market info")
def get_market_info(gecko: CoinGeckoAPI, ids: str) -> MARKET_INFO:
    """
    Returns dynamic coin info.
    """
    return gecko.get_coins_markets("eur", ids=ids)


def translate_market_info_to_coin_objects(
    market_info: MARKET_INFO,
) -> typing.List[Coin]:
    """
    Creates Coin dataclasses based on defined fields.
    """
    known_fields = fields(Coin)
    return [
        Coin(**{kf.name: coin_info[kf.name] for kf in known_fields})
        for coin_info in market_info
    ]


def main() -> int:
    """
    Main application function.

    Returns exit code.
    """
    # Make it so that we can pass the list of coins we want as command line arguments
    coins_to_retrieve: typing.List[str] = sys.argv[1:] or ["link", "btc", "eth"]
    print("Will retrieve: ", coins_to_retrieve)

    gecko = CoinGeckoAPI()
    check_api(gecko)
    coin_ids = get_coin_ids(gecko, coins_to_retrieve)
    if not coin_ids:
        print("Zero coin ID retrieved; is the symbol list correct?")
        return -1

    print(
        "Retrieved coin IDs:\n\t", "\n\t".join(f"{k}: {v}" for k, v in coin_ids.items())
    )
    market_info = get_market_info(gecko, ",".join(coin_ids.values()))
    coins = translate_market_info_to_coin_objects(market_info)
    for coin in coins:
        print(coin)
    return 0


# Entry point
if __name__ == "__main__":
    sys.exit(main())
