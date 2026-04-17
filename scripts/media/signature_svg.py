"""Deterministische Fake-Handschrift via Perlin-Noise-ähnlicher Pfade."""
from __future__ import annotations
import hashlib
import math
import random

def _seed_from(name: str) -> int:
    return int(hashlib.sha256(name.encode()).hexdigest()[:8], 16)


def _pen_path(rnd: random.Random, text: str, amplitude: float = 4.0, tightness: float = 0.25) -> str:
    """Simuliere eine Unterschrift als SVG-Path (ohne Text, nur Schnörkel)."""
    n_strokes = 1 + max(1, sum(1 for c in text if c == " ")) + rnd.randint(1, 2)
    x, y = 10.0, 40.0
    commands: list[str] = [f"M {x:.1f} {y:.1f}"]
    stroke_lengths = [rnd.randint(18, 38) for _ in range(n_strokes)]
    for slen in stroke_lengths:
        for i in range(slen):
            x += rnd.uniform(3.0, 6.0) * tightness * 10
            y = 40.0 + amplitude * math.sin(i * 0.55 + rnd.random() * 2 * math.pi)
            commands.append(f"Q {x-1:.1f} {y-rnd.uniform(0, 4):.1f}, {x:.1f} {y:.1f}")
        # Sprung (z.B. Lücke zwischen Vor- und Nachname)
        x += rnd.uniform(8, 15)
        y = 40.0 + rnd.uniform(-3, 3)
        commands.append(f"M {x:.1f} {y:.1f}")
    return " ".join(commands)


def signature_svg(name: str, width: int = 280, height: int = 70) -> str:
    rnd = random.Random(_seed_from(name))
    d = _pen_path(rnd, name)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
        f'<path d="{d}" stroke="#14205a" stroke-width="1.4" fill="none" stroke-linecap="round"/>'
        f'</svg>'
    )
