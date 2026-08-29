from __future__ import annotations

import math
from dataclasses import dataclass

_SAME_PERSON_COSINE = 0.55


def cosine(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na > 0 and nb > 0 else 0.0


def _normalize(e: tuple[float, ...]) -> tuple[float, ...]:
    norm = math.sqrt(sum(x * x for x in e))
    return tuple(x / norm for x in e) if norm > 0 else e


def centroid(embeddings: list[tuple[float, ...]]) -> tuple[float, ...]:
    n = len(embeddings)
    return tuple(sum(e[i] for e in embeddings) / n for i in range(len(embeddings[0])))


@dataclass(frozen=True)
class FaceCluster:
    cluster_id: str
    member_indices: tuple[int, ...]


def cluster_embeddings(
    embeddings: list[tuple[float, ...]],
    threshold: float = _SAME_PERSON_COSINE,
    min_cluster_size: int = 5,
) -> list[FaceCluster]:
    """Single-link agglomerative clustering via union-find: two faces are the
    same character when embedding cosine >= threshold. Clusters smaller than
    min_cluster_size are dropped (extras/背景路人).

    Known failure mode of single-link: transitive chaining (A~B, B~C) can merge two
    look-alike characters — the conservative 0.55 threshold biases toward over-splitting
    instead; the FR-3.3 manual merge/split UI is the intended backstop (NOT built in v1 —
    see README 已知实现边界). Pairwise O(n²) on
    pre-normalized vectors: fine per-episode (~10² faces); a whole-drama call with 10³+
    faces should move to a numpy backend behind the FaceEngine seam."""
    normed = [_normalize(e) for e in embeddings]
    parent = list(range(len(embeddings)))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for i in range(len(normed)):
        for j in range(i + 1, len(normed)):
            if sum(x * y for x, y in zip(normed[i], normed[j])) >= threshold:
                parent[find(i)] = find(j)

    groups: dict[int, list[int]] = {}
    for i in range(len(embeddings)):
        groups.setdefault(find(i), []).append(i)
    kept = [sorted(members) for members in groups.values() if len(members) >= min_cluster_size]
    kept.sort(key=lambda m: (-len(m), m[0]))
    return [FaceCluster(cluster_id=f"c{i + 1}", member_indices=tuple(m)) for i, m in enumerate(kept)]


def rank_by_similarity(
    reference: tuple[float, ...],
    candidates: list[tuple[float, ...]],
) -> list[tuple[int, float]]:
    scored = [(idx, cosine(reference, emb)) for idx, emb in enumerate(candidates)]
    return sorted(scored, key=lambda t: (-t[1], t[0]))
