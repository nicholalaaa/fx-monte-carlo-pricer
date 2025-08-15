import numpy as np
from fx_mc_pricer.mc import price_european_mc
from fx_mc_pricer.bs_closed_form import bs_price_fx


def test_mc_with_many_paths_matches_bs_within_2se():
    S0, K, T, r_d, r_f, sigma = 100.0, 100.0, 1.0, 0.03, 0.01, 0.20
    price, se, meta = price_european_mc(S0, K, T, r_d, r_f, sigma, otype="call", n_paths=300_000, steps=1, antithetic=True, seed=123)
    bs = bs_price_fx(S0, K, T, r_d, r_f, sigma, otype="call")
    assert abs(price - bs) <= 2.5 * se
