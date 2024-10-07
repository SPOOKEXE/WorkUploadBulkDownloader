from tqdm import tqdm
from re import sub, search
from json import loads
from requests import get, Response

valid_url = r'.*workupload.com/'

def extract(url: str) -> dict:
	uri = sub(valid_url, '', url).split('/')
	return {'type': uri[0],'id': uri[1]}

def get_download_url(parts: dict, headers: dict) -> str:
	api_url = f"https://workupload.com/api/{parts['type']}/getDownloadServer/{parts['id']}"
	data_response = get(api_url, headers=headers)
	dl_url = loads(data_response.text)['data']['url']
	return dl_url

def get_file_information(url: str, headers: dict, cookies : dict) -> dict:
	file_response = get(url, headers=headers, cookies=cookies, stream=True)
	print(file_response.status_code, file_response.reason, file_response.headers)
	print(file_response.text)
	name = file_response.headers.get('Content-Disposition')
	name = search(r'filename="(.+)"', name).group(1)
	size = file_response.headers.get('Content-Length', 0)
	return {'name': name,'size': int(size),'response': file_response}

def download(name: str, size: int, response: Response) -> None:
	progress_bar = tqdm(total=size, unit='iB', unit_scale=True)
	with open(name, 'wb') as file:
		for chunk in response.iter_content(chunk_size=1024):
			if chunk:
				progress_bar.update(len(chunk))
				file.write(chunk)
	progress_bar.close()

if __name__ == '__main__':
	link = ""

	captcha : str = ""
	token : str = ''

	headers = {'Cookie': f'token={token}', 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'}
	cookies = {'captcha' : captcha}

	parts = extract(link)
	dl_url = get_download_url(parts, headers)
	print(dl_url)
	content = get_file_information(dl_url, headers, cookies)
	download(content['name'], content['size'], content['response'])
