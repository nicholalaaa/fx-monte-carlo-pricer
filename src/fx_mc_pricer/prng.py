import numpy as np


class XorShift32:
    """Simple xorshift32 PRNG (for demo/teaching). Not cryptographic."""
    def __init__(self, seed=123456789):
        self.state = np.uint32(seed if seed != 0 else 2463534242)

    def rand_uint32(self):
        x = self.state
        x ^= (x << np.uint32(13)) & np.uint32(0xFFFFFFFF)
        x ^= (x >> np.uint32(17))
        x ^= (x << np.uint32(5)) & np.uint32(0xFFFFFFFF)
        self.state = x
        return x

    def rand_uniform(self, size=None):
        if size is None:
            return (self.rand_uint32() / np.float64(2**32)).astype(float)
        out = np.empty(size, dtype=np.float64)
        it = np.nditer(out, flags=['multi_index'], op_flags=['writeonly'])
        while not it.finished:
            it[0] = self.rand_uint32() / np.float64(2**32)
            it.iternext()
        return out


def normals_box_muller(n, rng: XorShift32):
    """Generate n standard normals using Box-Muller (pairs of uniforms)."""
    m = (n + 1) // 2
    u1 = rng.rand_uniform(size=m)
    u2 = rng.rand_uniform(size=m)
    # avoid log(0)
    u1 = np.clip(u1, 1e-12, 1-1e-12)
    R = np.sqrt(-2.0 * np.log(u1))
    Theta = 2.0 * np.pi * u2
    z0 = R * np.cos(Theta)
    z1 = R * np.sin(Theta)
    z = np.empty(n, dtype=np.float64)
    z[0:2*m:2] = z0
    z[1:2*m:2] = z1
    return z[:n]
