#!/usr/bin/python3
'''
    helping methods to parse dblp json file
'''
import json


def get_papers(data: list) -> dict:
    '''
    hashing paper entries wrt paper_id
    keys:  title, authors, n_citations, & references, cited_by
    '''
    d = {}
    for i in data:
        ref = i['references'] if 'references' in i else []
        if i['id'] not in d:
            d[i['id']] = {
                            'title': i['title'],
                            'authors': i['authors'],
                            'n_citation': i['n_citation'],
                            'references': ref,
                            'cited_by': []
                        }
        d[i['id']]['title'] = i['title']
        d[i['id']]['authors'] = i['authors']
        d[i['id']]['n_citation'] = i['n_citation']
        d[i['id']]['references'] = ref
        for r in ref:
            if r not in d:
                d[r] = {
                            'title': i['title'],
                            'authors': i['authors'],
                            'n_citation': i['n_citation'],
                            'references': ref,
                            'cited_by': []
                        }
            d[r]['cited_by'].append(i['id'])
    return d


def get_authors(data: list) -> dict:
    '''
    hashing authors wrt author_id
    keys : name, org, papers
    '''
    d = {}
    for i in data:
        paper = i['id']
        authors = i['authors']
        for j in authors:
            ID = j['id']
            name = j['name'] if 'name' in j else ""
            # org = j['org'] if 'org' in j else None
            if ID not in d:
                d[ID] = {
                            'name': set(),
                            'papers': list()
                        }
            d[ID]['name'].add(name)
            d[ID]['papers'].append(paper)
    return d


def read_json(fin: str) -> list:
    f = open(fin, 'r')
    data = json.load(f)  # file -> ds
    return data


def load_data(fin="./data/prl/prl_dblp.json"):
    '''
    format : list(dict)
    dict.keys():'fos', 'alias_ids', 'volume', 'id', 'page_end',
                'venue', 'authors', 'references', 'year', 'doi', 'page_start',
                'issue', 'n_citation', 'publisher', 'title', 'doc_type',
                'indexed_abstract'
    returns : papers, authors
    '''
    data = read_json(fin)
    return get_papers(data), get_authors(data)


def get_el(fin="./data/prl/prl_dblp.json", el_cit="./data/prl/el_cit.txt", el_co="./data/prl/el_co.txt"):
    '''
    create graph in edge list format from dblp json file
    input: 
        fin: dblp file name
        el_cit: file name for citation graph in edgelist format
        el_co: file name for co-authorship graph in el format
    output:
        two edgelist files
            
    '''
    papers, _ = load_data(fin)
    # citation network
    with open(el_cit, 'w') as f:
        for v in papers:
            for u in papers[v]['cited_by']:
                f.write("{} {}\n".format(u,v))
                
    # co-auth net
    co_auth_freq = {} # how many papers two authors have published togather
    for p in papers:
        author_count = len(papers[p]['authors'])
        #print(p)
        for i in range(author_count):
            for j in range(i+1, author_count):
                #print(papers[p]['authors'][i]['id'], papers[p]['authors'][j]['id'])
                key = frozenset([papers[p]['authors'][i]['id'], papers[p]['authors'][j]['id']])
                co_auth_freq.setdefault(key, 0)
                co_auth_freq[key] += 1
        with open(el_co, 'w') as f:
    	    for k in co_auth_freq:
    	        edge = list(k)
    	        weight = co_auth_freq[k]
    	        f.write("{} {} {}\n".format(edge[0], edge[1], weight))
    
    
if __name__ == '__main__':
    print('run the clubAnalyser.py or experiment*.py files')
