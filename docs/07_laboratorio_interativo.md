# Laboratório interativo de geometria complexa

Dez experiências combinam controles, gráficos e resultados numéricos. O notebook [Geometria e amplitudes](../notebooks/06_laboratorio_interativo.ipynb) reúne sete laboratórios; [Raízes, ondas e Fourier](../notebooks/07_raizes_ondas_fourier.ipynb) acrescenta três. O módulo [interactive_geometry.py](../src/interactive_geometry.py) permite reutilizar as figuras em outros notebooks.

[Voltar ao livro](../README.md) · [Conhecer as aplicações](09_onde_sao_usados.md)

## Preparação e execução

As dependências estão em [requirements-interactive.txt](../requirements-interactive.txt). Esse arquivo inclui os quatro requisitos originais e acrescenta `ipympl`, responsável por conectar os gráficos Matplotlib à interface do JupyterLab. `ipywidgets`, o suporte de widgets do Jupyter e demais dependências transitivas são resolvidos pelo instalador. Não é necessário instalar Plotly, SciPy, Qiskit, Node.js ou uma biblioteca 3D separada para estes laboratórios. O desenho 3D usa `mplot3d`, já incluído no Matplotlib. [Documentação de backends](https://matplotlib.org/stable/users/explain/figure/backends.html) e [instalação do ipympl](https://matplotlib.org/ipympl/installing.html).

Na raiz do projeto, em PowerShell, com uma `.venv` criada e o `uv` instalado:

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
| Amplitudes | P(0) e fases de α e β | fase relativa e probabilidades nas bases 0/1 e +/− |
| Raízes da unidade | número inteiro de raízes | simetrias e potências que retornam a 1 |
| Ondas | amplitude, frequência angular, fase e instante | rotação e projeção real ao longo do tempo |
| Fourier | amplitude, harmônico e fase | forma do sinal, coeficientes complexos e espectro de amplitudes |

A base algébrica é a representação polar e a fórmula de Euler: multiplicar complexos multiplica módulos e soma ângulos. Potências de módulo unitário repetem a rotação. As construções seguem as notas do [MIT, seções 1.3–1.8](https://ocw.mit.edu/courses/18-04-complex-variables-with-applications-spring-2018/6eae09885b0fab3f068e31752198abea_MIT18_04S18_topic1.pdf), conferidas com o [OpenStax, seção 10.5](https://openstax.org/books/algebra-and-trigonometry-2e/pages/10-5-polar-form-of-complex-numbers).

Na hélice, a terceira coordenada é o parâmetro `t`: o número complexo continua sendo representado por duas componentes reais. Não se assume dinâmica física, Hamiltoniano ou unidade de tempo. Na superfície, a altura é uma função real, `h = a² + b²`. Essas duas figuras são construções didáticas derivadas das fórmulas existentes.

O painel de amplitudes usa `α = √p exp(iφα)` e `β = √(1−p) exp(iφβ)`, com `0 ≤ p ≤ 1`. O primeiro par de barras mostra P(0), P(1); o segundo mostra `P(±) = |(α ± β)/√2|²`. Cada par soma 1 separadamente e corresponde a uma escolha distinta de base. Mova apenas uma fase e compare; depois acrescente o mesmo ângulo às duas fases e compare os ajustes completos. A [ponte quântica](06_ponte_para_qubits.md#fase-relativa) explica as combinações, a fase global e os casos de amplitude nula. [IBM Quantum Learning](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/single-systems/quantum-information) e [TU Delft, Born rule](https://ocw.tudelft.nl/course-lectures/1-2-1-born-rule/).

## Casos especiais

- **Origem:** o argumento matemático de zero não é definido. Os painéis mostram essa condição e retiram o arco. A função `argument()` continua com a convenção numérica de `cmath.phase`; o [capítulo de argumento](02_modulo_argumento.md) explica a distinção.
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

Para exportar as dez prévias estáticas sem abrir janelas:

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

Os testes verificam normalização, casos nulos, rotações, raízes, frequências, coordenadas dos gráficos, eventos de mouse, restauração e renderização nos limites dos controles. A execução dos notebooks e o estado da validação estão registrados na [auditoria](AUDITORIA_E_MELHORIAS.md).

Para executar todos os notebooks e atualizar as saídas dos cinco notebooks estáticos:

```powershell
.venv/Scripts/python.exe scripts/validate_notebooks.py --save-static --output assets/interactive/notebook-validation.json
```

O comando sem `--save-static` somente verifica a execução. As saídas dos laboratórios com widgets não são gravadas como sessões interativas portáteis.

## Compartilhar a experiência

O README usa SVGs, PNGs e um GIF gerados pelo próprio projeto. O [GitHub renderiza esses formatos e apresenta notebooks de forma estática](https://docs.github.com/en/repositories/working-with-files/using-files/working-with-non-code-files); ele não executa os controles do Matplotlib. Para explorar, o leitor baixa ou clona o repositório, instala os requisitos no ambiente e abre o JupyterLab seguindo os comandos acima.

O link **Explorar números complexos** do README aponta para o notebook real. Não há URL pública de aplicação neste momento. A configuração abaixo prepara uma rota de publicação dos próprios notebooks, com kernel Python e `ipympl`.

<a id="publicar-com-binder"></a>
### Publicar com Binder

O arquivo [binder/requirements.txt](../binder/requirements.txt) inclui as dependências interativas do projeto. O Binder reconhece essa pasta como configuração do ambiente. [Guia oficial do Binder](https://mybinder.readthedocs.io/en/latest/introduction.html).

1. Disponibilize esta versão do repositório em um repositório público no GitHub, incluindo `binder/`, `src/`, `notebooks/` e os dois arquivos de requisitos da raiz.
2. No [formulário do Binder](https://mybinder.org/), informe a URL do repositório e a referência Git. Prefira um commit específico para identificar a versão do conteúdo.
3. No campo de caminho, selecione **URL** e informe `lab/tree/notebooks/06_laboratorio_interativo.ipynb`. Inicie a construção do ambiente e aguarde a abertura do JupyterLab.
4. Execute as células e confira um slider, a câmera 3D e os dois pares de barras das amplitudes. Abra também `07_raizes_ondas_fourier.ipynb` e confira as três experiências.
5. Depois dessa conferência, substitua o destino do botão **Explorar números complexos** no README pelo link gerado pelo Binder. A [documentação de interfaces](https://mybinder.readthedocs.io/en/latest/howto/user_interface.html) explica o parâmetro `urlpath=lab/tree/...`.

Esse caminho está preparado, mas a construção remota ainda não foi executada. Um commit fixa o conteúdo; as faixas de versões nos requisitos continuam permitindo atualizações das dependências. Sessões do Binder são temporárias: baixe seus notebooks modificados antes de sair. Consulte os [limites do serviço](https://mybinder.readthedocs.io/en/latest/about/user-guidelines.html) antes de usá-lo com uma turma.

Para quem prefere uma prévia sem movimento, a animação de Euler possui uma [imagem estática equivalente](../assets/book/euler_poster.png). Os gráficos têm descrições no texto e podem ser controlados por código, mas os canvases não oferecem acesso completo por leitores de tela.
