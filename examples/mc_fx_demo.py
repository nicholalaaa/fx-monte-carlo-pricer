from fx_mc_pricer.mc import compare_to_bs, price_forward_mc


def main():
    S0, K, T, r_d, r_f, sigma = 100.0, 100.0, 1.0, 0.03, 0.01, 0.20
    cfg = dict(n_paths=200_000, steps=1, antithetic=True, seed=7)

    print("European CALL (MC vs BS):")
    res = compare_to_bs(S0, K, T, r_d, r_f, sigma, otype="call", **cfg)
    print(f"  MC: {res['mc']:.6f}  BS: {res['bs']:.6f}  |  abs err: {res['abs_err']:.6f}  (SE: {res['se']:.6f})  paths={res['meta']['paths']}")

    print("\nEuropean PUT (MC vs BS):")
    res = compare_to_bs(S0, K, T, r_d, r_f, sigma, otype="put", **cfg)
    print(f"  MC: {res['mc']:.6f}  BS: {res['bs']:.6f}  |  abs err: {res['abs_err']:.6f}  (SE: {res['se']:.6f})  paths={res['meta']['paths']}")

    print("\nForward PV (MC vs closed-form):")
    pf, se_f, meta_f = price_forward_mc(S0, K, T, r_d, r_f, sigma, **cfg)
    pv_cf = (S0 * (2.718281828459045**(-r_f*T)) - K * (2.718281828459045**(-r_d*T)))
    print(f"  MC PV: {pf:.6f}  Closed-form PV: {pv_cf:.6f}  |  (SE: {se_f:.6f})  paths={meta_f['paths']}")


if __name__ == "__main__":
    main()
