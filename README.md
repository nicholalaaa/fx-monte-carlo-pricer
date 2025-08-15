# fx-monte-carlo-pricer

Excel/VBA + Python **Monte Carlo** pricer for FX (USD/JPY-style) with:
- Custom **PRNG** (xorshift32 + Box–Muller)
- **Antithetic variates** toggle
- **One-step** (exact GBM) and **multi-step** paths
- Call/Put/Forward pricing with **Black–Scholes** cross-checks
- Plots and variance/SE reporting

---

## Install (Python)
```bash
pip install -r requirements.txt
```


## Quick demo (4 configurations)
Run the same configs as in your HW:
1) 1 step, no antithetic  
2) 1 step, antithetic  
3) 2 steps, no antithetic  
4) 2 steps, antithetic

```bash
export PYTHONPATH=$PWD/src
python -m examples.mc_fx_hw_demo
``` 
The script prints a table with **MC price**, **SE**, **95% CI**, and **variance ratio** vs baseline.

---

## Model
Domestic risk-neutral GBM:
```
dS_t / S_t = (r_d - r_f) dt + sigma dW_t
```
- Discount with **domestic** rate `r_d`.
- One step uses the exact lognormal update; multi-step splits `T` into equal substeps.

---

## Python API
```python
from fx_mc_pricer.mc import price_european_mc, price_forward_mc
from fx_mc_pricer.bs_closed_form import bs_price_fx

price, se, meta = price_european_mc(S0, K, T, r_d, r_f, sigma,
                                    otype="call", n_paths=200_000,
                                    steps=1, antithetic=True, seed=42)
```
- `meta["variance"]` and `se` help quantify estimator quality.
- Use `steps=1` for exact terminal sampling; `steps>1` to experiment with path discretization.

---

## Tests
```bash
export PYTHONPATH=$PWD/src
pytest -q
```
- `test_mc_matches_bs.py`: MC price within ~2–3x SE of BS at large path counts.  
- `test_antithetic_variance.py`: antithetic SE <= plain SE.

---

## Notes & tips
- Start with `antithetic=True` and `steps=1` for fastest convergence.
- Increase `n_paths` to tighten the confidence interval; SE scales ~ 1/sqrt(N).
- Set a fixed `seed` for reproducibility in demos; randomize it for stress runs.
