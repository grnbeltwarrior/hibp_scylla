#!/usr/bin/env python3

# Have I been pwned with option to lookup on scylla.sh
# Test email: rudolphthered@hotmail.com, this was used in TryHackMe's Advent of Cyber 2.
# Like this: https://scylla.sh/search/?q=email:rudolphthered@hotmail.com

# Requirements:
#	https://haveibeenpwned.com/API/Key
#		You need a key, so you can procure one here with an email address and $3.50 per month.

import json
import os
import argparse
import requests
import time

# Credit to @m0nkeyplay for doing a lot of the heavy lifting of the HIBP API calls.
# https://github.com/m0nkeyplay/hibp_quickCheck/blob/master/hibp_check.py
# I took what I needed and left the rest, SOP for @grnbeltwarrior.

# Take either single email address or from a list:
def how2use():
	print("""
	########################################################################
	##                Have I been pwned? Is it in Scylla?                 ##
	##                          @GrnBeltWarrior                           ##
	##                                                                    ##
	##  Switches:                                                         ##
	##  	-e <email>                                                    ##
	##  	-f <file>                                                     ##
	##  	-s optional: boolean to check scylla.sh API for password(s)   ##
	## ./hibp_scylla.py                                                   ##
	## ./hibp_scylla.py -e rudolphthered@hotmail.com -s                   ##
	## ./hibp_scylla.py -f ./email_list.txt -s                            ##
	########################################################################
	""")

ap = argparse.ArgumentParser()
ap.add_argument("-e", "--email", required=False, help="Search for a single email.")
ap.add_argument("-f", "--file", required=False, help="Grab emails from a list of emails: -f /path/to/file.txt")
ap.add_argument("-s", "--scylla", action="store_true", required=False, help="Used to query Scylla.sh API for password.")
args = vars(ap.parse_args())

if args['email']:
	chkType = 'email'
	chkIt = args['email']
	scylla = args['scylla']
elif args['file']:
	chkType = 'file'
	chkIt = args['file']
	scylla = args['scylla']
else:
	how2use()
	exit()

headers = {}
#HIBP API:
headers['content-type']= 'application/json'
headers['api-version']= '3'
headers['user-agent']= 'grnbeltwarrior'
headers['hibp-api-key']= 'https://haveibeenpwned.com/API/Key'

def breach(email, scylla):
	url = 'https://haveibeenpwned.com/api/v3/breachedaccount/'+email+'?truncateResponse=false'
	try:
		response = requests.get(url, headers=headers)
	except:
		print("We were unable to connect.")
		exit()
	if response.status_code == 404:
		print(f"{email} was not found in a breach.")
	elif response.status_code == 200:
		data = response.json()
		print(f"Breach details for {email}")
		#print(f"Details: {data}")
		for result in data:
			breach = result['Name']
			domain = result['Domain']
			breachDate = result['BreachDate']
			sensitive = result['IsSensitive']
			print(f"\tAccount: {email}\n\tBreach: {breach}\n\tSensitive: {sensitive}\n\tDomain: {domain}\n\tBreach Date:{breachDate}\n\t")
		if scylla == True:
			# Scylla.sh API:
			print("Checking Scylla.sh")
			your_lucene_query = "email:" + email
			payload = {'q': your_lucene_query, 'size': '100', 'start': '0'}
			r = requests.get('https://scylla.sh/search', params=payload)
			scylla_data = r.json()
			if scylla_data:
				for scylla_result in scylla_data:
					try:
						domain = scylla_result['fields']['domain']
					except:
						domain = ""
					try:
						email = scylla_result['fields']['email']
					except:
						email = ""
					# Never underestimate an empty password
					try:
						password = scylla_result['fields']['password']
					except:
						password = ""
					if password == "":
						print(f"Scylla Result for: {email} from: {domain} with no password recorded.")
					else:
						print(f"Scylla Result for: {email} from: {domain} with a password of: {password}")
			else:
				print(f"No Scylla entries for {email}")
			print(f"\n\n")

if __name__ == '__main__':
	how2use()
	print(args)
	if headers['hibp-api-key']=='https://haveibeenpwned.com/API/Key':
		print(f"The API Key was not correctly set, it costs $3.50 per month, at the time of this scripts creation.\nRegister @ {headers['hibp-api-key']}")
		exit()
	if chkType == 'email':
		breach(chkIt, scylla)
	elif chkType == 'file':
		if not os.path.isfile(chkIt):
			print(f"Can not open specified path/file {chkIt}")
		else:
			get_emails = open(chkIt, 'r')
			for line in get_emails:
				scrubEmail = line.strip()
				breach(scrubEmail, scylla)
				time.sleep(5)
			get_emails.close()

	else:
		print("Danger Will Robinson! DANGER!")
