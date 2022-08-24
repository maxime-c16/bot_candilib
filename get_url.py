from __future__ import print_function

import os.path
import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from base64 import urlsafe_b64decode
from base64 import urlsafe_b64encode

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def search_messages(service, query):
	result = service.users().messages().list(userId='me',q=query).execute()
	messages = [ ]
	if 'messages' in result:
		messages.extend(result['messages'])
	while 'nextPageToken' in result:
		page_token = result['nextPageToken']
		result = service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
		if 'messages' in result:
			messages.extend(result['messages'])
	return messages

def get_size_format(b, factor=1024, suffix="B"):
	"""
	Scale bytes to its proper byte format
	e.g:
		1253656 => '1.20MB'
		1253656678 => '1.17GB'
	"""
	for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
		if b < factor:
			return f"{b:.2f}{unit}{suffix}"
		b /= factor
	return f"{b:.2f}Y{suffix}"


def clean(text):
	return "".join(c if c.isalnum() else "_" for c in text)

def parse_parts(service, parts, folder_name, message):
	"""
	Utility function that parses the content of an email partition
	"""
	if parts:
		for part in parts:
			filename = part.get("filename")
			mimeType = part.get("mimeType")
			body = part.get("body")
			data = body.get("data")
			file_size = body.get("size")
			part_headers = part.get("headers")
			if part.get("parts"):
				parse_parts(service, part.get("parts"), folder_name, message)
			if mimeType == "text/plain":
				if data:
					text = urlsafe_b64decode(data).decode()
			elif mimeType == "text/html":
				if not filename:
					filename = "index.html"
				filepath = os.path.join(folder_name, filename)
				with open(filepath, "wb") as f:
					f.write(urlsafe_b64decode(data))
			else:
				for part_header in part_headers:
					part_header_name = part_header.get("name")
					part_header_value = part_header.get("value")
					if part_header_name == "Content-Disposition":
						if "attachment" in part_header_value:
							attachment_id = body.get("attachmentId")
							attachment = service.users().messages() \
										.attachments().get(id=attachment_id, userId='me', messageId=message['id']).execute()
							data = attachment.get("data")
							filepath = os.path.join(folder_name, filename)
							if data:
								with open(filepath, "wb") as f:
									f.write(urlsafe_b64decode(data))

def parse_parts(service, parts, folder_name, message):
	"""
	Utility function that parses the content of an email partition
	"""
	if parts:
		for part in parts:
			filename = part.get("filename")
			mimeType = part.get("mimeType")
			body = part.get("body")
			data = body.get("data")
			file_size = body.get("size")
			part_headers = part.get("headers")
			if part.get("parts"):
				parse_parts(service, part.get("parts"), folder_name, message)
			if mimeType == "text/plain":
				if data:
					text = urlsafe_b64decode(data).decode()
					return(text)
			elif mimeType == "text/html":
				if not filename:
					filename = "index.html"
				filepath = os.path.join(folder_name, filename)
			else:
				for part_header in part_headers:
					part_header_name = part_header.get("name")
					part_header_value = part_header.get("value")
					if part_header_name == "Content-Disposition":
						if "attachment" in part_header_value:
							attachment_id = body.get("attachmentId")
							attachment = service.users().messages() \
										.attachments().get(id=attachment_id, userId='me', messageId=message['id']).execute()
							data = attachment.get("data")
							filepath = os.path.join(folder_name, filename)

def read_message(service, message):
	"""
	This function takes Gmail API `service` and the given `message_id` and does the following:
		- Downloads the content of the email
		- Creates a folder for each email based on the subject
		- Downloads text/html content (if available) and saves it under the folder created as index.html
		- Downloads any file that is attached to the email and saves it in the folder created
	"""
	msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
	payload = msg['payload']
	headers = payload.get("headers")
	parts = payload.get("parts")
	folder_name = "email"
	has_subject = False
	if headers:
		for header in headers:
			name = header.get("name")
			value = header.get("value")
			if name.lower() == "subject":
				has_subject = True
				folder_name = clean(value)
				folder_counter = 0
	data = parse_parts(service, parts, folder_name, message)
	return data

def get_url_from_email(data):
	if data:
		i = 0
		for line in data.split("\n"):
			if "https" in line:
				if i == 0:
					i += 1
					continue
				else:
					return line

def	refactor_url(url):
	if url:
		url = url.replace("[", "")
		url = url.replace("]", "")
		return url

def get_url():
	"""Shows basic usage of the Gmail API.
	Lists the user's Gmail labels.
	"""
	creds = None
	if os.path.exists('token.json'):
		creds = Credentials.from_authorized_user_file('token.json', SCOPES)
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				'credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
		with open('token.json', 'w') as token:
			token.write(creds.to_json())

	try:
		service = build('gmail', 'v1', credentials=creds)
		results = search_messages(service, "noreply@interieur.gouv.fr")
		print ("searching for Candilib mail...")
		data = read_message(service, results[0])
		print ("found mail")
		print ("refactoring url...")
		new_url = refactor_url(get_url_from_email(data))
		return new_url

	except HttpError as error:
		print(f'An error occurred: {error}')

sys.modules[__name__] = get_url
