import requests, os
session = requests.session()
koryavov = {'e': open('../KORPARSED.txt')}

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
		if text: return [[], text, []]
		return [[], 'No interesting results', []]
	
	if image_url:
		image = session.get(image_url, stream = True).raw
		return [[image], text, []]
	
	return [[], text, []]

def urlim(user_id, query):
	os.system("cutycapt --url=" + query + " --out=url_image.png")
	return [[], query, ["url_image.png"]]

def DDG(user_id, query):
	urlim(user_id, "\"https://duckduckgo.com/" + query.replace(' ', '+') + "\"")

def search_parsed_file(f, query):
	print('query: ', query)
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
		return [[], search_parsed_file(koryavov[query[0]], query[2:]), []]

call = {'ddg': ddg, 'urlim': urlim, 'DDG': DDG, 'ks': ks}
