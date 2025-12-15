# perlin.py
# not for use (for now) but will be later
import math
import random

class PerlinNoise:
    def __init__(self, seed=None):
        self.permutation = list(range(256))
        random.Random(seed).shuffle(self.permutation)
        self.permutation += self.permutation

    def fade(self, t):
        return t * t * t * (t * (t * 6 - 15) + 10)

    def lerp(self, a, b, t):
        return a + t * (b - a)

    def grad(self, hash, x):
        return x if (hash & 1) == 0 else -x

    def noise(self, x):
        xi = int(math.floor(x)) & 255
        xf = x - math.floor(x)

        u = self.fade(xf)

        a = self.permutation[xi]
        b = self.permutation[xi + 1]

        return self.lerp(
            self.grad(a, xf),
            self.grad(b, xf - 1),
            u
        )
