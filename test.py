import nose
from nose.tools import *
import yaml
import index
def read_configure():
	return yaml.load(open("config.yaml","r"))

def read_configure_test():
	"Configure File is Readable."
	testconfig = index.read_configure()
	ok_("Blog" in testconfig)
	ok_("Author" in testconfig['Blog'])
	ok_("Templete" in testconfig)
	ok_("Body" in testconfig['Templete'])

def read_html_test():
	"""
	Importable from 'eval'
	testconfig = yaml.load(open("config.yaml","r"))
	load_module = __import__("lib." + testconfig['Templete']['Body'])
	output = getattr(load_module,dir(load_module)[-1])
	"""
	output = index.read_module("haml")
	eq_(output.html_output("h1") ,"h1\n")

if __name__ == "__main__": nose.main()
