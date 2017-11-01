import requests, os
import json
session = requests.session()
koryavov = {'e': open('../KORPARSED.txt')}

class attachments():
	def __init__(self, images = [], text = '', docs = [], voice = [], audio = []):
		self.images = images
		self.text = text
		self.docs = docs
		self.voice = voice
		self.audio = audio

def ddg(user_id, query):
	query = query[:255]
	response = session.get('http://api.duckduckgo.com/', params={'q': query, 'format': 'json'} ).json()

	text = response.get('AbstractText')
	image_url = response.get('Image')

	if not text:
		if response.get('RelatedTopics'):
			text = "Related topics:\n\n"
			for topic in response.get('RelatedTopics'):
				temp = topic.get('Result')
				if not temp: continue
				temp = str(temp)
				temp = temp[temp.find('>')+1:].replace('</a>', '\n')
				text += temp + '\n\n'
		print(response.get('Results'))
		if response.get('Results'):
			text += "Results:\n\n"
			for topic in response.get('Results'):
				temp = topic.get('Result')
				if not temp: continue
				temp = str(temp)
				temp = temp[temp.find('>')+1:].replace('</a>', '\n')
				text += temp + '\n\n'
		if text: return attachments(text = text) 
		return attachments(text = 'No results')
	
	if image_url:
		image = session.get(image_url, stream = True).raw
		return attachments(text = text, images = [image])
	
	return attachments(text = text)

def DDG(user_id, query):
	os.system('echo `duck --json -C ' + query + '` > search')
	answers = ''
	with open('search') as f:
		for line in f:
			answers += line
	decoder = json.JSONDecoder()
	answers = decoder.decode(answers)
	text = ''
	for answer in answers[:10]:
		text += answer['title'] + '\n' + answer['url'] + '\n' + answer['abstract'] + '\n\n'
	return attachments(text = text)

def urlim(user_id, query):
	os.system("cutycapt --url=" + query + " --out=url_image.png")
	return attachments(images = ['url_image.png'])

def search_parsed_file(f, query):
	query = query.replace(' ', '')
	f.seek(0, 0)
	page = '0'
	pages = ''
	for line in f:
		if line[0] == '|':
			page = line[1:-2]
			continue
		if query in line: pages += page + '\n'
	if not pages: return 'Not found'
	else: return pages

def ks(user_id, query):
	if query[0] in koryavov:
		return attachments(text = search_parsed_file(koryavov[query[0]], query[2:]))

def tts(user_id, query):
	os.system('espeak -w voice.wav "' + query + '"')
	return attachments(voice = ['voice.wav'])

def TTS(user_id, query):
	n = query[:query.find(' ')]
	if not n.isnumeric(): return attachments()
	
	n = int(n)
	file_names = []
	while len(query) > n:
		file_names.append('voice' + str(len(file_names)) + '.wav')
		os.system('espeak -w ' + file_names[-1] + ' "' + query[:n] + '"')
		query = query[n:]
	if len(query):
		file_names.append('voice' + str(len(file_names)) + '.wav')
		os.system('espeak -w ' + file_names[-1] + ' "' + query + '"')
	return attachments(voice = file_names)

call = {'ddg': ddg, 'urlim': urlim, 'DDG': DDG, 'ks': ks, 'tts': tts, 'TTS': TTS}
