#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys,io,time
import cgi
import os
import yaml
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

class Pysimb:
	def __init__(self):
		config_file = open_utf8("config.yaml")
		self.configure = yaml.load(config_file)
		self.cgi_value = cgi.parse_qs(os.environ['QUERY_STRING']) if 'QUERY_STRING' in os.environ else {}

	def read_module(self):
		"Dinamic Module Import"
		self.modules = {}
		load_modules = __import__("lib." + self.configure['Output']['Body'])
		self.modules['Body'] = getattr(load_modules,dir(load_modules)[-1])
		load_modules = __import__("lib." + self.configure['Output']['Entry'])
		self.modules['Entry'] = getattr(load_modules,dir(load_modules)[-1])

	def bodyhtml(self,string):
		string = self.modules['Body'].output(string)
		string = self.parse_string_body(string)
		return self.parse_string_index(string)

	def entryhtml(self,string):
		dp("[Run] Entryhtml is Start.\n")
		dp("[Show] String is " + string)
		string = self.modules['Body'].output(string)
		dp("[Run] Module is Running.")
		string = self.parse_string_entry(string)
		return self.parse_string_body(string)

	def escape_cgi(self,string):
		return string.replace("/","")
	
	def parse_string_index(self,string):
		filelist_array = self.generator_filelist(self.configure['Dir']['Entry'])
		entrylist_string = "";
		for file_item in filelist_array:
			load_entry_array = open_utf8(self.configure['Dir']['Entry'] + "/" + file_item).readlines()
			entry_title = load_entry_array.pop(0)
			load_entry_string = "".join(load_entry_array)
			load_entry_string = self.modules['Entry'].output(load_entry_string)
			entrylist_string = entrylist_string + (
					"<h2>" + 
						"<a href='./index.py?file=" + file_item + "'>"
						+ entry_title 
						+ "</a>"
						+ load_entry_string
					+ "<h2>")
		string = string.replace("@{entrylist}",
								entrylist_string)
		return string

	def parse_string_entry(self,string):
		self.cgi_value['file'][0] = self.escape_cgi(self.cgi_value['file'][0])
		load_entry_array = open_utf8(self.configure['Dir']['Entry'] + "/" + self.cgi_value['file'][0]).readlines()
		dp("[Run] load_entry_array is loaded")
		entry_title = load_entry_array.pop(0)
		load_entry_string = "".join(load_entry_array)
		load_entry_string = self.modules['Entry'].output(load_entry_string)
		string = string.replace("@{entry_body}",
								 load_entry_string)
		string = string.replace("@{entry_title}",
								 entry_title)
		return string

	def parse_string_body(self,string):
		load_header = open_utf8(self.configure['Dir']['Templete'] + "/" + self.configure['File']['Head']).read()
		load_header = self.modules['Body'].output(load_header)
		load_footer = open_utf8(self.configure['Dir']['Templete'] + "/" + self.configure['File']['Foot']).read()
		load_footer = self.modules['Body'].output(load_footer)
		string = string.replace("!{HEAD}",load_header)
		string = string.replace("!{FOOT}",load_footer)
		string = self.parse_string_shered(string)
		return string

	def parse_string_shered(self,string):
		string = self.parse_publish_css(string)
		string = string.replace("@{filelist}",
								self.parse_filelist(self.configure['Dir']['Entry']))
		string = string.replace("@{title}",
								self.configure['Blog']['Title'])
		string = string.replace("@{author}",
								self.configure['Blog']['Author'])
		string = string.replace("@{description}"
								,self.configure['Blog']['Description'])
		string = string.replace("@{public_dir}",
								self.configure['Dir']['Public'])
		string = string.replace("@{css_file}",
								self.configure['File']['CSS'])
		string = string.replace("@{link}",
								self.configure['Blog']['Link'])
		return string

	def parse_publish_css(self,string):
		if "CSS" in self.configure['Output']:
			load_modules = __import__("lib." + self.configure['Output']['Entry'])
			self.modules['CSS'] = getattr(load_modules,dir(load_modules)[-1])
			css_string = self.modules['CSS'].output(
					open_utf8(self.configure['Dir']['Public'] + '/' + self.configure['File']['CSS']).read())
			return string
		else:
			return string.replace("@{publish_css}","<link rel='stylesheet' href='@{public_dir}/@{css_file}' type='text/css'>")
	
	def load_module(self,target_mod):
		modules = __import__("lib." + target_mod)
		for i,mod_item in enumerate(dir(modules)):
			if mod_item == target_mod: return getattr(modules,dir(modules)[i]) 

	def generate_from_metalibrary(self,lib_name):
		generator_meta = self.load_module(lib_name)
		print(generator_meta.output(self.configure))

	def generator_filelist(self,target_dir):
		generator_filelist = self.load_module(self.configure['Generator']['Filelist'])
		return generator_filelist.output(target_dir + "/")

	def parse_filelist(self,target_dir):
		return_string = ""
		file_list = self.generator_filelist(target_dir)
		for file_item in file_list:
			entrytitle = open_utf8(target_dir + "/" + file_item).readlines()[0]
			return_string = return_string + "<li><a href='index.py?file=" + file_item + "'>" + entrytitle.rstrip("\n") + "</a></li>\n"
		return return_string

def open_utf8(filename):
	return open(filename,encoding="UTF-8")

def dp(string):
	"""
	Print Function for Debug in Browser.
	"""
	debug = False
	er = "<br />"
	if debug:
		print(string,er)
	
def main():
	system = Pysimb()
	system.read_module()
	dp("[Run]Start\n")
	if "meta"  in system.cgi_value:
		if system.cgi_value["meta"][0] in system.configure['Meta']:
			system.generate_from_metalibrary(system.configure['Meta'][system.cgi_value["meta"][0]])
			sys.exit()
	print("Content-Type: text/html;charset=UTF-8\n\n")
	if "file" in system.cgi_value:
		print(system.entryhtml(
				open_utf8(system.configure['Dir']['Templete'] + "/" + system.configure['File']['Entry']).read()
			)) 
	else:
		print(system.bodyhtml(
				open_utf8(system.configure['Dir']['Templete'] + "/" + system.configure['File']['Index']).read()
			))

if __name__ == "__main__" : main()
