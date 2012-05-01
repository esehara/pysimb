import os,time

def output(target_dir):
	return_list = []
	file_list = []
	dir_list = os.listdir(target_dir)
	for dir_elem in dir_list:
		file_list.append((dir_elem,time.strftime('%Y/%m/%d %X',(time.localtime(os.path.getmtime(target_dir + "/" + dir_elem))))))
	for i,path in enumerate(sorted(file_list,key=lambda a: a[1],reverse=True)):
		return_list.append(path[0])
	return return_list
