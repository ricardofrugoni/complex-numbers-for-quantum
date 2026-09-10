from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.complex_geometry import plot_complex, rotate

ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

# 1. z = 3 + 4i
fig, ax = plt.subplots(figsize=(6,6))
plot_complex(3 + 4j, label="z", ax=ax)
ax.set_title("Número complexo no plano: z = 3 + 4i")
fig.tight_layout()
fig.savefig(ASSETS / "plano_complexo_3_4i.png", dpi=160)
plt.close(fig)

# 2. Rotação por i
z = 1 + 1j
z2 = rotate(z, np.pi/2)
fig, ax = plt.subplots(figsize=(6,6))
plot_complex(z, label="z", ax=ax, limits=(-2.5,2.5))
plot_complex(z2, label="i·z", ax=ax, limits=(-2.5,2.5))
ax.set_title("Multiplicação por i = rotação de 90°")
fig.tight_layout()
fig.savefig(ASSETS / "rotacao_por_i.png", dpi=160)
plt.close(fig)

# 3. Círculo unitário
theta = np.linspace(0, 2*np.pi, 400)
u = np.exp(1j*theta)
fig, ax = plt.subplots(figsize=(6,6))
ax.plot(u.real, u.imag)
ax.axhline(0, linewidth=0.8)
ax.axvline(0, linewidth=0.8)
ax.set_aspect("equal", adjustable="box")
ax.set_xlabel("Parte real")
ax.set_ylabel("Parte imaginária")
ax.set_title("Círculo unitário: exp(iθ)")
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(ASSETS / "circulo_unitario_euler.png", dpi=160)
plt.close(fig)

print(f"Figuras salvas em {ASSETS}")
