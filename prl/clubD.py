#!/usr/bin/python3
'''
    All reusable pieces of codes in one file..
    ... cause I messed up with the design.
'''
import rawDataParser as rdp
from igraph import Graph
from igraph import VertexClustering


def input_edgelist(fin, directed=True) -> Graph:
    '''
        creates a Graph from the edgelist
    '''
    G = Graph.Read_Ncol(fin, directed=directed, weights=not directed)
    return G


def getLargestConnectedComponent(G: Graph, file: str) -> Graph:
    '''
        returns the largest (weakly, in case of directed) connected component
    '''
    f=open(file+"_output_file.txt","a")
    weak_components = G.components(mode="WEAK")  # VertexClustering Obj
    weak_components_list=[]
    for component in weak_components:
       weak_components_list.append(len(component))
    weak_components_list.sort(reverse=True)
    f.write("Results for largely connected components\n-----------------------------------------\n")
    f.write("Sl.No\tSize\n-----------------------------------------\n")
    for i,weak_component in enumerate(weak_components_list):
       f.write('{}\t{}\n'.format(i+1,weak_component))
    
    strong_components = G.components(mode="STRONG")
    strong_components_list=[]
    for component in strong_components:
       strong_components_list.append(len(component))
    strong_components_list.sort(reverse=True)
    f.write("\n\nResults for strongly connected components\n-----------------------------------------\n")                                                   
    f.write("Sl.No\tSize\n-----------------------------------------\n")
    for i,strong_component in enumerate(strong_components_list):
       f.write('{}\t{}\n'.format(i+1,strong_component))
    f.close()
    print("No. of LCC=",len(weak_components))
    print("No. of SCC=",len(strong_components))
    largest_weak_component = weak_components.giant()  # Grapg Obj
    return largest_weak_component

# def input_aminer_json


def detect_communities(G: Graph, directed=True) -> VertexClustering:
    """
        input: igraph.Graph Obj
        process: community detection
        output: igraph.VertexClustering Obj
    """
    if directed:
        vertexDendrogram = G.community_walktrap()  # VertexDendrogram obj
        communities = vertexDendrogram.as_clustering()  # VertexClustering Obj
    else:
        communities = G.community_multilevel(weights='weight')
        print("Modularity Score:", communities.modularity)
    # communities = vertexClusters.subgraphs() # List[Graph obj]
    print("No of communities detected :", len(communities))
    return communities


def prepare_output(fmap: str, vc: VertexClustering, directed=True) -> list:
    '''
        input:  dblp json file for paper->author mapping
                vertexClustering Obj
                isDirected
        process:
            if directed:
                paper -> author mapping
        output: list(set(authors))
    '''
    com = vc.subgraphs()
    res = []
    if directed:
     	for g in com:
            tmp = set()
            for v in g.vs:
                tmp.add(int(v['name']))  # author_id
            res.append(tmp)
    else:
        for g in com:
            tmp = set()
            for v in g.vs:
                tmp.add(int(v['name']))  # author_id
            res.append(tmp)
    return res


def write_communities(c: list, fout: str) -> None:
    f = open(fout, 'w')
    for i in range(len(c)):
        f.write("{}. {}\n\n".format(i+1, c[i]))
    f.close()


def community_intersection(c1: list, c2: list) -> list:
    res = [[None for x in c2] for y in c1]
    for i in range(len(c1)):
        for j in range(len(c2)):
            res[i][j] = c1[i].intersection(c2[j])
    return res

def potential_citation_clubs(club: list,c1: list, c2: list) -> list:
    pcc = [set() for x in c2]
    for i in range(len(c2)):
        for j in range(len(c1)):
            pcc[i] = pcc[i].union(club[j][i])
    return pcc

def write_clubs(c: list, fout: str) -> None:
    f = open(fout, 'w')
    for i in range(len(c)):
        for j in range(len(c[i])):
            if len(c[i][j]) != 0:
                f.write("({},{}). {}\n".format(i+1, j+1, c[i][j]))
    f.close()

def write_pcc(pcc: list, c2: list, fout: str) -> None:
    f = open(fout, 'w')
    for i in range(len(c2)):
        f.write("{}. {}\n\n".format(i+1, pcc[i]))
    f.close()


def write_pcc_sizes(pcc: list, c2: list, fout: str) ->None:
    f = open(fout, 'w')
    for i in range(len(c2)):
        f.write("{}. {}\n".format(i+1, len(pcc[i])))
    f.close()

if __name__ == '__main__':
    print("Not to be executed directly")
    print("Run the experiment files instead")
