from collections.abc import Sequence
from itertools import pairwise


def occuranceCounter(tokens: Sequence[int]) -> dict[tuple[int, int], int]:
    counts: dict[tuple[int, int], int] = {}
    for pair in pairwise(tokens):
        counts[pair] = counts.get(pair, 0) + 1
    return counts

# Merges all occurances of given pair and returns the tokens
def mergeTokens(tokens: Sequence[int], tokenPair: tuple[int,int], replaceWith: int) -> list[int]:
    output: list[int] = []
    i = 0
    length = len(tokens)
    while i < length:
        if i < (length - 1) and tokens[i] == tokenPair[0] and tokens[i + 1] == tokenPair[1]:
            output.append(replaceWith)
            i = i + 2
        else:
            output.append(tokens[i])
            i = i + 1
    return output

# adds the initial 255 tokens
def initVocab() -> dict[int, bytes]:
    return {i: bytes([i]) for i in range(256)}

# Auto Creates Vocb upto given size usign most common pair and mergining
def getVocab(
    vocab_size: int,
    tokens: Sequence[int],
) -> tuple[dict[int, bytes], dict[tuple[int, int], int], list[int]]:
    currTokens = list(tokens)
    vocab = initVocab()
    vocabStart = len(vocab)
    merges: dict[tuple[int, int], int] = {}
    if (len(vocab) < vocab_size):
        for i in range(vocab_size - len(vocab)):
            counts = occuranceCounter(currTokens)
            if not counts:
                break
            topPair = max(counts, key=lambda pair: counts.get(pair,0))
            if (counts[topPair] <= 1):
                break
            currTokens = mergeTokens(currTokens, topPair, (vocabStart + i))
            merges[topPair] = (vocabStart + i)
            vocab[vocabStart + i] = vocab[topPair[0]] + vocab[topPair[1]]
            print(f"merged {topPair} with {counts[topPair]} ocr. | len: {len(currTokens)}")
    else:
        print("vocab already maxxed!")
    return vocab, merges, currTokens

# Tokenizes text
def tokenize(text: str, merges: dict[tuple[int, int], int]) -> list[int]:
    tokens: list[int] = list(text.encode("utf-8"))
    print(f"Iniital size: {len(tokens)} | ", end='')
    while(True):
        counts = occuranceCounter(tokens)
        commonPairs = [k for k in merges if k in counts]
        if not commonPairs:
            break
        tokens = mergeTokens(tokens, commonPairs[0], merges[commonPairs[0]])
    print(f"Final Size: {len(tokens)}")
    print(f"Compression Ratio: {len(text) / len(tokens):.3f}")
    return tokens

# Reverts Tokens to text
def untokenize(tokens: Sequence[int], vocab: dict[int,bytes]) -> str:
    tokenUnmerged = b"".join(vocab[token] for token in tokens)
    return tokenUnmerged.decode("utf-8", errors='replace')

def train(text: Sequence[int],size: int) -> tuple[dict[int,bytes],dict[tuple[int,int],int],list[int]]:
    vocab, merges, final = getVocab(size, text)
    return vocab , merges, final

###
# example trian and encode
###

from pathlib import Path

import kagglehub

# Download the dataset
dataset_path = kagglehub.dataset_download(
    "madhavendraoo7/book-text-files"
)

print("Dataset downloaded to:", dataset_path)

dataset_path = Path(dataset_path)

text = ""

for file_path in sorted(dataset_path.glob("*.txt")):
    book = file_path.read_text(
        encoding="utf-8",
        errors="replace"
    )
    text += book

print(f"All Books are conmbined: {len(text)} chars long")

# Train Tokenizer
data = list(text.encode("utf-8"))

# get vocab, keep size > 255
vocab_size = 400
vocab, merges, tokenized = train(data, vocab_size)
compressionRatio = len(data)/len(tokenized)
print(f"Compressed by {compressionRatio}")

# tokeize and untokenize
tokens = tokenize(text, merges)
textBack = untokenize(tokens, vocab)

print(text == textBack)
