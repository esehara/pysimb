import os
import time
def load_module(target_mod,prefix):
	if __name__ == "__main__":
		return __import__(target_mod)
	else:
		load_modules = __import__(prefix + target_mod)
		for i,mod_elem in enumerate(dir(load_modules)):
			if mod_elem == target_mod:return getattr(load_modules,dir(load_modules)[i])


def output(configure):
	prefix = "" if __name__ == "__main__" else "lib."
	itemlist = []
	target_dir = ("../" if __name__ == "__main__" else "./") + configure["Dir"]["Entry"] + "/"
	file_gen  = load_module(configure["Generator"]["Filelist"],prefix)
	dir_list = file_gen.output(target_dir)
	entry_gen = load_module(configure["Output"]["Entry"],prefix)
	configure['LatestTime']  = time.strftime("%a,%d %b %Y %H:%M:%S " + configure["Time"]["Fix"],(time.localtime(os.path.getmtime(target_dir + "/" + dir_list[0]))))
	file_list = []
	for dir_elem in dir_list:
		entrydata  = open(target_dir + dir_elem,encoding="UTF-8").readlines()
		entrydate  = time.strftime("%a,%d %b %Y %H:%M:%S " + configure["Time"]["Fix"],(time.localtime(os.path.getmtime(target_dir + "/" + dir_elem))))
		entrytitle = entrydata.pop(0).rstrip("\n")
		entrybody  = "".join(entrydata)
		entrybody  = entry_gen.output(entrybody)
		itemlist.append({ "title":entrytitle
						 ,"link":configure["Blog"]["Link"] + "index.py?file=" + dir_elem
						 ,"description":entrybody
						 ,"date":entrydate})
	return generate_string(itemlist,configure)

def generate_string(itemlist,configure):
	string = '''Content-Type:text/xml

<?xml version="1.0" encoding="UTF-8" ?>
	<rss version="2.0"
		xmlns:dc="http://purl.org/dc/elements/1.1"
		xmlns:sy="http://purl.org/rss/1.0/mpdules/syndication/"
		xmlns:admin="http://webns.net/mvcb/"
		xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
	<channel>
		<title>%s</title>
		<description>%s</description>
		<dc:creator>%s</dc:creator>
		<dc:date>%s</dc:date>
	''' % (  configure["Blog"]["Title"]
			,configure["Blog"]["Description"]
			,configure["Blog"]["Author"]
			,configure["LatestTime"])
	for item_elem in itemlist:
		string = string + ("""
		<item>
			<title>%s</title>
			<link>%s</link>
			<description>%s</description>
			<dc:date>%s</dc:date>
		</item>
		""" % (item_elem['title']
			  ,item_elem['link']
			  ,item_elem['description']
			  ,item_elem['date']))
	string = string + """</channel>
</rss>"""
	return string

if __name__ == "__main__":
	import yaml
	config_file = open("../config.yaml",encoding="UTF-8")
	config_file = yaml.load(config_file)
	output(config_file)
