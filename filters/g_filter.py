import re

def is_word_count_within_limits(text, min_words=2, max_words=50):
    """Check if the number of words is within [min_words, max_words]."""
    word_count = len(text.split())
    return min_words <= word_count <= max_words

def is_gibberish(text):
    """Detect gibberish: mostly non-alphabetic or repeated chars."""
    # Remove whitespace
    stripped = re.sub(r'\s+', '', text)
    if not stripped.isalpha():
        # If most chars are not alphabetic or numbers, it's probably gibberish.
        non_alpha = sum(1 for c in stripped if not c.isalpha())
        if non_alpha / len(stripped) > 0.5:
            return True
    # Detect repeated single character like "aaaaaaa"
    if len(set(stripped)) <= 2 and len(stripped) > 5:
        return True
    # Detect if all consonants/vowels (very unlikely in real words)
    vowels = set("aeiou")
    if all(c in vowels for c in stripped.lower()) or all(c not in vowels for c in stripped.lower()):
        return True
    return False

def text_filter(text, min_words=2, max_words=50):
    """Combined filter: returns True if text is clean, False otherwise."""
    if not is_word_count_within_limits(text, min_words, max_words):
        return False
    if is_gibberish(text):
        return False
    return True