from my_bpe import Tokenizer

training_file = 'output.txt'
val_file = 'val.txt'
merges = 1500


tokenizer = Tokenizer(req_training=True)
with open(training_file,'r') as f:
    corpus = f.read()

with open(val_file,'r') as f:
    val = f.read()

cmp = tokenizer.train(corpus,val,merges)
# return the compression ratio and vocab size
print(cmp)

text = "Hello there! \n This is a test. \n I am testing the tokenizer. \n"

tokens = tokenizer.encoder(text)
print(tokens)

print(tokenizer.decoder(tokens))

print(tokenizer.decoder(tokenizer.encoder(val)) == val)