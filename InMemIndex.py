from Tokenizer import Tokenize
from tqdm import tqdm
import pickle
from Document import Document_Object

class InMemIndex():
    
    Index = {} # Token --> Set<Document_Object>
    FrequencyIndex = {} # Token --> Frequency
    VocabularyIndex = {} # Permutation --> Tokens
    DocumentCount = 0
    tokenizer = Tokenize()
    
    def __init__(self) -> None:
        pass
    
    def addDoc(self, doc:Document_Object) -> None:
        self.DocumentCount += 1
        tokens = self.tokenizer.tokenize(doc.text)

        
        for token in tokens:
            if token in self.Index.keys():
                 self.Index[token].add(doc)
                 self.FrequencyIndex[token] += 1
            else:
                docSet = set()
                docSet.add(doc)
                self.Index[token] = docSet
                self.FrequencyIndex[token] = 1
    
    def query(self, q:str): # returns a set of Document_Objects
        
        query = self.tokenizer.tokenize(q)
        
        if len(query) == 0:
            return None
        keys = self.Index.keys()
        for word in query:
            if word not in keys:
                return None

        resultSet = self.Index[query[0]]
        for q in query:
            resultSet = resultSet.intersection(self.Index[q])
        return resultSet

    def buildVocab(self):
        keys = sorted(self.FrequencyIndex.keys())
        for token in tqdm(keys, desc='Building Vocabulary Index'):
            for i in range(len(token)):
                temp = token[:i] + token[i+1:]
                if temp in self.VocabularyIndex.keys():
                    self.VocabularyIndex[temp].append(token)
                else:
                    self.VocabularyIndex[temp] = []
                    self.VocabularyIndex[temp].append(token)
                    
                
                
    def str2file(self, path):
        with open(path, 'w', encoding='utf8') as file:
            for key in tqdm(sorted(self.Index.keys()), desc='Saving Index to text file'):
                docSet = self.Index[key]
                docIds = []
                for doc in docSet:
                    docIds.append(doc.id)
                file.write(f'{key} {docIds}\n')
    
    def str2fileFreq(self, path):
        with open(path, 'w', encoding='utf8') as file:
            for key in tqdm(sorted(self.FrequencyIndex.keys()), desc='Saving Frequency Index to text file'):
                file.write(f'{key} {self.FrequencyIndex[key]}\n')
    
    def str2fileVocab(self, path):
        with open(path, 'w', encoding='utf8') as file:
            for key in tqdm(sorted(self.VocabularyIndex.keys()), desc='Saving Vocabulary Index to text file'):
                file.write(f'{key} {self.VocabularyIndex[key]}\n')            
    
    def store2Disk(self, path):
        print('Storing Index to disk: ', end='')
        with open(path,'wb') as file:
            file.write(pickle.dumps(self.Index))
        print('Done')
            
    def loadFromDisk(self, path):
        print('Loading Index from disk: ', end='')
        with open(path, 'rb') as file:
            self.Index = pickle.loads(file.read())   
        print('Done')     

    def store2DiskFreq(self, path):
        print('Storing Frequency Index to disk: ', end='')
        with open(path,'wb') as file:
            file.write(pickle.dumps(self.FrequencyIndex))
        print('Done')
            
    def loadFromDiskFreq(self, path):
        print('Loading Frequency Index from disk: ', end='')
        with open(path, 'rb') as file:
            self.FrequencyIndex = pickle.loads(file.read(), encoding='utf8')   
        print('Done')
        

    def store2DiskVocab(self, path):
        print('Storing Vocabulary Index to disk: ', end='')
        with open(path,'wb') as file:
            file.write(pickle.dumps(self.VocabularyIndex))
        print('Done')
            
    def loadFromDiskVocab(self, path):
        print('Loading Vocabulary Index from disk: ', end='')
        with open(path, 'rb') as file:
            self.VocabularyIndex = pickle.loads(file.read(), encoding='utf8')   
        print('Done')
        
    def store2DiskCount(self, path):
        print('Storing DocumentCount to disk: ', end='')
        with open(path,'wb') as file:
            file.write(pickle.dumps(self.DocumentCount))
        print('Done')
            
    def loadFromDiskCount(self, path):
        print('Loading DocumentCount Index from disk: ', end='')
        with open(path, 'rb') as file:
            self.DocumentCount = pickle.loads(file.read(), encoding='utf8')   
        print('Done')