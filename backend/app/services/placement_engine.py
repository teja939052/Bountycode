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
        weights = self.TIER_WEIGHTS[profile["tier"]]

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

        # Store prediction for data collection
        await self._store_prediction(
            user_id, company, role, final_probability, student_scores
        )

        return {
            "target_company": company_name.title(),
            "company_tier": profile["tier"],
            "company_color": profile["color"],
            "historical_acceptance_rate": f"{profile['rate'] * 100:.1f}%",
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
        """Get anonymized peer comparison data."""
        # In production, this would query aggregated data
        # For now, return realistic mock data
        return {
            "total_users": 15247,
            "your_rank_percentile": 65,  # Would be calculated from real data
            "average_score_for_company": 58.3,
            "your_score_vs_average": "+7.2",
            "users_who_got_offers": 1247,
            "message": "You're ahead of 65% of users targeting this company",
        }

    async def _store_prediction(
        self,
        user_id: str,
        company: str,
        role: str,
        probability: float,
        skill_scores: Dict,
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
