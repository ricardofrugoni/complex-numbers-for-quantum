# Módulo e argumento: distância e direção

[← Plano complexo](01_plano_complexo.md) · [Entrada](../README.md) · [Conjugado →](03_conjugado.md)

As coordenadas dizem quanto andar em cada eixo. Existe outra descrição igualmente útil: quanto se afastar da origem e em qual direção.

<a id="modulo"></a>
## Um triângulo revela o módulo

Para $z=a+bi$, as projeções formam um triângulo retângulo:

$$r=|z|=\sqrt{a^2+b^2}.$$

![O vetor de z, suas projeções e um círculo de mesmo módulo aparecem juntos no plano.](../assets/interactive/plano.png)

No [laboratório](../notebooks/06_laboratorio_interativo.ipynb#plano), escolha $3+4i$. Os catetos medem 3 e 4; a seta mede $\sqrt{9+16}=5$. Todos os pontos do círculo têm esse mesmo módulo. A reflexão $3-4i$, desenhada com outra linha, preserva a distância.

<a id="argumento"></a>
## O arco revela o argumento

Para $z\ne0$, um argumento $\theta$ mede a rotação do eixo real positivo até o vetor. O sentido anti-horário é positivo. Em Python, `cmath.phase(z)` equivale a `atan2(b, a)` e considera o quadrante corretamente; `atan(b/a)` sozinho perde essa informação.

```python
import cmath
import math

z = 3 + 4j
theta = cmath.phase(z) if z != 0 else None
print(abs(z))  # 5.0
print(math.degrees(theta) if theta is not None else 'indefinido')
# Aproximadamente 53.13 graus
```

O ângulo $\theta+2\pi$ aponta na mesma direção que $\theta$. Um **argumento principal** escolhe um representante; `cmath.phase` retorna valores entre $-\pi$ e $\pi$, com uma convenção que distingue zeros com sinal no corte do eixo real negativo. O [notebook](../notebooks/02_modulo_argumento.ipynb) compara essas direções.

> **Algo contraintuitivo**
> Um ponto pode se mover continuamente e o número que representa seu argumento principal saltar de perto de $180°$ para perto de $-180°$. O salto está na escolha do ângulo, não no percurso.

## Observe a origem

Em $z=0$, o módulo é zero e o argumento matemático é indefinido: uma seta sem comprimento não escolhe direção. Bibliotecas podem devolver um ângulo por convenção numérica. Os laboratórios sinalizam essa diferença em vez de atribuir uma fase à origem.

Compare $1+i$ e $-1-i$: ambos têm módulo $\sqrt2$, mas apontam em direções opostas. **Mover a direção sem mudar o módulo** será a base das rotações e dos fatores de fase.

## Onde isso reaparece em computação quântica?

Para amplitudes de um estado normalizado em uma base ortonormal, o módulo ao quadrado fornece probabilidades de medição. A fase relativa continua relevante para operações posteriores. Um $|z|^2$ arbitrário, como $|3+4i|^2=25$, não é uma probabilidade.

## Para aprofundar

[OpenStax — forma polar](https://openstax.org/books/algebra-and-trigonometry-2e/pages/10-5-polar-form-of-complex-numbers) · [Python — `phase`](https://docs.python.org/3/library/cmath.html#cmath.phase) · [IBM — amplitudes e normalização](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/single-systems/quantum-information).

**[Continue: o espelho de um número →](03_conjugado.md)**
