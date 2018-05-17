# coding: utf-8
import grequests
import json

class Arbitrage(object):

	def __init__(self, **kwargs):
		self.timeout = kwargs.get('timeout', None)
		self.exception_handler = kwargs.get('exception_handler', None)
		self.ticker = {
			'btc' : {
				'bitflyer' : {'ask': 0, 'bid': 0 },
				'btcbox' : {'ask': 0, 'bid': 0 },
				'zaif' : {'ask': 0, 'bid': 0 },
				'bitbank' : {'ask': 0, 'bid': 0 },
				'quoinex' : {'ask': 0, 'bid': 0 }
			},
			'eth' : {
				'bitflyer' : {'ask': 0, 'bid': 0 },
				'btcbox' : {'ask': 0, 'bid': 0 },
				'zaif' : {'ask': 0, 'bid': 0 },
				'bitbank' : {'ask': 0, 'bid': 0 },
				'quoinex' : {'ask': 0, 'bid': 0 }
			},
			'xrp' : {
				'bitbank' : {'ask': 0, 'bid': 0 },
				'quoinex' : {'ask': 0, 'bid': 0 }
			}
		}

	def _bitflyer_ticker_hooks(self, r, *args, **kwargs):
		json = r.json()
		if json['product_code'] == 'BTC_JPY':
			coin = 'btc'
		else:
			coin = 'eth'
		self.ticker[coin]['bitflyer']['bid'] = float(json['best_bid'])
		self.ticker[coin]['bitflyer']['ask'] = float(json['best_ask'])

	def _bitflyer_ticker(self, params):
		uri ='https://api.bitflyer.jp/v1/ticker'
		hooks = {'response': self._bitflyer_ticker_hooks}
		return grequests.get(uri, params=params, hooks=hooks, timeout=self.timeout)

	def _btcbox_ticker_hooks(self, r, *args, **kwargs):
		json = r.json()
		if 'coin=btc' in r.url:
			coin = 'btc'
		else:
			coin = 'eth'
		self.ticker[coin]['btcbox']['bid'] = float(json['buy'])
		self.ticker[coin]['btcbox']['ask'] = float(json['sell'])

	def _btcbox_ticker(self, params):
		uri ='https://www.btcbox.co.jp/api/v1/ticker'
		hooks = {'response': self._btcbox_ticker_hooks}
		return grequests.get(uri, params=params, hooks=hooks, timeout=self.timeout)

	def _zaif_ticker_hooks(self, r, *args, **kwargs):
		json = r.json()
		if 'btc_jpy' in r.url:
			coin = 'btc'
		else:
			coin = 'eth'
		self.ticker[coin]['zaif']['bid'] = float(json['bid'])
		self.ticker[coin]['zaif']['ask'] = float(json['ask'])

	def _zaif_ticker(self, params):
		uri ='https://api.zaif.jp/api/1/ticker/{0}'.format(params['coin'])
		hooks = {'response': self._zaif_ticker_hooks}
		return grequests.get(uri, params=None, hooks=hooks, timeout=self.timeout)

	def _bitbank_ticker_hooks(self, r, *args, **kwargs):
		json = r.json()
		if 'btc_jpy' in r.url:
			coin = 'btc'
		elif 'eth_btc' in r.url:
			coin = 'eth'
		else:
			coin = 'xrp'
		self.ticker[coin]['bitbank']['bid'] = float(json['data']['buy'])
		self.ticker[coin]['bitbank']['ask'] = float(json['data']['sell'])

	def _bitbank_ticker(self, params):
		uri ='https://public.bitbank.cc/{0}/ticker'.format(params['pair'])
		hooks = {'response': self._bitbank_ticker_hooks}
		return grequests.get(uri, params=None, hooks=hooks, timeout=self.timeout)

	def _quoinex_ticker_hooks(self, r, *args, **kwargs):
		json = r.json()
		if '5' in r.url:
			coin = 'btc'
		elif '29' in r.url:
			coin = 'eth'
		else:
			coin = 'xrp'
		self.ticker[coin]['quoinex']['bid'] = float(json['market_bid'])
		self.ticker[coin]['quoinex']['ask'] = float(json['market_ask'])

	def _quoinex_ticker(self, params):
		uri ='https://api.quoine.com/products/{0}'.format(params['id'])
		hooks = {'response': self._quoinex_ticker_hooks}
		return grequests.get(uri, params=None, hooks=hooks, timeout=self.timeout)

	def get_ticker(self):
		reqs = [
			self._bitflyer_ticker({'product_code': 'BTC_JPY'}),
			self._bitflyer_ticker({'product_code': 'ETH_BTC'}),
			self._btcbox_ticker({'coin': 'btc'}),
			self._btcbox_ticker({'coin': 'eth'}),
			self._zaif_ticker({'coin': 'btc_jpy'}),
			self._zaif_ticker({'coin': 'eth_jpy'}),
			self._bitbank_ticker({'pair': 'btc_jpy'}),
			self._bitbank_ticker({'pair': 'eth_btc'}),
			self._bitbank_ticker({'pair': 'xrp_jpy'}),
			self._quoinex_ticker({'id': '5'}),
			self._quoinex_ticker({'id': '29'}),
			self._quoinex_ticker({'id': '83'})			
		]
		grequests.map(reqs, exception_handler=self.exception_handler)
		ticker = self.ticker
		ticker['eth']['bitflyer']['bid'] = ticker['eth']['bitflyer']['bid'] * ticker['btc']['bitflyer']['bid']
		ticker['eth']['bitflyer']['ask'] = ticker['eth']['bitflyer']['ask'] * ticker['btc']['bitflyer']['ask']
		ticker['eth']['bitbank']['bid'] = ticker['eth']['bitbank']['bid'] * ticker['btc']['bitbank']['bid']
		ticker['eth']['bitbank']['ask'] = ticker['eth']['bitbank']['ask'] * ticker['btc']['bitbank']['ask']
		return json.dumps(ticker)

