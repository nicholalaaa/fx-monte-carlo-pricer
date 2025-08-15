# fx-monte-carlo-pricer

Excel/VBA + Python **Monte Carlo** pricer for FX (USD/JPY-style) instruments with:
- Custom **PRNG** (xorshift32 + Box–Muller)
- **Antithetic variates** toggle
- **One-step** (exact GBM) and **multi-step** paths
- Call/Put/Forward pricing with **Black–Scholes** cross-checks
- Plots and variance/SE reporting

> Drop your `.xlsm` and exported VBA modules into `vba/`; Python replication is provided here for reviewers.

---

## Install (Python)
```bash
python -m venv .venv && source .venv/bin/activate   # or your env tool
pip install -r requirements.txt
```

## Quick demo
```bash
export PYTHONPATH=$PWD/src      # Windows PowerShell: $env:PYTHONPATH="$PWD/src"
python -m examples.mc_fx_demo
```
This prints MC vs BS prices, **95% CI**, and the **variance reduction** from antithetic variates.

---

## Excel/VBA
1) Copy your workbook to `vba/` (e.g., `vba/FX_MC_Pricer.xlsm`).  
2) In VBA Editor: right-click each module -> **Export File...** into `vba/modules/`  
   Suggested names: `PRNG.bas`, `MonteCarlo.bas`, `Antithetic.bas`, `UI.bas`.

---

## API (Python)
```python
from fx_mc_pricer.mc import price_european_mc, price_forward_mc
from fx_mc_pricer.bs_closed_form import bs_price_fx

p, se, meta = price_european_mc(S0, K, T, r_d, r_f, sigma, otype="call",
                                n_paths=200_000, steps=1, antithetic=True, seed=42)
```
- GBM under domestic risk-neutral: \(dS_t/S_t = (r_d - r_f)dt + \sigma dW_t\).  
- Discount factor uses **domestic** rate \(r_d\).

---

## Tests
```bash
export PYTHONPATH=$PWD/src
pytest -q
```
- `test_mc_matches_bs.py`: MC price within ~2×SE of BS (large n_paths).
- `test_antithetic_variance.py`: variance reduction factor < 1.

## License
MIT
