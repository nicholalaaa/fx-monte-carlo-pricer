import numpy as np
from fx_mc_pricer.mc import price_european_mc


def test_antithetic_reduces_variance():
    S0, K, T, r_d, r_f, sigma = 100.0, 100.0, 1.0, 0.03, 0.01, 0.25
    p_plain, se_plain, meta_plain = price_european_mc(S0, K, T, r_d, r_f, sigma, n_paths=80_000, steps=2, antithetic=False, seed=1)
    p_anti, se_anti, meta_anti = price_european_mc(S0, K, T, r_d, r_f, sigma, n_paths=80_000, steps=2, antithetic=True, seed=1)
    # Antithetic should not have higher variance; usually strictly lower
    assert se_anti <= se_plain * 1.01
