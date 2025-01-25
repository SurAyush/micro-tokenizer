# Coding a simple tokenizer using Byte Pair Encoding (BPE) algorithm from scarth
# It will first split the text using regex into pieces, then apply BPE to merge the most frequent pairs of characters

import regex as re
import pickle

class Tokenizer():

    def __init__(self, req_training=False):
        
        self.req_training = req_training
        self.merges = {}
        self.vocab = {}
        self.vocab_size = 256 
        self.splitter = re.compile(r"""'s|'t|'re|'ve|'m|'ll|'d| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+""")       # from OpenAi's gpt2
        if req_training == False:        # load info from file
            self.load_vocab()
        
    
    def get_pairs(self,tokens):
        '''tokens: list of list of idx'''

        counts = {}
        for tok in tokens:
            for pair in zip(tok[:-1],tok[1:]):
                counts[pair] = counts.get(pair,0) + 1
        
        return counts
    
    def rep_merge(self,tokens,pair,index):
        '''replaces pair and merges to vocab'''
        res = []
        for tok in tokens:
            i = 0
            mod_tokens = []
            while i<len(tok):
                if i+1<len(tok) and tok[i]==pair[0] and tok[i+1]==pair[1]:
                    mod_tokens.append(index)
                    i += 2
                else:
                    mod_tokens.append(tok[i])
                    i+=1
            res.append(mod_tokens)

        return res

    def load_vocab(self):
        with open("vocab.pkl", "rb") as f:
            self.vocab = pickle.load(f)
        with open("merges.pkl", "rb") as f:
            self.merges = pickle.load(f)
        self.vocab_size = len(self.vocab)

        
    def train(self, corpus, val, number_of_merges):
        
        if self.req_training == False:
            print("Tokenizer is not in training mode. Cannot train again.")
            return None
        
        tokens = re.findall(self.splitter, corpus)
        tokens = [list(t.encode('utf-8')) for t in tokens]             
        val_tokens = re.findall(self.splitter, val)
        val_tokens = [list(t.encode('utf-8')) for t in val_tokens]     
      
        n = number_of_merges
        idx = 256
        tok = tokens.copy()
        while number_of_merges>0:
            counts = self.get_pairs(tok)
            most_freq = max(counts, key=counts.get) 
            self.merges[most_freq] = idx
            tok = self.rep_merge(tok, most_freq, idx)
            idx += 1
            number_of_merges-=1

        train_initial = sum(len(el) for el in tokens)
        train_final = sum(len(el) for el in tok)

        self.vocab = {i:bytes([i]) for i in range(0,256)}
        for (k1,k2),v in self.merges.items():
            self.vocab[v] = self.vocab[k1] + self.vocab[k2]

        val_encoded = self.encoder(val)
        val_initial = sum(len(el) for el in val_tokens)
        val_final = len(val_encoded)

        # save the config
        with open("vocab.pkl", "wb") as f:
            pickle.dump(self.vocab, f)
        with open("merges.pkl", "wb") as f:
            pickle.dump(self.merges, f)
        
        self.vocab_size = len(self.vocab)

        return {'val_compression': val_initial/val_final, 'train_compression': train_initial/train_final, 'vocab_size': self.vocab_size}

    
    def encoder(self,text):

        '''inputs: string'''

        tokens = re.findall(self.splitter, text)
        tokens = [list(t.encode('utf-8')) for t in tokens]             # list of list of idx

        while True:
            pairs = self.get_pairs(tokens)
            if not pairs:
                break
            # order the pair acc to index in merges table    --- merge 256 appears before 257 and hence independent of 257 ie. 257 -> (256,32) but 256 will never contains anything ahead
            min_pair = min(pairs, key=lambda x: self.merges.get(x, float('inf'))) 
            if min_pair not in self.merges:          # key: inf of all pairs
                break
            tokens = self.rep_merge(tokens, min_pair, self.merges[min_pair])
        
        out = []
        for tok in tokens:
            out.extend(tok)
        
        return out
    
    def decoder(self, input):
        '''inputs: list of idx'''

        tokens = b''.join([self.vocab[i] for i in input])
        text = tokens.decode('utf-8', errors='replace')
        return text





