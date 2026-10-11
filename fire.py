"""Fire simulation -> animated GIF. Usage: python fire.py [--size 50] [--fps 30] [--seconds 3] [--scale 8] [--out fire.gif]"""
import argparse
import numpy as np
from PIL import Image
from matplotlib.colors import LinearSegmentedColormap

p = argparse.ArgumentParser()
p.add_argument("--size", type=int, default=50)
p.add_argument("--fps", type=int, default=30)
p.add_argument("--seconds", type=int, default=3)
p.add_argument("--scale", type=int, default=8, help="pixels per grid cell")
p.add_argument("--out", default="fire.gif")
a = p.parse_args()

rng, cols, n = np.random.default_rng(), np.arange(a.size), a.fps * a.seconds
grid = np.zeros((n, a.size, a.size), np.float32)

for t in range(n):
    cur, prev = grid[t], grid[t - 1]                      # grid[-1] is still zeros at t=0
    cur[-1] = rng.integers(80, 101, a.size)               # flickering fuel row
    for y in range(a.size - 2, -1, -1):                   # bottom -> top
        src = np.clip(cols + rng.integers(-1, 2, a.size), 0, a.size - 1)   # wind
        cur[y] = np.maximum(0, 0.9 * (cur[y + 1, src] - rng.integers(0, 6, a.size)) + 0.1 * prev[y])

pal = (LinearSegmentedColormap.from_list("fire", ["black", "orange", "white"], N=256)(range(256))[:, :3] * 255).astype(np.uint8).ravel().tolist()
idx = (grid * 2.55).clip(0, 255).astype(np.uint8).repeat(a.scale, 1).repeat(a.scale, 2)
imgs = [Image.fromarray(f) for f in idx]
for im in imgs:
    im.putpalette(pal)
imgs[0].save(a.out, save_all=True, append_images=imgs[1:], duration=1000 // a.fps, loop=0)
print(f"Saved {a.out}: {n} frames, {a.size * a.scale}x{a.size * a.scale}px")
