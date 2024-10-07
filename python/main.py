from typing import Optional
from urllib.parse import quote

import hashlib
import requests
import time
import threading
import json

CAPTCHA_URL = "https://workupload.com/captcha"
PUZZLE_URL = "https://workupload.com/puzzle"

# TODO: captcha solver works but need to do the full request fluidly
# Download URL -> Solve Captcha for download url (set referer) -> Captcha request -> Request again with cookies once solved

def sha256(message):
	"""Compute the SHA-256 hash of a given message."""
	return hashlib.sha256(message.encode()).hexdigest()

def submit_captcha(data, solutions):
	"""Submit the captcha solutions to the server."""
	captcha_value = '+'.join(map(str, solutions)) + '+'
	headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'}
	cookies = {'captcha' : quote(json.dumps(data))}
	print(headers)
	response = requests.post(CAPTCHA_URL, headers=headers, cookies=cookies, data={'captcha': captcha_value})
	print(response.headers, response.cookies)
	response.raise_for_status()
	return response.headers

def solve_captcha_puzzle(data : dict) -> Optional[list]:
	"""Solve the given captcha puzzle"""
	found = []
	puzzle = data['puzzle']
	find_hashes = data['find']
	for i in range(data['range']):
		# Concatenate puzzle with the current index
		test_string = f"{puzzle}{i}"
		hash_hex = sha256(test_string)
		# Check if the computed hash is in the find list
		if hash_hex in find_hashes:
			found.append(i)
		# If we found all required hashes, we can break early
		if len(found) == len(find_hashes):
			break
	if found:
		return found
	return None

def solve_captcha():
	"""Fetch the puzzle and solve it."""
	response = requests.get(PUZZLE_URL)
	response.raise_for_status()  # Raise an error for bad responses
	res = response.json()
	if not res.get("success"):
		print("Failed to retrieve puzzle.")
		return
	found = solve_captcha_puzzle(res['data'])
	if found:
		print(found)
		submit_captcha(res['data'], found)

def periodic_solver():
	"""Run the solve_puzzle function periodically."""
	while True:
		solve_captcha()
		time.sleep(20)  # Wait for 20 seconds before the next attempt

periodic_solver()
