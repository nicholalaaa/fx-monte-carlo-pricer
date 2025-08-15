import numpy as np
from scipy.stats import norm


def bs_price_fx(S, K, T, r_d, r_f, sigma, otype="call"):
    """Black-Scholes price for FX with continuous foreign dividend yield r_f."""
    if T <= 0 or sigma <= 0 or S <= 0 or K <= 0:
        return np.nan
    sqrtT = np.sqrt(T)
    d1 = (np.log(S/K) + (r_d - r_f + 0.5*sigma*sigma)*T) / (sigma*sqrtT)
    d2 = d1 - sigma*sqrtT
    disc_d = np.exp(-r_d*T)
    disc_f = np.exp(-r_f*T)
    if str(otype).lower().startswith("c"):
        return S*disc_f*norm.cdf(d1) - K*disc_d*norm.cdf(d2)
    else:
        return K*disc_d*norm.cdf(-d2) - S*disc_f*norm.cdf(-d1)
