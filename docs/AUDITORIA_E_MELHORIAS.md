# Auditoria e propostas de melhoria

## Abrangência

Foram examinados o README, o plano, os requisitos, os seis documentos conceituais, todas as células dos cinco notebooks originais, os módulos Python, o gerador de figuras, os cinco testes originais e os arquivos de configuração. As três figuras existentes foram inventariadas. Também foi inspecionado o ambiente `.venv`, sem tratar caches e bibliotecas de terceiros como código do projeto. Não foi encontrado outro `AGENTS.md` local. Na conferência final, o Git estava disponível com o commit inicial `c68b947`; a comparação confirmou que, entre os arquivos preexistentes, somente o README recebeu uma seção adicional de acesso aos laboratórios.

O conteúdo constitui uma introdução coerente à geometria complexa e uma ponte inicial para qubits. O plano exclui explicitamente esfera de Bloch, portas e algoritmos. A expansão entregue aprofunda visualmente os tópicos existentes; as propostas que mudariam essa sequência ou a estrutura estão separadas abaixo para decisão.

## Entrega implementada

| Adição | Benefício esperado | Custo ou limitação |
|---|---|---|
| Sete laboratórios reutilizáveis em `src/interactive_geometry.py` | Comparar parâmetros e verificar resultados geométricos imediatamente | Mais código de visualização a manter |
| Notebook `06_laboratorio_interativo.ipynb` | Reunir experimentos e exercícios em um ponto de entrada | Um sexto notebook complementar à trilha original |
| Hélice de Euler e superfície de módulo ao quadrado | Relacionar curvas, projeções, alturas e níveis, com câmera giratória | 3D exige leitura cuidadosa de eixos; não acrescenta uma componente ao número complexo |
| Sliders, restauração e acesso por código | Explorar casos extremos e reproduzir estados exatos | O canvas não oferece acessibilidade completa de uma interface HTML semântica |
| Testes de matemática e eventos | Reduzir regressões que produziriam gráficos plausíveis, mas incorretos | Pequeno aumento do tempo de testes |
| Gerador de prévias PNG | Revisar figuras e reutilizá-las em materiais | PNG não preserva interatividade |
| Requisito adicional separado e guia de execução | Ativar Jupyter interativo sem alterar os requisitos originais | Exige instalar `ipympl` e seus componentes de widgets |

Os benefícios pedagógicos são hipóteses de projeto, fundamentadas na relação direta entre equações e representações; não foi realizado estudo com alunos e não se afirma ganho de aprendizagem medido.

## Necessidades reais de instalação

A `.venv` encontrada aponta para CPython 3.13.4 e contém apenas os arquivos de inicialização do ambiente, sem distribuições instaladas em `site-packages`. Uma consulta ao Python confirmou a ausência de `pip`. Há um executável `uv` disponível, capaz de instalar no ambiente sem adicionar `pip`. O `python` genérico do PATH é outro interpretador, Python 3.14.5 do MSYS2; por isso os comandos indicam explicitamente `.venv/Scripts/python.exe`.

| Dependência direta | Situação no projeto | Necessidade |
|---|---|---|
| NumPy `>=2.0` | Já consta em `requirements.txt` | Amostragem de curvas, vetores e superfícies |
| Matplotlib `>=3.8` | Já consta em `requirements.txt` | Gráficos 2D/3D, sliders e botões |
| JupyterLab `>=4.0` | Já consta em `requirements.txt` | Abrir e executar os notebooks |
| pytest `>=8.0` | Já consta em `requirements.txt` | Executar a suíte de testes; dispensável para apenas estudar |
| ipympl `>=0.9.5,<0.11` | Novo, em `requirements-interactive.txt` | Eventos de mouse e controles Matplotlib dentro do JupyterLab |

O instalador também resolve dependências transitivas, incluindo `ipywidgets`, componentes de comunicação com o kernel e suporte de widgets no Jupyter. A lista exata depende das versões resolvidas. A tabela oficial de compatibilidade cobre as famílias selecionadas; a instalação e os testes locais precisam confirmar a combinação efetivamente obtida. [Compatibilidade do ipympl](https://matplotlib.org/ipympl/installing.html).

Não há necessidade funcional de Plotly, SciPy, Qiskit, Three.js, Node.js ou PyQt para a rota recomendada via JupyterLab. Matplotlib inclui `mplot3d`; não existe uma instalação separada de `mpl_toolkits` a fazer. Uma interface 3D WebGL poderia ser avaliada futuramente se medições de desempenho justificassem a dependência adicional. [Matplotlib, toolkits](https://matplotlib.org/stable/users/explain/toolkits/mplot3d.html).

Instalação proposta, restrita à `.venv` do projeto:

```powershell
uv pip install --python .venv/Scripts/python.exe -r requirements-interactive.txt
```

Nenhum notebook executa instalação automática. A aprovação de bibliotecas não autoriza as mudanças de escopo, arquitetura ou textos listadas a seguir.

## Melhorias que precisam de aval

| Prioridade | Evidência local e proposta | Benefício | Impacto e trade-off | Situação |
|---|---|---|---|---|
| Alta | `argument(0)` retorna a convenção de `cmath.phase`, enquanto a direção matemática na origem é indefinida. Propor uma política explícita para `argument` e `to_polar`, acompanhada de uma ressalva no capítulo 2 | Evitar interpretar zero como tendo uma direção física | Lançar exceção ou retornar `None` muda a API e pode exigir ajustar exemplos; manter a convenção exige explicação | Não aplicado à API nem aos capítulos originais; os novos painéis tratam zero explicitamente |
| Alta | `probability_from_amplitude` calcula `abs(alpha)**2` para qualquer valor. Propor explicitar no nome ou contrato que o contexto probabilístico depende de normalização | Evitar interpretar valores maiores que 1 como probabilidades válidas | Renomear ou validar modifica o contrato e possivelmente chamadas existentes | Não aplicado |
| Alta | README cita fontes gerais, mas os capítulos não trazem links precisos. Propor revisão das referências e casos de fronteira em cada módulo | Facilitar verificação e estudo autônomo | Atualiza os textos didáticos; exige revisão para manter progressão e vocabulário | Referências novas constam apenas nos materiais complementares |
| Média | Notebooks 1 e 3 usam `Path('..')`, supondo execução a partir de `notebooks/`. Propor bootstrap consistente ou instalação do projeto como pacote | Evitar falha de importação ao mudar o diretório de execução | Corrigir caminhos é pequeno; empacotar com `pyproject.toml` altera a estrutura e os comandos | Novo notebook detecta a raiz; originais preservados |
| Média | `complex_geometry.py` importa Matplotlib mesmo para operações numéricas. Propor separar cálculo e desenho | Permitir uso matemático sem carregar a interface gráfica | Reorganiza módulos/importações e requer compatibilidade da API | Não aplicado |
| Média | Dependências originais só têm limites inferiores. Propor um lockfile e política de atualização | Reproduzir o ambiente e diagnosticar regressões | Exige escolher gerenciador e manter versões; um lock deve contemplar plataformas desejadas | Não aplicado |
| Média | `generate_assets.py` executa escrita de arquivos ao ser importado. Propor `main()` e parâmetros explícitos | Tornar o gerador importável e controlar destinos | Pequena alteração no fluxo do script original | Novo script já usa `main()`; original preservado |
| Média | Falta uma rotina de CI para testes e notebooks | Detectar problemas de kernel, caminhos e dependências antes de integrar mudanças | Requer escolher hospedagem, versão de Python e política de CI | Validação local implementada e executada; CI não configurada |
| Média | Os cinco notebooks antigos declaram formato 4.5, mas suas células não têm `id`; o validador atual emite `MissingIDFieldWarning` | Evitar incompatibilidade com validadores futuros | Adicionar identificadores modifica metadados dos arquivos originais, sem alterar o texto | Registrado para aval; originais preservados |
| Opcional | Expandir para esfera de Bloch, mudanças de base, fase global/relativa e interferência com portas | Mostrar fenômenos quânticos além da normalização | Muda explicitamente o escopo; exige álgebra linear e revisão dos capítulos/plano | Aguarda decisão; sem implementação |
| Opcional | Migrar visualizações para Plotly ou aplicativo web | Compartilhamento no navegador e recursos de interface adicionais | Novas dependências, outra arquitetura e possível duplicação de lógica; demanda verificação de acessibilidade e desempenho | Não aplicado |

Manter Python, NumPy, Matplotlib e Jupyter é a recomendação técnica para esta etapa: os objetivos atuais cabem nessas ferramentas. Não foi identificado um requisito que justificasse migração de linguagem. Essa é uma avaliação de engenharia para o tamanho e o escopo observados, não uma comparação universal entre linguagens.

## Conferência científica e nuances

As fórmulas de módulo, polar e multiplicação foram conferidas entre as notas universitárias do MIT e o livro universitário OpenStax. A normalização e a regra de probabilidades foram conferidas entre IBM Quantum Learning e TU Delft. Não se encontrou conflito material nessas identidades. A conferência das fontes foi complementada pelos testes de implementação registrados abaixo.

Há uma diferença de convenção relevante no argumento principal: a direção admite múltiplos ângulos, enquanto bibliotecas escolhem um intervalo e respeitam zeros com sinal. Esse comportamento numérico é descrito pelo Python e não deve ser confundido com uma direção definida na origem. A nova interface explicita a origem e exibe a escolha numérica do argumento nos demais pontos. [Python, `cmath`](https://docs.python.org/3/library/cmath.html).

Na ponte quântica, o experimento mostra somente as probabilidades na base computacional. A explicação formal de interferência e fase relativa requer conteúdo que o plano reserva para etapas seguintes. A distinção entre fase global e relativa aparece na [referência da IBM](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/quantum-circuits/limitations-on-quantum-information), mas não foi convertida em reescrita do capítulo original.

Para este tema matemático e técnico, notas universitárias, livros e documentação primária são mais adequados que meta-análises de estudos empíricos. As notas não foram tratadas como artigos revisados por pares. IBM é fornecedora comercial de computação quântica, e as documentações técnicas são mantidas pelos próprios projetos: são autoridades sobre suas interfaces, não evidências independentes de superioridade comercial. Não foram usadas alegações promocionais. A conferência universitária limita a dependência de uma única fonte comercial.

## Fontes consultadas

Consultas realizadas em 10 de setembro de 2026. Datas editoriais são indicadas quando identificáveis; a data de rastreamento de busca não foi tratada como publicação.

1. Jeremy Orloff, MIT OpenCourseWare. [18.04, Topic 1: Complex algebra and the complex plane](https://ocw.mit.edu/courses/18-04-complex-variables-with-applications-spring-2018/6eae09885b0fab3f068e31752198abea_MIT18_04S18_topic1.pdf), curso de primavera de 2018, seções 1.3–1.8. Geometria, conjugação, soma, desigualdade triangular e Euler.
2. OpenStax, Rice University. [Algebra and Trigonometry 2e, seção 10.5](https://openstax.org/books/algebra-and-trigonometry-2e/pages/10-5-polar-form-of-complex-numbers). Módulo, forma polar, multiplicação e potências. Livro universitário aberto.
3. IBM Quantum Learning. [Quantum information](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/single-systems/quantum-information). Amplitudes e normalização; página corrente, sem data editorial identificada.
4. TU Delft OpenCourseWare. [1.2.1 Born rule](https://ocw.tudelft.nl/course-lectures/1-2-1-born-rule/). Conferência independente da interpretação de `|α|²` e `|β|²` e da condição de normalização.
5. IBM Quantum Learning. [Limitations on quantum information](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/quantum-circuits/limitations-on-quantum-information). Limite da explicação introdutória: fases global e relativa.
6. Python Software Foundation. [cmath — Mathematical functions for complex numbers](https://docs.python.org/3/library/cmath.html). Convenções de `phase`, `polar`, `rect` e cortes. Documentação corrente; a execução local usa a versão indicada no ambiente.
7. Matplotlib Development Team. [Backends](https://matplotlib.org/stable/users/explain/figure/backends.html), [Slider](https://matplotlib.org/stable/gallery/widgets/slider_demo.html), [mplot3d view angles](https://matplotlib.org/stable/api/toolkits/mplot3d/view_angles.html). Eventos, requisitos de interação e rotação da câmera.
8. Matplotlib Development Team. [ipympl](https://matplotlib.org/ipympl/) e [Installing](https://matplotlib.org/ipympl/installing.html). Kernel ativo, instalação e compatibilidade com JupyterLab.

## Estado da validação

Após aprovação, o comando de instalação foi executado na `.venv`: o instalador resolveu e instalou 105 distribuições, contando dependências transitivas. A única dependência direta nova em relação aos requisitos originais é `ipympl`. Não foi necessário instalar `pip`.

Ambiente validado: CPython 3.13.4, NumPy 2.5.3, Matplotlib 3.11.1, JupyterLab 4.6.3, pytest 9.1.1, ipympl 0.10.0 e ipywidgets 8.1.9. Essas são as versões efetivamente instaladas nesta execução, não um lockfile ou uma garantia sobre outras combinações.

| Verificação realizada | Resultado |
|---|---|
| Suíte original e novos testes | **37 testes passaram** |
| Arraste de mouse nas duas figuras 3D | Eventos simulados alteraram a câmera e preservaram os dados |
| Sliders e botão Restaurar | Eventos simulados atualizaram valores e restauraram o estado inicial |
| Normalização e casos de fronteira | Amplitudes nulas, fases, escala zero, origem e limites dos controles verificados |
| Seis notebooks em kernels isolados | Todos executaram, totalizando 15 células de código |
| Saídas do notebook complementar | **Sete saídas de widgets** confirmadas no resultado de execução |
| Prévia das sete experiências | PNGs gerados e inspecionados visualmente; rótulos 3D da hélice ajustados |
| JupyterLab local | Inicializou com as extensões; servidor temporário encerrado ao fim da tentativa de revisão |
| Interação visual no navegador | **Não verificada**: nenhum navegador está disponível à automação nesta sessão |

Os [resultados dos notebooks e versões](../assets/interactive/notebook-validation.json) e as [prévias gráficas](../assets/interactive/) estão disponíveis no projeto. A execução com widgets e os eventos simulados não substituem a revisão da interface no navegador do usuário. Não se afirma que essa etapa visual tenha sido concluída.

Para repetir a validação de execução sem modificar os notebooks:

```powershell
.venv/Scripts/python.exe scripts/validate_notebooks.py --output assets/interactive/notebook-validation.json
```

A validação dos notebooks antigos emitiu o aviso de identificadores de célula mencionado acima; eles continuaram executáveis. O kernel também emitiu um aviso sobre transporte TCP sem criptografia; a execução ocorreu localmente. Nenhum desses avisos foi ocultado ou tratado como falha matemática, e não houve mudança de configuração de segurança.
