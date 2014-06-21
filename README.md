# Reminders

*Because some mail group's calendars suck.*

Reminder is a script that reads events and dates from a flat text file and sends an email with today events. I use this script to send birthday reminders to my school's class mailing list. 

## Requirements

See requirements.txt.  Reminders has been tested on Python 2.7.5. Reminders expects a [MailGun](http://www.mailgun.com/) account to deliver mail.  (Free MailGun accounts allow you to send up to 10,000 emails per month.)

## Instalation

The recommended method for installing this script is to create a `virtualenv`, install the requirements there via `pip`, and run the script periodically via a crontab job.


	$ mkvirtualenv reminders
	$ pip install -r requirements.txt

	# Make copies of sample settings and data files.
	$ cp settings-sample.py settings.py
	$ cp sample-data data

To set the crontab job, use `crontab -e` and specify the python path to your virtualenv's Python binary.  

	(reminders)$ which python
	/home/youruser/.virtualenvs/reminders/bin/python

	(reminders) $ crontab -e
	00 07 * * *      /home/youruser/.virtualenvs/reminders/bin/python /home/youruser/reminders/main.py


## Configuration file

### Program specific settings

	DATAFILE = 'data'
	CHAR_COMMENT = '#'
	CHAR_FIELD_SEPARATOR = '|'
	TEMPLATES_DIR = 'templates'
	TEXT_TEMPLATE_NAME = 'text_reminder.html'
	HTML_TEMPLATE_NAME = 'html_reminder.html'

### Mailgun specific config options

	MG_KEY ='key-1234567890abcdefghijklmn'
	MG_DOMAIN = 'mg.example.com'
	MG_RECEPIENT = 'recepient@example.com'



## Data file format

The data file format is pretty straightforward.  

* Comments lines begin with `#`.  
* Each line is an event in the form `[date]|[event name]|[comment]`.

* The event's date must be specified in ISO format (i.e., YYYY-MM-DD).
* The vertical bar `|` char is used as field separator.
* Comments are optional.

### Example

	# Doe's Family birthdays
	1969-01-02|Jane Doe
	1969-01-04|John Doe


## Templates

Templates are parsed using [Jinja2](http://jinja.pocoo.org/docs/).  You can refer to Jinja2's for the template's language syntax.  

Two template files are used to generate the mail that is sent with the reminders of the day:

* `text_reminder.html`, used to render the text part of the email.
* `html_reminder.html`, used to render the html part of the email.

The template's filenames can be configured in the `settings.py` file.

When the templates are rendered, two variables are exposed:

* `events`, a list of events.  Each event is a tuple in the form (date, event name, comment).
* `today`, today's date.



-----------
Happy coding.




