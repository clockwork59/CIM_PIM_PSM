#!/usr/bin/env python3
# coding: utf-8

import zipfile
import xml.etree.ElementTree as ET
import os
import re
import sys

def read_xml(zf, path):
    with zf.open(path) as f:
        return ET.fromstring(f.read())

def col_to_index(r):
    m = re.match(r'([A-Z]+)([0-9]+)', r)
    col = m.group(1)
    row = int(m.group(2))
    n = 0
    for ch in col:
        n = n*26 + (ord(ch)-64)
    return n-1, row-1

def convert(xlsx_path, out_dir):
    ns = {'main': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    nsr = {'rel': 'http://schemas.openxmlformats.org/package/2006/relationships'}

    zf = zipfile.ZipFile(xlsx_path)
    wb = read_xml(zf, 'xl/workbook.xml')
    rels_root = read_xml(zf, 'xl/_rels/workbook.xml.rels')

    rels = {}
    for rel in rels_root.findall('rel:Relationship', nsr):
        rels[rel.get('Id')] = rel.get('Target')

    sheets = []
    for s in wb.find('main:sheets', ns).findall('main:sheet', ns):
        name = s.get('name')
        rid = s.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
        target = rels.get(rid)
        if target.startswith('/'):
            target = target[1:]
        if not target.startswith('xl/'):
            target = 'xl/' + target
        sheets.append((name, target))

    # shared strings
    shared = []
    try:
        ss = read_xml(zf, 'xl/sharedStrings.xml')
        for si in ss.findall('main:si', ns):
            texts = []
            for t in si.findall('.//main:t', ns):
                texts.append(t.text or '')
            shared.append(''.join(texts))
    except Exception:
        shared = []

    def get_cell_value(c):
        t = c.get('t')
        v_el = c.find('main:v', ns)
        if t == 's' and v_el is not None:
            idx = int(v_el.text)
            return shared[idx] if 0 <= idx < len(shared) else ''
        elif t == 'str' and v_el is not None:
            return v_el.text or ''
        elif t == 'inlineStr':
            is_el = c.find('main:is', ns)
            if is_el is not None:
                t_el = is_el.find('.//main:t', ns)
                return (t_el.text or '') if t_el is not None else ''
            return ''
        elif t == 'b' and v_el is not None:
            return 'TRUE' if v_el.text == '1' else 'FALSE'
        else:
            return v_el.text if v_el is not None else ''

    os.makedirs(out_dir, exist_ok=True)
    created = []

    for name, path in sheets:
        root = read_xml(zf, path)
        rows = []
        width = 0
        for row in root.findall('.//main:row', ns):
            items = []
            max_ci = -1
            for c in row.findall('main:c', ns):
                r = c.get('r')
                if not r:
                    continue
                ci, ri = col_to_index(r)
                val = get_cell_value(c)
                items.append((ci, val))
                if ci > max_ci:
                    max_ci = ci
            if max_ci >= 0:
                line = [''] * (max_ci + 1)
                for ci, val in items:
                    line[ci] = val
                rows.append(line)
                if len(line) > width:
                    width = len(line)
            else:
                rows.append([])

        rows = [ (r + ['']*(width-len(r))) for r in rows ] if width > 0 else rows

        safe_name = re.sub(r'[\\/:*?"<>|]+', '-', name).strip()
        out_path = os.path.join(out_dir, f"{safe_name}.md")
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write('# ' + name + '\n\n')
            if rows:
                header = rows[0]
                f.write('| ' + ' | '.join([ (h or '').replace('|','\\|') for h in header ]) + ' |\n')
                f.write('| ' + ' | '.join(['---']*len(header)) + ' |\n')
                for r in rows[1:]:
                    f.write('| ' + ' | '.join([ (v or '').replace('|','\\|') for v in r ]) + ' |\n')
            else:
                f.write('> (empty sheet)\n')
        created.append(out_path)

    return created

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: xlsx_to_md.py <xlsx_path> <output_dir>')
        sys.exit(1)
    xlsx_path = sys.argv[1]
    out_dir = sys.argv[2]
    files = convert(xlsx_path, out_dir)
    for p in files:
        print(p)

