from app.data.study_materials import get_article, get_articles, get_categories


PLACEMENT_CORE_IDS = {
    "dbms-er-model-keys",
    "dbms-normalization-fd",
    "dbms-transactions-concurrency",
    "os-process-threads-scheduling",
    "os-memory-virtual-memory",
    "os-deadlocks-synchronization",
    "networks-tcp-ip-dns-http",
    "networks-subnetting-routing",
    "networks-udp-reliability",
    "aptitude-percentages-profit-loss",
    "aptitude-time-work-speed",
    "aptitude-number-system-algebra",
    "aptitude-reasoning-series-arrangements",
    "aptitude-verbal-comprehension-grammar",
}


def test_placement_subject_categories_are_discoverable():
    category_ids = {category["id"] for category in get_categories()}
    assert {"dbms", "operating-systems", "computer-networks", "aptitude"} <= category_ids


def test_authored_placement_core_articles_are_registered():
    all_ids = {article["id"] for article in get_articles()}
    assert PLACEMENT_CORE_IDS <= all_ids


def test_authored_placement_core_articles_have_complete_learning_material():
    for article_id in PLACEMENT_CORE_IDS:
        article = get_article(article_id)
        assert article is not None, article_id
        assert len(article["sections"]) >= 4, article_id
        assert all(len(section["body"]) >= 100 for section in article["sections"]), article_id
        assert len(article["key_takeaways"]) >= 4, article_id
        assert len(article["quiz"]) >= 4, article_id
        for question in article["quiz"]:
            assert len(question["options"]) >= 4, article_id
            assert 0 <= question["answer"] < len(question["options"]), article_id
            assert question["explanation"], article_id
        exercise = article["exercise"]
        assert exercise["task"] and exercise["starter"] and exercise["solution"], article_id


def test_subject_articles_are_assigned_to_their_own_curriculum():
    expected = {
        "dbms": "dbms-er-model-keys",
        "operating-systems": "os-process-threads-scheduling",
        "computer-networks": "networks-tcp-ip-dns-http",
        "aptitude": "aptitude-percentages-profit-loss",
    }
    for category, article_id in expected.items():
        article = get_article(article_id)
        assert article["category"] == category
        assert category in article["curriculum"]
