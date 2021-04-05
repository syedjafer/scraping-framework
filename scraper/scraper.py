from util.data_source import get_speciality_data, get_state_code_data, parseCookieFile
from constant import scraper as con_scraper
from logger.logger import Logger
import traceback
from web_connection.req import get_new_tr_obj
from web_connection.timer import get_request_object
import os
import requests
from bs4 import BeautifulSoup

class Scraper:
	def __init__(self, output_path):
		self.output_path = output_path
		self.logger = Logger(out_path=self.output_path)
		self.all_urls = set()
		self.result = []

	def collect_urls(self):
		try:
			specialities = get_speciality_data()
			state_code_data = get_state_code_data()
			for speciality_key, code in specialities.items():
				for item in state_code_data:
					furl = con_scraper.SPECIALITY_URL.format(code, item[0], item[1])
					self.all_urls.add(furl)
			print(len(self.all_urls))
		except Exception as ex:
			traceback.print_exc()
			raise ex

	def collect_data(self):
		res = open("all_result_2.csv","a")
		req_obj = get_new_tr_obj()
		cookies = parseCookieFile(cookiefile=os.path.join(os.getcwd(), "static_input", "cookies.txt" ))
		try:
			for url in self.all_urls:
				# req_obj = get_new_tr_obj()
				try:
					req = req_obj.get(url, timeout=30)
					if req.status_code == 200:
						try:
							soup = BeautifulSoup(req.content, "html.parser")
							trs = soup.find_all("tr")
							for row in range(1,len(trs)):
								try:
									each_data = trs[row].find_all("td")
									specialty_name = each_data[1].text.strip() if each_data[1] else None
									location = each_data[2].text.strip().replace(","," ") if  len(each_data)>2 and each_data[2] else None
									doc_name = each_data[0].text
									doc_url = each_data[0].find("a")
									doc_url = doc_url["href"] if doc_url else ""
									actual_doc_url = con_scraper.BASE_URL + doc_url
								except Exception as ex:
									traceback.print_exc()
								else:
									if actual_doc_url != "https://doctorfinder.ama-assn.org/doctorfinder/":
										self.logger.info( "{}, {}".format(specialty_name.strip(), doc_name.strip().replace("\n","")))
										fdata = "|".join([ str(specialty_name).strip().replace("\n",""), str(location).strip().replace("\n",""), str(doc_name).strip().replace("\n",""), actual_doc_url.strip() ])+"\n"
										# self.result.append(fdata)
										print( "{}, {}".format(specialty_name.strip(), doc_name.strip().replace("\n","")))

										res.write(fdata)
						except Exception as ex:
							traceback.print_exc()
							# raise ex
				except Exception as ex:
					pass
			res.close()
		except Exception as ex:
			traceback.print_exc()
			# raise ex
