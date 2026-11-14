"""Tests for the curated external learning resource catalogue."""
import pytest

from app.routes import learning_resources


def test_resource_catalog_has_unique_ids_and_required_provenance():
    catalog = learning_resources._catalog()
    resources = catalog["resources"]
    ids = [item["id"] for item in resources]

    assert len(ids) == len(set(ids))
    assert len(resources) >= 20
    for item in resources:
        assert item["title"]
        assert item["provider"]
        assert item["url"].startswith("https://")
        assert item["domains"]
        assert item["topics"]
        assert item["rights"]
        assert item["recommended_use"]


def test_domain_filter_finds_dsa_sources():
    matches = [
        item for item in learning_resources._catalog()["resources"]
        if learning_resources._score(item, "dsa", "binary trees heaps graphs") > 0
    ]

    assert any(item["id"] == "mit-ocw-6006-algorithms" for item in matches)
    assert any(item["id"] == "open-data-structures" for item in matches)


def test_domain_filter_finds_sql_sources():
    matches = [
        item for item in learning_resources._catalog()["resources"]
        if learning_resources._score(item, "dbms", "sql joins transactions") > 0
    ]

    assert any(item["id"] == "postgresql-tutorial" for item in matches)
    assert any(item["id"] == "practical-intro-databases" for item in matches)


@pytest.mark.asyncio
async def test_resource_endpoint_returns_original_links_and_rights_notice():
    result = await learning_resources.list_learning_resources(
        domain="dsa", topic="graphs shortest paths", limit=8
    )

    assert result["resources"]
    assert result["count"] <= 8
    assert "original publishers" in result["notice"]
    assert all(item["url"].startswith("https://") for item in result["resources"])
