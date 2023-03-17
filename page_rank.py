
import pandas as pd
import networkx as nx
from collections import Counter

def jobtitle_top_n (df, n= 100):
    """Takes in the raw data frame and gives a list of top n jobtitles """
    value_counts = df['jobtitle'].value_counts()
    value_counts  = value_counts .sort_values(ascending=False)   
    df_jobtitle = value_counts.to_frame().reset_index()
    return list(df_jobtitle['index'][:n])



def create_edge_list(df_for_top_n):
    """this fuction takes a dataframe with the n most common job titles and converts them into edge list which are tuples"""
    smaller_tuples = []
    
    #creating tuples corresponding to a userid
    df_tuples = df_for_top_n.groupby('id').apply(lambda x: tuple(x['jobtitle'])[::-1]).reset_index()
    df_tuples.columns = ['id', 'job_order']
    
    #creating tuples with two elements 
    for original_tuple in df_tuples['job_order']:
        for i in range(len(original_tuple) - 1):
            smaller_tuples.append(original_tuple[i:i+2])

    #returning tuples which doesn't correspond to themselves         
    edge_list = [(x,y) for x,y in smaller_tuples if x != y]
    
    return edge_list

def page_rank_top_n(edge_list):
    
        # create a directed graph
        G = nx.DiGraph()

        # add edges to the graph
        G.add_edges_from(edge_list)

        # calculate the PageRank of each node
        pr = nx.pagerank(G, alpha=0.85)

        return(pr)


    
if __name__ == "__main__":


    df_raw = pd.read_csv('Ramya_Linkedin_Data.csv')
    df_raw= df_raw.drop(df_raw.columns[[0,1]], axis=1)
    df_raw = df_raw.dropna(subset=['jobSalary'])

    df_filtered = df_raw[df_raw['jobtitle'].isin(jobtitle_top_n (df_raw, n= 1000))]
    pr = page_rank_top_n(create_edge_list(df_filtered))
    output = pd.DataFrame(sorted(pr.items(), key= lambda item: item[1], reverse = True))
    output.to_csv('ranks.csv', index=False)
    