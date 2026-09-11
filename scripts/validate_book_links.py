"""Verifica links locais, âncoras, tabelas e formato dos notebooks, sem acessar a rede."""

from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import nbformat

ROOT = Path(__file__).resolve().parents[1]


def read_text(path):
    if path.suffix == '.ipynb':
        notebook = nbformat.read(path, as_version=4)
        nbformat.validate(notebook)
        return '\n\n'.join(cell.source for cell in notebook.cells if cell.cell_type == 'markdown')
    return path.read_text(encoding='utf-8-sig')


def anchors(text):
    found = set(re.findall(r'<a\s+id="([^"]+)"', text))
    for heading in re.findall(r'^#{1,6}\s+(.+)$', text, re.M):
        heading = re.sub(r'[^\w\- ]', '', heading.lower())
        found.add(heading.strip().replace(' ', '-'))
    return found


def main():
    documents = [ROOT/'README.md', ROOT/'PROJECT_PLAN.md', *sorted((ROOT/'docs').glob('*.md')),
                 *sorted((ROOT/'notebooks').glob('*.ipynb'))]
    texts = {p.resolve(): read_text(p) for p in documents}
    all_anchors = {path: anchors(text) for path, text in texts.items()}
    errors, count = [], 0
    for path, text in texts.items():
        if re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', text):
            errors.append(f'{path.name}: caractere de controle no texto')
        explicit = re.findall(r'<a\s+id="([^"]+)"', text)
        if len(explicit) != len(set(explicit)):
            errors.append(f'{path.name}: âncoras explícitas repetidas')
        prose = re.sub(r'```.*?```', '', text, flags=re.S)
        links = re.findall(r'\]\(([^\s)]+)\)', prose) + re.findall(r'href="([^"]+)"', prose)
        for link in links:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc:
                continue
            target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            count += 1
            if not target.exists():
                errors.append(f'{path.relative_to(ROOT)}: arquivo ausente {link}')
            elif parsed.fragment and target in texts and unquote(parsed.fragment) not in all_anchors[target]:
                errors.append(f'{path.relative_to(ROOT)}: âncora ausente {link}')
        expected = None
        for line in prose.splitlines():
            if line.startswith('|'):
                pipes = len(re.findall(r'(?<!\\)\|', line))
                if expected is None:
                    expected = pipes
                elif expected != pipes:
                    errors.append(f'{path.name}: tabela com {pipes} separadores; esperados {expected}: {line[:100]}')
            else:
                expected = None
    print(f'{len(documents)} documentos; {count} links locais conferidos.')
    if errors:
        print('\n'.join(errors))
        raise SystemExit(1)
    print('Links, âncoras, tabelas e formato dos notebooks: OK.')


if __name__ == '__main__':
    main()
