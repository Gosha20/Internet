import requests
import argparse

import sys


def get_json(url, param=None):
	try:
		response = requests.get(url, params=param)
		return response.json()
	except requests.exceptions.SSLError:
		print('SSLError, \n End Work, sorry')
		sys.exit(1)
	except requests.ConnectionError:
		print('Connection error or bad url, \n End Work, sorry')
		sys.exit(1)


def get_full_info(name, access_token):
	json = get_json('https://api.vk.com/method/users.get', {
		'user_ids': name,
		'access_token': access_token,
		'fields': 'city, bdate, counters',
		'v': '5.74'})
	result = ''
	if 'response' in json:
		f_name = json['response'][0]['first_name']
		s_name = json['response'][0]['last_name']
		city = '______'
		bdate = '______'
		if __field_in_json('city', json):
			city = json['response'][0]['city']['title']
		if __field_in_json('bdate', json):
			bdate = json['response'][0]['bdate']
		if __field_in_json('counters', json):
			for k, v in json['response'][0]['counters'].items():
				result += k + " - " + str(v) + '\n'
		return "INFO ABOUT ACCOUNT\nname is {0} {1}\ncity is {2}\nbirthday {3}\n".format(
			f_name, s_name, city, bdate) + result
	if 'error' in json:
		return json['error']['error_msg']


def __field_in_json(field, json):
	return field in json['response'][0]


if __name__ == '__main__':
	access_token = open('token.txt', 'r').read()
	parser = argparse.ArgumentParser()
	parser.add_argument("--name", type=str, help="user screen name")
	args = parser.parse_args()
	if args.name:
		result = get_full_info(args.name, access_token)
		print(result)
	else:
		print('Write pls user id or name')
