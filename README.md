# Custom Tokenizer

A byte-level Byte Pair Encoding (BPE) tokenizer implemented from scratch in Python.

## Implemented

- Counts adjacent token pairs
- Merges frequent token pairs
- Builds a vocabulary of byte sequences
- Tokenizes text using learned merge rules
- Reconstructs text from token IDs
- Supports UTF-8 text and downloaded book-text datasets

## Tokenizer flow

```text
Training text -> getVocab() -> vocabulary and merge rules
Text -> tokenize() -> token IDs
Token IDs -> untokenize() -> text
```

## Basic usage

```python
training_tokens = list(training_text.encode("utf-8"))
vocab, merges, _ = getVocab(500, training_tokens)

tokens, _ = tokenize("text to tokenize", merges)
text = untokenize(tokens, vocab)
```

The tokenizer starts with the 256 possible byte values and adds new tokens for frequently occurring byte pairs.
