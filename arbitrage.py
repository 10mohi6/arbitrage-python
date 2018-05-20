# coding: utf-8
import grequests

__all__ = ['ticker']

class Arbitrage:

	def __init__(self, timeout, exception_handler):
		self.ticker = {
			'btc' : {
				'bitflyer' : {'ask': 0, 'bid': 0, 'max': 0, 'min': 0},
				'btcbox' : {'ask': 0, 'bid': 0, 'max': 0, 'min': 0},
				'zaif' : {'ask': 0, 'bid': 0, 'max': 0, 'min': 0},
				'bitbank' : {'ask': 0, 'bid': 0, 'max': 0, 'min': 0},
				'quoinex' : {'ask': 0, 'bid': 0, 'max': 0, 'min': 0},
				'diff' : {'ask': '', 'bid': '', 'price': 0}
			},
			'eth' : {
				'btcbox' : {'ask': 0, 'bid': 0, 'max': 0, 'min': 0},
				'zaif' : {'ask': 0, 'bid': 0, 'max': 0, 'min': 0},
				'quoinex' : {'ask': 0, 'bid': 0, 'max': 0, 'min': 0},
				'diff' : {'ask': '', 'bid': '', 'price': 0}
			},
			'xrp' : {
				'bitbank' : {'ask': 0, 'bid': 0, 'max': 0, 'min': 0},
				'quoinex' : {'ask': 0, 'bid': 0, 'max': 0, 'min': 0},
				'diff' : {'ask': '', 'bid': '', 'price': 0}
			}
		}
		self.timeout = timeout
		self.exception_handler = exception_handler

	def get_ticker(self):
		reqs = [
			self._get_ticker_bitflyer({'product_code': 'BTC_JPY'}),
			self._get_ticker_btcbox({'coin': 'btc'}),
			self._get_ticker_btcbox({'coin': 'eth'}),
			self._get_ticker_zaif({'coin': 'btc_jpy'}),
			self._get_ticker_zaif({'coin': 'eth_jpy'}),
			self._get_ticker_bitbank({'pair': 'btc_jpy'}),
			self._get_ticker_bitbank({'pair': 'xrp_jpy'}),
			self._get_ticker_quoinex({'id': '5'}),
			self._get_ticker_quoinex({'id': '29'}),
			self._get_ticker_quoinex({'id': '83'})
		]
		grequests.map(reqs, exception_handler=self.exception_handler)
		price, ask, bid = self._get_ticker_diff('btc', ['bitflyer', 'btcbox', 'zaif', 'bitbank', 'quoinex'])
		self.ticker['btc'][ask]['min'] = 1
		self.ticker['btc'][bid]['max'] = 1
		self.ticker['btc']['diff']['ask'] = ask
		self.ticker['btc']['diff']['bid'] = bid
		self.ticker['btc']['diff']['price'] = price
		price, ask, bid = self._get_ticker_diff('eth', ['btcbox', 'zaif', 'quoinex'])
		self.ticker['eth'][ask]['min'] = 1
		self.ticker['eth'][bid]['max'] = 1
		self.ticker['eth']['diff']['ask'] = ask
		self.ticker['eth']['diff']['bid'] = bid
		self.ticker['eth']['diff']['price'] = price
		price, ask, bid = self._get_ticker_diff('xrp', ['bitbank', 'quoinex'])
		self.ticker['xrp'][ask]['min'] = 1
		self.ticker['xrp'][bid]['max'] = 1
		self.ticker['xrp']['diff']['ask'] = ask
		self.ticker['xrp']['diff']['bid'] = bid
		self.ticker['xrp']['diff']['price'] = price
		return self.ticker

	def _get_ticker_diff(self, coin, exchanges):
		ask = 10000000
		bid = 0
		ask_exc = ''
		bid_exc = ''
		for exc in exchanges:
			if self.ticker[coin][exc]['ask'] < ask:
				ask = self.ticker[coin][exc]['ask']
				ask_exc = exc
			if self.ticker[coin][exc]['bid'] > bid:
				bid = self.ticker[coin][exc]['bid']
				bid_exc = exc
		return (bid - ask), ask_exc, bid_exc

	def _get_ticker_bitflyer_hooks(self, r, *args, **kwargs):
		json = r.json()
		if json['product_code'] == 'BTC_JPY':
			coin = 'btc'
		else:
			coin = 'eth'
		self.ticker[coin]['bitflyer']['bid'] = float(json['best_bid'])
		self.ticker[coin]['bitflyer']['ask'] = float(json['best_ask'])

	def _get_ticker_bitflyer(self, params):
		uri ='https://api.bitflyer.jp/v1/ticker'
		hooks = {'response': self._get_ticker_bitflyer_hooks}
		return grequests.get(uri, params=params, hooks=hooks, timeout=self.timeout)

	def _get_ticker_btcbox_hooks(self, r, *args, **kwargs):
		json = r.json()
		if 'coin=btc' in r.url:
			coin = 'btc'
		else:
			coin = 'eth'
		self.ticker[coin]['btcbox']['bid'] = float(json['buy'])
		self.ticker[coin]['btcbox']['ask'] = float(json['sell'])

	def _get_ticker_btcbox(self, params):
		uri ='https://www.btcbox.co.jp/api/v1/ticker'
		hooks = {'response': self._get_ticker_btcbox_hooks}
		return grequests.get(uri, params=params, hooks=hooks, timeout=self.timeout)

	def _get_ticker_zaif_hooks(self, r, *args, **kwargs):
		json = r.json()
		if 'btc_jpy' in r.url:
			coin = 'btc'
		else:
			coin = 'eth'
		self.ticker[coin]['zaif']['bid'] = float(json['bid'])
		self.ticker[coin]['zaif']['ask'] = float(json['ask'])

	def _get_ticker_zaif(self, params):
		uri ='https://api.zaif.jp/api/1/ticker/{0}'.format(params['coin'])
		hooks = {'response': self._get_ticker_zaif_hooks}
		return grequests.get(uri, params=None, hooks=hooks, timeout=self.timeout)

	def _get_ticker_bitbank_hooks(self, r, *args, **kwargs):
		json = r.json()
		if 'btc_jpy' in r.url:
			coin = 'btc'
		elif 'eth_btc' in r.url:
			coin = 'eth'
		else:
			coin = 'xrp'
		self.ticker[coin]['bitbank']['bid'] = float(json['data']['buy'])
		self.ticker[coin]['bitbank']['ask'] = float(json['data']['sell'])

	def _get_ticker_bitbank(self, params):
		uri ='https://public.bitbank.cc/{0}/ticker'.format(params['pair'])
		hooks = {'response': self._get_ticker_bitbank_hooks}
		return grequests.get(uri, params=None, hooks=hooks, timeout=self.timeout)

	def _get_ticker_quoinex_hooks(self, r, *args, **kwargs):
		json = r.json()
		if '5' in r.url:
			coin = 'btc'
		elif '29' in r.url:
			coin = 'eth'
		else:
			coin = 'xrp'
		self.ticker[coin]['quoinex']['bid'] = float(json['market_bid'])
		self.ticker[coin]['quoinex']['ask'] = float(json['market_ask'])

	def _get_ticker_quoinex(self, params):
		uri ='https://api.quoine.com/products/{0}'.format(params['id'])
		hooks = {'response': self._get_ticker_quoinex_hooks}
		return grequests.get(uri, params=None, hooks=hooks, timeout=self.timeout)

def ticker(**kwargs):
	timeout = kwargs.get('timeout', None)
	exception_handler = kwargs.get('exception_handler', None)

	arbitrage = Arbitrage(timeout=timeout, exception_handler=exception_handler)
	return arbitrage.get_ticker()
