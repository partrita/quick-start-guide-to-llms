"""Sentence splitting that stays linear in the size of its input.

Splitting on punctuation with a single regular expression is polynomial in the
worst case: on hostile input such as a long run of spaces, quotes or repeated
punctuation the engine retries the tail of the pattern from every position, so
one request can pin a worker for minutes (CWE-1333, CWE-400). Walking the string
once removes the backtracking entirely.
"""

# Punctuation that ends a sentence, and the quotes/brackets that may trail it.
_SENTENCE_END = ".?!"
_TRAILING_MARKS = "'\")]"


def split_sentences(text):
    """Split ``text`` after sentence-ending punctuation.

    The delimiter -- the punctuation, any closing quotes or brackets, the spaces
    before it and the whitespace after it -- is dropped, matching the previous
    ``re.split`` behaviour (the old pattern was
    ``r'(?<!\\s)\\s*[\\.\\?!][\\'\"\\)\\]]*\\s*'``).

    Runs in O(len(text)) for every input, so it cannot be used for a
    denial-of-service attack.
    """
    parts = []
    start = 0
    index = 0
    length = len(text)

    while index < length:
        if text[index] not in _SENTENCE_END:
            index += 1
            continue

        # Keep the spaces that precede the punctuation out of the sentence.
        end = index
        while end > start and text[end - 1] == " ":
            end -= 1
        parts.append(text[start:end])

        index += 1
        while index < length and text[index] in _TRAILING_MARKS:
            index += 1
        while index < length and text[index].isspace():
            index += 1
        start = index

    parts.append(text[start:])
    return parts
