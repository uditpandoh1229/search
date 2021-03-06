from os import system, name
import re
def process_files(filenames):
    file_to_terms = {}
    for file in filenames:
        pattern = re.compile('[\W_]+')
        file_to_terms[file] = open(file, 'r').read().lower()
        print( file_to_terms[file] )
        file_to_terms[file] = pattern.sub(' ',file_to_terms[file])
        print( file_to_terms[file] )
        re.sub(r'[\W_]+','', file_to_terms[file])
        file_to_terms[file] = file_to_terms[file].split()
        print( file_to_terms[file] )
    return file_to_terms

def index_one_file(termlist):
    fileIndex = {}
    for index, word in enumerate(termlist):
        if word in fileIndex.keys():
            fileIndex[word].append(index)
        else:
            fileIndex[word] = [index]
    return fileIndex

def make_indices(termlists):
    total = {}
    for filename in termlists.keys():
        total[filename] = index_one_file(termlists[filename])
    return total

def fullIndex(regdex):
    total_index = {}
    for filename in regdex.keys():
        for word in regdex[filename].keys():
            if word in total_index.keys():
                if filename in total_index[word].keys():
                    total_index[word][filename].extend(regdex[filename][word][:])
                else:
                    total_index[word][filename] = regdex[filename][word]
            else:
                total_index[word] = {filename: regdex[filename][word]}
    return total_index

def one_word_query(word, invertedIndex):
    pattern = re.compile('[\W_]+')
    word = pattern.sub(' ',word)
    if word in invertedIndex.keys():
        return [filename for filename in invertedIndex[word].values()]
    else:
        return []

def free_text_query(string,index):
    pattern = re.compile('[\W_]+')
    string = pattern.sub(' ',string)
    result = []
    for word in string.split():
        result += one_word_query(word,index)
    print(result)
    return list(set(result))

def phrase_query(string, invertedIndex):
    pattern = re.compile('[\W_]+')
    string = pattern.sub(' ',string)
    listOfLists, result = [],[]
    for word in string.split():
        listOfLists.append(free_text_query(word,invertedIndex))
    setted = set(listOfLists[0]).intersection(*listOfLists)
    for filename in setted:
        temp = []
        for word in string.split():
            temp.append(invertedIndex[word][filename][:])
        for i in range(len(temp)):
            for ind in range(len(temp[i])):
                temp[i][ind] -= i
        if set(temp[0]).intersection(*temp):
            result.append(filename)
        print('\n temp : \n')
        print(temp)
    return result

filenames=['./data/15147_split_1.pdf']
termslist=process_files(filenames)
print('\n\n\n\n')
print(termslist)
print('\n\n\n\n')
print('\nterm list \n')
print(termslist)
print('\n\n')
print('\n\n')
totaldict=make_indices(termslist)
print('total dictionary \n')
print(totaldict)
print('\n\n')
print('\n\n')
index=fullIndex(totaldict)
print('full index \n')
print(index)
print('\n\n')

search_term = input("Enter Term to Search for\n")
# print(phrase_query(search_term,index))
try: print(index[search_term])
except: print("Not in files")

