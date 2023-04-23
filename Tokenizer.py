from string import punctuation
from hazm import Normalizer, word_tokenize

class Tokenize():
    
    normalizer = Normalizer()
    
    def __init__(self) -> None:
        pass
    
    def tokenize(self,st: str) -> list:
        delimeters = punctuation + '،'
        table = str.maketrans(delimeters, ' ' * len(delimeters))
        input = st.translate(table)
        input = input.replace(u'\u0626', u'\u0649').replace(u'\u0647\u0654', u'\u0647')\
            .replace(u'\u0621', ' ').replace(u'\u200C', '')
        input = input.lower()
        
        final = ''
        for i in range(len(input)):
            if input[i] < u'\u06FF' and input[i] > u'\u0600':
                final += input[i]
            
            elif input[i] < u'\u007F' and input[i] > u'\u0020':
                final += input[i]
            
            else:
                final += ' '  

                
                      
        temp = word_tokenize(self.normalizer.normalize(final))
        tokens = []
        for t in temp:
            if len(t) >= 2:
                tokens.append(t)
        
        return tokens
    