from assistant.skills import skill_registry


def run_skill(skill_name: str, *args, **kwargs):
    skill_func = skill_registry.get(skill_name)
    if not skill_func:
        raise ValueError(f"Skill '{skill_name}' not found in registry.")

    return skill_func(*args, **kwargs)