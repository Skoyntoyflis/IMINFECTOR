import time
import os
import sys
import json
from pathlib import Path
import argparse

from digg_preprocessing import digg_preprocessing


import numpy as np 
import pandas as pd 
import igraph as ig
import networkx as nx
import runpy

os.path.join("..","Data","Digg","Init_Data")
digg_preprocessing(os.path.join("..","Data","Digg","Init_Data"))


# g = ig.Graph.Read_Ncol("../Weibo/Weibo_network.txt")
g = ig.Graph.Read_Ncol("../Digg_network.txt")
G = g.to_networkx()
H = G.to_undirected()
print("Nodes in whole graph:",G.number_of_nodes())
print("Edges in whole graph:",G.number_of_edges())


#--------- Create k-core decomposed graphs and store them ---------
for i in range(2,15):
  df = pd.read_csv("digg_friends.csv",header=None) # mutual, time, node_id1, node_id2
  with open('../Digg_incr_dic.json','r') as f:
    data = f.read()
  data = "[" + data + "]"
  dic = pd.read_json(data).transpose()# node_index, node_id

  #--------- Create k-core decomposition ----------------
  kG = nx.k_core(G,k=i)
  print("Nodes in ",i,"-core graph:",kG.number_of_nodes())
  
  #--------- Drop nodes that are not in kG --------------
  nodes  =pd.DataFrame(kG.nodes()) # node_index, node_id of kG
  
  dic[1]=dic.index
  dic.reset_index(inplace=True)
  dic = dic.drop(['index'],axis=1)


  df.columns = ['Mutual', 'Time', 'Node_id1', 'Node_id2']
  dic.columns = ['Node_index', 'Node_id']
  nodes = nodes.reset_index()
  nodes.columns = ['Node_index_kG', 'Node_index']

  merged = pd.merge(dic,nodes,on='Node_index')

  df_dr1 = df.drop(df.loc[~df['Node_id1'].isin(merged['Node_id'])].index)
  df_dr2 = df_dr1.drop(df_dr1.loc[~df['Node_id2'].isin(merged['Node_id'])].index)
  
  
  #--------- Store to file ------------------------------
  filename = "digg_friends_k"+str(i)+"G.csv"
  p = ""
  df_dr2.to_csv(Path(p+filename),index=False,sep=",",header=False)





#--------- Create K-Truss decomposed graphs and store them ---------
for i in range(2,7):
  df = pd.read_csv("digg_friends.csv",header=None) # mutual, time, node_id1, node_id2
  with open('../Digg_incr_dic.json','r') as f:
    data = f.read()
  data = "[" + data + "]"
  dic = pd.read_json(data).transpose()# node_index, node_id

  #--------- Create K-truss decomposition ----------------
  tH = nx.k_truss(H,k=i)
  print("Nodes in ",i,"-truss graph:",tH.number_of_nodes())
  
  #--------- Drop nodes that are not in kG --------------
  nodes  =pd.DataFrame(tH.nodes()) # node_index, node_id of kG
  
  dic[1]=dic.index
  dic.reset_index(inplace=True)
  dic = dic.drop(['index'],axis=1)


  df.columns = ['Mutual', 'Time', 'Node_id1', 'Node_id2']
  dic.columns = ['Node_index', 'Node_id']
  nodes = nodes.reset_index()
  nodes.columns = ['Node_index_tH', 'Node_index']

  merged = pd.merge(dic,nodes,on='Node_index')

  df_dr1 = df.drop(df.loc[~df['Node_id1'].isin(merged['Node_id'])].index)
  df_dr2 = df_dr1.drop(df_dr1.loc[~df['Node_id2'].isin(merged['Node_id'])].index)
  
  
  #--------- Store to file ------------------------------
  filename = "digg_friends_t"+str(i)+"H.csv"
  p = ""
  df_dr2.to_csv(Path(p+filename),index=False,sep=",",header=False)

