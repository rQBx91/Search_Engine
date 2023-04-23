import math
from Tokenizer import Tokenize, Normalizer
from InMemIndex import InMemIndex
import json
import math
import re

class QueryRanking():
    
    tokenizer = Tokenize()
    normalizer = Normalizer()
    LocalIndex = {}
    LocalVocabIndex = {}
    LocalFrequencyIndex = {}
    JSONDict = {}
    DocumentCount = 0

    
    def __init__(self, Index: InMemIndex, jsonPath) -> None:
        self.LocalIndex = Index.Index
        self.LocalVocabIndex = Index.VocabularyIndex
        self.LocalFrequencyIndex = Index.FrequencyIndex
        self.DocumentCount = int(Index.DocumentCount)
        print('Reading JSON file: ', end='')
        with open(jsonPath, 'r', encoding='utf8') as jsonFile:
            self.JSONDict = json.loads(jsonFile.read()) 
        print('Done')
    
        
    def sugguest(self, q: str) -> list:
        
        qtokens = self.tokenizer.tokenize(q)
        if len(qtokens) == 0:
            return None
        
        qdict = {}
        for token in qtokens:
            qdict[token] = {}
            
        keys = self.LocalVocabIndex.keys()            
        for token in qtokens:
            keys = self.LocalVocabIndex.keys()
            for i in range(len(token)):
                temp = token[:i] + token[i+1:]
                if temp in keys:
                    for item in self.LocalVocabIndex[temp]:
                        qdict[token] |= {item:self.LocalFrequencyIndex[item]}  
                                        
        
        ranked = {}
        n = len(qtokens)
        for token in qtokens:
            ranked[token] = []
            
        keys = self.LocalFrequencyIndex.keys()
        for token in qdict:
            if len(qdict[token]) == 0:
                continue
            sum = 0
            for item in qdict[token]:
                sum += int(qdict[token][item])
            for item in qdict[token]:
                if item == token:
                    weight = 1 - (1/qdict[token][item])
                    weight /= n
                else:
                    weight = int(qdict[token][item])/sum
                    weight /= n
                ranked[token].append((item, weight))
        
        for token in ranked:
            ranked[token].sort(key=lambda y: y[1], reverse=True)
        
        rs = 1
        for token in ranked:
            if len(ranked[token]):
                rs *= len(ranked[token])
        
        
        result = [None] * n
        for i,token in enumerate(ranked):
            if len(ranked[token]) == 0:
                continue
            result[i] = ranked[token] * (rs//len(ranked[token]))
        
        zipRes = []
        for i in range(len(ranked)):
            if result[i] == None:
                continue
            if i == 0:
                zipRes = result[i]
            else:
                zipRes = zip(zipRes,result[i])
          
        finalRes = [] 
        if len(qtokens) > 1:       
            for items in zipRes:
                st = q
                wei = 0
                for i,item in enumerate(items):
                    st = st.replace(qtokens[i], item[0])
                    wei += item[1]
                finalRes.append((st,wei))
        elif len(qtokens) == 1:
           finalRes= zipRes
        if finalRes != None:
            finalRes = set(finalRes)
            finalRes = list(finalRes)
            finalRes.sort(key=lambda y: y[1], reverse=True)
            
        if len(finalRes) == 0:
            return None
        
        return finalRes
  
  
    def query(self, q:str): # returns a set of Document_Objects
        
        query = self.tokenizer.tokenize(q)
        
        if len(query) == 0:
            return None
        keys = self.LocalIndex.keys()
        for word in query:
            if word not in keys:
                return None

        resultSet = self.LocalIndex[query[0]]
        for q in query:
            resultSet = resultSet.intersection(self.LocalIndex[q])
        return resultSet
            
            
    def context(self, q: str) -> list:
        suggestions = self.sugguest(q)
        
        if suggestions == None:
            return None
        
        querySize = [None] * len(suggestions)
        for i,sugg in enumerate(suggestions):
            querySize[i] = len(self.query(sugg[0]))

        sum = 0
        for i in querySize:
            sum += i
        
        contex = []
        for i,item in enumerate(suggestions):
            weight = (item[1] + (querySize[i]/sum)*2) / 3
            contex.append((item[0],weight))
            
        temp = set(contex)
        contex = list(temp)
        contex.sort(key=lambda y: y[1], reverse=True)
        
        return contex
    
    
    def term_value(self, token, docid, idf):
        text = self.JSONDict[docid]['abstract']
        text = self.normalizer.normalize(text)
        textTokens = self.tokenizer.tokenize(text)
        num = len(re.findall(token, text))

        lenght = len(textTokens)
        if lenght != 0:
            tf = num / lenght
        else:
            tf = 0
        return tf * idf

    
    def rank(self, q: str) -> list:
        context  = self.context(q)
        result = []
        if context == None:
            return None
        for res in context:
            query = res[0]
            docSet = self.query(query)
            if len(docSet) == 0:
                result.append((None, None, 0))
                continue
            qtokens = self.tokenizer.tokenize(query) 
            x = self.DocumentCount/len(docSet)    
            idf = math.log10(x)              
            for doc in docSet:
                sum  = 0
                for token in qtokens:
                    sum += self.term_value(token, str(doc.id), idf)
                url = self.JSONDict[str(doc.id)]['url']
                
                result.append((query, url, sum * res[1]))
        
        resultSet = set(result)
        result = list(resultSet)
        result.sort(key=lambda y: y[2], reverse=True)
                
        return result