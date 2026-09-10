# 2. Módulo e argumento

Para

$$
z=a+bi,
$$

o módulo é

$$
|z|=\sqrt{a^2+b^2}.
$$

Geometricamente, $|z|$ é a distância entre a origem e o ponto $(a,b)$.

O argumento $\arg(z)$ é o ângulo entre o eixo real positivo e o vetor associado a $z$.

$$
\theta=\arg(z).
$$

Em código, é preferível calcular o ângulo com uma função equivalente a `atan2(b,a)`, porque ela identifica corretamente o quadrante.

## Exemplo

Para $z=3+4i$:

$$
|z|=5.
$$

O argumento é

$$
\theta=\operatorname{atan2}(4,3).
$$

## Interpretação

- módulo → tamanho;
- argumento → direção/fase.

## Conexão futura

Em computação quântica, amplitudes complexas possuem magnitude e fase. Probabilidades dependem do módulo ao quadrado; fases tornam-se essenciais para interferência.

## Exercícios

1. Calcule módulo e argumento de $1+i$.
2. Compare $1+i$ e $-1-i$.
3. Dois números podem ter o mesmo módulo e argumentos diferentes?
