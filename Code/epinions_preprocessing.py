import igraph as ig
import time
import pandas as pd
import json
import numpy as np 

graph = pd.read_csv("../Data/epinions/soc-sign-epinions.txt", sep="	", header=None, names=["FromNodeId", "ToNodeId", "Sign"])

#--- Compute outdegree
outdegree = graph.groupby("FromNodeId").agg('count').reset_index()
outdegree = outdegree.drop(graph.columns[2],axis=1)
outdegree.columns = ["FromNodeId","outdegree"]


# #--- An edge is a follow, hence influence is reverse, that is why we compute the outdegree instead of the indegree
# outdegree["outdegree"] = 1/outdegree["outdegree"]
# outdegree["outdegree"] = outdegree["outdegree"].apply(lambda x:float('%s' % float('%.6f' % x)))

#--- Assign it
# graph = graph.merge(outdegree, on="FromNodeId")


#--- Compute outdegree+
outdegree_plus = graph.query('Sign == 1').groupby("FromNodeId").agg('count').reset_index()
outdegree_plus = outdegree_plus.drop(graph.columns[2],axis=1)
outdegree_plus.columns = ["FromNodeId","outdegree+"]

#--- Compute outdegree-
outdegree_minus = graph.query('Sign == -1').groupby("FromNodeId").agg('count').reset_index()
outdegree_minus = outdegree_minus.drop(graph.columns[2],axis=1)
outdegree_minus.columns = ["FromNodeId","outdegree-"]

#--- Compute indegree
indegree = graph.groupby("ToNodeId").agg('count').reset_index()
indegree = indegree.drop(graph.columns[2],axis=1)
indegree.columns = ["ToNodeId","indegree"]

#--- Compute indegree+
indegree_plus = graph.query('Sign == 1').groupby("ToNodeId").agg('count').reset_index()
indegree_plus = indegree_plus.drop(graph.columns[2],axis=1)
indegree_plus.columns = ["ToNodeId","indegree+"]

#--- Compute indegree-
indegree_minus = graph.query('Sign == -1').groupby("ToNodeId").agg('count').reset_index()
indegree_minus = indegree_minus.drop(graph.columns[2],axis=1)
indegree_minus.columns = ["ToNodeId","indegree-"]


print(outdegree, outdegree_plus, outdegree_minus, indegree, indegree_plus, indegree_minus)

#--- Compute common neighbors