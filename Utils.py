import os
from Document import Document_Object
from tqdm import tqdm
import json
from InMemIndex import InMemIndex

scriptPath = os.getcwd()      
       

def Build(Index: InMemIndex) -> None:

    loadFromJSON(Index, scriptPath+'/resources/DocumentStore.json')
    Index.buildVocab()
    Index.store2Disk(scriptPath+'/resources/Index.pickle')
    Index.store2DiskFreq(scriptPath+'/resources/FrequencyIndex.pickle')
    Index.store2DiskVocab(scriptPath+'/resources/VocabularyIndex.pickle')
    Index.store2DiskCount(scriptPath+'/resources/DocumentCount.pickle')


def Load() -> InMemIndex:
    Index = InMemIndex()
    Index.loadFromDisk(scriptPath+'/resources/Index.pickle') 
    Index.loadFromDiskFreq(scriptPath+'/resources/FrequencyIndex.pickle')
    Index.loadFromDiskVocab(scriptPath+'/resources/VocabularyIndex.pickle')
    Index.loadFromDiskCount(scriptPath+'/resources/DocumentCount.pickle')
    return Index

def checkIndex():
    if os.path.exists(scriptPath+'/resources/Index.pickle') and\
          os.path.exists(scriptPath+'/resources/FrequencyIndex.pickle') and\
              os.path.exists(scriptPath+'/resources/VocabularyIndex.pickle') and\
                os.path.exists(scriptPath+'/resources/DocumentCount.pickle'):
        return True
    return False

def FormatSuggestions(ranked:list, N:int) -> str:
    result = ''
    if ranked == None:
        return 'No result found'
    for i,item in enumerate(ranked):
        if i == N:
            break
        if item[0] == None:
            continue
        score = "{:.4f}".format(item[2])
        result += f'{i}){item[0]}:{item[1]} --> score: {score}\n'
        i += 1
    return result

def loadFromJSON(Index: InMemIndex ,path):
        with open(path, 'r', encoding='utf8') as jsonFile:
            print('Parsing JSON file: ', end='')
            jsonDict = json.loads(jsonFile.read())
            print('Done')
            docList = []
            for id in tqdm(jsonDict, desc='Building Index from JSON file'):
                text = f'{jsonDict[id]["title"]} {jsonDict[id]["abstract"]}'
                if text == None:
                    text = ''
                doc = Document_Object(int(id), jsonDict[id]['url'], text)
                Index.addDoc(doc=doc)