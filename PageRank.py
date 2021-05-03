#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import time
import numpy as np

T = 50 #iterations
beta = 0.85


# In[2]:


# function to find the total dead ends
def find_dead_ends(graph):
    dead_end = set() 
    dead_end_ordered = []

    # first pass finding all nodes with no outgoing edge      
    order_1 = []
    for node in graph:
        if len(graph[node]) == 0 and node not in dead_end:
            dead_end.add(node)  
            order_1.append(node)
    
    if len(order_1) > 0:
        dead_end_ordered.append(order_1)

    while True:    
        updated = False

        # second pass finding all nodes whose outgoing edges are all to dead ends
        next_removal = []
        for node in graph:
            if graph[node].issubset(dead_end) and node not in dead_end:
                updated = True
                dead_end.add(node)
                next_removal.append(node)

        if not updated:
            break

        dead_end_ordered.append(next_removal)
    
    return dead_end_ordered 


# In[3]:


# building another function to find outgoing and incoming edges
def build_graphs(data):
    outgoing = {}
    incoming = {}

    for node1, node2 in data:
        node1 = int(node1)
        node2 = int(node2)
        if node1 not in outgoing:
            outgoing[node1] = {node2}
        else:
            outgoing[node1].add(node2)
        if node2 not in outgoing:
            outgoing[node2] = set()

        if node2 not in incoming:
            incoming[node2] = {node1}
        else:
            incoming[node2].add(node1)
        if node1 not in incoming:
            incoming[node1] = set()
    
    return outgoing, incoming


# In[4]:


# page rank if no dead ends
def page_rank(outgoing_graph, incoming_graph, dead_ends):
    n = len(outgoing_graph) - len(dead_ends)
    initial_rank = 1 / n
    v = dict()
    v_tmp = dict()
    
    # initialize all pageranks
    for node in outgoing_graph:
        v[node] = initial_rank

    for _ in range(T):
        for i in outgoing_graph:
            if i in dead_ends:
                continue

            incoming = incoming_graph[i].difference(dead_ends)
            summation = 0
            for j in incoming:

                out_deg_j = len(outgoing_graph[j].difference(dead_ends))
                summation += v[j] / out_deg_j
            
            v_tmp[i] = beta * summation + (1 - beta) * initial_rank

        for key in v_tmp:
            v[key] = v_tmp[key]

    return v


# In[5]:


# page rank calculator function with dead ends using the previous function
def page_rank_with_dead_ends(outgoing_graph, incoming_graph, dead_ends_ordered):
    dead_ends = set(np.hstack(dead_ends_ordered))
    v = page_rank(outgoing_graph, incoming_graph, dead_ends)

    for end in dead_ends_ordered[::-1]:
        end = set(end)
        dead_ends = dead_ends.difference(end)

        for i in end:
            summation = 0
            incoming = incoming_graph[i].difference(dead_ends)

            for j in incoming:
                out_deg_j = len(outgoing_graph[j])
                summation += v[j] / out_deg_j
            
            v[i] = summation
            
    return v


# In[6]:


def lines(path):
    lines = [line.rstrip("\n") for line in open(path, encoding="utf8")]
    metadata = lines[:3]
    data = [line.split() for line in lines[4:]]
    return data

# sorting the pageranks and writing in an output file
def output_page_rank(ranks, num):
    sorted_ranks = sorted(ranks.items(), key=lambda kv: kv[1], reverse=True)
    with open(r"output.txt".format(num), "w+") as out_file:
        out_file.write("PageRank\tIds\n")
        for node, rank in sorted_ranks:
            out_file.write("{}\t{}\n".format(rank, node))

def main(fname):
    print(fname)
    file_path = "C:/Users/MANIK MARWAHA/Desktop/web-Google.txt".format(fname)
    data = lines(file_path)

    outgoing_graph, incoming_graph = build_graphs(data)

    dead_ends_ordered = find_dead_ends(outgoing_graph)
    v = page_rank_with_dead_ends(outgoing_graph, incoming_graph, dead_ends_ordered)
    output_page_rank(v, "800")


# In[7]:


if __name__ == "__main__":
    start_time = time.time()
    main("web-Google")
    execution_time = time.time() - start_time
    print(execution_time)