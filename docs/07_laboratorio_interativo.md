# Laboratório interativo de geometria complexa

O notebook [06_laboratorio_interativo.ipynb](../notebooks/06_laboratorio_interativo.ipynb) acrescenta sete experiências aos módulos existentes. Cada uma combina controles, gráficos e resultados numéricos. O módulo [interactive_geometry.py](../src/interactive_geometry.py) também permite reutilizar as figuras em outros notebooks.

## Preparação e execução

As dependências estão em [requirements-interactive.txt](../requirements-interactive.txt). Esse arquivo inclui os quatro requisitos originais e acrescenta `ipympl`, responsável por conectar os gráficos Matplotlib à interface do JupyterLab. `ipywidgets`, o suporte de widgets do Jupyter e demais dependências transitivas são resolvidos pelo instalador. Não é necessário instalar Plotly, SciPy, Qiskit, Node.js ou uma biblioteca 3D separada para estes laboratórios. O desenho 3D usa `mplot3d`, já incluído no Matplotlib. [Documentação de backends](https://matplotlib.org/stable/users/explain/figure/backends.html) e [instalação do ipympl](https://matplotlib.org/ipympl/installing.html).

**Execute a instalação somente após autorizar as dependências.** Na raiz do projeto, em PowerShell, usando o `uv` já disponível:

```powershell
uv pip install --python .venv/Scripts/python.exe -r requirements-interactive.txt
.venv/Scripts/python.exe -m jupyterlab notebooks/06_laboratorio_interativo.ipynb
```

Em um ambiente que já tenha `pip`, a alternativa é `python -m pip install -r requirements-interactive.txt`. O `pip` não é necessário quando se usa `uv`. Selecione no Jupyter o kernel correspondente à `.venv`; a primeira célula mostra o caminho do Python. Reinicie o kernel após instalar `ipympl`.

Execute as células em ordem. `%matplotlib widget` deve preceder a criação das figuras. Os botões restauram os valores; nas figuras 3D, “Restaurar vista” recupera a câmera sem alterar os parâmetros. Arrastar a área 3D gira a câmera. As funções preservam o ângulo da câmera ao mudar os sliders.

Os controles precisam de um kernel ativo. Uma prévia do notebook em um visualizador estático e um PNG exportado não mantêm interatividade. O notebook informa a ausência de `ipympl` com uma mensagem acionável, sem instalar nada automaticamente. [ipympl](https://matplotlib.org/ipympl/).

## Experiências e interpretação

| Experiência | Controles | O que comparar |
|---|---|---|
| Plano e conjugado | partes real e imaginária | vetor, projeções, círculo de mesmo módulo, arco de argumento e reflexão |
| Soma vetorial | componentes de dois vetores | caminho ponta a cauda, resultante e desigualdade triangular |
| Multiplicação | ponto, módulo e ângulo do multiplicador | transformação da grade inteira, escala e rotação |
| Euler em 3D | módulo, fase inicial, voltas e posição | trajetória, círculo projetado e componentes seno/cosseno |
| Potências | ângulo e expoente inteiro | repetição de pontos e argumento principal versus ângulo acumulado |
| Módulo ao quadrado em 3D | partes real e imaginária | altura da superfície e curvas de nível |
| Amplitudes | P(0) e fases de α e β | mudança dos vetores e probabilidades na base computacional |

A base algébrica é a representação polar e a fórmula de Euler: multiplicar complexos multiplica módulos e soma ângulos. Potências de módulo unitário repetem a rotação. As construções seguem as notas do [MIT, seções 1.3–1.8](https://ocw.mit.edu/courses/18-04-complex-variables-with-applications-spring-2018/6eae09885b0fab3f068e31752198abea_MIT18_04S18_topic1.pdf), conferidas com o [OpenStax, seção 10.5](https://openstax.org/books/algebra-and-trigonometry-2e/pages/10-5-polar-form-of-complex-numbers).

Na hélice, a terceira coordenada é o parâmetro `t`: o número complexo continua sendo representado por duas componentes reais. Não se assume dinâmica física, Hamiltoniano ou unidade de tempo. Na superfície, a altura é uma função real, `h = a² + b²`. Essas duas figuras são construções didáticas derivadas das fórmulas existentes.

O painel de amplitudes usa `α = √p exp(iφα)` e `β = √(1−p) exp(iφβ)`, com `0 ≤ p ≤ 1`. Assim, a soma das probabilidades permanece 1, dentro do erro de ponto flutuante. As barras descrevem apenas a medição na base `|0⟩, |1⟩`; observar barras invariantes às fases não permite concluir que fases sejam irrelevantes para outras operações. [IBM Quantum Learning](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/single-systems/quantum-information) e [TU Delft, Born rule](https://ocw.tudelft.nl/course-lectures/1-2-1-born-rule/).

## Casos especiais

- **Origem:** o argumento matemático de zero não é definido. Os novos painéis mostram essa condição e retiram o arco. A função original `argument()` continua com a convenção numérica de `cmath.phase`; uma eventual alteração dessa API está na auditoria para aprovação.
- **Voltas:** o argumento principal pode saltar entre valores próximos de +180° e −180° sem descontinuidade do ponto. No limite do corte, zeros com sinal e arredondamentos podem determinar qual extremo aparece. [Python, `cmath.phase`](https://docs.python.org/3/library/cmath.html#cmath.phase).
- **Multiplicador zero:** todos os pontos da grade passam à origem, e não há uma direção final definida.
- **Potências:** os pontos são passos discretos; os segmentos somente mostram sua ordem. Pontos coincidentes podem se sobrepor. Use o painel de ângulos para acompanhar todos os expoentes.
- **Módulo ao quadrado:** para um complexo arbitrário, pode exceder 1. Sua interpretação como probabilidade requer o contexto de amplitude de um estado normalizado.
- **Câmera:** girar a vista 3D não altera o número complexo. Os eixos 3D representam grandezas diferentes e não definem uma distância física conjunta.

## Uso por código e exportação

```python
from src.interactive_geometry import complex_plane, euler_helix

lab = complex_plane()
lab.set_values(a=3, b=4)
print(lab.values)
print({nome: (s.valmin, s.valmax) for nome, s in lab.sliders.items()})
lab.reset()

helix = euler_helix()
helix.axes[0].view_init(elev=40, azim=25)
helix.fig.savefig('assets/minha_helice.png', dpi=160)
```

`set_values` valida limites, valores finitos e passos antes de modificar os controles. Acesso numérico e controle por código complementam o uso do mouse; as figuras Matplotlib ainda não constituem uma interface plenamente acessível a leitores de tela.

Para exportar as sete prévias estáticas sem abrir janelas:

```powershell
.venv/Scripts/python.exe scripts/explore_geometry.py todos --output assets/interactive
```

Para uma janela local, caso o Python já tenha um backend gráfico funcional:

```powershell
.venv/Scripts/python.exe scripts/explore_geometry.py euler3d
```

A janela local depende do backend disponível, por exemplo TkAgg. O script detecta backends estáticos e orienta o uso do notebook. A execução recomendada para este projeto é o JupyterLab.

## Verificação

```powershell
.venv/Scripts/python.exe -m pytest -q
```

Os novos testes verificam normalização, casos nulos, rotações conhecidas, coordenadas dos gráficos, eventos de mouse nos controles, botão de restauração, preservação da câmera e renderização nos limites dos sliders. A execução completa do notebook e o estado da validação estão registrados na [auditoria](AUDITORIA_E_MELHORIAS.md).
