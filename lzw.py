import os
import pickle

PATH = os.getcwd()

def compress(path):
    DICTIONARY_SIZE = 256
    dictionary = {}
    result = []
    temp = ""
    input = open(path, "rb").read()

    for i in range(0, DICTIONARY_SIZE):
        dictionary[str(chr(i))] = i

    for c in input:
        temp2 = temp+str(chr(c))
        if temp2 in dictionary.keys():
            temp = temp2
        else:
            result.append(dictionary[temp])
            dictionary[temp2] = DICTIONARY_SIZE
            DICTIONARY_SIZE+=1
            temp = ""+str(chr(c))

    if temp != "":
        result.append(dictionary[temp])


    output = open(PATH+"//"+"compressed_lzw.bin", "wb")
    pickle.dump(result, output)

def decompress():
    DICTIONARY_SIZE = 256
    dictionary = {}
    result = []
    input = pickle.load(open(PATH+"//"+"compressed_lzw.bin", "rb"))

    for i in range(0, DICTIONARY_SIZE):
        dictionary[i] = str(chr(i))

    previous = chr(input[0])
    input = input[1:]
    result.append(previous)

    for bit in input:
        aux = ""
        if bit in dictionary.keys():
            aux = dictionary[bit]
        else:
            aux = previous+previous[0]
        result.append(aux)
        dictionary[DICTIONARY_SIZE] = previous + aux[0]
        DICTIONARY_SIZE+= 1
        previous = aux


    output = open(PATH+"//"+"decompressed_lzw.txt", "w")
    for l in result:
            output.write(l)
    output.close()
