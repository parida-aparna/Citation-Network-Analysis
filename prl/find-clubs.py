#!/usr/bin/python3
'''
    1. get gcc of citation network
    2. get gcc of co-authorship network
    3. detect communities in both of them
    4. replace papers in citation network with corresponding authors
    5. find intersection between the comminities found in both the networks
'''
import pickle
import clubD as cd
import analysis1 as an
import sys

def getCommunities(fnam, directed):
    g = cd.input_edgelist(fnam, directed)
    gcc = cd.getLargestConnectedComponent(g,sys.argv[1])
    communities = cd.detect_communities(gcc, directed)
    if directed:
        pickle.dump(communities, open(sys.argv[1]+"_communities_cit.bin", 'wb')) #sys.argv[1]=journal name
    else:
        pickle.dump(communities, open(sys.argv[1]+"_communities_co.bin", 'wb'))
    return cd.prepare_output(sys.argv[1]+"_dblp.json", communities, directed)

def pcc_analysis(pcc: set):
    f = open(sys.argv[1]+"_pcc_analysis.txt","w")
    for i in range(len(pcc)):
        f.write("\n\nPCC {}\n\n".format(i+1))
        comp,score = an.getClubs(pcc[i], sys.argv[1]+"_dblp.json") 
        for j in range(len(comp)): 
       	    f.write(f'{j}.\t{comp[j]}\t{score[j]}\n')
    f.close()

def pcc_cliques(pcc: set):
    f1=open(sys.argv[1]+"_pcc_cliques.txt","w")
    f2=open(sys.argv[1]+"_pcc_cliques_sizes.txt","w")
    for i in range(len(pcc)):
        res=[]
        g = an.getCliques(pcc[i], sys.argv[1]+"_dblp.json")
        res=g.cliques()
        no=g.clique_number()
        f1.write(f'\nPCC-{i+1}:\nLargest clique size:{no}\nCliques:\n{res}\n\n')
        for j in res:
            if(len(j)==no):
                f2.write(f'\nPCC-{i+1}:\nSize:\t{no}\nClique:\t{j}\n')

if __name__ == '__main__':
    # getting communities
    c1 = getCommunities(sys.argv[2], True) #sys.argv[2]=network(e.g:author author citation network)
    c2 = getCommunities(sys.argv[3], False) #sys.argv[3]=network(e.g:co-authorship network)
    # getting clubs
    c1 = pickle.load(open(sys.argv[1]+"_communities_cit.bin", 'rb'))
    c2 = pickle.load(open(sys.argv[1]+"_communities_co.bin", 'rb'))
    c1 = cd.prepare_output(sys.argv[1]+"_dblp.json", c1, True)
    c2 = cd.prepare_output("NA", c2, False)
    # getting communities
    cd.write_communities(c1, sys.argv[1]+"_communities_cit.txt")
    cd.write_communities(c2, sys.argv[1]+"_communities_co.txt")
    # getting clubs
    c = cd.community_intersection(c1, c2)
    pcc = cd.potential_citation_clubs(c, c1, c2)
    pcc_analysis(pcc)
    pcc_cliques(pcc)
    cd.write_clubs(c, sys.argv[1]+'_clubs.txt')
    cd.write_pcc(pcc, c2, sys.argv[1]+'_pcc.txt')
    cd.write_pcc_sizes(pcc, c2, sys.argv[1]+'_pcc_sizes.txt')
