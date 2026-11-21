from app.data.study_materials import get_article, get_articles


SQL_PLACEMENT_ARTICLE_IDS = {
    "sql-relational-foundations",
    "sql-select-filter-sort",
    "sql-aggregation-group-having",
    "sql-subqueries-cte",
    "sql-window-functions",
    "sql-normalization-transactions",
    "sql-indexes-query-plans",
    "sql-set-operations",
}


def test_sql_placement_lessons_are_registered_in_study_library():
    articles = {article["id"]: article for article in get_articles("sql")}
    assert SQL_PLACEMENT_ARTICLE_IDS.issubset(articles.keys())


def test_sql_placement_lessons_have_explanations_examples_quizzes_and_exercises():
    for article_id in SQL_PLACEMENT_ARTICLE_IDS:
        article = get_article(article_id)
        assert article is not None, article_id
        assert len(article["sections"]) >= 4, article_id
        assert all(len(section["body"]) >= 100 for section in article["sections"]), article_id
        assert all(section.get("code") for section in article["sections"]), article_id
        assert len(article["quiz"]) >= 4, article_id
        assert all(0 <= quiz["answer"] < len(quiz["options"]) for quiz in article["quiz"]), article_id
        assert all(quiz.get("explanation") for quiz in article["quiz"]), article_id
        exercise = article["exercise"]
        assert exercise["task"] and exercise["starter"] and exercise["solution"], article_id
        assert len(article["key_takeaways"]) >= 4, article_id
