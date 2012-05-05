"""
Yaml Filelist Module 

If You rewrite some entry,the entry is up in Pysimb.This Module can list entry.

usage:
    It is Setting by Yaml File.File Name is '(entry dir)/entry.yaml'.

example:
    - foo.markdown
    - bar.markdown
    ...etc,etc

"""
import yaml

def output(target_dir):
	return yaml.load(open(target_dir + "entry.yaml").read())
