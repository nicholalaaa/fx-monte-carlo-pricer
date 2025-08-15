import numpy as np
from .prng import XorShift32, normals_box_muller
from .bs_closed_form import bs_price_fx


def simulate_terminal_gbm_fx(S0, T, r_d, r_f, sigma, steps, n_paths, antithetic=False, seed=42):
    dt = T / steps
    nudt = (r_d - r_f - 0.5 * sigma * sigma) * dt
    sidt = sigma * np.sqrt(dt)
    rng = XorShift32(seed)

    if antithetic:
        half = (n_paths + 1) // 2
        Z = normals_box_muller(steps * half, rng).reshape(steps, half)
        # build antithetic pair paths
        S_plus = np.full(half, S0, dtype=np.float64)
        S_minus = S_plus.copy()
        for k in range(steps):
            z = Z[k]
            S_plus *= np.exp(nudt + sidt * z)
            S_minus *= np.exp(nudt - sidt * z)
        ST = np.concatenate([S_plus, S_minus], axis=0)[:n_paths]
        eff_paths = len(ST)
    else:
        Z = normals_box_muller(steps * n_paths, rng).reshape(steps, n_paths)
        S = np.full(n_paths, S0, dtype=np.float64)
        for k in range(steps):
            S *= np.exp(nudt + sidt * Z[k])
        ST = S
        eff_paths = n_paths

    return ST, eff_paths


def price_european_mc(S0, K, T, r_d, r_f, sigma, otype="call", n_paths=200_000, steps=1, antithetic=True, seed=42):
    ST, eff = simulate_terminal_gbm_fx(S0, T, r_d, r_f, sigma, steps, n_paths, antithetic, seed)
    if str(otype).lower().startswith("c"):
        payoff = np.maximum(ST - K, 0.0)
    else:
        payoff = np.maximum(K - ST, 0.0)
    disc = np.exp(-r_d * T)
    pv = disc * payoff
    price = float(pv.mean())
    var = float(pv.var(ddof=1))
    se = np.sqrt(var / eff)
    return price, se, {"variance": var, "paths": eff}


def price_forward_mc(S0, K, T, r_d, r_f, sigma, n_paths=200_000, steps=1, antithetic=True, seed=42):
    ST, eff = simulate_terminal_gbm_fx(S0, T, r_d, r_f, sigma, steps, n_paths, antithetic, seed)
    disc = np.exp(-r_d * T)
    pv = disc * (ST - K)
    price = float(pv.mean())
    var = float(pv.var(ddof=1))
    se = np.sqrt(var / eff)
    return price, se, {"variance": var, "paths": eff}


def compare_to_bs(S0, K, T, r_d, r_f, sigma, otype="call", **mc_kwargs):
    mc_price, se, meta = price_european_mc(S0, K, T, r_d, r_f, sigma, otype=otype, **mc_kwargs)
    bs = bs_price_fx(S0, K, T, r_d, r_f, sigma, otype=otype)
    return {"mc": mc_price, "bs": float(bs), "se": se, "abs_err": abs(mc_price - bs), "meta": meta}
