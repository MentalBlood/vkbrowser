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

forbidden = [';', '|', '>', '<', '&', '`']

def safety_check(query, correct = True):
	if correct:
		for element in forbidden: query.replace(element, ' ')
		return 1
	for element in forbidden:
		if element in query: return 0
	return 1

def parse(user_id, input_string):
	if not (safety_check(input_string)): return 0
	if input_string[0] != '.': return 0
	input_string = input_string[1:]
	first_space = input_string.find(' ')
	if first_space == -1: return 0
	command = input_string[:first_space]
	if command in functions.call:
		args = input_string[first_space+1:]
		return functions.call[command](user_id, args)

def upload_attachments(attachments, vk, upload, user_id):
	uploaded = []
	for image in attachments.images:
		photo = upload.photo_messages(photos = image)[0]
		uploaded.append('photo{}_{}'.format(photo['owner_id'], photo['id']))
	i = 0
	for document in attachments.docs:
		i += 1
		document_file = open(document, "rb")
		document_file = upload.document_wall(doc = document_file.raw, title = "doc"+str(i))[0]
		os.system('rm -f ' + document)
		uploaded.append('doc{}_{}'.format(document_file['owner_id'], document_file['id']))
	
	for voice in attachments.voice:
		voice_file = open(voice, "rb")
		voice_file = upload.audio_message(audio = voice_file.raw)[0]
		os.system('rm -f ' + voice)
		uploaded.append('doc{}_{}'.format(voice_file['owner_id'], voice_file['id']))

	if user_id:
		if uploaded or attachments.text:
			vk.messages.send(user_id = user_id, attachment = ','.join(uploaded), message = attachments.text)
			return 1
		return 0
	
	return uploaded

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
		if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
			print(event.user_id, event.text)
			reply = parse(event.user_id, event.text)
			if not reply: continue
			upload_attachments(reply, vk, upload, event.user_id)

if __name__ == '__main__':
	main()
