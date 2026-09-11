# O plano complexo: um número ganha direção

[Entrada do livro](../README.md) · [Próxima descoberta: módulo e argumento →](02_modulo_argumento.md)

<a id="por-que-complexos"></a>
## Por que sair da reta real?

Na reta real, elevar qualquer número ao quadrado produz um resultado não negativo. A equação $x^2=-1$ pede algo que essa reta não oferece. Podemos ampliar o sistema de números e trabalhar com uma nova unidade, mantendo regras consistentes de soma e multiplicação.

<a id="unidade-imaginaria"></a>
## A unidade imaginária

Definimos $i$ por $i^2=-1$. Assim, $i$ e $-i$ resolvem $x^2+1=0$. O nome “imaginário” não significa que as operações sejam arbitrárias: elas têm uma representação geométrica precisa.

<a id="forma-cartesiana"></a>
## Duas coordenadas, um número

$$z=a+bi,\qquad a,b\in\mathbb{R}.$$

$a=\operatorname{Re}(z)$ é a parte real e $b=\operatorname{Im}(z)$ é a parte imaginária. **A parte imaginária é o número real $b$**, enquanto $bi$ é o termo imaginário. Em Python, usamos `j` no lugar de $i$:

```python
z = 3 + 4j
print(z.real, z.imag)  # 3.0 4.0
```

<a id="plano-complexo"></a>
## Veja o número no plano

![Plano de z e seu conjugado, com projeções nos eixos, círculo de mesmo módulo e arco do argumento.](../assets/interactive/plano.png)

No gráfico, a coordenada horizontal é $a$ e a vertical é $b$. O laboratório começa em $3+2i$; mova `b` para 4 para encontrar $3+4i$. O ponto está três unidades à direita e quatro acima da origem. A seta liga a origem ao mesmo ponto: ela revela comprimento e direção.

<a id="geometria"></a>
## A geometria organiza a informação

Fixar $a$ e variar $b$ faz o ponto subir e descer. Fixar $b$ e variar $a$ move o ponto horizontalmente. Os números reais continuam aqui: são os pontos do eixo horizontal, com $b=0$.

**[Mova o ponto no laboratório](../notebooks/06_laboratorio_interativo.ipynb#plano)** ou acompanhe a [demonstração curta](../notebooks/01_plano_complexo.ipynb). Compare $1+i$, $-1+i$ e $-1-i$: as coordenadas mudam, mas a distância à origem permanece $\sqrt2$.

> **Veja isto geometricamente**
> Um único símbolo $z$ guarda duas coordenadas reais. A utilidade aparece quando operações algébricas passam a descrever deslocamentos, reflexões e rotações.

## Onde isso reaparece em computação quântica?

Uma amplitude pode ser um número complexo. Este plano ajuda a enxergar sua magnitude e fase, mas um único ponto não representa todo o estado de um qubit: serão necessárias duas amplitudes organizadas em um vetor normalizado. A [ponte quântica](06_ponte_para_qubits.md) retoma essa distinção.

## Para aprofundar

[MIT — álgebra e plano complexo, §§1.2–1.4](https://ocw.mit.edu/courses/18-04-complex-variables-with-applications-spring-2018/6eae09885b0fab3f068e31752198abea_MIT18_04S18_topic1.pdf) · [Python — representação cartesiana](https://docs.python.org/3/library/cmath.html) · [Fontes comentadas](REFERENCIAS.md).

**[Continue: distância e direção →](02_modulo_argumento.md)**
