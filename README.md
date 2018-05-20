# arbitrage

[![PyPI version](https://badge.fury.io/py/arbitrage.svg)](https://badge.fury.io/py/arbitrage)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Get current coin (btc/eth/xrp) ticker from exchanges (bitflyer/btcbox/zaif/bitbank/quoinex)


## Installation

    $ pip install arbitrage

## Usage

```python
import arbitrage

ticker = arbitrage.ticker()
print(ticker)
# {
# 	'btc': {
# 		'bitflyer': {'ask': 915466.0, 'bid': 915022.0, 'max': 0, 'min': 0},
# 		'btcbox': {'ask': 915499.0, 'bid': 913968.0, 'max': 0, 'min': 0},
# 		'zaif': {'ask': 915450.0, 'bid': 915400.0, 'max': 1, 'min': 0},
# 		'bitbank': {'ask': 915204.0, 'bid': 915171.0, 'max': 0, 'min': 0},
# 		'quoinex': {'ask': 914711.0, 'bid': 914358.97, 'max': 0, 'min': 1},
# 		'diff': {'ask': 'quoinex', 'bid': 'zaif', 'price': 689.0}
# 	},
# 	'eth': {
# 		'btcbox': {'ask': 78362.0, 'bid': 77986.0, 'max': 1, 'min': 0},
# 		'zaif': {'ask': 77965.0, 'bid': 77820.0, 'max': 0, 'min': 1},
# 		'quoinex': {'ask': 78290.0, 'bid': 77710.00001, 'max': 0, 'min': 0},
# 		'diff': {'ask': 'zaif', 'bid': 'btcbox', 'price': 21.0}
# 	},
# 	'xrp': {
# 		'bitbank': {'ask': 75.362, 'bid': 75.351, 'max': 1, 'min': 1},
# 		'quoinex': {'ask': 75.6704, 'bid': 75.12, 'max': 0, 'min': 0},
# 		'diff': {'ask': 'bitbank', 'bid': 'bitbank', 'price': -0.01099999999999568}
# 	}
# }


def exception_handler(request, exception):
	print('Request failed', exception)

ticker = arbitrage.ticker(timeout=30, exception_handler=exception_handler)
```

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request