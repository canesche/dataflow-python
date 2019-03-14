import networkx as nx
from graphviz import Source

# function main
if __name__ == "__main__" :

    path_origin = "res/grafo.dot"
    path_destiny = "res/grafo_final.dot"

    # read a graph
    graph = nx.DiGraph(nx.drawing.nx_pydot.read_dot(path_origin))

    dict = {}
    listClosed = []
    # verify inputs
    for n in graph.nodes():
        dict[n] = graph.in_degree(n)

    listNodes = []
    for n in dict.keys():
        if dict[n] == 0:
            listNodes.append(n)

    new_nodes = {}

    while len(listNodes) != 0:
        node = listNodes[0]
        listNodes.remove(node)
        listClosed.append(node)
        
        #print(node, list(graph.successors(node)))

        if len(list(graph.predecessors(node))) == 0 :
            new_nodes[node] = [0, list(graph.successors(node))]
        else :
            maior = 0
            for i in list(graph.predecessors(node)):
                if maior < new_nodes[i][0] :
                    maior = new_nodes[i][0]
            new_nodes[node] = [(maior+1), list(graph.successors(node))]
        
        for s in graph.successors(node):
            dict[s] = dict[s] - 1
            if dict[s] == 0:
                listNodes.append(s)

    #print(listClosed)
    #print(new_nodes)

    # Create a new graph
    new_graph = nx.DiGraph()

    name_node = []
    for node in new_nodes:
        for successor in new_nodes[node][1]:
            diff = abs(new_nodes[node][0] - new_nodes[successor][0])
            print(new_nodes[node], new_nodes[successor], successor, diff)
            if diff <= 1 :
                new_graph.add_edge(node, successor)
            elif diff == 2 :
                new_graph.add_edge(node, node+'_'+str(1))
                new_graph.add_edge(node+'_'+str(1),successor)
            else :
                new_graph.add_edge(node, node+'_'+str(1))
                diff = diff - 1
                for i in range(1,diff) :
                    new_graph.add_edge(node+'_'+str(i), node+'_'+str(i+1))
                new_graph.add_edge(node+'_'+str(i+1),successor)

    nx.drawing.nx_pydot.write_dot(new_graph, path_destiny)

    
    s1 = Source.from_file(path_origin)
    s2 = Source.from_file(path_destiny)
    s1.view()
    s2.view()

