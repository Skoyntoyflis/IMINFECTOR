import time
import os
import sys
import json
from pathlib import Path
import argparse

from weibo_preprocessing import weibo_preprocessing

import numpy as np 
import pandas as pd 
import igraph as ig
import networkx as nx
import runpy

if __name__ == '__main__':

  os.path.join("..","Data","Weibo","Init_Data")
  weibo_preprocessing(os.path.join("..","Data","Weibo","Init_Data"))

  print("Reading network with networkx")
  G = nx.read_edgelist("../Weibo_network.txt",data=(("time", int),),create_using=nx.DiGraph())
  print("Transforming to undirected")
  H = G.to_undirected()
  print("Nodes in whole graph:",G.number_of_nodes())
  print("Edges in whole graph:",G.number_of_edges())



  print("Starting k-core decompositions\n")
  
  kG_previous = G
  #--------- Create k-core decomposed graphs and store them ---------
  for i in range(2,15):
    start = time.time()
    
    #--------- Create k-core decomposition ----------------
    kG = nx.k_core(kG_previous,k=i)
    print("Nodes in ",i,"-core graph:",kG.number_of_nodes())
    
    #--------- Drop nodes that are not in kG --------------
    nodes  =pd.DataFrame(kG.nodes()) # node_index, node_id
    nodes.columns = ['Node_id']
    nodes = nodes.astype('int64')
    
    df = pd.read_csv("../Weibo_network.txt",sep=" ",header=None) # node_id1, node_id2
    df.columns = ['Node_id1', 'Node_id2', 'Time']


    df_dr1 = df.drop(df.loc[~df['Node_id1'].isin(nodes['Node_id'])].index)
    df_dr2 = df_dr1.drop(df_dr1.loc[~df['Node_id2'].isin(nodes['Node_id'])].index)
    
    
    #--------- Store to file ------------------------------
    filename = "Weibo_network_k"+str(i)+"G.csv"
    p = "../K-core_networks/"
    df_dr2.to_csv(Path(p+filename),index=False,sep=",",header=False)
    
    kG_previous = kG
    print("Time taken for this decomposition is: %s seconds\n" % (time.time() - start))





  # #--------- Create K-Truss decomposed graphs and store them ---------
  # for i in range(2,5):
  #   df = pd.read_csv("../Data/Digg/Init_Data/digg_friends.csv",header=None) # mutual, time, node_id1, node_id2
  #   with open('../Data/Digg/Digg_incr_dic.json','r') as f:
  #     data = f.read()
  #   data = "[" + data + "]"
  #   dic = pd.read_json(data).transpose()# node_index, node_id

  #   #--------- Create K-truss decomposition ----------------
  #   tH = nx.k_truss(H,k=i)
  #   print("Nodes in ",i,"-truss graph:",tH.number_of_nodes())
    
  #   #--------- Drop nodes that are not in kG --------------
  #   nodes  =pd.DataFrame(tH.nodes()) # node_index, node_id of kG
    
  #   dic[1]=dic.index
  #   dic.reset_index(inplace=True)
  #   dic = dic.drop(['index'],axis=1)


  #   df.columns = ['Mutual', 'Time', 'Node_id1', 'Node_id2']
  #   dic.columns = ['Node_index', 'Node_id']
  #   nodes = nodes.reset_index()
  #   nodes.columns = ['Node_index_tH', 'Node_index']

  #   merged = pd.merge(dic,nodes,on='Node_index')

  #   df_dr1 = df.drop(df.loc[~df['Node_id1'].isin(merged['Node_id'])].index)
  #   df_dr2 = df_dr1.drop(df_dr1.loc[~df['Node_id2'].isin(merged['Node_id'])].index)
    
    
  #   #--------- Store to file ------------------------------
  #   filename = "digg_friends_t"+str(i)+"H.csv"
  #   p = "../Data/Digg/Init_Data/"
  #   df_dr2.to_csv(Path(p+filename),index=False,sep=",",header=False)

