# Números Complexos para Computação Quântica

Projeto introdutório para estudar **números complexos de forma geométrica e computacional** antes de avançar para o formalismo de estados quânticos.

A ideia central é construir a seguinte ponte:

```text
números reais
    ↓
plano complexo
    ↓
módulo e argumento
    ↓
forma polar
    ↓
fórmula de Euler
    ↓
multiplicação = escala + rotação
    ↓
amplitudes complexas
    ↓
estados quânticos e fase
```

## Por que este repositório existe?

Estados de qubits são descritos com amplitudes que, em geral, são números complexos:

$$
|\psi\rangle = \alpha|0\rangle + \beta|1\rangle,
\qquad \alpha,\beta \in \mathbb{C}.
$$

Para compreender posteriormente **fase, interferência, portas quânticas e evolução unitária**, não basta tratar números complexos como uma regra algébrica envolvendo $i$. É útil entender sua geometria.

Este projeto começa no plano complexo e termina apenas com uma **ponte introdutória para amplitudes quânticas**. Ele não substitui o estudo formal de álgebra linear ou informação quântica.

## Conteúdo

| Módulo | Tema | Representação geométrica | Conexão futura |
|---|---|---|---|
| 1 | $z=a+bi$ | ponto/vetor no plano | amplitudes complexas |
| 2 | módulo e argumento | distância e ângulo | magnitude e fase |
| 3 | conjugado | reflexão no eixo real | módulo, produto interno |
| 4 | forma polar | raio + ângulo | fase |
| 5 | fórmula de Euler | círculo unitário | rotações e fases |
| 6 | multiplicação complexa | escala + rotação | operações quânticas |
| 7 | ponte para qubits | amplitudes $\alpha,\beta$ | normalização e interferência |

## Estrutura

```text
.
├── README.md
├── PROJECT_PLAN.md
├── requirements.txt
├── docs/
│   ├── 01_plano_complexo.md
│   ├── 02_modulo_argumento.md
│   ├── 03_conjugado.md
│   ├── 04_forma_polar_euler.md
│   ├── 05_operacoes_geometricas.md
│   └── 06_ponte_para_qubits.md
├── notebooks/
│   ├── 01_plano_complexo.ipynb
│   ├── 02_modulo_argumento.ipynb
│   ├── 03_operacoes_geometricas.ipynb
│   ├── 04_forma_polar_euler.ipynb
│   └── 05_ponte_para_qubits.ipynb
├── src/
│   └── complex_geometry.py
├── scripts/
│   └── generate_assets.py
├── assets/
└── tests/
    └── test_complex_geometry.py
```

## Como executar

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
# .venv\Scripts\activate       # Windows

pip install -r requirements.txt
jupyter lab
```

Para gerar as figuras usadas no projeto:

```bash
python scripts/generate_assets.py
```

Para rodar os testes:

```bash
pytest -q
```

## Conceitos mínimos a dominar

Ao final, você deve conseguir explicar e calcular:

1. parte real e imaginária;
2. módulo $|z|$;
3. argumento $\arg(z)$;
4. conjugado $z^*$;
5. conversão cartesiana ↔ polar;
6. fórmula de Euler $e^{i\theta}=\cos\theta+i\sin\theta$;
7. por que multiplicar por $e^{i\theta}$ produz uma rotação;
8. por que amplitudes quânticas podem ter fase mesmo quando probabilidades usam módulos ao quadrado.

## Regra de estudo

Para cada módulo:

1. leia o texto;
2. feche o texto e explique o conceito sem consultar;
3. execute o notebook;
4. altere os exemplos;
5. resolva os exercícios;
6. escreva em uma frase a conexão com computação quântica.

## Status no roadmap

Este repositório corresponde ao bloco **B1 — Matemática I: números complexos e álgebra linear dirigida**. É uma prática complementar. Concluir este projeto não significa concluir sozinho B1, porque o bloco também exige vetores complexos, produto interno, matrizes, ortogonalidade, autovalores, unitariedade e produto tensorial.

## Fontes principais

- MIT OpenCourseWare — Linear Algebra 18.06.
- IBM Quantum Learning — Basics of Quantum Information.
- Python `cmath` — representação cartesiana/polar e funções complexas.
- NumPy — operações e ângulos de números complexos.

Veja referências e observações nos documentos de cada módulo.
