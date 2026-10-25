import re

def analyze_text(text: str, target_word: str) -> tuple:
    """Analyze a text and return (total_words, target_count, longest_word).

    - Words are sequences of letters/digits (inner apostrophes and hyphens
      are kept), so punctuation does not stick to words.
    - The search for target_word is case-insensitive.
    - If several words share the maximum length, the first one is returned.
    - For an empty text the longest word is an empty string.
    """
    words = re.findall(r"\w+(?:['\u2019-]\w+)*", text)

    total_words = len(words)
    target_count = sum(1 for w in words if w.casefold() == target_word.strip().casefold())
    longest_word = max(words, key=len, default="")

    return total_words, target_count, longest_word


if __name__ == "__main__":
    sample = "Python is great. I love python, and PYTHON loves programmers!"
    result = analyze_text(sample, "python")
    print(result)  # (10, 3, 'programmers')

    total, count, longest = analyze_text(sample, "Python")
    print(f"Total words: {total}")
    print(f"'python' occurrences: {count}")
    print(f"Longest word: {longest}")