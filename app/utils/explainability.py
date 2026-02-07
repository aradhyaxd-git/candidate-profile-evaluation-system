def explain_experience(years, score):
    return f"{years} years → {score}/25 (5 points per year)"


def explain_projects(projects, tier, score):
    return f"{projects} projects × Tier {tier} context → {score}/25"


def explain_skill(level, score):
    return f"{level} skill → {score}/20"


def explain_learning(level, score):
    return f"{level} learning velocity → {score}/15"


def explain_readiness(level, score):
    return f"{level} readiness → {score}/15"
