from __future__ import annotations

from libs.domain.value_objects.facecluster__valueobject import (
    cluster_embeddings,
    cosine,
    rank_by_similarity,
)

_A = (1.0, 0.0, 0.0)
_A2 = (0.95, 0.05, 0.0)
_B = (0.0, 1.0, 0.0)
_B2 = (0.05, 0.95, 0.0)
_LONER = (0.0, 0.0, 1.0)


def test_cosine_basics() -> None:
    assert cosine(_A, _A) == 1.0
    assert cosine(_A, _B) == 0.0
    assert cosine((0.0, 0.0), (0.0, 0.0)) == 0.0


def test_two_characters_form_two_clusters() -> None:
    clusters = cluster_embeddings([_A, _A2, _B, _B2, _A, _B], min_cluster_size=2)
    assert len(clusters) == 2
    sizes = sorted(len(c.member_indices) for c in clusters)
    assert sizes == [3, 3]


def test_small_clusters_dropped_as_extras() -> None:
    clusters = cluster_embeddings([_A, _A2, _A, _LONER], min_cluster_size=3)
    assert len(clusters) == 1
    assert len(clusters[0].member_indices) == 3


def test_cluster_ids_ordered_by_size() -> None:
    clusters = cluster_embeddings([_A, _A2, _A, _A, _B, _B2], min_cluster_size=2)
    assert clusters[0].cluster_id == "c1"
    assert len(clusters[0].member_indices) > len(clusters[1].member_indices)


def test_rank_by_similarity_is_descending_and_stable() -> None:
    ranking = rank_by_similarity(_A, [_B, _A2, _A])
    assert [idx for idx, _ in ranking] == [2, 1, 0]
    assert ranking[0][1] == 1.0
