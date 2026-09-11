# Referências para continuar a exploração

[Entrada do livro](../README.md)

Fontes consultadas em 10 de setembro de 2026 e reconferidas na revisão de 11 de setembro de 2026. As explicações, exemplos numéricos e figuras deste repositório são construções didáticas próprias; os links permitem conferir a matemática e seguir para tratamentos mais completos.

| Tema | Fonte e uso no livro |
|---|---|
| Álgebra, plano, conjugado, Euler | [Jeremy Orloff, MIT 18.04, Topic 1 (2018)](https://ocw.mit.edu/courses/18-04-complex-variables-with-applications-spring-2018/6eae09885b0fab3f068e31752198abea_MIT18_04S18_topic1.pdf): fundamento matemático e interpretação geométrica |
| Forma polar, potências e raízes | [OpenStax, Algebra and Trigonometry 2e, §10.5](https://openstax.org/books/algebra-and-trigonometry-2e/pages/10-5-polar-form-of-complex-numbers): conferência independente da geometria polar |
| Raízes da unidade | [MIT 18.03, Complex Numbers, Roots of Unity (2010)](https://ocw.mit.edu/courses/18-03-differential-equations-spring-2010/resources/mit18_03s10_c05/): potências e simetrias |
| Ondas | [MIT 6.007, anexo à aula 18 (2011)](https://ocw.mit.edu/courses/6-007-electromagnetic-energy-from-motors-to-lasers-spring-2011/95bea9116bb2924f60df6860462d55c8_MIT6_007S11_lec18.pdf): ondas eletromagnéticas, fase e frequência |
| Diagramas de fasores | [OpenStax, University Physics vol. 2, §15.2](https://openstax.org/books/university-physics-volume-2/pages/15-2-simple-ac-circuits): rotação, projeções e defasagem entre tensão e corrente |
| Circuitos AC | [James L. Kirtley Jr., MIT 6.061, capítulo 2 (2011)](https://ocw.mit.edu/courses/6-061-introduction-to-electric-power-systems-spring-2011/9cf8de165233601f547b284cee5c2131_MIT6_061S11_ch2.pdf): fasores, impedância e regime permanente |
| DFT, espectros e convenções | [NumPy — Discrete Fourier Transform](https://numpy.org/doc/stable/reference/routines.fft.html): sinais dos expoentes, normalização e sinais reais |
| Amplitudes e estados puros | [John Watrous, IBM Quantum Learning — Quantum information](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/single-systems/quantum-information): coordenadas complexas, normalização e probabilidades |
| Regra de Born | [TU Delft — Born rule](https://ocw.tudelft.nl/course-lectures/1-2-1-born-rule/): conferência universitária da conexão entre amplitudes e probabilidades |
| Fases global e relativa | [IBM — Limitations on quantum information](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/quantum-circuits/limitations-on-quantum-information): equivalência por fase global e diferença de fase relativa |
| Combinação de amplitudes | [Aram Harrow, MIT 8.06 — Quantum Computing, §2.1, pp. 3–4](https://ocw.mit.edu/courses/8-06-quantum-physics-iii-spring-2016/766eb82809dd269944b11e838ed1814b_MIT8_06S16_chap5.pdf): conferência universitária da matriz de Hadamard usada para as coordenadas na base +/−; notas atualizadas em 23/05/2016 |
| Janela para QFT | [IBM — Phase-estimation procedure](https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms/phase-estimation-and-factoring/phase-estimation-procedure): fatores de fase nas matrizes da QFT |
| Convenções numéricas | [Python 3.13 — cmath](https://docs.python.org/3.13/library/cmath.html): coordenadas, argumento principal e zeros com sinal; a execução local usa Python 3.13 |
| Interação local | [Matplotlib — ipympl](https://matplotlib.org/ipympl/) e [compatibilidade](https://matplotlib.org/ipympl/installing.html): widgets e kernel ativo |
| Leitura no GitHub | [GitHub — arquivos não textuais](https://docs.github.com/en/repositories/working-with-files/using-files/working-with-non-code-files): SVG, GIF e prévias estáticas de notebooks |
| Publicação dos notebooks | [Binder — introdução](https://mybinder.readthedocs.io/en/latest/introduction.html), [interfaces](https://mybinder.readthedocs.io/en/latest/howto/user_interface.html) e [repo2docker — localização da configuração](https://repo2docker.readthedocs.io/en/latest/use/repository/): pasta `binder/` e abertura direta no JupyterLab; [limites](https://mybinder.readthedocs.io/en/latest/about/user-guidelines.html) de sessões temporárias |

## Relações conferidas e limites da interpretação

| Relação | Conferência e consequência para o livro |
|---|---|
| Multiplicação combina escala e rotação | MIT 18.04 e OpenStax §10.5 concordam. A soma de argumentos é entendida módulo uma volta; fatores nulos não recebem direção. |
| Conjugado produz módulo ao quadrado | A identidade algébrica e a reflexão geométrica concordam. O resultado é não negativo, inclusive zero, e pode exceder 1 fora de um estado normalizado. |
| Fasores descrevem regime senoidal permanente | MIT 6.061 e OpenStax Física §15.2 fornecem tratamentos complementares. As magnitudes de pico do exemplo são mantidas consistentes; transientes e misturas de frequências exigem outro tratamento. |
| Fourier retém magnitude e fase | A decomposição do cosseno obtida por Euler coincide com os coeficientes da DFT calculados no notebook. NumPy e IBM/QFT usam convenções de sinal e normalização explicitadas no capítulo. |
| Uma fase relativa pode mudar uma distribuição em outra base | A combinação normalizada de amplitudes segue a matriz nas notas de Harrow e o exemplo de Hadamard da IBM. A regra de Born transforma cada coordenada em probabilidade. Cada par de barras corresponde a uma base própria. |
| Uma fase global preserva todas as probabilidades | A demonstração da IBM usa linearidade e módulo unitário. No livro, a verificação computacional compara as duas bases exibidas; a afirmação sobre qualquer base depende da demonstração, não apenas do gráfico. |

No painel quântico, a identidade $P(\pm)=1/2\pm\sqrt{p(1-p)}\cos(\Delta\varphi)$ é uma derivação algébrica das amplitudes normalizadas. Ela fornece uma conferência independente dos valores calculados por soma e subtração de complexos. Os testes incluem amplitudes nulas, interferência completa e uma rotação comum das duas fases. Os resíduos perto de zero são tratados como erro numérico, não como novos efeitos físicos.

As notas de Harrow trazem “Spring 2015” no cabeçalho, uma atualização em maio de 2016 e estão no curso de 2016. A referência registra a atualização do documento. TU Delft é uma aula introdutória em vídeo sobre a regra de Born; a derivação da segunda base foi conferida no material escrito do MIT e da IBM.

## Como interpretar as fontes

Na conferência dos anexos, a página da aula 18 do MIT usa um título sobre sistemas lineares e fasores, mas seu PDF abre como *Electromagnetic Waves*. O livro identifica o conteúdo efetivamente consultado e usa MIT 6.061 e OpenStax para os fasores. A nota de raízes do curso MIT 18.03 de 2010 traz a data de aula de 15 de fevereiro de 2008; o ano da oferta do curso não foi tratado como data original de autoria.

Livros universitários, notas de cursos e documentação primária são adequados para conferir identidades matemáticas e comportamento de software. Não os apresentamos como revisões sistemáticas ou estudos experimentais sobre aprendizagem. A proposta visual é uma escolha editorial; não se afirma um ganho pedagógico medido.

MIT e OpenStax oferecem uma conferência cruzada da base matemática; IBM e TU Delft, da interpretação probabilística. A IBM também é fornecedora comercial de computação quântica: usamos seu material técnico, sem inferir superioridade de seus produtos. Documentações de Python, NumPy e Matplotlib são autoridades sobre suas próprias interfaces.

Duas diferenças de convenção merecem atenção: o argumento principal de bibliotecas é uma escolha numérica, não uma direção matemática na origem; sinais e normalizações de Fourier variam entre definições. Os capítulos explicitam ambas. Não foram incluídas alegações históricas de autoria ou prioridade sem verificação documental.
