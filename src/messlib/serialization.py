from messlib.classes_abstract import Strategy


def Strat2Dict(strategy: Strategy) -> dict:
    return strategy.__dict__


def Dict2Strat(dict_in: dict) -> Strategy:
    strategy = Strategy()
    strategy.__dict__ = dict_in
    return strategy
