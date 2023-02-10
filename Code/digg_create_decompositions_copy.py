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
import networkit as nk

if __name__ == '__main__':
  os.chdir(os.path.join("..","Data","Digg","Init_Data"))
  # digg_preprocessing(os.path.join("..","Data","Digg","Init_Data"))

  # print("Reading network with networkx")
  # G = nx.read_edgelist("../Digg_network.txt",data=(("time", int),),create_using=nx.DiGraph())
  # no_nodes = G.number_of_nodes()
  # no_edges = G.number_of_edges()
  # print("Nodes in whole graph:",no_nodes)
  # print("Edges in whole graph:",no_edges)


  
  print("Reading network with networkit")
  start = time.time()
  G = nk.graphio.readGraph("../Digg_network.txt", fileformat= nk.graphio.Format.EdgeList, separator=" ", firstNode=0, continuous=False, directed=True)
  # G = nk.nxadapter.nx2nk(G)
  no_nodes = G.numberOfNodes()
  no_edges = G.numberOfEdges()
  print(G.isWeighted(), G.isDirected())
  print("Nodes in whole graph:",no_nodes)
  print("Edges in whole graph:",no_edges)

  nodeIdMap = nk.graphtools.getContinuousNodeIds(G)
  
  print(nodeIdMap)
  
  print("Starting k-core decompositions\n")
  kG = nk.centrality.CoreDecomposition(G, storeNodeOrder=True)
  kG.run()
  # list_k_core = kG.maxCoreNumber()
  # print(set(kG.scores()[:10]))
  # print(set(kG.getNodeOrder()[:10]))
  part = kG.getPartition()
  
  k=2
  
  members=[]
  for i in range(1,k):
    members = members + list(part.getMembers(i))
  
  # print(part.subsetSizes())


  
  print("Nodes in ",k,"-core graph:",(no_nodes-len(members)))
  
  nodes_to_drop = pd.DataFrame(members)
  nodes_to_drop.columns = ['Node_id']
  nodes_to_drop = nodes_to_drop.astype('int64')
  
  df = pd.read_csv("../Digg_network.txt",sep=" ",header=None) # node_id1, node_id2
  df.columns = ['Node_id1', 'Node_id2', 'Time']
  
  print(nodes_to_drop)
  print(df.loc[df['Node_id1'].isin(nodes_to_drop['Node_id'])].index)
  # print(df.loc[df['Node_id2'].isin(nodes_to_drop['Node_id'])].index)
  
  # df_dr1 = df.drop(df.loc[df['Node_id1'].isin(nodes_to_drop['Node_id'])].index)
  # df_dr2 = df_dr1.drop(df_dr1.loc[~df['Node_id2'].isin(nodes_to_drop['Node_id'])].index)
  
  print("Time taken for this decomposition is: %s seconds\n" % (time.time() - start))
  
  
  
  
  
  # # kG_previous = G
  # #--------- Create k-core decomposed graphs and store them ---------
  # for i in range(2,2):
  #   start = time.time()
    
  #   #--------- Create k-core decomposition ----------------
  #   kG = nx.k_core(G,k=i)
  #   print("Nodes in ",i,"-core graph:",kG.number_of_nodes())
    
  #   #--------- Drop nodes that are not in kG --------------
  #   nodes  =pd.DataFrame(kG.nodes()) # node_index, node_id
  #   nodes.columns = ['Node_id']
  #   nodes = nodes.astype('int64')


  #   df = pd.read_csv("../Digg_network.txt",sep=" ",header=None) # node_id1, node_id2
  #   df.columns = ['Node_id1', 'Node_id2', 'Time']
   

  #   df_dr1 = df.drop(df.loc[~df['Node_id1'].isin(nodes['Node_id'])].index)
  #   df_dr2 = df_dr1.drop(df_dr1.loc[~df['Node_id2'].isin(nodes['Node_id'])].index)
    
  #   #--------- Store to file ------------------------------
  #   filename = "Digg_network_k"+str(i)+"G.txt"
  #   p = "../K-core_networks/"
  #   df_dr2.to_csv(Path(p+filename),index=False,sep=" ",header=False)
    
  #   kG_previous = kG
  #   print("Time taken for this decomposition is: %s seconds\n" % (time.time() - start))
  


  # print("Transforming to undirected for k-truss")
  # H = G.to_undirected()
  # print("Starting K-truss decompositions\n")

  # # tH_previous = H
  # #--------- Create K-Truss decomposed graphs and store them ---------
  # for i in range(7,8):
  #   start = time.time()
    
  #   #--------- Create K-truss decomposition ----------------
  #   tH = nx.k_truss(H,k=i)
  #   print("Nodes in ",i,"-truss graph:",tH.number_of_nodes())
    
  #   #--------- Drop nodes that are not in tH --------------
  #   nodes  =pd.DataFrame(tH.nodes()) # node_index, node_id
  #   nodes.columns = ['Node_id']
  #   nodes = nodes.astype('int64')

  #   df = pd.read_csv("../Digg_network.txt",sep=" ",header=None) # node_id1, node_id2
  #   df.columns = ['Node_id1', 'Node_id2', 'Time']

  #   df_dr1 = df.drop(df.loc[~df['Node_id1'].isin(nodes['Node_id'])].index)
  #   df_dr2 = df_dr1.drop(df_dr1.loc[~df['Node_id2'].isin(nodes['Node_id'])].index)
    
    
  #   #--------- Store to file ------------------------------
  #   filename = "Digg_network_t"+str(i)+"H.txt"
  #   p = "../K-truss_networks/"
  #   df_dr2.to_csv(Path(p+filename),index=False,sep=" ",header=False)
    
  #   tH_previous = tH
  #   print("Time taken for this decomposition is: %s seconds\n" % (time.time() - start))

