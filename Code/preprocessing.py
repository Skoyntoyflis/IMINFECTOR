import os
from weibo_preprocessing import weibo_preprocessing
from digg_preprocessing import digg_preprocessing


"""
Main
"""
# def run():
if __name__ == '__main__':
	## Create folder structure
	# abspath = os.path.abspath(__file__)
	# dname = os.path.dirname(abspath)
	# os.chdir(os.path.join(dname,"..","Data"))
	# for dataset in ["Digg","Weibo","MAG"]:
	# 	for folder in ["Init_Data","Embeddings", "Seeds","Spreading"]:
	# 		os.makedirs(os.path.join(dataset,folder))
		
	ans = weibo_preprocessing(os.path.join("..","Data","Weibo","Init_Data"))
	# ans = digg_preprocessing(os.path.join("..","Data","Digg","Init_Data"))
	print(ans)
