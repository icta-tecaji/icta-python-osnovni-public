"""Iz sledečega list-a pridobite vrednost ffff."""

our_list = ["a", ["bb", "cc"], "d", [["eee"], ["ffff"], "ggg"]]

# Rešitev
print(our_list)  # noqa: T201
print(our_list[3])  # noqa: T201
print(our_list[3][1])  # noqa: T201
print(our_list[3][1][0])  # noqa: T201
