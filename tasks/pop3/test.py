import re
import base64
str = '''Received: from mxback3j.mail.yandex.net ([127.0.0.1])
	by mxback3j.mail.yandex.net with LMTP id 3aNEdZJx
	for <nabgosha@yandex.ru>; Thu, 3 May 2018 20:32:34 +0300
Received: from mxback3j.mail.yandex.net (localhost.localdomain [127.0.0.1])
	by mxback3j.mail.yandex.net (Yandex) with ESMTP id B98601580C3B
	for <nabgosha@yandex.ru>; Thu,  3 May 2018 20:32:34 +0300 (MSK)
Received: from localhost (localhost [::1])
	by mxback3j.mail.yandex.net (nwsmtp/Yandex) with ESMTP id Pr080tveT7-WXg4UZbt;
	Thu, 03 May 2018 20:32:33 +0300
X-Yandex-Front: mxback3j.mail.yandex.net
X-Yandex-TimeMark: 1525368753
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed; d=yandex.ru; s=mail; t=1525368753;
	bh=sKHDIwxchGsuGN6PHF+5MDBC0gsGVEU+DZSTE3VFJbA=;
	h=From:To:Subject:Message-Id:Date;
	b=aZfg2Nziy83poIkoRmncZXm1NWh3UZbFsdVfNhkwDBmj+v9nIYKiQoZDdkQo8kaL/
	 2BsRbHVhmMw4PBYvtlGsf4k/hvBYr5n7OFyS54DUvBOqqsY83rVKmfIdgUNLm6DRHo
	 nYT6ahzu/xHuNEKcaZYmwLMwyShLFfu/StAaZbO8=
Authentication-Results: mxback3j.mail.yandex.net; dkim=pass header.i=@yandex.ru
X-Yandex-Spam: 1
X-Yandex-Sender-Uid: 624227591
Received: by web44g.yandex.ru with HTTP;
	Thu, 03 May 2018 20:32:33 +0300
From: =?utf-8?B?0LPQvtGI0LAg0L3QsNCx?= <nabgosha@yandex.ru>
To: nabgosha <nabgosha@yandex.ru>
Subject: =?utf-8?B?0J7QvSDQs9C+0LLQvtGA0LjQuyDQvdCwINGC0L7QvCDQuNC30YvRgdC60LDQvdC90L7QvCDRhNGA0LA=?=
	=?utf-8?B?0L3RhtGD0LfRgdC60L7QvCDRj9C30YvQutC1LCDQvdCwINC60L7RgtC+0YDQvtC8INC90LUg0YLQvtC7?=
	=?utf-8?B?0YzQutC+INCz0L7QstC+0YDQuNC70LgsINC90L4g0Lgg0LTRg9C80LDQu9C4INC90LDRiNC4INC00LU=?=
	=?utf-8?B?0LTRiywg0Lgg0YEg0YLQtdC80LgsINGC0LjRhdC40LzQuCwg0L/QvtC60YDQvtCy0LjRgtC10LvRjNGB?=
	=?utf-8?B?0YLQstC10L3QvdGL0LzQuCDQuNC90YLQvtC90LDRhtC40Y/QvNC4LCDQutC+0YLQvtGA0YvQtSDRgdCy?=
	=?utf-8?B?0L7QudGB0YLQstC10L3QvdGLINGB0L7RgdGC0LDRgNC10LLRiNC10LzRg9GB0Y8g0LIg0YHQstC10YI=?=
	=?utf-8?B?0LUg0Lgg0L/RgNC4INC00LLQvtGA0LUg0LfQvdCw0YfQuNGC0LXQu9GM0L3QvtC80YMg0YfQtdC70L4=?=
	=?utf-8?B?0LLQtdC60YMuINCe0L0g0L/QvtC00L7RiNC10Lsg0Log0JDQvdC90LUg0J/QsNCy0LvQvtCy0L3QtSwg?=
	=?utf-8?B?0L/QvtGG0LXQu9C+0LLQsNC7INC10LUg0YDRg9C60YMsINC/0L7QtNGB0YLQsNCy0LjQsiDQtdC5INGB?=
	=?utf-8?B?0LLQvtGOINC90LDQtNGD0YjQtdC90L3Rg9GOINC4INGB0LjRj9GO0YnRg9GOINC70YvRgdC40L3Rgywg?=
	=?utf-8?B?0Lgg0L/QvtC60L7QudC90L4g0YPRgdC10LvRgdGPINC90LAg0LTQuNCy0LDQvdC1Lg==?=
MIME-Version: 1.0
Message-Id: <8804481525368753@web44g.yandex.ru>
X-Mailer: Yamail [ http://yandex.ru ] 5.0
Date: Thu, 03 May 2018 22:32:33 +0500
Content-Type: multipart/mixed;
	boundary="----==--bound.880449.web44g.yandex.ru"
Return-Path: nabgosha@yandex.ru
X-YandexSms-Digest: 746d218856b328fe7407dfb96a0aa605


------==--bound.880449.web44g.yandex.ru
Content-Transfer-Encoding: base64
Content-Type: text/plain; charset=utf-8

0J7QvSDQs9C+0LLQvtGA0LjQuyDQvdCwINGC0L7QvCDQuNC30YvRgdC60LDQvdC90L7QvCDRhNGA
0LDQvdGG0YPQt9GB0LrQvtC8INGP0LfRi9C60LUsINC90LAg0LrQvtGC0L7RgNC+0Lwg0L3QtSDR
gtC+0LvRjNC60L4g0LPQvtCy0L7RgNC40LvQuCwg0L3QviDQuCDQtNGD0LzQsNC70Lgg0L3QsNGI
0Lgg0LTQtdC00YssINC4INGBINGC0LXQvNC4LCDRgtC40YXQuNC80LgsINC/0L7QutGA0L7QstC4
0YLQtdC70YzRgdGC0LLQtdC90L3Ri9C80Lgg0LjQvdGC0L7QvdCw0YbQuNGP0LzQuCwg0LrQvtGC
0L7RgNGL0LUg0YHQstC+0LnRgdGC0LLQtdC90L3RiyDRgdC+0YHRgtCw0YDQtdCy0YjQtdC80YPR
gdGPINCyINGB0LLQtdGC0LUg0Lgg0L/RgNC4INC00LLQvtGA0LUg0LfQvdCw0YfQuNGC0LXQu9GM
0L3QvtC80YMg0YfQtdC70L7QstC10LrRgy4g0J7QvSDQv9C+0LTQvtGI0LXQuyDQuiDQkNC90L3Q
tSDQn9Cw0LLQu9C+0LLQvdC1LCDQv9C+0YbQtdC70L7QstCw0Lsg0LXQtSDRgNGD0LrRgywg0L/Q
vtC00YHRgtCw0LLQuNCyINC10Lkg0YHQstC+0Y4g0L3QsNC00YPRiNC10L3QvdGD0Y4g0Lgg0YHQ
uNGP0Y7RidGD0Y4g0LvRi9GB0LjQvdGDLCDQuCDQv9C+0LrQvtC50L3QviDRg9GB0LXQu9GB0Y8g
0L3QsCDQtNC40LLQsNC90LUu0J7QvSDQs9C+0LLQvtGA0LjQuyDQvdCwINGC0L7QvCDQuNC30YvR
gdC60LDQvdC90L7QvCDRhNGA0LDQvdGG0YPQt9GB0LrQvtC8INGP0LfRi9C60LUsINC90LAg0LrQ
vtGC0L7RgNC+0Lwg0L3QtSDRgtC+0LvRjNC60L4g0LPQvtCy0L7RgNC40LvQuCwg0L3QviDQuCDQ
tNGD0LzQsNC70Lgg0L3QsNGI0Lgg0LTQtdC00YssINC4INGBINGC0LXQvNC4LCDRgtC40YXQuNC8
0LgsINC/0L7QutGA0L7QstC40YLQtdC70YzRgdGC0LLQtdC90L3Ri9C80Lgg0LjQvdGC0L7QvdCw
0YbQuNGP0LzQuCwg0LrQvtGC0L7RgNGL0LUg0YHQstC+0LnRgdGC0LLQtdC90L3RiyDRgdC+0YHR
gtCw0YDQtdCy0YjQtdC80YPRgdGPINCyINGB0LLQtdGC0LUg0Lgg0L/RgNC4INC00LLQvtGA0LUg
0LfQvdCw0YfQuNGC0LXQu9GM0L3QvtC80YMg0YfQtdC70L7QstC10LrRgy4g0J7QvSDQv9C+0LTQ
vtGI0LXQuyDQuiDQkNC90L3QtSDQn9Cw0LLQu9C+0LLQvdC1LCDQv9C+0YbQtdC70L7QstCw0Lsg
0LXQtSDRgNGD0LrRgywg0L/QvtC00YHRgtCw0LLQuNCyINC10Lkg0YHQstC+0Y4g0L3QsNC00YPR
iNC10L3QvdGD0Y4g0Lgg0YHQuNGP0Y7RidGD0Y4g0LvRi9GB0LjQvdGDLCDQuCDQv9C+0LrQvtC5
0L3QviDRg9GB0LXQu9GB0Y8g0L3QsCDQtNC40LLQsNC90LUu
------==--bound.880449.web44g.yandex.ru
Content-Disposition: attachment;
	filename="-10.png"
Content-Transfer-Encoding: base64
Content-Type: image/png;
	name="-10.png"

iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAAAXNSR0IArs4c6QAAAARnQU1BAACx
jwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAFLaVRYdFhNTDpjb20uYWRvYmUueG1wAAAAAAA8
P3hwYWNrZXQgYmVnaW49Iu+7vyIgaWQ9Ilc1TTBNcENlaGlIenJlU3pOVGN6a2M5ZCI/Pgo8eDp4
bXBtZXRhIHhtbG5zOng9ImFkb2JlOm5zOm1ldGEvIiB4OnhtcHRrPSJBZG9iZSBYTVAgQ29yZSA1
LjYtYzEzOCA3OS4xNTk4MjQsIDIwMTYvMDkvMTQtMDE6MDk6MDEgICAgICAgICI+CiA8cmRmOlJE
RiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMi
PgogIDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiLz4KIDwvcmRmOlJERj4KPC94OnhtcG1l
dGE+Cjw/eHBhY2tldCBlbmQ9InIiPz4gSa46AAAHaElEQVRIS51XW2wcVxn+5r53r7322o5tEtdc
EpfESRMEFZSiUIkqRFSFgpoXaJ+IeKtUkHjgpUECFQmpAimIBwRB4gUCBRRIlUZNE8XIlfvQUprW
JXFt7/qWXa93d3Zndq58Z3Zj3HadNjn20cyeOXP+2/f//zfSj3/6S7x8+QpM03ymsFh4PAgx5Hs+
AslFQskhLvehFVTR9G5CklS0h9S53vXlknL8kcfwwvkXL15/58YTPDknQTICyTFSYdbIK/uMmNpn
xLW84YW2YfprBhAaIacsqbzH3c66/Mors6eWFhaPplNp6JpO2TJCrwUtuQteOgPb34TshzCUDBLq
AIaMQ0ipefhw7tpcvlhVICfOVirVeDKdpDH89ywKHYG3536U+tJIhAq0ZhO1oIgedQ96tXHIUFD3
V7g9pNPlu1FgXm7ZrUQyFUfI4EbDs6EkhyDFB6DIBpq0es19A3W3ADvYhOWX0QhuIgxDiuwuNIAH
MW835FCCux0skp6EV70OaeNtxJom7NV/oeEVIctxVL0FLNuz2HQXoERAez/IJAr0qY7KqUX3OwFR
liQpFNZKcucQYiZ0m3DmL8CZ+zOCyg2oal/nMAVuaEeu7nagsFLlX974NIaNKd5p8MJmV8MjXwmh
gR+0NwiX08WhREUCB5Ia77wolKMdVExWlP8ruu1YWoCQe1QpwRlnqGLQJWKny5BlmVa4HqqbJfi+
y0OFLhQiXCnr7azlYWJdKOc6TjTFvViTov3toUga/MDDivMqFuzLYMphKHaYCqh0OyO6bURvOXYD
omhQiw/oJqwTijTqNawW57C+ci2aq8W3YNaqfESQqWJPe4Shi5Q8wAz4GFp+FSX3GpVpx337UHID
Yz9smA0jkUpB02NEd8fl3BUJ9X2U1lfQMJcxMjqJBx/6Fibv/Rws28EaFbAsB4l4OtorkB4SUAlF
YEJDw1+HF1i0/AOYmJdFXIxYHPF44j1ChXsDIbS8BqdVwte++X2c/cdr+PvZX+Avf3wOZ8/N4sST
z8BzKlSsSKFBFBJFMrDhzqPszvE+Fv3uGuPIPbRyC1ydXUQ7Q2ChZa3j6LHv4czvn8XBfRKe/dlz
OHXqJ9i7G/jdb36EY48+zZhvwG40iIvoNArTOwI7taGLZOkTk/fXSuuldCwW23osUC5eWV9epCUa
Zl9/B4cme3D8+CM4d+5v0b6R4TEUim/jekHFgXsnYZlFDI18PEL7VjHqamu0eHHnese08r0q9u0/
GAmdnp6OhCZSIzj9q9/i6EMP4/w/X8bEmIZDh6aooBXF+KOODym0EuJaG2zpdDa6PvnECZz87ndw
5syv8fkHvhCtpeJ33ia7ChZ6C5epej9enb2EwvIq9u+fxMmTT+Hq9AzK5Y2OMincLFfw0ksXiOps
pwZ8NJt3qPKigMjoy/XRfT4e+/oJka44ffrneP75PyCb7dk6XTxznCr682wsfMfzHZZJqzPtHev1
jq4W6aHpBnp6JzAzcwlHjnyRcZ7B7rFReCw2V65M44EHH8blyy8gk90T7XX9ZoTojDqKLNtnWh2K
FBSKIHDBriB8Ga11RfUtc0ReihSxzAY2yv/lskzL7mGFk7C+eoO/fWT7xpFk6/R8CwlWrF5tYit3
Q5rluTVUWnOwZBYSj7VflGFVv3hbwZFmHeFOq4V6vQ67ucnVELF4D9KZHuiGQYta5EA9GNQPRM9I
k9q600KVjcLMZVBNGlCqRfirs+LU7enUdoE4ZOtF/hbuExVMN2LI9fdjeOQezgnkBvLRWiA6EqlR
jzoWuTFya2dIjotGxkCpPw9FTUMZOgwps5tt19xOIVi92EESSi9nP/xQcCoJSfIrSXQXgkZUN4H2
W21UKBSwG4myqEBHIJN1iN7uMp6emHzWctkkOFU2CV5D12bLJeO6pZ0QlCIYBvWpyGUpdTCiNjlt
LzT2Vj9sUxlRld5bmQTr8HhYAMX1EbJN2vlBmMO7sJnPwtsoYte7i4ibG3AWLyJsLDPGcbBJhAqz
gCBSkFJG2ocL0Ki7o1QQvdXxG7cp9gqNdNF010gCdFQpcD0/gHWSR3l8Cvn9x5Ck1fZ//gS39G+o
RgKO61uyQokBYyTy1fJJ2kkMZB5gBRu0kvEmWumjrbh1u5FJAEx7HpWMi1Y6B8ncxLicxX2JvRgd
/QxyU18B4kkaZ6CwtIgjhw+Oyslk8t1m04KqGCRzSyi13uS8FrU2wUJEXn7Yl4No8n7QQiPcJOXR
yMs89Bo5GDSg2Sijt/eTSGUnaGmDQKwhPzw4KU9NHXjaiBloNVsRiauRUdaogBjvZw07m81WqGeA
0g2E5iq01DCWvQqqxI2hp1FYuIDN8huIG1keocEmi1Ae/cbjc4Wl4s2m1fxqrVbn1wQJmk6CR957
R0NRidg6QKYSU1MwmTKl1RlUls7jrTf/ikq5ALMuGKeFbG6XLj31g1O4enUaqWTqs57nfbtQKH6q
Xq1B1bQ7ktt2ERFOaiwJjqXG6FqTH4M17Bnflzl836G9DtNxeXkFR7/8pfr/APM+VpeXFk/aAAAA
AElFTkSuQmCC
------==--bound.880449.web44g.yandex.ru--'''
regexp = re.compile('(Subject: |\t)=\?utf-8\?B\?(.*?)\?=')
# a = re.findall('Subject: =\?utf-8\?B', str)
# if a:
#     subject = [x[1] for x in re.findall(regexp, str)]
#     subject = [bytes(x, 'utf-8') for x in subject]
#     print(subject)
#     print(('').join([base64.b64decode(x).decode('utf-8') for x in subject ]))
def write(masbytes, filename):
    result = base64.b64decode(masbytes)
    with open(filename, 'wb') as file:
        file.write(result)
def get_full_message(message):
    boundary = re.search('boundary="(.*?)"',message).group(1).replace('.','\.')
    blocks = re.split('--'+boundary, message)[1:-1]
    for block in blocks:
        headers, masbytes = block.split('\n\n')
        if headers.startswith('\nContent-Disposition: attachment;'):
            print(headers)
            filename = re.findall('filename="(.*)"', headers)[0]
            write(bytes(masbytes,'utf-8'), filename)
            print(re.findall('filename="(.*)"', headers)[0])
        else:
            print(headers)
            text_message = base64.b64decode(masbytes).decode()
            print(text_message)

get_full_message(str)



# write()