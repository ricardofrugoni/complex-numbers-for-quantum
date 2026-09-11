# Um livro aberto, visual e explorável

O projeto é um lugar de conhecimento sobre números complexos, útil também para quem ainda não estuda computação quântica. A experiência editorial segue **curiosidade → intuição → visualização → matemática → demonstração → aplicação → conexão quântica**.

## Como os capítulos contam essa história

Uma motivação abre cada tema. Equações e figuras se explicam mutuamente; exemplos calculados revelam relações; notebooks permitem mudar os parâmetros. Convites como “observe”, “compare” e “experimente” acompanham o leitor sem exigir uma avaliação ou uma sequência de tarefas.

Cada capítulo oferece uma descoberta, uma ligação com outros conceitos, uma janela quântica e referências para aprofundamento. Curiosidades devem reforçar a matemática e ter base verificável. Aplicações avançadas explicitam os pré-requisitos que ainda faltam.

## Mapa do conteúdo

| Percurso | Ideia que se torna visível | Demonstração |
|---|---|---|
| Plano complexo | Um número tem duas coordenadas | Ponto, vetor e projeções |
| Módulo e argumento | Distância e direção | Círculos de mesmo módulo |
| Conjugado | Reflexão que preserva a distância | Vetor e seu espelho |
| Operações, polar e Euler | Somar desloca; multiplicar escala e gira | Soma vetorial, grade e hélice |
| Raízes da unidade | Potências organizam simetrias | Polígonos regulares |
| Aplicações | Magnitude e fase descrevem sinais e oscilações | Ondas, fasores, Fourier e espiral |
| Ponte quântica | Amplitudes são coordenadas de um estado | Normalização e prévia de fase relativa |

Os nomes existentes dos arquivos são mantidos para preservar links. A ordem de leitura é indicada pela navegação dos capítulos e pela trilha do README, sem depender da numeração dos arquivos.

## Papéis de cada parte

- **README:** entrada visual, demonstração breve e índice navegável.
- **Capítulos:** explicações completas, exemplos e referências.
- **Sete notebooks:** cinco demonstrações curtas e dois laboratórios que reúnem dez experiências interativas.
- **`src/`:** cálculos e visualizações reutilizáveis.
- **`assets/` e seus geradores:** SVGs, PNGs e GIF reproduzíveis, descritos nos documentos.
- **Testes e validação:** conferência matemática, controles e execução das demonstrações.

## Escopo e janelas futuras

A base inclui forma cartesiana e polar, módulo, argumento, conjugado, Euler, operações, potências e raízes da unidade. Ondas, fasores, circuitos AC, Fourier e sistemas dinâmicos mostram aplicações sem exigir um curso completo dessas áreas.

A ponte quântica apresenta estados puros de um qubit, normalização e uma comparação introdutória entre fase global e relativa. Produto interno, matrizes unitárias, QFT, espaços de Hilbert, sistemas compostos e algoritmos aparecem como destinos futuros com seus pré-requisitos explicitados.

Um ponto no plano representa um número complexo. Não deve ser confundido com o estado inteiro de um qubit, a esfera de Bloch ou uma trajetória física. Multiplicar por qualquer complexo também não é, em geral, uma operação quântica válida.

## Critérios editoriais da entrega

O critério é a qualidade do material: navegação funcional; conceitos acompanhados de geometria; exemplos executáveis; interações que esclarecem relações; fontes precisas; casos especiais explícitos; figuras legíveis com alternativa estática à animação. Não há uma prova, lista obrigatória de exercícios ou requisito de memorização para o leitor.

Novos conteúdos devem manter esse fluxo e reaproveitar Python, Matplotlib e Jupyter quando atenderem à demonstração. A publicação de uma aplicação hospedada é uma possibilidade futura; o livro e os laboratórios possuem uma rota local documentada.

A configuração em `binder/` e o [guia de publicação](docs/07_laboratorio_interativo.md#publicar-com-binder) preparam a hospedagem dos próprios notebooks. O link público só será anunciado depois da construção e da conferência nessa plataforma. O laboratório quântico permite comparar fases e probabilidades em duas bases, com os pré-requisitos e limites explicados no capítulo da ponte.
