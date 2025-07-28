
def skill(func):
    func.__is_skill__ = True
    return func
