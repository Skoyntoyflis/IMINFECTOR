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


if __name__ == '__main__':
  os.chdir(os.path.join("..","Data","Digg","Init_Data"))
  # digg_preprocessing(os.path.join("..","Data","Digg","Init_Data"))

  print("Reading network with networkx")
  G = nx.read_edgelist("../Digg_network.txt",data=(("time", int),),create_using=nx.DiGraph())

  print("Nodes in whole graph:",G.number_of_nodes())
  print("Edges in whole graph:",G.number_of_edges())

  coreness = nx.core_number(G)

  
  coreness_pd = pd.DataFrame(coreness.items(), columns=['ID','core'])

  # print(coreness_pd.max(axis=1))
  count=0
  keep_cores = pd.DataFrame()
  for i in reversed(range(2,212)):
    no_keep_cores = coreness_pd['core'].value_counts(ascending=True)[i]
    keep_cores = pd.concat([keep_cores, coreness_pd.loc[coreness_pd['core']==i]])
    count += no_keep_cores
    if i == 3:
      keep_cores_3k =keep_cores
    elif i == 4:
      keep_cores_4k =keep_cores
  
  print(count)
  print("3-core:",keep_cores_3k)
  print("4-core:",keep_cores_4k)
  
  # print(coreness_pd["core"].value_counts(ascending=True)[211])
  
  # print(coreness_pd.loc[coreness_pd['core']==211])
  
  # print(coreness_pd['core'].value_counts(ascending=True)[211])
  # print(coreness_pd['core'].value_counts(ascending=True)[210])
  # print(coreness_pd['core'].value_counts(ascending=True)[209])
  # print(coreness_pd['core'].value_counts(ascending=True)[208])
  # print(coreness_pd['core'].value_counts(ascending=True)[207])
  # print(coreness_pd['core'].value_counts(ascending=True)[206])

  # print(coreness_pd)
  
  
  # print(coreness)



  print("Starting k-core decompositions\n")
  
  # kG_previous = G
  #--------- Create k-core decomposed graphs and store them ---------
  for i in range(2,2):
    start = time.time()
    
    #--------- Create k-core decomposition ----------------
    kG = nx.k_core(G,k=i)
    print("Nodes in ",i,"-core graph:",kG.number_of_nodes())
    
    #--------- Drop nodes that are not in kG --------------
    nodes  =pd.DataFrame(kG.nodes()) # node_index, node_id
    nodes.columns = ['Node_id']
    nodes = nodes.astype('int64')


    df = pd.read_csv("../Digg_network.txt",sep=" ",header=None) # node_id1, node_id2
    df.columns = ['Node_id1', 'Node_id2', 'Time']
   

    df_dr1 = df.drop(df.loc[~df['Node_id1'].isin(nodes['Node_id'])].index)
    df_dr2 = df_dr1.drop(df_dr1.loc[~df['Node_id2'].isin(nodes['Node_id'])].index)
    
    #--------- Store to file ------------------------------
    filename = "Digg_network_k"+str(i)+"G.txt"
    p = "../K-core_networks/"
    df_dr2.to_csv(Path(p+filename),index=False,sep=" ",header=False)
    
    kG_previous = kG
    print("Time taken for this decomposition is: %s seconds\n" % (time.time() - start))
  


  # print("Transforming to undirected for k-truss")
  # H = G.to_undirected()
  # print("Starting K-truss decompositions\n")

  # tH_previous = H
  #--------- Create K-Truss decomposed graphs and store them ---------
  for i in range(2,2):
    start = time.time()
    
    #--------- Create K-truss decomposition ----------------
    tH = nx.k_truss(H,k=i)
    print("Nodes in ",i,"-truss graph:",tH.number_of_nodes())
    
    #--------- Drop nodes that are not in tH --------------
    nodes  =pd.DataFrame(tH.nodes()) # node_index, node_id
    nodes.columns = ['Node_id']
    nodes = nodes.astype('int64')

    df = pd.read_csv("../Digg_network.txt",sep=" ",header=None) # node_id1, node_id2
    df.columns = ['Node_id1', 'Node_id2', 'Time']

    df_dr1 = df.drop(df.loc[~df['Node_id1'].isin(nodes['Node_id'])].index)
    df_dr2 = df_dr1.drop(df_dr1.loc[~df['Node_id2'].isin(nodes['Node_id'])].index)
    
    
    #--------- Store to file ------------------------------
    filename = "Digg_network_t"+str(i)+"H.txt"
    p = "../K-truss_networks/"
    df_dr2.to_csv(Path(p+filename),index=False,sep=" ",header=False)
    
    tH_previous = tH
    print("Time taken for this decomposition is: %s seconds\n" % (time.time() - start))

