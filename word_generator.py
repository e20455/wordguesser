#Generate a wordlist from a list of words. Adds the definition as the hint.
#uses data from WordNet
#Princeton University, 2010. About WordNet. [online]. Available from: https://wordnet.princeton.edu/citing-wordnet [Accessed 5th January 2023]. 
from PyDictionary import PyDictionary
dictionary=PyDictionary()

words = []

with open ('words.txt', 'r') as my_file:
    for line in my_file:
        try:
            line = line.split('\n')[0]
            print('Processing {}'.format(line))
            definition = dictionary.meaning(line)
            definition = list(definition.values())[0][0]
            words.append('{},{}\n'.format(line, definition))
        except:
            print("Couldn't find definition for: {}".format(line))
    my_file.close()

with open('wordlist.txt', 'w') as wordlist:
    wordlist.writelines(words)
    wordlist.close()