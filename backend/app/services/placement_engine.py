import math
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from app.database import gamification_collection, skill_graph_collection, predictions_collection


class PlacementEngine:
    """
    Pure math-driven placement probability calculator.
    Zero AI cost. Deterministic scoring matrix.
    """

    # Company profiles with real acceptance rate data
    COMPANY_PROFILES = {
        # FAANG
        "google": {"rate": 0.002, "min_score": 8, "tier": "FAANG", "color": "#4285F4"},
        "amazon": {"rate": 0.010, "min_score": 7, "tier": "FAANG", "color": "#FF9900"},
        "meta": {"rate": 0.005, "min_score": 8, "tier": "FAANG", "color": "#1877F2"},
        "microsoft": {"rate": 0.020, "min_score": 7, "tier": "FAANG", "color": "#00A4EF"},
        "apple": {"rate": 0.005, "min_score": 8, "tier": "FAANG", "color": "#A2AAAD"},
        "netflix": {"rate": 0.003, "min_score": 9, "tier": "FAANG", "color": "#E50914"},

        # Product Companies
        "flipkart": {"rate": 0.030, "min_score": 6, "tier": "Product", "color": "#2874F0"},
        "razorpay": {"rate": 0.040, "min_score": 6, "tier": "Product", "color": "#072654"},
        "swiggy": {"rate": 0.035, "min_score": 6, "tier": "Product", "color": "#FC8019"},
        "zomato": {"rate": 0.035, "min_score": 6, "tier": "Product", "color": "#E23744"},
        "phonepe": {"rate": 0.040, "min_score": 6, "tier": "Product", "color": "#5F259F"},
        "uber": {"rate": 0.008, "min_score": 7, "tier": "Product", "color": "#000000"},
        "airbnb": {"rate": 0.006, "min_score": 7, "tier": "Product", "color": "#FF5A5F"},
        "spotify": {"rate": 0.008, "min_score": 7, "tier": "Product", "color": "#1DB954"},

        # Services / IT
        "tcs": {"rate": 0.150, "min_score": 4, "tier": "Services", "color": "#0072C6"},
        "infosys": {"rate": 0.120, "min_score": 4, "tier": "Services", "color": "#007CC3"},
        "wipro": {"rate": 0.120, "min_score": 4, "tier": "Services", "color": "#005B9E"},
        "hcl": {"rate": 0.110, "min_score": 4, "tier": "Services", "color": "#003366"},
        "tech mahindra": {"rate": 0.100, "min_score": 4, "tier": "Services", "color": "#E91E63"},
        "cognizant": {"rate": 0.100, "min_score": 4, "tier": "Services", "color": "#0033A0"},
        "accenture": {"rate": 0.080, "min_score": 5, "tier": "Services", "color": "#A100FF"},
        "capgemini": {"rate": 0.090, "min_score": 5, "tier": "Services", "color": "#0070AD"},

        # Startups (India)
        "paytm": {"rate": 0.050, "min_score": 6, "tier": "Startup", "color": "#00BAF2"},
        "ola": {"rate": 0.045, "min_score": 6, "tier": "Startup", "color": "#2A6DFF"},
        "byju's": {"rate": 0.055, "min_score": 5, "tier": "Startup", "color": "#00C853"},
        "cred": {"rate": 0.040, "min_score": 7, "tier": "Startup", "color": "#1A1A1A"},
        "meesho": {"rate": 0.050, "min_score": 6, "tier": "Startup", "color": "#F43397"},
    }

    # Skill weights by company tier
    TIER_WEIGHTS = {
        "FAANG": {
            "dsa": 0.30,
            "system_design": 0.25,
            "behavioral": 0.20,
            "aptitude": 0.10,
            "resume": 0.15,
        },
        "Product": {
            "dsa": 0.25,
            "system_design": 0.20,
            "behavioral": 0.25,
            "aptitude": 0.10,
            "resume": 0.20,
        },
        "Services": {
            "dsa": 0.20,
            "system_design": 0.10,
            "behavioral": 0.25,
            "aptitude": 0.30,
            "resume": 0.15,
        },
        "Startup": {
            "dsa": 0.25,
            "system_design": 0.30,
            "behavioral": 0.20,
            "aptitude": 0.05,
            "resume": 0.20,
        },
    }

    # Role-specific skill emphasis. Values are multipliers applied to the
    # tier weights before renormalization, so e.g. DSA weighs more for SDEs
    # and behavioral weighs more for PMs. Neutral = 1.0 (no change).
    ROLE_WEIGHTS = {
        "sde": {"dsa": 1.30, "system_design": 1.20, "behavioral": 0.85, "aptitude": 0.70, "resume": 0.90},
        "backend": {"dsa": 1.35, "system_design": 1.35, "behavioral": 0.80, "aptitude": 0.60, "resume": 0.80},
        "frontend": {"dsa": 1.00, "system_design": 1.15, "behavioral": 0.95, "aptitude": 0.70, "resume": 1.00},
        "full_stack": {"dsa": 1.15, "system_design": 1.25, "behavioral": 0.90, "aptitude": 0.65, "resume": 0.95},
        "data": {"dsa": 1.30, "system_design": 1.00, "behavioral": 0.80, "aptitude": 1.20, "resume": 0.90},
        "data_scientist": {"dsa": 1.30, "system_design": 0.95, "behavioral": 0.80, "aptitude": 1.25, "resume": 0.90},
        "data_engineer": {"dsa": 1.30, "system_design": 1.10, "behavioral": 0.80, "aptitude": 1.10, "resume": 0.90},
        "ml": {"dsa": 1.40, "system_design": 0.95, "behavioral": 0.80, "aptitude": 1.10, "resume": 0.85},
        "devops": {"dsa": 0.85, "system_design": 1.30, "behavioral": 0.90, "aptitude": 0.70, "resume": 1.00},
        "pm": {"dsa": 0.60, "system_design": 0.70, "behavioral": 1.50, "aptitude": 0.90, "resume": 1.30},
        "management": {"dsa": 0.60, "system_design": 0.75, "behavioral": 1.45, "aptitude": 0.85, "resume": 1.35},
        "qa": {"dsa": 0.85, "system_design": 1.05, "behavioral": 1.10, "aptitude": 0.90, "resume": 1.10},
        "analyst": {"dsa": 0.90, "system_design": 0.70, "behavioral": 1.10, "aptitude": 1.40, "resume": 1.10},
        "consultant": {"dsa": 0.85, "system_design": 0.90, "behavioral": 1.25, "aptitude": 0.95, "resume": 1.10},
        "support": {"dsa": 0.70, "system_design": 0.80, "behavioral": 1.35, "aptitude": 0.95, "resume": 1.10},
        "general": {"dsa": 1.00, "system_design": 1.00, "behavioral": 1.00, "aptitude": 1.00, "resume": 1.00},
    }

    ROLE_PROFILE_LABELS = {
        "sde": "SDE",
        "backend": "Backend Engineer",
        "frontend": "Frontend Engineer",
        "full_stack": "Full-Stack Engineer",
        "data": "Data Engineer / Analytics",
        "data_scientist": "Data Scientist",
        "data_engineer": "Data Engineer",
        "ml": "Machine Learning",
        "devops": "DevOps / Infrastructure",
        "pm": "Product Manager",
        "management": "Engineering Manager",
        "qa": "QA / Quality",
        "analyst": "Business Analyst",
        "consultant": "Consultant",
        "support": "Support / Operations",
        "general": "General",
    }

    # Sub-skill breakdown for granular analysis
    SUB_SKILLS = {
        "dsa": [
            "two_pointer", "sliding_window", "binary_search", "sorting",
            "hashing", "stacks_queues", "linked_lists", "trees",
            "graphs", "dynamic_programming", "greedy", "recursion",
        ],
        "system_design": [
            "load_balancing", "caching", "database_design", "message_queues",
            "microservices", "api_design", "security", "monitoring",
        ],
        "behavioral": [
            "leadership", "conflict_resolution", "teamwork", "communication",
            "problem_solving", "adaptability", "customer_focus", "innovation",
        ],
        "aptitude": [
            "quantitative", "logical_reasoning", "verbal_ability",
            "data_interpretation", "puzzles", "mental_ability",
        ],
        "resume": [
            "content_quality", "ats_optimization", "keyword_usage",
            "formatting", "impact_statements", "tailoring",
        ],
    }

    def __init__(self):
        pass

    async def calculate_probability(
        self,
        user_id: str,
        company_name: str,
        role: str = "SDE",
    ) -> Dict[str, Any]:
        """
        Zero-cost deterministic scoring matrix calculation.
        Returns probability, breakdown, what-if scenarios, and improvement roadmap.
        """
        company = company_name.lower().strip()
        if company not in self.COMPANY_PROFILES:
            # Try to find partial match
            matches = [c for c in self.COMPANY_PROFILES if company in c or c in company]
            if matches:
                company = matches[0]
            else:
                raise ValueError(f"Company '{company_name}' not found. Supported: {', '.join(self.COMPANY_PROFILES.keys())}")

        profile = self.COMPANY_PROFILES[company]
        weights = self._effective_weights(profile["tier"], role)

        # Get user's actual scores
        student_scores = await self._get_user_scores(user_id)
        experience_data = await self._get_experience_data(user_id)

        # Calculate base weighted score
        base_score = sum(student_scores.get(skill, 0) * weights[skill] for skill in weights)

        # Hard minimum threshold penalty
        normalized_min_bar = profile["min_score"] * 10
        penalty_multiplier = 1.0
        if base_score < normalized_min_bar:
            # Exponential decay based on distance from cutoff
            ratio = base_score / normalized_min_bar
            penalty_multiplier = 0.4 * ratio

        # Experience modifiers
        experience_modifier = self._calculate_experience_modifier(experience_data)

        # Final probability calculation
        raw_probability = base_score * penalty_multiplier * experience_modifier
        final_probability = min(99.0, max(1.0, raw_probability))

        # Generate what-if scenarios
        what_if_scenarios = self._generate_what_if_analysis(
            student_scores, weights, final_probability, profile
        )

        # Generate improvement roadmap
        improvement_roadmap = self._generate_improvement_roadmap(
            student_scores, weights, profile, final_probability
        )

        has_skill_graph = await self._has_skill_graph(user_id)

        # Explainable factors: per-skill contribution to the weighted score
        factors = self._compute_factors(student_scores, weights, profile, base_score)

        # Confidence band based on how much real data the model saw
        confidence_band = self._compute_confidence_band(
            has_skill_graph, experience_data, final_probability
        )

        # Ranked next-best moves (impact / effort)
        next_best_moves = self._compute_next_best_moves(
            what_if_scenarios, improvement_roadmap
        )

        # Plain-language summary of the result
        what_it_means = self._build_plain_language_summary(
            final_probability, confidence_band, factors, weights, experience_modifier
        )

        # Store prediction for data collection
        await self._store_prediction(
            user_id, company, role, final_probability, student_scores,
            snapshot={
                "factors": factors,
                "confidence_band": confidence_band,
                "next_best_moves": next_best_moves[:3],
            },
        )

        return {
            "target_company": company_name.title(),
            "company_tier": profile["tier"],
            "company_color": profile["color"],
            "historical_acceptance_rate": f"{profile['rate'] * 100:.1f}%",
            "role": role,
            "role_profile": self._role_profile_label(role),
            "current_probability": round(final_probability, 1),
            "probability_band": self._get_probability_band(final_probability),
            "breakdown": {
                "base_score": round(base_score, 1),
                "penalty_applied": penalty_multiplier < 1.0,
                "penalty_multiplier": round(penalty_multiplier, 2),
                "experience_modifier": round(experience_modifier, 2),
                "raw_probability": round(raw_probability, 1),
            },
            "skill_scores": student_scores,
            "skill_weights": weights,
            "sub_skills": await self._get_sub_skill_breakdown(user_id),
            "what_if_scenarios": what_if_scenarios,
            "improvement_roadmap": improvement_roadmap,
            "comparison": await self._get_peer_comparison(user_id, company),
            "factors": factors,
            "confidence_band": confidence_band,
            "next_best_moves": next_best_moves,
            "what_it_means": what_it_means,
        }

    async def _get_user_scores(self, user_id: str) -> Dict[str, float]:
        """Fetch user's skill scores from database."""
        skill_graph = await skill_graph_collection.find_one({"user_id": user_id})

        if not skill_graph:
            return {skill: 0 for skill in self.TIER_WEIGHTS["FAANG"].keys()}

        categories = skill_graph.get("categories", {})
        return {
            "dsa": categories.get("dsa", {}).get("score", 0),
            "system_design": categories.get("system_design", {}).get("score", 0),
            "behavioral": categories.get("behavioral", {}).get("score", 0),
            "aptitude": categories.get("aptitude", {}).get("score", 0),
            "resume": categories.get("resume", {}).get("score", 0),
        }

    async def _has_skill_graph(self, user_id: str) -> bool:
        """Check whether the user has any non-zero skill assessment data."""
        skill_graph = await skill_graph_collection.find_one({"user_id": user_id})
        if not skill_graph:
            return False
        categories = skill_graph.get("categories", {})
        return any(
            cat_data.get("score", 0) > 0
            for cat_data in categories.values()
        )

    def _compute_factors(
        self,
        student_scores: Dict[str, float],
        weights: Dict[str, float],
        profile: Dict,
        base_score: float,
    ) -> List[Dict[str, Any]]:
        """Explainable per-skill factor breakdown.

        Each factor shows the skill's score, its weight for this company tier,
        its actual contribution to the weighted score, and how far below (or
        above) the company's minimum bar it is — so the probability is never a
        black box.
        """
        min_bar = profile["min_score"] * 10
        factors = []
        for skill, weight in weights.items():
            score = student_scores.get(skill, 0)
            contribution = score * weight
            contribution_pct = (contribution / base_score * 100) if base_score > 0 else 0.0
            gap = min_bar - score
            if score >= min(min_bar, 80):
                verdict = "strong"
                message = f"Meets or exceeds the bar ({min_bar:.0f}+)."
            elif score >= 60:
                verdict = "on_track"
                message = f"Close to the bar ({min_bar:.0f}). A {gap:.0f}-point push would help."
            elif score >= 40:
                verdict = "gap"
                message = f"Below the bar ({min_bar:.0f}) by {gap:.0f} points."
            else:
                verdict = "critical"
                message = f"Far below the bar ({min_bar:.0f}). Highest priority."
            factors.append({
                "key": skill,
                "label": self._humanize_skill(skill),
                "score": round(score, 1),
                "weight": round(weight, 2),
                "contribution": round(contribution, 1),
                "contribution_pct": round(contribution_pct, 1),
                "target": min_bar,
                "gap": round(gap, 1),
                "verdict": verdict,
                "message": message,
                "how_to_improve": self._get_specific_action(skill),
                "impact_if_full": round(max(0.0, 100 - score) * weight * 0.8, 1),
            })
        return factors

    def _humanize_skill(self, skill: str) -> str:
        return {
            "dsa": "Data Structures & Algorithms",
            "system_design": "System Design",
            "behavioral": "Behavioral / STAR",
            "aptitude": "Aptitude / Quant",
            "resume": "Resume Quality",
        }.get(skill, skill.replace("_", " ").title())

    def _resolve_role_profile(self, role: str) -> Dict[str, float]:
        """Map a free-form role string to a role weighting profile."""
        if not role:
            return self.ROLE_WEIGHTS["general"]
        r = str(role).lower().strip()
        if r in self.ROLE_WEIGHTS:
            return self.ROLE_WEIGHTS[r]

        def _has(*keys: str) -> bool:
            return any(k in r for k in keys)

        if _has("machine learning", "ai engineer", "deep learning") or "ml" in r.split():
            return self.ROLE_WEIGHTS["ml"]
        if _has("product manager", "program manager", "product owner"):
            return self.ROLE_WEIGHTS["pm"]
        if _has("data scientist", "data science"):
            return self.ROLE_WEIGHTS["data_scientist"]
        if _has("data engineer"):
            return self.ROLE_WEIGHTS["data_engineer"]
        if _has("backend", "server-side", "java developer", "node developer"):
            return self.ROLE_WEIGHTS["backend"]
        if _has("frontend", "front-end", "ui developer", "web developer", "react", "javascript", "html", "css"):
            return self.ROLE_WEIGHTS["frontend"]
        if _has("full stack", "full-stack", "fullstack"):
            return self.ROLE_WEIGHTS["full_stack"]
        if _has("devops", "sre", "infrastructure", "site reliability"):
            return self.ROLE_WEIGHTS["devops"]
        if _has("qa", "quality", "tester", "test engineer"):
            return self.ROLE_WEIGHTS["qa"]
        if _has("analyst", "business intelligence", "finance"):
            return self.ROLE_WEIGHTS["analyst"]
        if _has("manager", "lead ", " head", "director", "principal"):
            return self.ROLE_WEIGHTS["management"]
        if _has("consultant"):
            return self.ROLE_WEIGHTS["consultant"]
        if _has("support", "operations", "operations engineer"):
            return self.ROLE_WEIGHTS["support"]
        if _has("data"):
            return self.ROLE_WEIGHTS["data"]
        if _has("engineer", "developer", "sde", "programmer", "intern", "graduate"):
            return self.ROLE_WEIGHTS["sde"]
        return self.ROLE_WEIGHTS["general"]

    def _effective_weights(self, tier: str, role: str) -> Dict[str, float]:
        """Tier weights rebalanced by the role profile, renormalized to sum 1."""
        tier_weights = self.TIER_WEIGHTS[tier]
        role_weights = self._resolve_role_profile(role)
        combined = {
            skill: tier_weights[skill] * role_weights.get(skill, 1.0)
            for skill in tier_weights
        }
        total = sum(combined.values()) or 1.0
        return {skill: round(value / total, 4) for skill, value in combined.items()}

    def _role_profile_label(self, role: str) -> str:
        profile = self._resolve_role_profile(role)
        for key, weights in self.ROLE_WEIGHTS.items():
            if profile is weights:
                return self.ROLE_PROFILE_LABELS.get(key, key)
        return "General"

    async def calculate_time_to_offer(
        self,
        user_id: str,
        company_name: str,
        role: str = "SDE",
    ) -> Dict[str, Any]:
        """Estimate how many weeks until an offer, from current readiness.

        Transparent and deterministic: typical interview-process length for the
        company tier, plus the prep weeks needed to close weighted skill gaps at
        the user's observed practice velocity. Returns a range, not a magic date.
        """
        company = company_name.lower().strip()
        if company not in self.COMPANY_PROFILES:
            matches = [c for c in self.COMPANY_PROFILES if company in c or c in company]
            if matches:
                company = matches[0]
            else:
                raise ValueError(
                    f"Company '{company_name}' not found. Supported: {', '.join(self.COMPANY_PROFILES.keys())}"
                )

        profile = self.COMPANY_PROFILES[company]
        weights = self._effective_weights(profile["tier"], role)
        student_scores = await self._get_user_scores(user_id)
        experience = await self._get_experience_data(user_id)
        has_skill_graph = await self._has_skill_graph(user_id)

        min_bar = profile["min_score"] * 10
        total_practice = (
            experience["total_interviews"]
            + experience["total_coding"]
            + experience["total_aptitude"]
        )

        # Weighted gap to the company's minimum bar (in contribution points).
        total_gap = 0.0
        gaps = []
        for skill, weight in weights.items():
            gap = max(0.0, min_bar - student_scores.get(skill, 0))
            weighted = gap * weight
            total_gap += weighted
            if gap > 0:
                gaps.append({
                    "skill": skill,
                    "label": self._humanize_skill(skill),
                    "gap": round(gap, 1),
                    "weight": round(weight, 2),
                })
        gaps.sort(key=lambda g: g["gap"] * g["weight"], reverse=True)

        # Improvement velocity (points/week) from observed practice intensity.
        streak = experience["streak"]
        if streak >= 14 and total_practice >= 50:
            velocity = 5.0
        elif streak >= 7 and total_practice >= 20:
            velocity = 4.0
        elif total_practice >= 10:
            velocity = 3.0
        elif total_practice > 0:
            velocity = 2.0
        else:
            velocity = 1.5

        # Typical application-to-offer process length by company tier.
        process_base = {
            "FAANG": 10.0,
            "Product": 8.0,
            "Services": 6.0,
            "Startup": 7.0,
        }.get(profile["tier"], 8.0)

        # Experienced candidates move through rounds faster (small, capped effect).
        experience_mult = 1.0 - min(0.2, math.log(total_practice + 1) * 0.04)
        adjusted_process = max(4.0, process_base * experience_mult)

        prep_weeks = math.ceil(total_gap / velocity) if total_gap > 0 else 0
        weeks = adjusted_process + prep_weeks

        # Range widens when we know less about the user.
        if has_skill_graph and total_practice >= 10:
            spread = 2.0
            data_note = "Based on your skill assessments and practice history."
        elif has_skill_graph:
            spread = 3.0
            data_note = "Based on skill assessments; practice history would tighten this."
        else:
            spread = 4.0
            data_note = "No skill scores recorded — estimate is wide. Take an assessment to sharpen it."

        low = max(1.0, weeks - spread)
        high = weeks + spread

        accelerants = []
        if gaps:
            accelerants.append(f"Close the {gaps[0]['label']} gap — the single biggest time saver.")
        if streak < 7:
            accelerants.append("Build a 7-day streak — consistent practice roughly doubles your improvement speed.")
        if velocity < 4.0:
            accelerants.append(f"Push past {velocity:.0f} points/week with daily drills to cut weeks off this estimate.")
        if total_practice == 0:
            accelerants.append("Start practicing — a zero-activity account can't compress the timeline yet.")
        accelerants.append("Report your outcome after the interview — it sharpens every future estimate.")

        if total_gap == 0:
            readiness = "on_track"
        elif total_gap < 15:
            readiness = "close"
        else:
            readiness = "preparing"

        return {
            "target_company": company_name.title(),
            "company_tier": profile["tier"],
            "role": role,
            "weeks_estimate": int(round(weeks)),
            "range": f"{int(round(low))}-{int(round(high))} weeks",
            "low_weeks": int(round(low)),
            "high_weeks": int(round(high)),
            "process_time_weeks": round(adjusted_process, 1),
            "prep_weeks": prep_weeks,
            "readiness": readiness,
            "velocity": round(velocity, 1),
            "total_gap": round(total_gap, 1),
            "gaps": gaps[:3],
            "accelerants": accelerants,
            "data_note": data_note,
        }

    def _compute_confidence_band(
        self,
        has_skill_graph: bool,
        experience: Dict[str, int],
        probability: float,
    ) -> Dict[str, Any]:
        """Estimate a confidence band from how much real data the model saw.

        The band widens when the skill level had to be guessed and narrows when
        both skill scores and practice history are present.
        """
        total_practice = (
            experience["total_interviews"]
            + experience["total_coding"]
            + experience["total_aptitude"]
        )
        if has_skill_graph and total_practice >= 10:
            spread = 6.0
            data_completeness = "high"
            note = "Based on your skill assessments and practice history."
        elif has_skill_graph:
            spread = 10.0
            data_completeness = "medium"
            note = "Based on skill assessments; adding practice history would tighten this."
        else:
            spread = 16.0
            data_completeness = "low"
            note = "No skill scores recorded — estimated from practice activity only. Take an assessment to tighten this."

        low = min(99.0, max(1.0, probability - spread))
        high = min(99.0, max(1.0, probability + spread))
        return {
            "low": round(low, 1),
            "high": round(high, 1),
            "spread": round(spread, 1),
            "range": f"{round(low, 0):.0f}-{round(high, 0):.0f}%",
            "data_completeness": data_completeness,
            "note": note,
        }

    def _compute_next_best_moves(
        self,
        what_if_scenarios: List[Dict[str, Any]],
        improvement_roadmap: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Rank the highest-leverage actions by projected gain per unit of effort."""
        moves = []
        for sc in what_if_scenarios:
            gain = self._parse_delta(sc.get("impact_delta", "0"))
            effort_rank = {"Low": 1, "Medium": 2, "High": 3}.get(sc.get("effort", "Medium"), 2)
            moves.append({
                "id": sc.get("id", f"scenario_{len(moves)}"),
                "title": sc.get("title", ""),
                "description": sc.get("description", ""),
                "projected_gain": round(gain, 1),
                "effort": sc.get("effort", "Medium"),
                "effort_rank": effort_rank,
                "time_estimate": sc.get("time_estimate", ""),
                "target_skill": sc.get("target_skill", ""),
            })

        # Critical roadmap items (hard requirements) get promoted as moves too.
        for item in improvement_roadmap:
            skill = item.get("skill", "")
            if item.get("priority") == "critical" and not any(
                skill in m.get("title", "") for m in moves
            ):
                moves.append({
                    "id": f"roadmap_{skill}",
                    "title": f"Close the {self._humanize_skill(skill)} gap",
                    "description": item.get("action", ""),
                    "projected_gain": round(item.get("gap", 0) * 0.4, 1),
                    "effort": "High",
                    "effort_rank": 3,
                    "time_estimate": item.get("estimated_time", ""),
                    "target_skill": skill,
                })

        moves.sort(key=lambda m: (m["projected_gain"] / m["effort_rank"]), reverse=True)
        return moves[:5]

    @staticmethod
    def _parse_delta(delta: str) -> float:
        """Parse '+12.3%' → 12.3"""
        if not delta:
            return 0.0
        digits = delta.replace("+", "").replace("%", "").strip()
        try:
            return float(digits)
        except ValueError:
            return 0.0

    def _build_plain_language_summary(
        self,
        probability: float,
        confidence_band: Dict[str, Any],
        factors: List[Dict[str, Any]],
        weights: Dict[str, float],
        experience_modifier: float,
    ) -> str:
        """Deterministic plain-English explanation — zero AI cost."""
        band = confidence_band["range"]
        strongest = max(factors, key=lambda f: f["score"], default=None)
        weakest = min(factors, key=lambda f: f["score"], default=None)
        gap_factors = [f for f in factors if f["verdict"] in ("gap", "critical")]

        parts = [f"Your estimated chance of an offer from this company is {probability:.0f}%, with a realistic range of {band}."]

        if experience_modifier >= 1.0:
            parts.append("Your practice history is working in your favor.")
        elif experience_modifier < 0.9:
            parts.append("You have little practice history yet, so this range is wider than it could be.")

        if strongest and strongest["score"] > 0:
            parts.append(f"Your strongest area is {strongest['label'].lower()} ({strongest['score']:.0f}/100).")
        if weakest and weakest["score"] > 0 and weakest is not strongest:
            parts.append(f"The biggest drag is {weakest['label'].lower()} ({weakest['score']:.0f}/100).")

        if gap_factors:
            names = ", ".join(f["label"].lower() for f in gap_factors[:2])
            parts.append(f"Closing the gaps in {names} moves the number most.")
        else:
            parts.append("You're above the bar on every factor — consistency is your main lever now.")

        return " ".join(parts)

    async def _get_experience_data(self, user_id: str) -> Dict[str, int]:
        """Fetch user's practice experience data."""
        gamification = await gamification_collection.find_one({"user_id": user_id})

        if not gamification:
            return {
                "total_interviews": 0,
                "total_coding": 0,
                "total_aptitude": 0,
                "streak": 0,
                "level": 1,
            }

        return {
            "total_interviews": gamification.get("total_interviews", 0),
            "total_coding": gamification.get("total_coding", 0),
            "total_aptitude": gamification.get("total_aptitude", 0),
            "streak": gamification.get("streak", 0),
            "level": gamification.get("level", 1),
        }

    def _calculate_experience_modifier(self, experience: Dict[str, int]) -> float:
        """
        Calculate experience modifier with diminishing returns.
        More practice = higher modifier, but with a cap.
        """
        total_practice = (
            experience["total_interviews"] +
            experience["total_coding"] +
            experience["total_aptitude"]
        )

        # Logarithmic scaling with diminishing returns
        if total_practice == 0:
            return 0.85  # New user penalty
        elif total_practice < 10:
            return 0.90 + (total_practice * 0.01)
        elif total_practice < 50:
            return 1.00 + (math.log(total_practice) * 0.05)
        elif total_practice < 200:
            return 1.10 + (math.log(total_practice) * 0.03)
        else:
            return min(1.30, 1.20 + (math.log(total_practice) * 0.01))

    def _get_probability_band(self, probability: float) -> Dict[str, str]:
        """Get human-readable probability band."""
        if probability >= 70:
            return {
                "label": "High Chance",
                "color": "#10B981",
                "message": "You're well-prepared! Focus on maintaining your edge.",
            }
        elif probability >= 50:
            return {
                "label": "Moderate Chance",
                "color": "#F59E0B",
                "message": "Good foundation. A focused 2-week sprint could boost you significantly.",
            }
        elif probability >= 30:
            return {
                "label": "Challenging",
                "color": "#F97316",
                "message": "Significant preparation needed. Focus on one skill at a time.",
            }
        else:
            return {
                "label": "Tough",
                "color": "#EF4444",
                "message": "Every expert was once a beginner. Start with the basics.",
            }

    def _generate_what_if_analysis(
        self,
        current_scores: Dict[str, float],
        weights: Dict[str, float],
        current_prob: float,
        profile: Dict,
    ) -> List[Dict[str, Any]]:
        """
        Generate deterministic what-if scenarios.
        Shows how improving specific skills affects probability.
        """
        scenarios = []

        # Scenario A: Target the highest-weight, lowest-score skill
        skill_gaps = []
        for skill, weight in weights.items():
            current = current_scores.get(skill, 0)
            # Assume they can improve by 20 points
            potential_improvement = min(20, 100 - current)
            potential_gain = potential_improvement * weight * 0.8  # 80% efficiency
            skill_gaps.append({
                "skill": skill,
                "current": current,
                "improvement": potential_improvement,
                "gain": potential_gain,
                "weight": weight,
            })

        # Sort by potential gain
        skill_gaps.sort(key=lambda x: x["gain"], reverse=True)

        # Top skill improvement scenario
        top = skill_gaps[0]
        scenarios.append({
            "id": "skill_boost",
            "title": f"Boost {top['skill'].replace('_', ' ').title()} by {top['improvement']:.0f} points",
            "description": f"Focus on {top['skill'].replace('_', ' ')} for 2 weeks",
            "impact_delta": f"+{top['gain']:.1f}%",
            "projected_probability": f"{min(99.0, current_prob + top['gain']):.1f}%",
            "effort": "High" if top['improvement'] > 15 else "Medium",
            "time_estimate": "2-3 weeks",
        })

        # Scenario B: Balanced improvement across all skills
        balanced_gain = sum(min(10, 100 - current_scores.get(s, 0)) * w * 0.6 for s, w in weights.items())
        scenarios.append({
            "id": "balanced",
            "title": "Improve all skills by 10 points each",
            "description": "Balanced practice across all areas",
            "impact_delta": f"+{balanced_gain:.1f}%",
            "projected_probability": f"{min(99.0, current_prob + balanced_gain):.1f}%",
            "effort": "Medium",
            "time_estimate": "3-4 weeks",
        })

        # Scenario C: Consistent practice streak
        streak_gain = 7.0  # Fixed bonus for 7-day streak
        scenarios.append({
            "id": "streak",
            "title": "Maintain a 7-day practice streak",
            "description": "Complete daily drills for 7 consecutive days",
            "impact_delta": f"+{streak_gain:.1f}%",
            "projected_probability": f"{min(99.0, current_prob + streak_gain):.1f}%",
            "effort": "Low",
            "time_estimate": "1 week",
        })

        # Scenario D: Resume optimization
        resume_gap = 100 - current_scores.get("resume", 0)
        if resume_gap > 20:
            resume_gain = min(20, resume_gap) * weights.get("resume", 0.15) * 0.9
            scenarios.append({
                "id": "resume",
                "title": "Optimize resume with ATS checker",
                "description": "Fix formatting and add quantified achievements",
                "impact_delta": f"+{resume_gain:.1f}%",
                "projected_probability": f"{min(99.0, current_prob + resume_gain):.1f}%",
                "effort": "Low",
                "time_estimate": "1-2 days",
            })

        return scenarios

    def _generate_improvement_roadmap(
        self,
        current_scores: Dict[str, float],
        weights: Dict[str, float],
        profile: Dict,
        current_prob: float,
    ) -> List[Dict[str, Any]]:
        """Generate a step-by-step improvement roadmap."""
        roadmap = []

        # Find skills below company minimum
        min_bar = profile["min_score"] * 10
        for skill, weight in sorted(weights.items(), key=lambda x: x[1], reverse=True):
            current = current_scores.get(skill, 0)
            if current < min_bar:
                gap = min_bar - current
                roadmap.append({
                    "priority": "critical",
                    "skill": skill,
                    "current_score": round(current, 1),
                    "target_score": min_bar,
                    "gap": round(gap, 1),
                    "action": self._get_specific_action(skill),
                    "resources": self._get_resources(skill),
                    "estimated_time": f"{math.ceil(gap / 5)} days",
                })

        # Find weak skills (below 70)
        for skill, weight in sorted(weights.items(), key=lambda x: x[1], reverse=True):
            current = current_scores.get(skill, 0)
            if current < 70 and current >= min_bar:
                roadmap.append({
                    "priority": "high",
                    "skill": skill,
                    "current_score": round(current, 1),
                    "target_score": 70,
                    "gap": round(70 - current, 1),
                    "action": self._get_specific_action(skill),
                    "resources": self._get_resources(skill),
                    "estimated_time": f"{math.ceil((70 - current) / 10)} days",
                })

        return roadmap[:5]  # Top 5 priorities

    def _get_specific_action(self, skill: str) -> str:
        """Get specific action for improving a skill."""
        actions = {
            "dsa": "Complete 10 coding challenges focusing on weak topics. Use the hint matrix for stuck problems.",
            "system_design": "Practice 3 system design questions. Use the cheat sheet for common patterns.",
            "behavioral": "Prepare 5 STAR stories. Use the prompt-and-push loop to strengthen weak areas.",
            "aptitude": "Take 2 aptitude practice tests. Focus on speed and accuracy.",
            "resume": "Run your resume through the ATS checker. Fix all critical issues and add metrics.",
        }
        return actions.get(skill, "Practice more in this area")

    def _get_resources(self, skill: str) -> List[str]:
        """Get specific resources for skill improvement."""
        resources = {
            "dsa": [
                "Use PlacementPro's company-specific coding challenges",
                "Review cheat sheet for common patterns",
                "Practice progressive hints for stuck problems",
            ],
            "system_design": [
                "Read the system design cheat sheet",
                "Practice with the mock interviewer feedback",
                "Study common architecture patterns",
            ],
            "behavioral": [
                "Use the STAR method template generator",
                "Practice with the prompt-and-push loop",
                "Review company-specific leadership principles",
            ],
            "aptitude": [
                "Take daily placement drills",
                "Practice time management",
                "Focus on accuracy over speed initially",
            ],
            "resume": [
                "Use the anti-plagiarism humanizer",
                "Add quantified achievements",
                "Run through ATS formatting checklist",
            ],
        }
        return resources.get(skill, ["Practice consistently"])

    async def _get_sub_skill_breakdown(self, user_id: str) -> Dict[str, Any]:
        """Get granular sub-skill breakdown."""
        skill_graph = await skill_graph_collection.find_one({"user_id": user_id})

        if not skill_graph:
            return {}

        breakdown = {}
        categories = skill_graph.get("categories", {})

        for cat_id, cat_data in categories.items():
            if cat_id in self.SUB_SKILLS:
                skills = cat_data.get("skills", {})
                sub_scores = {}
                for sub_skill in self.SUB_SKILLS[cat_id]:
                    sub_scores[sub_skill] = skills.get(sub_skill, {}).get("score", 0)

                breakdown[cat_id] = {
                    "overall": cat_data.get("score", 0),
                    "sub_skills": sub_scores,
                    "weakest": min(sub_scores.items(), key=lambda x: x[1])[0] if sub_scores else None,
                    "strongest": max(sub_scores.items(), key=lambda x: x[1])[0] if sub_scores else None,
                }

        return breakdown

    async def _get_peer_comparison(self, user_id: str, company: str) -> Dict[str, Any]:
        """Get anonymized peer comparison computed from real prediction data.

        Falls back to honest labels when there is not enough data yet.
        """
        # Recent predictions for this company (capped to keep this cheap).
        per_user: Dict[str, List[float]] = {}
        total_predictions = 0
        async for doc in predictions_collection().find(
            {"company": company}
        ).sort("created_at", -1).limit(500):
            uid = doc.get("user_id")
            prob = doc.get("probability", 0)
            if uid:
                per_user.setdefault(uid, []).append(prob)
            total_predictions += 1

        user_probs = per_user.get(user_id, [])
        user_probability = (sum(user_probs) / len(user_probs)) if user_probs else None

        averages = {uid: sum(probs) / len(probs) for uid, probs in per_user.items()}
        company_avg = (sum(averages.values()) / len(averages)) if averages else None

        percentile = None
        if user_probability is not None and averages:
            below = sum(1 for avg in averages.values() if avg < user_probability)
            percentile = int((below / len(averages)) * 100)

        your_vs_avg = None
        if user_probability is not None and company_avg is not None:
            diff = user_probability - company_avg
            your_vs_avg = f"{'+' if diff >= 0 else ''}{diff:.1f}"

        if total_predictions < 10:
            return {
                "total_users": len(averages),
                "total_predictions": total_predictions,
                "your_rank_percentile": percentile,
                "average_score_for_company": round(company_avg, 1) if company_avg is not None else None,
                "your_score_vs_average": your_vs_avg,
                "users_who_got_offers": None,
                "message": "Limited peer data yet — we're warming up. The more students predict, the sharper this becomes.",
            }

        return {
            "total_users": len(averages),
            "total_predictions": total_predictions,
            "your_rank_percentile": percentile,
            "average_score_for_company": round(company_avg, 1),
            "your_score_vs_average": your_vs_avg,
            "users_who_got_offers": None,
            "message": f"You're around the {percentile}th percentile of students targeting this company.",
        }

    async def _store_prediction(
        self,
        user_id: str,
        company: str,
        role: str,
        probability: float,
        skill_scores: Dict,
        snapshot: Optional[Dict] = None,
    ):
        """Store prediction for data collection and model improvement."""
        prediction = {
            "user_id": user_id,
            "company": company,
            "role": role,
            "probability": probability,
            "skill_scores": skill_scores,
            "created_at": datetime.now(timezone.utc),
        }
        if snapshot:
            prediction["snapshot"] = snapshot

        await predictions_collection().insert_one(prediction)

    async def get_prediction_history(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user's prediction history to track improvement."""
        cursor = predictions_collection().find(
            {"user_id": user_id}
        ).sort("created_at", -1).limit(20)

        history = []
        async for doc in cursor:
            history.append({
                "company": doc.get("company", "").title(),
                "probability": doc.get("probability", 0),
                "date": doc.get("created_at"),
            })

        return history

    def get_all_companies(self) -> List[Dict[str, Any]]:
        """Get list of all supported companies."""
        return [
            {
                "id": company,
                "name": company.title(),
                "tier": profile["tier"],
                "acceptance_rate": f"{profile['rate'] * 100:.1f}%",
                "color": profile["color"],
            }
            for company, profile in self.COMPANY_PROFILES.items()
        ]
