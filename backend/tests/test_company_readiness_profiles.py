from app.services.readiness_engine import build_target_profile


def test_company_display_names_resolve_to_canonical_readiness_profiles():
    assert build_target_profile(company="Tech Mahindra")["company"] == "tech_mahindra"
    assert build_target_profile(company="LTI Mindtree")["company"] == "lti_mindtree"
    assert build_target_profile(company="TCS NQT")["company"] == "tcs"
    assert build_target_profile(company="Infosys SP")["company"] == "infosys"
    assert build_target_profile(company="Wipro Turbo")["company"] == "wipro"


def test_company_target_profile_weights_are_normalized():
    for company in ("TCS", "Infosys", "Wipro", "Accenture", "Tech Mahindra", "LTI Mindtree"):
        profile = build_target_profile(role="sde", company=company)
        assert profile["skills"]
        assert abs(sum(skill["weight"] for skill in profile["skills"]) - 1.0) < 0.001
        assert all(skill["domain"] for skill in profile["skills"])
