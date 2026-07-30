from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.oxml.ns import qn

SRC = 'GitHub_and_GitLab_CLI_Command_Guide.docx'
OUT = 'GitHub_and_GitLab_CLI_Command_Guide.md'

def iter_blocks(parent):
    body = parent.element.body
    for child in body.iterchildren():
        if child.tag == qn('w:p'):
            yield Paragraph(child, parent)
        elif child.tag == qn('w:tbl'):
            yield Table(child, parent)

def clean(text):
    return ' '.join(text.replace('\u00a0', ' ').split())

def escape_cell(text):
    return clean(text).replace('\\', '\\\\').replace('|', '\\|').replace('\n', '<br>')

def is_code(p):
    runs = [r for r in p.runs if r.text.strip()]
    return bool(runs) and all((r.font.name or '').lower() == 'consolas' for r in runs)

def list_marker(p):
    style = p.style.name.lower()
    if 'list bullet' in style:
        return '- '
    if 'list number' in style:
        return '1. '
    return ''

doc = Document(SRC)
lines = []
in_code = False

for block in iter_blocks(doc):
    if isinstance(block, Table):
        if in_code:
            lines += ['```', '']; in_code = False
        rows = [[escape_cell(c.text) for c in row.cells] for row in block.rows]
        if rows:
            lines.append('| ' + ' | '.join(rows[0]) + ' |')
            lines.append('| ' + ' | '.join(['---'] * len(rows[0])) + ' |')
            for row in rows[1:]:
                lines.append('| ' + ' | '.join(row) + ' |')
            lines.append('')
        continue

    text = clean(block.text)
    if not text:
        continue
    if is_code(block):
        if not in_code:
            lines.append('```shell'); in_code = True
        lines.append(text)
        continue
    if in_code:
        lines += ['```', '']; in_code = False

    style = block.style.name
    if style.startswith('Heading '):
        level = int(style.split()[-1])
        lines += ['#' * level + ' ' + text, '']
    else:
        marker = list_marker(block)
        lines += [marker + text, '']

if in_code:
    lines.append('```')

# Remove redundant blank lines while retaining readable separation.
result = []
for line in lines:
    if line == '' and result and result[-1] == '':
        continue
    result.append(line)

with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(result).rstrip() + '\n')
print(OUT)
