# -*- coding: utf-8 -*-
import time
import os
import sys
import json
import argparse
import extract_feats_and_trainset
import preprocess_for_imm
import rank_nodes
import infector
import iminfector
import evaluation


parser = argparse.ArgumentParser()

parser.add_argument('--sampling_perc', type=int, default=120,help='')
parser.add_argument('--learning_rate', type=float, default=0.1,help='')
parser.add_argument('--n_epochs', type=int, default=5,help='')
parser.add_argument('--embedding_size', type=int, default=50,help='')
parser.add_argument('--num_neg_samples', type=int, default=10,help='')


if __name__ == '__main__':
	start = time.time()
	abspath = os.path.abspath(__file__)
	dname = os.path.dirname(abspath)
	os.chdir(os.path.join(dname,"..","Data"))
	args=parser.parse_args()
	
	#--- Parameters
	learning_rate = float(args.learning_rate)
	embedding_size = int(args.embedding_size)
	sampling_perc = int(args.sampling_perc)
	n_epochs = int(args.n_epochs)
	num_neg_samples = int(args.num_neg_samples)

	log= open("time_log.txt","a")


	network = "/home/mdakm/Dimitris/IMINFECTOR/Data/Digg/K-truss_networks/Digg_network_t7H.txt"
	
 
	for fn in ["Digg"]: #"Weibo","Digg","mag"
		network = fn+"/"+fn+"_network.txt"
		extract_feats_and_trainset.run(fn,sampling_perc,log, network)
		preprocess_for_imm.run(fn,log, network)
		rank_nodes.run(fn) 
		infector.run(fn,learning_rate,n_epochs,embedding_size,num_neg_samples,log)
		iminfector.run(fn,embedding_size,log)
		evaluation.run(fn,log)
	
	print("--- %s seconds ---\n" % (time.time() - start))
	log.close()

