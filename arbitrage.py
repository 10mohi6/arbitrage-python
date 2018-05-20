# coding: utf-8
import grequests

__all__ = ['ticker']

TICKER = {
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
_timeout = 0
_ticker = TICKER

def _diff(coin, exchanges):
	global _ticker
	ask = 10000000
	bid = 0
	ask_exc = ''
	bid_exc = ''
	for exc in exchanges:
		if _ticker[coin][exc]['ask'] < ask:
			ask = _ticker[coin][exc]['ask']
			ask_exc = exc
		if _ticker[coin][exc]['bid'] > bid:
			bid = _ticker[coin][exc]['bid']
			bid_exc = exc
	return (bid - ask), ask_exc, bid_exc

def _bitflyer_ticker_hooks(r, *args, **kwargs):
	global _ticker
	json = r.json()

	if json['product_code'] == 'BTC_JPY':
		coin = 'btc'
	else:
		coin = 'eth'
	_ticker[coin]['bitflyer']['bid'] = float(json['best_bid'])
	_ticker[coin]['bitflyer']['ask'] = float(json['best_ask'])

def _bitflyer_ticker(params):
	global _timeout
	uri ='https://api.bitflyer.jp/v1/ticker'
	hooks = {'response': _bitflyer_ticker_hooks}
	return grequests.get(uri, params=params, hooks=hooks, timeout=_timeout)

def _btcbox_ticker_hooks(r, *args, **kwargs):
	global _ticker
	json = r.json()
	if 'coin=btc' in r.url:
		coin = 'btc'
	else:
		coin = 'eth'
	_ticker[coin]['btcbox']['bid'] = float(json['buy'])
	_ticker[coin]['btcbox']['ask'] = float(json['sell'])

def _btcbox_ticker(params):
	global _timeout
	uri ='https://www.btcbox.co.jp/api/v1/ticker'
	hooks = {'response': _btcbox_ticker_hooks}
	return grequests.get(uri, params=params, hooks=hooks, timeout=_timeout)

def _zaif_ticker_hooks(r, *args, **kwargs):
	global _ticker
	json = r.json()
	if 'btc_jpy' in r.url:
		coin = 'btc'
	else:
		coin = 'eth'
	_ticker[coin]['zaif']['bid'] = float(json['bid'])
	_ticker[coin]['zaif']['ask'] = float(json['ask'])

def _zaif_ticker(params):
	global _timeout
	uri ='https://api.zaif.jp/api/1/ticker/{0}'.format(params['coin'])
	hooks = {'response': _zaif_ticker_hooks}
	return grequests.get(uri, params=None, hooks=hooks, timeout=_timeout)

def _bitbank_ticker_hooks(r, *args, **kwargs):
	global _ticker
	json = r.json()
	if 'btc_jpy' in r.url:
		coin = 'btc'
	elif 'eth_btc' in r.url:
		coin = 'eth'
	else:
		coin = 'xrp'
	_ticker[coin]['bitbank']['bid'] = float(json['data']['buy'])
	_ticker[coin]['bitbank']['ask'] = float(json['data']['sell'])

def _bitbank_ticker(params):
	global _timeout
	uri ='https://public.bitbank.cc/{0}/ticker'.format(params['pair'])
	hooks = {'response': _bitbank_ticker_hooks}
	return grequests.get(uri, params=None, hooks=hooks, timeout=_timeout)

def _quoinex_ticker_hooks(r, *args, **kwargs):
	global _ticker
	json = r.json()
	if '5' in r.url:
		coin = 'btc'
	elif '29' in r.url:
		coin = 'eth'
	else:
		coin = 'xrp'
	_ticker[coin]['quoinex']['bid'] = float(json['market_bid'])
	_ticker[coin]['quoinex']['ask'] = float(json['market_ask'])

def _quoinex_ticker(params):
	global _timeout
	uri ='https://api.quoine.com/products/{0}'.format(params['id'])
	hooks = {'response': _quoinex_ticker_hooks}
	return grequests.get(uri, params=None, hooks=hooks, timeout=_timeout)

def ticker(**kwargs):
	global _timeout, _ticker, TICKER
	_ticker = TICKER
	_timeout = kwargs.get('timeout', 30)
	_exception_handler = kwargs.get('exception_handler', None)
	reqs = [
		_bitflyer_ticker({'product_code': 'BTC_JPY'}),
		_btcbox_ticker({'coin': 'btc'}),
		_btcbox_ticker({'coin': 'eth'}),
		_zaif_ticker({'coin': 'btc_jpy'}),
		_zaif_ticker({'coin': 'eth_jpy'}),
		_bitbank_ticker({'pair': 'btc_jpy'}),
		_bitbank_ticker({'pair': 'xrp_jpy'}),
		_quoinex_ticker({'id': '5'}),
		_quoinex_ticker({'id': '29'}),
		_quoinex_ticker({'id': '83'})			
	]
	grequests.map(reqs, exception_handler=_exception_handler)
	price, ask, bid = _diff('btc', ['bitflyer', 'btcbox', 'zaif', 'bitbank', 'quoinex'])
	_ticker['btc'][ask]['min'] = 1
	_ticker['btc'][bid]['max'] = 1
	_ticker['btc']['diff']['ask'] = ask
	_ticker['btc']['diff']['bid'] = bid
	_ticker['btc']['diff']['price'] = price
	price, ask, bid = _diff('eth', ['btcbox', 'zaif', 'quoinex'])
	_ticker['eth'][ask]['min'] = 1
	_ticker['eth'][bid]['max'] = 1
	_ticker['eth']['diff']['ask'] = ask
	_ticker['eth']['diff']['bid'] = bid
	_ticker['eth']['diff']['price'] = price
	price, ask, bid = _diff('xrp', ['bitbank', 'quoinex'])
	_ticker['xrp'][ask]['min'] = 1
	_ticker['xrp'][bid]['max'] = 1
	_ticker['xrp']['diff']['ask'] = ask
	_ticker['xrp']['diff']['bid'] = bid
	_ticker['xrp']['diff']['price'] = price
	return _ticker
