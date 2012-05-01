Welcome Pysimb
==============

What is Pysimb?
---------------

 Pysimb is __Sim__ple __B__log System written by Python3.x .

Overview
--------

 Pysimb is influenced by [Blosxom](http://www.blosxom.com/).I think Blosxom System is Very Cool and Simple,and Powerful.and, Pysimb is also simple system.
 Of course,I know that Blosxom Clone [Pyblosxom](http://pyblosxom.bluesock.org/) is already exist.


Feature
-------

* Pysimb is written by Python3.
* Pysimb is very simple.
* Pysimb is plugin based system.


Configure
---------

 Configuration File is written by [Yaml](http://yaml.org/).

For Developer
-------------

 Pysimb is used to assemble the plug-in.There plug-in have Output method.In this way,Pysimb Main System import plugin seamlessly.

 Example

    Mainsystem ->
                  Body.output(use Haml)
                  entry.templete
                                -> Entry.output(use Markdown)
