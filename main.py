import vk_api, os
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType

import functions

def captcha_handler(captcha):
	with open('captcha.jpg', 'wb') as f:
		a = requests.post(captcha.get_url())
		f.write(a.content)
	os.system("mirage captcha.jpg")
	key = input("Enter captcha code: ")
	return captcha.try_again(key)

def parse(user_id, input_string):
	if input_string[0] != '.': return 0
	input_string = input_string[1:]
	first_space = input_string.find(' ')
	if first_space == -1: return 0
	command = input_string[:first_space]
	if command in functions.call:
		args = input_string[first_space+1:]
		return functions.call[command](user_id, args)

def main():
	with open("../auth.txt", "r") as f:
		login, password = f.readline()[:-1], f.readline()[:-1]
	vk_session = vk_api.VkApi(login, password, captcha_handler = captcha_handler)

	try:
		vk_session.auth()
	except vk_api.AuthError as error_msg:
		print(error_msg)
		return
	
	os.system("clear")
	print("Successfully started :)")
	vk = vk_session.get_api()

	upload = VkUpload(vk_session)  # Для загрузки изображений
	longpoll = VkLongPoll(vk_session)

	for event in longpoll.listen():
		if event.type == VkEventType.MESSAGE_NEW and event.to_me:
			reply = parse(event.user_id, event.text)
			if not reply: continue
			print(event.user_id, event.text)
			attachments = []
			for image in reply[0]:
				photo = upload.photo_messages(photos = image)[0]
				attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))
			i = 0
			for document in reply[2]:
				i += 1
				print("Uploading document " + str(i))
				document_file = open(document, "rb")
				document = upload.document_wall(doc = document_file.raw, title = "doc"+str(i))[0]
				attachments.append('doc{}_{}'.format(document['owner_id'], document['id']))
			vk.messages.send(user_id = event.user_id, attachment = ','.join(attachments), message = reply[1])

if __name__ == '__main__':
	main()
