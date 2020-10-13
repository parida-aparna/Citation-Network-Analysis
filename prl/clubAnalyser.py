#!/usr/bin/python3
'''
    Everything about analysis
    1. collaboration
    2. projection
    3. club citations
    4. journal citaions
'''
import rawDataParser as rdp
from graphviz import Digraph
from igraph import Graph
import random


class Analysis:
    def __init__(self, club, db: str):
        '''
            input: dblp aminer json file name
        '''
        self.members = club
        self.papers, self.authors = rdp.load_data(db)
        self.collab = self.get_coauth_matrix()
        self.projection = self.get_reference_matrix()

    def get_coauth_matrix(self) -> list:
        '''
            input:
                club: list of authors
            returns:
                collaboration matrix,
                where matrix(i, j) = set of paper published by i & j togather
        '''
        club = self.members
        coauth = [[set() for x in range(len(club))] for y in range(len(club))]
        for i in range(len(club)):
            for j in range(i, len(club)):
                paper_i = self.authors[club[i]]['papers']
                paper_j = self.authors[club[j]]['papers']
                coauth[i][j] = set(paper_i).intersection(paper_j)
                coauth[j][i] = coauth[i][j]
        return coauth

    def get_reference_matrix(self) -> list:
        '''
            input:
                club: list of authors
            output:
                projection matrix where,
                each element matrix(i, j): set of citations(a, b) from i to j
                a, b are authored by i & j respectively
        '''
        club = self.members
        ref = [[set() for x in range(len(club))] for y in range(len(club))]
        for i in range(len(club)):
            i_papers = self.authors[club[i]]['papers']
            for k in i_papers:
                i_paper_ref = self.papers[k]['references']
                for j in range(len(club)):
                    j_papers = self.authors[club[j]]['papers']
                    tmp = set()
                    for l in set(j_papers).intersection(i_paper_ref):
                        # i cites j with k->l, author(k)=i, author(l)=j
                        tmp.add((k, l))
                    ref[i][j].update(tmp)
        return ref

    def count_journal_cit(self) -> list:
        '''
            input: list of authors
            output: respective citation count
                total citation for an author
                    = sum(len(cited_by) for all his papers)
        '''
        club = self.members
        count = [0] * len(club)
        for i in range(len(club)):
            i_papers = self.authors[club[i]]['papers']
            for p in i_papers:
                count[i] += len(self.papers[p]['cited_by'])
        return count

    def get_club_cit(self) -> list:
        '''
            input:
                club: list of authors
            returns:
                totatl citation from club =  row wise union of ref matrix )
        '''
        club = self.members
        ref = self.projection
        cit = [None] * len(club)
        for i in range(len(club)):
            tmp = set()
            for j in range(len(club)):
                tmp.update(ref[j][i])
            cit[i] = tmp
        return cit

    def visualise(self, fout="tmp.gv", engine='dot', format='pdf') -> None:
        coauth = self.collab
        ref = self.projection
        club = self.members
        scc = self.compute_scc()
        # color = ['green', 'blue', 'gold', 'cyan', 'orange', 'magenta']
        color = ["#"+"".join([random.choice('1234567890ABCDEF') for _ in range(6)]) for _ in club]
        g = Digraph(comment="induced sub graph", format=format, engine=engine)
        for i, x in enumerate(club):
            g.node(str(x), color=color[scc.membership[i]])
        # uncomment to show collab links
        """ with g.subgraph(name='coauth') as c:
            c.attr('edge', dir='none', color='red')
            for i in range(len(club)):
                for j in range(i, len(club)):
                    if i != j and len(coauth[i][j]) > 0:
                        c.edge(str(club[i]), str(club[j]), label=str(len(coauth[i][j]))) """
        with g.subgraph(name='cit') as c:
            for i in range(len(club)):
                for j in range(len(club)):
                    if len(ref[i][j]) > 0:
                        c.edge(str(club[i]), str(club[j]), label=str(len(ref[i][j])))
        g.render(fout, view=True)
    
    def masked_visualise(self, fout="tmp.gv", engine='dot', format='pdf') -> None:
        coauth = self.collab
        ref = self.projection
        club = self.members
        scc = self.compute_scc()
        # color = ['green', 'blue', 'gold', 'cyan', 'orange', 'magenta']
        color = ["#"+"".join([random.choice('1234567890ABCDEF') for _ in range(6)]) for _ in club]
        g = Digraph(comment="induced sub graph", format=format, engine=engine)
        for i, x in enumerate(club):
            g.node("A"+str(i), color=color[scc.membership[i]])
        # uncomment to show collab links
        """ with g.subgraph(name='coauth') as c:
            c.attr('edge', dir='none', color='red')
            for i in range(len(club)):
                for j in range(i, len(club)):
                    if i != j and len(coauth[i][j]) > 0:
                        c.edge(str(club[i]), str(club[j]), label=str(len(coauth[i][j]))) """
        with g.subgraph(name='cit') as c:
            for i in range(len(club)):
                for j in range(len(club)):
                    if len(ref[i][j]) > 0:
                        c.edge("A"+str(i), "A"+str(j), label=str(len(ref[i][j])))
        g.render(fout, view=True)

    def build_graph(self):
        club = self.members
        ref = self.projection
        g = Graph(directed=True) #creates an empty graph object which specifies that the graph should be directed.
        for i in club:           #builds the auth-auth citation network for each club.
            g.add_vertex(name=i)
        for i in range(len(club)):
            for j in range(len(club)):
                if len(ref[i][j]) > 0:
                    g.add_edge(i, j, weights=len(ref[i][j]))
        return g

    def compute_scc(self):
        '''
            strongly connected components of given club
            returns: vertexClusteringObject
        '''
        club = self.members
        ref = self.projection
        g = Graph(directed=True) #creates an empty graph object which specifies that the graph should be directed.
        for i in club:           #builds the auth-auth citation network for each club.
            g.add_vertex(name=i)
        for i in range(len(club)):
            for j in range(len(club)):
                if len(ref[i][j]) > 0:
                    g.add_edge(i, j, weights=len(ref[i][j]))
        scc = g.components(mode='STRONG')
        return scc

    def get_scc(self):
        '''
            returns:
                scc: as list of member vertices
                normalised score: for each scc
        '''
        total_weight=0
        scc = self.compute_scc()
        try:
            total_weight = sum(scc.graph.es['weights'])
        except KeyError:
            print("No citation edge exists")
        comp = []
        score = []
        
        for g in scc.subgraphs():
            tmp = []
            for v in g.vs:
                tmp.append(v['name'])
            comp.append(tmp)
            if total_weight > 0:
                score.append(sum(g.es['weights'])/total_weight)
            else:
                score.append(0)
        return comp, score


if __name__ == '__main__':
    print("Run analysis.py or visualise.py")
