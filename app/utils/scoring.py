def score_experience(years: int) -> int:
    return min(years * 5, 25)


def score_projects(projects: int) -> int:
    return min(projects * 5, 25)


def score_skill(level: str) -> int:
    return {"Low": 5, "Medium": 12, "High": 20}[level]


def score_learning_velocity(level: str) -> int:
    return {"Low": 5, "Medium": 10, "High": 15}[level]


def score_role_readiness(level: str) -> int:
    return {
        "Not Ready": 5,
        "Partially Ready": 10,
        "Ready": 15
    }[level]


def college_tier_multiplier(tier: int) -> float:
    return {1: 1.1, 2: 1.0, 3: 0.9}[tier]
