from messlib.data_structures.classes import Strategy


def strat2dict(strategy: Strategy) -> dict:
    return strategy.__dict__


def dict2strat(dict_in: dict) -> Strategy:
    strategy = Strategy()
    strategy.__dict__ = dict_in
    return strategy
