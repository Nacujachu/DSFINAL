import pickle
from math import log
class shared_dict(object):
    def __init__(self):        
        self.WORD_IDX = {}
        self.INV_WORD_IDX = {}
        self.DF = {}
        self.count = 0       
        self.total_doc = 0 
        
    
    def add_word(self , word):
        if word in self.WORD_IDX: 
            pass        
        else:
            self.WORD_IDX[word] = self.count
            self.INV_WORD_IDX[self.count] = word
            self.count = self.count + 1
            
    def add_doc(self , doc):
    
        self.total_doc += 1
        word_exist = set()
        
        for word in doc:
            word_exist.add(word)
            self.add_word(word)
        for word in word_exist:
            idx = self.WORD_IDX[word]
            if idx in self.DF:
                self.DF[idx] += 1
            else:
                self.DF[idx] = 1
    def get_seq(self , word_list , TOPK = 30):
        seq = []
        TF = {}
        tf_idf = {}
        
        total_word = len(word_list)
        
        for word in word_list:
            idx = self.WORD_IDX[word]
            
            if idx in TF:
                TF[idx] += 1
            else:
                TF[idx] = 1
                
        for word in word_list:
            idx = self.WORD_IDX[word]
            tf_idf[idx] = (TF[idx] / total_word) * log( self.total_doc / (self.DF[idx]+1) )
                
                
        sorted_word = list(reversed(sorted(tf_idf.items() , key = lambda d : d[1])))
                
        keep_word = []
                
        for k,v in sorted_word:
            keep_word.append(k)

            if(len(sorted_word) > TOPK):
                keep_word = keep_word[:TOPK]
                        
        return keep_word
                    
    def save_dict(self):
        out_f = open('word_index.pickle','wb')
                    
        pickle.dump(self.WORD_IDX , out_f)
        
        out_f.close()
        
    def load_dict(self):
        in_f = open('word_index.pickle','rb')
        self.WORD_IDX = pickle.load(in_f)
        in_f.close()

        for word , idx in self.WORD_IDX.items():
            self.INV_WORD_IDX[idx] = word
        
