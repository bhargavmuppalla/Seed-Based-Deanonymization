# Seed-Based-Deanonymization
Source code is available in Project1_final.py file. Code is written in local environment, So to execute this python file, 3 file paths has to be updated in main method.

 1. seed_G1 takes seed_G1.edgelist file path.
 2. seed_G2 takes seed_G1.edgelist file path.
 3. seed_node_pairs takes path for seed_node_pairs.txt file. 

After updating these file paths, Project1_final.py can be executed from terminal using command python Project1_final.py or from any editor like vscode. 

The execution takes around 15 min for given data and output is generated in muppallaProject1Output.txt file which will be generated in the same location from which python file is executed.

# Details of Source code
To start performing deanonymization we have to first create the graphs 
from edgelist which is done using the function load_graph(). Function takes 
edgelist file as input and using inbuilt function read_edgelist available in 
networkx package creates graph.<br /><br />
After reading graphs, load_pairs() is called to load the connections of nodes 
of graph1 and graph2. From this connection list, we segregate nodes which 
have a connection(connected from Graph1 to Graph2) from unconnected 
nodes for graph1 and graph2 using get_connected_nodes() and using 
get_unconnected_nodes() unconnected nodes of graph1 and graph2 are 
segregated.<br /><br />
Main logic is written in a function called deanonymization() . As first steps, 
degree of nodes of graph1 which doesn’t have a connection are calculated. 
Similarly for unconnected nodes of graph2 are also calculated.<br /><br />
Once degrees are calculated. Scores are calculated for each unconnected 
node of Graph1 with all unconnected nodes of Graph2.<br /><br />
Calculation of scores is done using calculate_scores() function<br /><br />
Formula to calculate b/w u and v is 
score(u,v) = total number of neighbors of u and v that are 
connected/sqrt(degree of u) * sqrt(degree of v)<br /><br />

To get the value for numerator of above formula, first all the 
neighbors of u(node of graph1) which has a connection are fetched 
using get_connected_neighbors() function. <br /><br />

Then neighbors of v(node of Graph2) which is connected to one of 
the nodes fetched in above step using 
get_neighbors_G2_connected_with_G1_neighbors(). Count of how 
many such connections exists is calculated and using this scores are 
calculated

After calculating scores. Eccentricity is calculated using calculate_ecce().

**Eccentricity = standard deviation/max1-max2** <br />

Standard deviation calculated with inbuild std function available in 
numpy library.<br />

If eccentricity value is greater than threshold value, which is defined as 0.5, 
then u(node in graph1) will be connected to v(node in graph2 which has 
highest score with u). this is implemented in add_new_connections().<br /><br />

u(node of graph1) is added to list of connected_nodes of graph1 and 
removed from unconnected_nodes list. Similarly v(node of graph2) is 
added to connected_nodes list of graph2 and removed from 
unconnected_nodes list as these 2 nodes are now connected to each 
other. And also a connection between u and v is added to 
connections list and we repeat the above steps for all unconnected 
nodes of graph1

# Results: 
In given seed_node_pairs, there are 500 connections. After 
deanonymization, connections increased to 2304. The Execution 
takes around 15 min
