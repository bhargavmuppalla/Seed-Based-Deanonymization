import networkx as nx
import math
import numpy as np

#Creates graph by reading the edges
def load_graph(seed):
    G = nx.read_edgelist(seed)
    return G

#Reads the connections between the nodes from a file and store the connections in dictionary
def load_pairs(node_pairs):
    with open(node_pairs,'r') as f:
        pairs = f.readlines()
    
    connections = {}
    for pair in pairs:
        pair = pair.strip('\n')
        pair = pair.split(' ')
        connections[pair[0]] = pair[1]

    return connections
  
#Get Nodes of Graph G1 and G2 which have a connection
def get_connected_nodes(pairs):
    g1nodes = []
    g2nodes = []
    
    for pair in pairs:
        g1nodes.append(pair)
        g2nodes.append(pairs[pair])
    return g1nodes,g2nodes
  
#Get Node of Graph G1 and G2 which are not connected.
def get_unconnected_nodes(G1,G2,connected_G1,connected_G2):
    g1nodes = []
    g2nodes = []

    for node in G1.nodes:
        if node not in connected_G1:
            g1nodes.append(node)

    for node in G2.nodes:
        if node not in connected_G2:
            g2nodes.append(node)
    return g1nodes,g2nodes
    

# returns neighbors of node which are connected 
def get_connected_neighbors(node,G,connections):
    connected_neighbors = []
    for neighbor in G.neighbors(node):
        if neighbor in connections:
            connected_neighbors.append(neighbor)
    return connected_neighbors
    
# returns count of numbers of neighbors of node in G2 connected to neighbors of node in G1
def get_neighbors_G2_connected_with_G1_neighbors(connected_neighbors_G1,G2,connections,node_G2):
    nodes_G2_connected_with_G1 = []
    count = 0
    for i in connected_neighbors_G1:
        nodes_G2_connected_with_G1.append(connections[i])
    
    for j in nodes_G2_connected_with_G1:
        if j in G2.neighbors(node_G2):
            count +=1
    return count
    
def calculate_standard_deviation(lst):
    sd = np.std(lst)
    return sd

# Calculate eccentricity
def calculate_ecce (scoreL):
    sd = calculate_standard_deviation(scoreL)
    max1 = max(scoreL)
    scoreL.remove(max1)
    max2 = max(scoreL)
    if sd == 0:
        ecce = 0
    else:
        ecce = (max1-max2)/sd
    return ecce

#Graph is updated by connecting node of Graph1 with node with max score of graph2 if eccentricity value is more than the threshold.
def add_new_connections(eccentricity,node,maxscore_node,threshold,connected_G1_nodes,connected_G2_nodes,connections,unconnected_G1_nodes,unconnected_G2_nodes):
    if eccentricity > threshold:
        connected_G1_nodes.append(node)
        connected_G2_nodes.append(maxscore_node)
        unconnected_G1_nodes.remove(node)
        unconnected_G2_nodes.remove(maxscore_node)
        connections[node] = maxscore_node
        
        
    return connected_G1_nodes,connected_G2_nodes,connections,unconnected_G1_nodes,unconnected_G2_nodes

#Scores are calucated betwen node of Graph1 with all unconnected nodes of Graph2.
def calculate_scores(node, G1, G2, connections, connected_G1_nodes, connected_G2_nodes, unconnected_G1_nodes, unconnected_G2_nodes, unconnected_G1_nodes_degree,unconnected_G2_nodes_degree):
    connected_neighbors_G1 = get_connected_neighbors(node,G1,connections)

    scores = {}

    for i in unconnected_G2_nodes:
        count = get_neighbors_G2_connected_with_G1_neighbors(connected_neighbors_G1,G2,connections,i)
        score = count/((math.sqrt(unconnected_G1_nodes_degree[node]))*(math.sqrt(unconnected_G2_nodes_degree[i])))
        scores[i] = score
    return scores

#Core function that calls other methods like scores, eccentricity and adding new connections and return the final output.
def deanonymization(threshold, G1, G2, connections, connected_G1_nodes, connected_G2_nodes, unconnected_G1_nodes, unconnected_G2_nodes):
    
    #calculate degree of unconnected G1 nodes
    unconnected_G1_nodes_degree = {}
    for node in unconnected_G1_nodes:
        unconnected_G1_nodes_degree[node] = G1.degree(node)

    #calculate degree of unconnected G2 nodes
    unconnected_G2_nodes_degree = {}
    for node in unconnected_G2_nodes:
        unconnected_G2_nodes_degree[node] = G2.degree(node)

    for node in unconnected_G1_nodes:
        scores = calculate_scores(node, G1, G2, connections, connected_G1_nodes, connected_G2_nodes, unconnected_G1_nodes, unconnected_G2_nodes,unconnected_G1_nodes_degree,unconnected_G2_nodes_degree)
        scoresL = list(scores.values())
        eccentricity = calculate_ecce(scoresL)

        for key, value in scores.items():
            if value == max(scoresL):
                maxscore_node = key 

        connected_G1_nodes,connected_G2_nodes,connections,unconnected_G1_nodes,unconnected_G2_nodes = add_new_connections(eccentricity,node,maxscore_node,threshold,connected_G1_nodes,connected_G2_nodes,connections,unconnected_G1_nodes,unconnected_G2_nodes)
    
    return connected_G1_nodes,connected_G2_nodes,connections,unconnected_G1_nodes,unconnected_G2_nodes

if __name__ == "__main__":
    seed_G1 = '/Users/bhargavmuppalla/Documents/privacy aware computing/IProject1/Proect1Data 2/seed_G1.edgelist'
    seed_G2 = '/Users/bhargavmuppalla/Documents/privacy aware computing/IProject1/Proect1Data 2/seed_G2.edgelist'
    seed_node_pairs = '/Users/bhargavmuppalla/Documents/privacy aware computing/IProject1/Proect1Data 2/seed_node_pairs.txt'

    G1 = load_graph(seed_G1)
    G2 = load_graph(seed_G2)
    connections = load_pairs(seed_node_pairs)

    connected_G1_nodes, connected_G2_nodes = get_connected_nodes(connections)
    unconnected_G1_nodes, unconnected_G2_nodes = get_unconnected_nodes(G1, G2, connected_G1_nodes, connected_G2_nodes)

    threshold = 0.5
    connected_G1_nodes,connected_G2_nodes,connections,unconnected_G1_nodes,unconnected_G2_nodes = deanonymization(threshold, G1, G2, connections, connected_G1_nodes, connected_G2_nodes, unconnected_G1_nodes, unconnected_G2_nodes)

with open('muppallaProject1Output.txt','w')as f:
    count = 0
    for i in connected_G1_nodes:
        pair = i + ' ' + connections[i]+'\n'
        count += 1
        f.write(pair)
print(count)