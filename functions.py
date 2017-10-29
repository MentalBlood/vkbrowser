import requests
session = requests.session()

def ddg(user_id, query):
	response = session.get('http://api.duckduckgo.com/', params={'q': query, 'format': 'json'} ).json()

	text = response.get('AbstractText')
	image_url = response.get('Image')

	if not text:
		text = 'No results'
		return [user_id, [image], text]
	
	if image_url:
		image = session.get(image_url, stream = True)
		
	return [user_id, [image], text]

call = {'ddg': ddg}
