"""
Python Simple Gmail to Text Save System for Cron.

Usage:
	Add setting for clontab.
	python3 YOUR-EMAIL-ID YOUR-EMAIL-PASSWORD SAVE_DIR

	or,this file set (imap valiable).
	target_dir -> SAVE_DIR
"""
import sys,os,re
import imaplib
import email.parser,email.utils

def _parser(num):
	typ,data = MailSystem.fetch(str(num),"(RFC822)")
	pre_message = email.parser.HeaderParser().parsestr(str(data[0][1],"UTF-8"))
	message = email.parser.HeaderParser().parsestr(
			str(data[0][1],"UTF-8" if pre_message.get_content_charset() is None 
				else pre_message.get_content_charset()))
	email_subject = email.header.decode_header(message['Subject'])[0]
	return (email_subject[0] if isinstance(email_subject[0],str) else 
			str(email_subject[0],"UTF-8" if email_subject[1] is None 
				else email_subject[1]),message.get_payload())

"--- Configure List ---"

imap = { "domain"  :"imap.gmail.com"
		,"user"    : None
		,"password": None
		,"target_dir":None
		,"mailbox" : "INBOX"
		,"check"   : 5
		,"use_subject":"Pysimb"}

if imap['user'] is None and imap['password'] is None and imap["target_dir"] is None:
	imap['user'] = sys.argv[1]
	imap['password'] = sys.argv[2]
	imap['target_dir'] = sys.argv[3]

if imap['user'] is None or imap['password'] is None or imap['target_dir'] is None:
	print("Oops!! Configuration Error.Check crontool/mail2text.py ;) ")
	exit()

MailSystem = imaplib.IMAP4_SSL(imap["domain"])
MailSystem.login(imap['user'],imap['password'])
typ,Maillist_num = MailSystem.select(imap['mailbox'])
Maillist_num = int(Maillist_num[0])

for boxlist in range(imap["check"]):
	subject,body = _parser(Maillist_num - boxlist)
	if re.compile("^\["+imap["use_subject"] + "\]").search(subject):
		target_file = imap["target_dir"] + subject.replace("[" + imap["use_subject"] + "]","").replace(" ","")
		if not os.path.exists(target_file):
			t_file = open(target_file,"w")
			t_file.write(body)
			t_file.close()
