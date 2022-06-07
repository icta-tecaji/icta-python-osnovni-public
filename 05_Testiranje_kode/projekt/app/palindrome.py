def is_palindrome(s):
    s = s.lower()
    s = s.replace(" ", "").strip()
    s = "".join(ch for ch in s if ch.isalnum())
    return s == s[::-1]
