import os
import re
import traceback

def get_speciality_data():
	try:
		specialities = {}
		speciality_path = os.path.join(os.getcwd(), "static_input", "specialities.txt")
		specialty_file = open(speciality_path,"r")
		data = specialty_file.readlines()
		for line in data:
			line = line.strip().split(",")
			specialities[line[1]] = line[0]
		return specialities
	except Exception as ex:
		traceback.print_exc()
		raise ex

def get_state_code_data():
	try:
		state_zip_code = []
		us_pincode_path = os.path.join(os.getcwd(), "static_input", "us_pincode.txt")
		state_zip_file = open(us_pincode_path,"r")
		data = state_zip_file.readlines()
		for line in data:
			line = line.strip().split(",")
			state_zip_code.append( (line[0], line[1]))
		return state_zip_code
	except Exception as ex:
		traceback.print_exc()
		raise ex

def parseCookieFile(cookiefile):
	cookies = {}
	try:
		with open (cookiefile, 'r') as fp:
			for line in fp:
				if not re.match(r'^\#', line):
					lineFields = line.strip().split('\t')
					try:
						cookies[lineFields[5]] = lineFields[6]
					except:
						pass
		return cookies
	except Exception as ex:
		traceback.print_exc()
		raise ex
