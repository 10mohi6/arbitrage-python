# arbitrage

[![PyPI version](https://badge.fury.io/py/arbitrage.svg)](https://badge.fury.io/py/arbitrage)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Get current coin (btc/eth/xrp) ticker from exchanges (bitflyer/btcbox/zaif/bitbank/quoinex)


## Installation

    $ pip install arbitrage

## Usage

```python
#
# sync
#
from arbitrage import Arbitrage

arbitrage = Arbitrage()
ticker = arbitrage.get_ticker()
print(ticker)
# {
#   "btc": {
#     "bitflyer": {"ask": 923717.0,"bid": 923175.0},
#     "btcbox": {"ask": 924397.0,"bid": 922298.0},
#     "zaif": {"ask": 922605.0,"bid": 922445.0},
#     "bitbank": {"ask": 922904.0,"bid": 922495.0},
#     "quoinex": {"ask": 921706.83,"bid": 921414.31}
#   },
#   "eth": {
#     "bitflyer": {"ask": 78700.6884,"bid": 78608.35125},
#     "btcbox": {"ask": 78919.0,"bid": 78509.0},
#     "zaif": {"ask": 78670.0,"bid": 78650.0},
#     "bitbank": {"ask": 79084.64972536,"bid": 77950.8459499},
#     "quoinex": {"ask": 79356.93999,"bid": 78400.01001}
#   },
#   "xrp": {
#     "bitbank": {"ask": 77.219,"bid": 77.171},
#     "quoinex": {"ask": 76.9898,"bid": 75.881}
#   }
# }


arbitrage = Arbitrage(timeout = 30, exception_handler = exception_handler)

def exception_handler(request, exception):
	print('Request failed', exception)
```

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request