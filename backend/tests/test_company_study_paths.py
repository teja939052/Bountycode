from app.data.study_materials import get_company_learning_path


def test_service_company_path_prioritizes_aptitude_and_database_foundations():
    path = get_company_learning_path("TCS NQT")
    assert path is not None
    assert path["company"] == "TCS"
    assert path["study_modules"]
    assert path["study_modules"][0]["category"] == "aptitude"
    assert {"dbms", "sql", "operating-systems", "computer-networks"} <= {
        module["category"] for module in path["study_modules"]
    }


def test_company_aliases_resolve_to_canonical_paths():
    assert get_company_learning_path("TCS-NQT")["company"] == "TCS"
    assert get_company_learning_path("Infosys Specialist Programmer")["company"] == "Infosys"
    assert get_company_learning_path("techm")["company"] == "Tech Mahindra"
    assert get_company_learning_path("Tech Mahindra")["company"] == "Tech Mahindra"
    assert get_company_learning_path("LTIMindtree")["company"] == "LTIMindtree"
    assert get_company_learning_path("Infosys SP")["company"] == "Infosys"


def test_company_path_is_explainable_and_unknown_companies_are_not_guessed():
    path = get_company_learning_path("Accenture")
    assert path["focus_areas"]
    assert path["module_count"] == len(path["study_modules"])
    assert "vary" in path["disclaimer"]
    assert get_company_learning_path("made-up-company") is None
