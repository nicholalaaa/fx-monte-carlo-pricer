from math import sqrt
from fx_mc_pricer.mc import price_european_mc
from fx_mc_pricer.bs_closed_form import bs_price_fx


S0 = 120.0
K = 120.0
T = 1.0
r_d = 0.005
r_f = 0.05
sigma = 0.10
otype = "call"      # or "put"
n_paths = 10_000
seed = 7

configs = [
    (1, False, "1 step, no antithetic"),
    (1, True,  "1 step, antithetic"),
    (2, False, "2 steps, no antithetic"),
    (2, True,  "2 steps, antithetic"),
]

bs = bs_price_fx(S0, K, T, r_d, r_f, sigma, otype=otype)

rows = []
baseline_var = None
for steps, anti, label in configs:
    price, se, meta = price_european_mc(
        S0, K, T, r_d, r_f, sigma, otype=otype,
        n_paths=n_paths, steps=steps, antithetic=anti, seed=seed
    )
    var = meta["variance"]
    if baseline_var is None:
        baseline_var = var
    vr = var / baseline_var  # variance ratio vs baseline
    lo, hi = price - 1.96*se, price + 1.96*se
    rows.append((label, steps, anti, price, se, lo, hi, vr, meta["paths"]))

# Pretty print
print(f"FX {otype.upper()} — MC vs BS (S0={S0}, K={K}, T={T}, r_d={r_d}, r_f={r_f}, sigma={sigma})\n")
print(f"Black–Scholes: {bs:.6f}\n")
print("Configuration                     Price       SE       95% CI low   95% CI high   Var Ratio   Paths")
print("-"*100)
for label, steps, anti, price, se, lo, hi, vr, paths in rows:
    print(f"{label:30s}  {price:9.6f}  {se:8.6f}  {lo:12.6f}   {hi:12.6f}    {vr:9.4f}   {paths:7d}")
