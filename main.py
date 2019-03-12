import networkx as nx

# supoe grafo conectado
numberOfFU = 16

if __name__ == "__main__":
    G = nx.DiGraph(
        nx.drawing.nx_pydot.read_dot(
            "/Users/vanessa/PycharmProjects/ModuloScheduling/res/h2v2_smooth_downsample_dfg__6.dot"))

    numberOfNodes = len(G.nodes())
    number = round((numberOfNodes / numberOfFU))

    if ((numberOfNodes / numberOfFU) - number) <= 0:
        numberOfConfig = 2 if (number < 2) else number
    else:
        numberOfConfig = 2 if ((number + 1) < 2) else (number + 1)

    # Permite apenas dois vértices de entrada
    i = 0
    novos_nos = []
    for n in G.nodes():
        if len(G.predecessors(n)) > 2:
            list_pre = G.predecessors(n)
            x = str(n)
            for e in list_pre:
                G.remove_edge(e, n)
            while len(list_pre) != 2:
                nodo = x[:4] + "N" + str(int(x[-2:]) + i)
                list_pre.append(nodo)
                novos_nos.append(nodo)
                G.add_edge(list_pre[0], nodo)
                G.add_edge(list_pre[1], nodo)

                list_pre.remove(list_pre[0])
                list_pre.remove(list_pre[0])
                i = i + 1
            G.add_edge(list_pre[0], n)
            G.add_edge(list_pre[1], n)

    for n in novos_nos:
        if len(G.predecessors(n)) > 2:
            list_pre = G.predecessors(n)
            x = str(n)

            for e in list_pre:
                G.remove_edge(e, n)

            while len(list_pre) != 2:
                nodo = x[:4] + "N" + str(int(x[-2:]) + i)
                list_pre.append(nodo)

                G.add_edge(list_pre[0], nodo)
                G.add_edge(list_pre[1], nodo)

                list_pre.remove(list_pre[0])
                list_pre.remove(list_pre[0])
                i = i + 1
            G.add_edge(list_pre[0], n)
            G.add_edge(list_pre[1], n)

    # busca em largura
    dict = {}
    listClosed = []
    for n in G.nodes():
        dict[n] = G.in_degree(n)

    listNodes = []
    for n in dict.keys():
        if dict[n] == 0:
            listNodes.append(n)

    while len(listNodes) != 0:
        node = listNodes[0]
        listNodes.remove(node)
        listClosed.append(node)
        for s in G.successors(node):
            dict[s] = dict[s] - 1
            if dict[s] == 0:
                listNodes.append(s)
    print("Busca em Largura:")
    print(listClosed)

    config = []
    time = []

    nx.drawing.nx_pydot.write_dot(G, "/Users/vanessa/PycharmProjects/ModuloScheduling/res/grafo_final.dot")

    for n in G.nodes():
        if len(G.predecessors(n)) > 2:
            print("Something is WRONG")
            print(n)
