# -*- coding: utf-8 -*-


"""
Recordatorios

Reads events from flat text file.
Sends mails for today events.
"""

import sys, os
import datetime
import requests

from jinja2 import Environment, FileSystemLoader

from settings import *


def read_events_from_file(fname):
	"""
	Reads events from file
	"""
	with open(fname) as f:
		lines = f.read().splitlines()


	if len(lines) == 0: return None

	r = []
	line_counter = 0

	for line in lines:

		line_counter += 1
		
		if line.startswith(CHAR_COMMENT):
			continue

		data = line.split(CHAR_FIELD_SEPARATOR)
		if len(data) == 2:
			# only date and name
			date, name = data
			comment = None


		elif len(data) == 3:
			# date, name, and comment
			date, name, comment = data

		else:
			print("ERROR: cannot parse file.")
			print("line %d of file [%s]" % (line_counter, fname))
			sys.exit(1)

		date = datetime.datetime.strptime(date, "%Y-%m-%d")
		r.append((date, name, None))

	return r


def filter_today_events(events):
	"""
	Returns a list of the events whose day and month match with today's date.
	"""
	# events is a list of tuples.
	# Each tuple contains:
	# 	date  		a datetime object
	#   name  		name of the person whose event is today
	#   comment  	a comment. Can be None

	today = datetime.date.today()

	r = [ event for event in events 
		if (event[0].day == today.day) and (event[0].month == today.month)]

	return r


def send_mail(from_address, to_address, subject, text, html=None):

	url = 'https://api.mailgun.net/v2/{0}/messages'.format(MG_DOMAIN)

	if html:
		request = requests.post(url, auth=('api', MG_KEY), data={
				'from':  from_address,
				'to': to_address,
				'subject': subject,
				'text': text,
				'html': html,
			})

	else:
		request = requests.post(url, auth=('api', MG_KEY), data={
				'from':  from_address,
				'to': to_address,
				'subject': subject,
				'text': text,
			})

	print('Status: {0}'.format(request.status_code))
	print('Body:   {0}'.format(request.text))


def format_text_message(jinja_env, events):

	return format_message(jinja_env, TEXT_TEMPLATE_NAME, events)



def format_html_message(jinja_env, events):

	return format_message(jinja_env, HTML_TEMPLATE_NAME, events)


def format_message(jinja_env, template_file, events):

	if not os.path.exists(os.path.join(TEMPLATES_DIR, template_file)):
		return None

	template = jinja_env.get_template(template_file)
	today = datetime.date.today()
	r = template.render(events=events, today=today)
	return r


def main():
	
	today = datetime.date.today()

	env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
	mail_title = 'Cumpleaños para el día de hoy ({0})'.format(today.strftime("%Y-%m-%d"))

	events = read_events_from_file(DATAFILE)
	events = filter_today_events(events)

	if events:

		text_message = format_text_message(env, events)
		html_message = format_html_message(env, events)

		send_mail(
			MG_FROM_ADDRESS,
			MG_TO_ADDRESS, 
			mail_title,
			text_message,
			html_message,
		)

	else:
		print("No events for today ({0})".format(today.strftime("%Y-%m-%d")))


if __name__ == '__main__':
	main()