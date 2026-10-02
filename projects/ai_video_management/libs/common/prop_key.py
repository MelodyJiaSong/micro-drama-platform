"""The routing key a props-tree entry carries (follow-up 174).

Every object lives once, under `props/p{N}_{名}/` — story props and the scene
objects that used to sit in zone libraries alike, numbered drama-wide. One
grammar (`libs.common.key_grammar`, shared with equipment), read by the tree
labels and by the downloads import:

| name                | key     | what it is                                  |
|---------------------|---------|---------------------------------------------|
| `p15_两层石木旅店`    | `p15`   | prop folder / its card                      |
| `p15-1_正面.png`     | `p15-1` | view 1 of that prop                         |
| `mesh/p15.glb`       | —       | the prop's one mesh (its name is the key)   |
"""
from __future__ import annotations

from libs.common.key_grammar import VIEW_NAMES, KeyGrammar, NumberedKey

PropKey = NumberedKey

_GRAMMAR = KeyGrammar("p")
split_name = _GRAMMAR.split_name
label = _GRAMMAR.label
parse_name = _GRAMMAR.parse_name
first_key = _GRAMMAR.first_key


__all__ = ["VIEW_NAMES", "PropKey", "first_key", "label", "parse_name", "split_name"]
