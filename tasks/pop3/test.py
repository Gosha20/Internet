import re
import base64

str = '''Received: from mxback5o.mail.yandex.net ([127.0.0.1])
	by mxback5o.mail.yandex.net with LMTP id pjJXbb9D
	for <nabgosha@yandex.ru>; Thu, 17 May 2018 13:31:28 +0300
Received: from mxback5o.mail.yandex.net (localhost.localdomain [127.0.0.1])
	by mxback5o.mail.yandex.net (Yandex) with ESMTP id C3C5E1E0116D
	for <nabgosha@yandex.ru>; Thu, 17 May 2018 13:31:28 +0300 (MSK)
Received: from localhost (localhost [::1])
	by mxback5o.mail.yandex.net (nwsmtp/Yandex) with ESMTP id wCRIcWyxGp-VSN8NeIn;
	Thu, 17 May 2018 13:31:28 +0300
X-Yandex-Front: mxback5o.mail.yandex.net
X-Yandex-TimeMark: 1526553088
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed; d=yandex.ru; s=mail; t=1526553088;
	bh=AgwToad/bWRgwGuggDg3NwaDEZvZmWAPhc5Hng8mUJA=;
	h=From:To:Subject:Message-Id:Date;
	b=dAvKdcHQrmhD0O8Nd5GOlccJGDzIQZCjiqGb2BGexq+7B1HsQ/6cRHzrLfXwUBj4D
	 7Bkq1oiTK3Ev5yHesOYM3GxOCKfp3D4zj2xFuEIO4Ujo6fzxFs5/vL1wl8LAn141Q5
	 igWCJDHaD8Jdb1glYfk/RMjjb6hLMoSiMX2oQtHA=
Authentication-Results: mxback5o.mail.yandex.net; dkim=pass header.i=@yandex.ru
X-Yandex-Spam: 1
X-Yandex-Sender-Uid: 624227591
Received: by web31o.yandex.ru with HTTP;
	Thu, 17 May 2018 13:31:28 +0300
From: =?utf-8?B?0LPQvtGI0LAg0L3QsNCx?= <nabgosha@yandex.ru>
To: nabgosha <nabgosha@yandex.ru>
Subject: anglish team
MIME-Version: 1.0
Message-Id: <12571241526553088@web31o.yandex.ru>
X-Mailer: Yamail [ http://yandex.ru ] 5.0
Date: Thu, 17 May 2018 15:31:28 +0500
Content-Transfer-Encoding: 7bit
Content-Type: text/plain
Return-Path: nabgosha@yandex.ru
X-YandexSms-Digest: b35b5f95f39e829b4bf4898bb0fd491c

hello
hello
.
..
hello'''


def get_full_message(message):
	boundary = re.search('boundary="(.*?)"', message)
	if boundary:
		boundary = boundary.group(1).replace('.', '\.')
		blocks = re.split('--' + boundary, message)[1:-1]
		split_by = '\r\n\r\n'
	else:
		blocks = [message]
		split_by = '\r\n'
	for block in blocks:
		headers, masbytes = block.split(split_by)
		if '\r\nContent-Disposition: attachment;' in headers:
			print(headers)
			filename = re.findall('filename="(.*)"', headers)[0]
			write(bytes(masbytes, 'utf-8'), filename)
			print('file download, you can open them')
		else:
			if 'Content-Transfer-Encoding: base64' in headers:
				print(headers)
				text_message = base64.b64decode(masbytes).decode()
			else:
				text_message = masbytes
			print(text_message)


REGEX = re.compile('(Subject: |\t)=\?utf-8\?B\?(.*?)\?=')


def get_headers(input):
	print(func_for_parse(r'(From: )=\?utf-8\?B\?(.*?)\?=', input, 'From: '))
	print(re.findall(r'To: .*?\n', input)[0])
	print(re.findall(r'Date: .*?\n', input)[0])
	print(func_for_parse('(Subject: |\t)=\?utf-8\?B\?(.*?)\?=', input, 'Subject: '))


def func_for_parse(regex, input_str, header):
	if re.findall(header + '=\?utf-8\?B', input_str) or re.findall(header + '=\?UTF-8\?B', input_str):
		input_str = input_str.replace('UTF-8', 'utf-8')
		string = [x[1] for x in re.findall(regex, input_str)]
		string = [bytes(x, 'utf-8') for x in string]
		return header + ''.join([base64.b64decode(x).decode('utf-8') for x in string])
	else:
		return re.findall(header + '.*\n', input_str)[0]


(get_full_message(str))
