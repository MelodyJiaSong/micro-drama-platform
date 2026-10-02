"""The routing key an equipment-tree entry carries.

Every piece of equipment lives once, as an `e{N}_{品质}_{名}/` folder somewhere
under `equipment/`. The number is a path code (drama follow-up 028): each folder
above it carries a number and a child's number starts with its parent's —
`5_近战武器/51_主手/e5103_…`. Those folders are walked through, never parsed,
and so is the quality tier in the name; the key is parsed as an ordinary number. Same
grammar as props (`libs.common.key_grammar`), read by the tree labels and by the
downloads import:

| name                     | key     | what it is                    |
|--------------------------|---------|-------------------------------|
| `e5103_灰_干草叉`          | `e5103` | item folder / its card        |
| `e5103-1_正面.png`        | `e5103-1` | view 1 of that item           |
"""
from __future__ import annotations

from libs.common.key_grammar import VIEW_NAMES, KeyGrammar, NumberedKey

EquipmentKey = NumberedKey

_GRAMMAR = KeyGrammar("e")
split_name = _GRAMMAR.split_name
label = _GRAMMAR.label
parse_name = _GRAMMAR.parse_name
first_key = _GRAMMAR.first_key


__all__ = ["VIEW_NAMES", "EquipmentKey", "first_key", "label", "parse_name", "split_name"]
