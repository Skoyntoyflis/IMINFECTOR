# -*- coding: utf-8 -*-
"""
Compute kcore and avg cascade length
Extract the train set for INFECTOR
"""
from tqdm import tqdm
import igraph as ig
import time
import pandas as pd
import json
import numpy as np
from datetime import datetime

   
def sort_papers(papers):
    """
    # Sort MAG diffusion cascade, which is a list of papers and their authors, in the order the paper'sdate
    """
    x =list(map(int,list(map(lambda x:x.split()[-1],papers))))
    return [papers[i].strip() for i in np.argsort(x)]
     
def remove_duplicates(cascade_nodes,cascade_times):
    """
    # Some tweets have more then one retweets from the same person
    # Keep only the first retweet of that person
    """
    duplicates = set([x for x in cascade_nodes if cascade_nodes.count(x)>1])
    for d in duplicates:
        to_remove = [v for v,b in enumerate(cascade_nodes) if b==d][1:]
        cascade_nodes= [b for v,b in enumerate(cascade_nodes) if v not in to_remove]
        cascade_times= [b for v,b in enumerate(cascade_times) if v not in to_remove]

    return cascade_nodes, cascade_times           
			
def store_samples(fn,cascade_nodes,cascade_times,initiators,train_set,op_time,sampling_perc=120):
    """
    # Store the samples for the train set as described in the node-context pair creation process for INFECTOR
    """
    #---- Inverse sampling based on copying time
    #op_id = cascade_nodes[0]
    no_samples = round(len(cascade_nodes)*sampling_perc/100)
    casc_len = len(cascade_nodes)
    #times = [op_time/(abs((cascade_times[i]-op_time))+1) for i in range(0,len(cascade_nodes))]
    times = [1.0/(abs((cascade_times[i]-op_time))+1) for i in range(0,casc_len)]
    s_times = sum(times)
    
    if s_times==0:
        samples = []	
    else:
        # print("Saved in train_set")
        probs = [float(i)/s_times for i in times]
        samples = np.random.choice(a=cascade_nodes, size=int(no_samples), p=probs) 
    
    #----- Store train set
    if(fn=="mag"):
        for op_id in initiators:    
            for i in samples:
                #---- Write inital node, copying node,length of cascade
                train_set.write(str(op_id)+","+i+","+str(casc_len)+"\n")                	
    else:                
        op_id = initiators[0]
        for i in samples:
            #if(op_id!=i):
            #---- Write initial node, copying node, copying time, length of cascade
            train_set.write(str(op_id)+","+i+","+str(casc_len)+"\n")


            
def run(fn,sampling_perc,log,network):    
    print("----------Start of Extract Feats-----------")
    print("Reading the network")
    # g = ig.Graph.Read_Ncol(fn+"/"+fn+"_network.txt")
    g = ig.Graph.Read_Ncol(network)
    
    
    vs = ig.VertexSeq(g)
    # in mag it is undirected
    if fn =="mag":
        g.to_undirected()
        
    
    f = open(fn+"/Init_Data/train_cascades.txt","r")  
    train_set = open(fn+"/train_set.txt","w")
    #----- Initialize features
    idx = 0
    deleted_nodes = []
    g.vs["Cascades_started"] = 0
    g.vs["Cumsize_cascades_started"] = 0
    g.vs["Cascades_participated"] = 0
    log.write(" net:"+fn+"\n")
    start_t = 0 #int(next(f))
    idx=0
    if(fn=="mag"):
        start_t = int(next(f))

    start = time.time()    
    #---------------------- Iterate through cascades to create the train set
    print("Iterating now through cascades to create the train set")
    initiators_whole=[]
    for line in tqdm(f):
        if(fn=="mag"):
            parts = line.split(";")
            initiators = parts[0].replace(",","").split(" ")
            op_time = int(initiators[-1])+start_t
            initiators = initiators[:-1]
            papers = parts[1].replace("\n","").split(":")
            papers = sort_papers(papers)
            papers = [list(map(lambda x: x.replace(",",""),i)) for i in list(map(lambda x:x.split(" "),papers))]
            
            #---- Extract the authors from the paper list
            flatten = []
            for i in papers:
                flatten = flatten+i[:-1]
            u,i = np.unique(flatten,return_index=True)
            cascade_nodes = list(u[np.argsort(i)])
            
            #--- Update metrics of initiators
            for op_id in initiators:
                try:
                    g.vs.find(name=op_id)["Cascades_started"]+=1
                    g.vs.find(name=op_id)["Cumsize_cascades_started"]+=len(papers)
                except:
                    continue
                
            cascade_times = []
            cascade_nodes = []
            for p in papers:
                tim = int(p[-1])+start_t            
                for j in p[:-1]:
                    if j!="" and j!=" " and j not in cascade_nodes:
                        try:
                            g.vs.find(name=j)["Cascades_participated"]+=1
                        except:
                            continue
                        cascade_nodes.append(j)
                        cascade_times.append(tim)
                        
        else: #digg and weibo
            initiators = []
            cascade = line.replace("\n","").split(";")
            if(fn=="Weibo"):
                cascade_nodes = list(map(lambda x:  x.split(" ")[0],cascade[1:]))
                #cascade_times = list(map(lambda x:  datetime.strptime(x.replace("\r","").split(" ")[1], '%Y-%m-%d-%H:%M:%S'),cascade[1:]))
                cascade_times = list(map(lambda x:  int(( (datetime.strptime(x.replace("\r","").split(" ")[1], '%Y-%m-%d-%H:%M:%S')-datetime.strptime("2011-10-28", "%Y-%m-%d")).total_seconds())),cascade[1:]))
            else:
                cascade_nodes = list(map(lambda x:  x.split(" ")[0],cascade))
                cascade_times = list(map(lambda x:  int(x.replace("\r","").split(" ")[1]),cascade))
            
            #---- Remove retweets by the same person in one cascade
            cascade_nodes, cascade_times = remove_duplicates(cascade_nodes,cascade_times)
            
            #---------- Dictionary nodes -> cascades
            op_id = cascade_nodes[0]
            op_time = cascade_times[0]

            #---------- Update metrics
            try:
                g.vs.find(name=op_id)["Cascades_started"]+= 1
                # print(op_id)
                # print(g.vs.find(name=op_id)["Cascades_started"])
                g.vs.find(op_id)["Cumsize_cascades_started"]+= len(cascade_nodes)
                # print(g.vs.find(op_id)["Cumsize_cascades_started"])
            except: 
                # print("Deleted")
                deleted_nodes.append(op_id)
                continue

            count2=0 
            for node in cascade_nodes[1:]:
                try:   
                    g.vs.find(name=node)["Cascades_participated"] +=1
                except:
                   count2+=1
            # print("Number of cascade nodes not found in graph=", count2)    
            

            if(len(cascade_nodes)<2):
                # print("True")
                continue
            initiators = [op_id]
            
            if op_id not in initiators_whole:
                initiators_whole.append(op_id)

        store_samples(fn,cascade_nodes[1:],cascade_times[1:],initiators,train_set,op_time,sampling_perc)
                    
        idx+=1
        if(idx%1000==0):
            print("-------------------",idx)
    
    print("Number of initiators from initiators_whole = ", len(initiators_whole))
       
    print("Number of nodes not found in the graph: ",len(deleted_nodes))
    f.close()
    train_set.close()
    log.write("Feature extraction time:"+str(time.time()-start)+"\n")
    
    
    kcores = g.shell_index()
    log.write("K-core time:"+str(time.time()-start)+"\n")
    a = np.array(g.vs["Cumsize_cascades_started"], dtype=np.float)
    # print(g.vs["Cumsize_cascades_started"])
    b = np.array(g.vs["Cascades_started"], dtype=np.float)
    # print(a,"\n",b)

    avg_casc_s = np.array([],dtype=np.float)
    count = 0
    count_initiators = 0
    for x in b:
        # print(x)
        if x==0:
            avg_casc_s =  np.append(avg_casc_s, 0)
        else:
            avg_casc_s =  np.append(avg_casc_s, a[count]/b[count])
            count_initiators+= 1
        count= count+1
    
    # print("Value of a and b: ", a ,b, len(a),len(b))
    # print("Value of avg cas size:", avg_casc_s)
    print("Found ", count_initiators, "initiators!")

    #------ Store node charateristics
    pd.DataFrame({"Node":g.vs["name"],
                  "Kcores":kcores,
                  "Participated":g.vs["Cascades_participated"],
                  "Avg_Cascade_Size": avg_casc_s}).to_csv(fn+"/node_features.csv",index=False)
    
	#------ Derive incremental node dictionary
    # graph = pd.read_csv(fn+"/"+fn+"_network.txt",sep=" ")
    graph = pd.read_csv(network,sep=" ")
    graph.columns = ["node1","node2","weight"]
    all = list(set(graph["node1"].unique()).union(set(graph["node2"].unique())))
    dic = {int(all[i]):i for i in range(0,len(all))}
    f= open(fn+"/"+fn+"_incr_dic.json","w")
    json.dump(dic,f)
    f.close()
    print("----------End of Extract Feats-----------")
