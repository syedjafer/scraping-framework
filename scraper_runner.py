from scraper.scraper import Scraper

sc = Scraper(output_path=r"/home/syedjafer/Documents/AI - Doctor Initiative/data")
sc.collect_urls()
sc.collect_data()
