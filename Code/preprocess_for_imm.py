"""
Weigh all networks based on weighted cascade, and derive the attribute file required for IMM
"""
from xml.dom.minicompat import NodeList
import igraph as ig
import pandas as pd
import numpy as np
import json
import time
import networkx as nx


def run(fn,log,network):
    print("----------Start of Preprocess for imm-----------")
    start = time.time()
    #--- Read graph
    attribute = open(fn+"/wc_"+fn+"_attribute.txt","w")
    # graph = pd.read_csv(fn+"/"+fn+"_network.txt",sep=" ")
    graph = pd.read_csv(network,sep=" ")
    if(graph.shape[1]>2):
        graph = graph.drop(graph.columns[2],axis=1)
    graph.columns = ["node1","node2"]

    #--- if it is undirected, turn it into directed
    if fn=="mag":
        tmp = graph.copy()
        graph = pd.DataFrame(np.concatenate([graph.values, tmp[["node2","node1"]].values]),columns=graph.columns)
        del tmp
    
    # #--- Compute incidence matrix
    # print("Incidence matrix computation")
    # g = ig.Graph.Read_Ncol(fn+"/"+fn+"_network.txt")
    # G = g.to_networkx()
    # # print(G)
    # R = nx.incidence_matrix(G, nodelist=None, edgelist=None, oriented=True, weight=None)
    # print(np.shape(R))
    # print(R.shape[0])


    # #--- Compute Basic Node Similarity Matrix
    # nodes = G.nodes
    # # upper=np.zeros((R.shape[0],1))  
    # for node_1 in nodes:
    #     for node_2 in nodes:
    #         if node_1 != node_2:
                
    #             print(up)

    

    #--- Compute influence weight
    outdegree = graph.groupby("node1").agg('count').reset_index()
    outdegree.columns = ["node1","outdegree"]
    
    #--- An edge is a follow, hence influence is reverse, that is why we compute the outdegree instead of the indegree
    outdegree["outdegree"] = 1/outdegree["outdegree"]
    outdegree["outdegree"] = outdegree["outdegree"].apply(lambda x:float('%s' % float('%.6f' % x)))
    
    #--- Assign it
    graph = graph.merge(outdegree, on="node1")
    
    #--- Find all nodes to create incremental ids for IMM
    all = list(set(graph["node1"].unique()).union(set(graph["node2"].unique()))) 
    
    dic = {int(all[i]):i for i in range(0,len(all))}
    graph['node1'] = graph['node1'].map(dic)
    graph['node2'] = graph['node2'].map(dic)
    
    #--- Store the ids to translate the seeds of IMM
    f= open(fn+"/"+fn+"_incr_dic.json","w")
    #f.write(json.dumps(dic))
    json.dump(dic,f)
    f.close()
    
    #--- Store
    graph = graph[["node2","node1","outdegree"]]
    graph.to_csv(fn+"/wc_"+fn+"_network.txt",header=False,index=False, sep=" ")
    log.write("Time for wc "+fn+" network:"+str(time.time()-start)+"\n")
    print("--- %s seconds ---\n" % (time.time() - start))
    
    attribute.write("n="+str(len(all)+1)+"\n")
    attribute.write("m="+str(graph.shape[0])+"\n")
    attribute.close()
    print("----------End of Preprocess for imm-----------")
