import heapq
from collections import defaultdict

class Node:
    def __init__(self, freq, symbol=None, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(frequencies):
    heap = [Node(freq, symbol) for symbol, freq in frequencies.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)
    return heap[0]

def build_huffman_codes(node, prefix="", codebook=None):
    if codebook is None:
        codebook = {}
    if node.symbol is not None:
        codebook[node.symbol] = prefix
    else:
        build_huffman_codes(node.left, prefix + "0", codebook)
        build_huffman_codes(node.right, prefix + "1", codebook)
    return codebook

def encode(data, codebook):
    encoded_data = ""
    for item in data:
        encoded_data += codebook[item]
    return encoded_data

def decode(encoded_data, root):
    decoded_data = ""
    node = root
    for bit in encoded_data:
        if bit == "0":
            node = node.left
        else:
            node = node.right
        if node.symbol is not None:
            decoded_data += str(node.symbol)
            node = root
    return decoded_data

def compress(path):
    with open(path, 'r') as f:
        data = f.read()

    frequencies = defaultdict(int)
    for item in data:
        frequencies[item] += 1

    huffman_tree = build_huffman_tree(frequencies)
    codebook = build_huffman_codes(huffman_tree)

    encoded_data = encode(data, codebook)

    byte_data = int(encoded_data,2)
    with open('compressed_huffman.bin' , 'wb') as f:
        f.write(byte_data.to_bytes((byte_data.bit_length() + 7) // 8, byteorder='big'))

    return encoded_data, huffman_tree

def decompress(encoded_data, huffman_tree):
    decoded_data = decode(encoded_data, huffman_tree)

    with open('decompressed_huffman.txt' , 'w') as f:
        f.write(decoded_data)
