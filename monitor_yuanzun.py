import requests as req
import bs4
import itchat
import time
import os
import traceback


def open_url(url):
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"}
	res = req.get(url, headers = headers)
	return res


def get_data(res):
	soup = bs4.BeautifulSoup(res.content, "html.parser")
	target = soup.find("div", style = "line-height:25px;padding-left:10px;")
	# print(target)
	# print(target.previous_sibling.previous_sibling.text)
	text = target.a.text[8:]
	href = target.a["href"]
	# print(text, href, sep = "\n")
	return text, href


def judge(content):
	c = 0
	f = open("yuanzun.txt", "r", encoding = "utf-8")
	t = f.read()
	# print(t)
	if t == content[0]:
		# print("okay")
		pass
	else: c = 1
	f.close()
	if c == 1:
		with open("yuanzun.txt", "w", encoding = "utf-8") as yz:
			yz.write(content[0])
			# print("different")
			return content


def call_wechat(result):
	user_name = "猪猪"
	result = f"更新了,title = \"{result[0]}\"\nhttp://www.dingdianzw.com{result[1]}"
	print(result)
	# print(itchat_user_name = itchat.search_friends(wechatAccount = user_name)[0]["UserName"])
	itchat_user_name = itchat.search_friends(name = user_name)[0]["UserName"]
	itchat.send(result, itchat_user_name)


def operation(url):
	while True:
		res = open_url(url)
		content = get_data(res)
		result = judge(content)
		if result != None:
			call_wechat(result)
		time.sleep(60)


def main():
	if not os.path.exists("yuanzun.txt"):
		open("yuanzun.txt", "w").close()
	itchat.auto_login(hotReload = True, enableCmdQR = 2)
	# itchat.run()
	try:
		url = "http://www.dingdianzw.com/book/11896.html"
		operation(url)
	except Exception as exc:
		user_name = "猪猪"
		itchat_user_name = itchat.search_friends(name = user_name)[0]["UserName"]
		itchat.send(f"Something was wrong/n{traceback.format_exc()}", itchat_user_name)


if __name__ == '__main__':
	main()