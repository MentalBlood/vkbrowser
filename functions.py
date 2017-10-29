import requests, os
session = requests.session()

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

#def DDG(user_id, query):


def urlim(user_id, query):
	os.system("cutycapt --url=" + query + " --out=url_image.png")
	return [[], query, ["url_image.png"]]

call = {'ddg': ddg, 'urlim': urlim}
