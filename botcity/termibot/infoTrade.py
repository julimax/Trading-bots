import config
from binance.client import Client

client = Client(config.apyKey, config.apySecurity)

infoTrade = client.futures_position_information()

count = 0
'''for i in infoTrade:
	print(count)
	print(infoTrade[count])
	count += 1
'''
print(infoTrade[54])
print(infoTrade[55])

print(infoTrade[56])

balance = client.futures_account_balance()

balance = int(float(balance[6]['balance']))
amount = int(balance/5)
print(amount)