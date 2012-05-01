#/usr/bin/env Python3
import markdown

def output(string):
	string = markdown.markdown(string,['headerid(level=2)'])
	return string;

if __name__ == "__main__":
	print(output("ほげ\n----"))
