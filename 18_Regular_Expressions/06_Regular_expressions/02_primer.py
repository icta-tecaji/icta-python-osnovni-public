from typing import List
import re


def search_in_list(list_text: List) -> int:
    # Naloga: koliko krat se pojavi beseda blue oz Blue v našem tekstu.
    blue_mentions = 0
    pattern = r"[Bb]lue"

    for line in list_text:
        if re.search(pattern, line):
            blue_mentions += 1

    return blue_mentions


def count_matches_in_list(list_text: List, pattern: str) -> int:
    counts = 0
    values = []
    for line in list_text:
        if re.search(pattern, line):
            counts += 1
            values.append(line)
    return counts, values


if __name__ == "__main__":
    # string_list = ["Julie's favorite color is Blue.", "Keli's favorite color is Green.", "Craig's favorite colors are blue and red."]
    # mentions = search_in_list(string_list)
    # print(f"Found {mentions} mentions.")

    titles = [
        "Interactive Dynamic Video",
        "Florida DJs May Face Felony for April Fools' Water Joke",
        "Technology ventures: From Idea to Enterprise",
        "Note by Note: The Making of Steinway python L1037 (2007)",
        "Title II kills investment? Comcast and other ISPs are now spending more",
        "Nuts and Bolts Business Advice",
        "Ask HN: How to improve my Python personal website?",
        "Shims, Jigs and Other Woodworking Concepts to Conquer Technical Debt",
        "That self-appendectomy",
        "Custom Deleters for C++ Smart Pointers",
        "How often to update third party libraries?",
        "Review my AI based marketing bot",
        "Ask HN: Am I the only one outraged by Twitter python shutting down share counts?",
        "Ten years later, Python did Boston's Big Dig deliver?",
    ]
    pattern = r"[Pp]ython"
    counts, values = count_matches_in_list(titles, pattern)
    print(f"Counter is {counts}. Values: {values}")
