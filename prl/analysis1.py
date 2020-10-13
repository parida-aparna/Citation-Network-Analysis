#!/usr/bin/python3
from clubAnalyser import Analysis



def getClubs(clubs: list, fin: str):
    club = list(clubs)
    fin = fin
    ca = Analysis(club, fin)  
    comp,score = ca.get_scc()
    return comp,score

def getCliques(clubs: list, fin: str):
    club = list(clubs)
    fin = fin
    ca = Analysis(club, fin) 
    g = ca.build_graph()
    return g
 
'''
############################################################# collab
coauth = ca.get_collab()#get_coauth_matrix
print("Coauthorship count-------------------------------------------")
for i in range(len(club)):
    for j in range(len(club)):
        print(len(coauth[i][j]), end=" | ")
    print("\n")
print("Coauthorship details-----------------------------------------")
for i in range(len(club)):
    for j in range(len(club)):
        print(coauth[i][j], end=" | ")
    print("\n")

###################################################### projection
ref = ca.get_projection()#get_reference_matrix
# output
print("Citation details :---------------------------------------- ")
for i in range(len(club)):
    for j in range(len(club)):
        print(ref[i][j], end=" | ")
    print("\n")
print("Citation count :---------------------------------------- ")
for i in range(len(club)):
    for j in range(len(club)):
        print(len(ref[i][j]), end=" | ")
    print("\n")
###################################################### journal cit
n_cit = ca.count_journal_cit()
print("Total citation from journal:---------------------------------")
for x in zip(club, n_cit):
    print(x)
###################################################### club cit
n_cit_club = ca.get_club_cit()
print("Totalo citation from club:-----------------------------------")
for ix, x in enumerate(club):
    print(x, len(n_cit_club[ix]))
'''
########################################################
'''import networkx as nx
G = nx.Graph()
for i in range(len(club)):
    for j in range(len(club)):
        if len(coauth[i][j]) > 1:
            G.add_edge(i,j)
import matplotlib.pyplot as plt
nx.draw( G )
plt.show()'''
