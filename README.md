# hibp_scylla

Dependancies:
You need an API key for HIBP. It's $3.50 a month. I wish it were free but here we are and it is not my call.

Python script to leverage haveibeenpwned.com and scylla.sh to see if you have been pwned and if a passwords is out there for that account.

	########################################################################
	##                Have I been pwned? Is it in Scylla?                 ##
	##                          @GrnBeltWarrior                           ##
	##                                                                    ##
	##  Switches:                                                         ##
	##  	-e <email>                                                      ##
	##  	-f <file>                                                       ##
	##  	-s optional: boolean to check scylla.sh API for password(s)     ##
	## ./hibp_scylla.py                                                   ##
	## ./hibp_scylla.py -s -e rudolphthered@hotmail.com                   ##
	## ./hibp_scylla.py -s -f ./email_list.txt -s                         ##
	########################################################################
