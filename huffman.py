import heapq
from collections import defaultdict
from PIL import Image

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
    #print(codebook)
    return codebook

def encode_image(image_data, codebook):
    encoded_data = ""
    for pixel in image_data:
        encoded_data += codebook[pixel]
    return encoded_data

def decode_image(encoded_data, root):
    decoded_data = ""
    node = root
    for bit in encoded_data:
        if bit == "0":
            node = node.left
        else:
            node = node.right
        if node.symbol is not None:
            decoded_data += node.symbol
            node = root
    return decoded_data

def compress_image(image_data):
    frequencies = defaultdict(int)
    for pixel in image_data:
        frequencies[pixel] += 1

    huffman_tree = build_huffman_tree(frequencies)
    codebook = build_huffman_codes(huffman_tree)

    encoded_data = encode_image(image_data, codebook)
    return encoded_data, huffman_tree

def decompress_image(encoded_data, huffman_tree):
    decoded_data = decode_image(encoded_data, huffman_tree)
    return decoded_data

def get_image_data(image_path):
    try:
        image = Image.open(image_path)
        image = image.convert("L")
        image_data = image.tobytes()
        return image_data
    except Exception as e:
        print("Error:", e)
        return None

# Usage
image_path = "ness.png"
image_data = get_image_data(image_path)
#if image_data:
#    print("Image data:", image_data)
#else:
#    print("Failed to get image data.")

compressed_data, huffman_tree = compress_image(image_data)
#print("Compressed data:", compressed_data)
#decompressed_data = decompress_image(compressed_data, huffman_tree)
#print("Decompressed data:", decompressed_data)
