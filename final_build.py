import json
import pprint
import math
import re
from nltk.stem import PorterStemmer
import matplotlib.pyplot as plt

ps = PorterStemmer()
global_index = {}
global_directory = []
global_vocabulary = []
global_sizes = []

# prefix = "../../"
prefix = ""

with open( prefix + "index.json", "r") as f:
    global_index = json.load(f)

old_index = global_index
global_index = {int(k):{int(i):[int(j) for j in global_index[k][i] ] for i in v} for k,v in global_index.items()}

with open(prefix + "global_sizes.json", "r") as f:
    for line in f:
        global_sizes.append(line.strip())

with open(prefix + "directory.json", "r") as f:
    for line in f:
        global_directory.append(line.strip())

total_docs = len(global_directory) + 1
with open(prefix + "vocabulary.json", "r") as f:
    for line in f:
        global_vocabulary.append(line.strip())

def get_total_frequency(filename):
    return( global_sizes[ global_directory.index(filename) ] )

def search(search_term):

    pattern = re.compile('[\W_]+')

    # search_terms = str(search_term).split("")
    search_terms = ''.join(e if e.isalnum() else " " for e in search_term)
    re.sub(r'[\W_]+','', search_terms)

    search_terms = search_terms.split()

    for i, term in enumerate( search_terms ):
        search_terms[i] = ps.stem(term)
    total_occurences = {}
    # print(search_terms)
    count = 0
    total_search_index = {}

    #Building Iniital Index with only documents containing search terms
    for i in search_terms:
        try:
            term_index = global_index [ global_vocabulary.index(i) ]
            for j in term_index:
                document_location = global_directory[j]
                if(document_location in total_search_index):
                    temp_list = total_search_index[ document_location ]
                    if( j in temp_list ):
                        temp_list_inner = temp_list[j]
                        temp_list_inner.append( global_index[global_vocabulary.index(i)][j] )
                        total_search_index[ document_location ] = temp_list_inner
                    else:
                        total_search_index[document_location][i] = global_index[global_vocabulary.index(i)][j]
                else:
                    total_search_index[ document_location ] = { i : global_index[global_vocabulary.index(i)][j] }
        except:
            print("nahi he bro")

    score = {}
    idf = {}
    # pprint.pprint(total_search_index)
    # for i in search_terms:
    #     try:
    #         idf[i] =
    #     except:
    #         print("Nahi mila")

    #For each term closenss


    # ax = fig.add_subplot(111, projection='3d')
    X = []
    Y = []
    points = []
    for sentence_terminator in range(1,15):
        X.append(sentence_terminator)
        for i in total_search_index:

            for j in search_terms:
                term_frequency = total_search_index[i]

                try:
                    if( i in score ):
                        score[i] += math.log( total_docs / len(old_index[str(global_vocabulary.index(j))].keys()) ) * (len(term_frequency[j])/int(get_total_frequency(i)))
                    else:
                        score[i] = math.log( total_docs / len(old_index[str(global_vocabulary.index(j))].keys()) ) * (len(term_frequency[j])/int(get_total_frequency(i)))
                except:
                    print('',end='')


            if( len(total_search_index[i]) > 1 ):
                keys = list(total_search_index[i].keys() )

                for x in range(len(keys)):
                    for z in total_search_index[i][keys[x]] :
                        # print(total_search_index[i][keys[x]])
                        xx = x+1
                        if(xx<len(keys)):
                            for aa in total_search_index[i][keys[xx]]:
                                if( aa - z <= sentence_terminator and aa - z > 0 ):
                                    # print(i,keys[xx],keys[x],aa,z)
                                    # print("crazy")
                                    score[i] += 10*math.log( total_docs / len(old_index[str(global_vocabulary.index(j))].keys()) ) * math.exp(z-aa)
                                    # print(math.exp(z-aa))



                    # for z in total_search_index[i][j]:
                    #     print(z)

        #For sequence finding

        # pprint.pprint(score)
        this_sum = 0
        scoress = []
        for i in score:
            scoress.append(score[i])
        for i in sorted(scoress):
            points.append( (sentence_terminator,i) )


    # print(X,Y)
    plt.scatter(*zip(*points))
    plt.show()

    return(sorted(score.items(), key=lambda x: score.get(x[0])))


search("Josephine+knot".lower())