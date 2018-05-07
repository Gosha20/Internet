import re
import base64
str = '''From: =?UTF-8?B?0JPQvtGI0LAg0J3QsNCx0L7QudGH0LXQvdC60L4=?= <gosha3548@gmail.com>
Date: Mon, 7 May 2018 20:11:58 +0500
Message-ID: <CAHN5DD5g4ZqBhrFYX5JHg3D1vgTEJatDE1cyM5BcCbApQOfudw@mail.gmail.com>
Subject: =?UTF-8?B?dGVtYSBuYSBhbmdsINC4INC90LAg0YDRg9GB0YHQutC+0Lwg0L3QsCDRgNGD0YHRgdC6?=
	=?UTF-8?B?0L7QvCDQvdCwINGA0YPRgdGB0LrQvtC8INC90LAg0YDRg9GB0YHQutC+0Lwg0L3QsCDRgNGD0YHRgdC6?=
	=?UTF-8?B?0L7QvCDQvdCwINGA0YPRgdGB0LrQvtC8INC90LAg0YDRg9GB0YHQutC+0Lwg0L3QsCDRgNGD0YHRgdC6?=
	=?UTF-8?B?0L7QvCDQvdCwINGA0YPRgdGB0LrQvtC8INGE0LjQvdCw0LvRjNC90LDRjyDRgdGC0YDQvtC60LA=?=
To: nabgosha@yandex.ru
'''
REGEX = re.compile('(Subject: |\t)=\?utf-8\?B\?(.*?)\?=')
def get_headers(input):
    print(func_for_parse(r'(From: )=\?utf-8\?B\?(.*?)\?=', input, 'From: '))
    print(re.findall(r'To: .*?\n', input)[0])
    print(re.findall(r'Date: .*?\n', input)[0])
    print(func_for_parse('(Subject: |\t)=\?utf-8\?B\?(.*?)\?=', input, 'Subject: '))


def func_for_parse(regex, input_str, header):
    if re.findall(header + '=\?utf-8\?B', input_str) or re.findall(header + '=\?UTF-8\?B', input_str):
        input_str=input_str.replace('UTF-8','utf-8')
        string = [x[1] for x in re.findall(regex, input_str)]
        string = [bytes(x, 'utf-8') for x in string]
        return header + ''.join([base64.b64decode(x).decode('utf-8') for x in string])
    else:
        return re.findall(header + '.*\n', input_str)[0]


get_headers(str)