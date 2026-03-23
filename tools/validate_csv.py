import csv, sys

base = 'D:/Fractal Softworks/Starsector/mods/starsector_lang_pack_fr_private/.claude/worktrees/objective-bartik/data/campaign'
errors = []

for fname in ['commodities.csv', 'special_items.csv']:
    path = base + '/' + fname
    print(f'=== {fname} ===')

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if chr(8217) in content:
        errors.append(f'{fname}: typographic apostrophe U+2019 found!')
        print('ERROR: typographic apostrophe found!')
    else:
        print('OK: No typographic apostrophes')

    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        expected = len(header)
        print(f'Columns: {expected}')
        rows = list(reader)

    bad = []
    for i, r in enumerate(rows):
        if len(r) != expected:
            bad.append((i + 2, len(r)))

    data = sum(1 for r in rows if r[0] and not r[0].startswith('#'))
    empty = sum(1 for r in rows if not r[0])
    comments = sum(1 for r in rows if r[0] and r[0].startswith('#'))

    print(f'Data: {data}, Empty: {empty}, Comments: {comments}')

    if bad:
        errors.append(f'{fname}: column mismatch at lines {bad}')
        print(f'COLUMN ERRORS: {bad}')
    else:
        print('OK: All rows match header count')
    print()

if errors:
    print(f'FAILED ({len(errors)} errors):')
    for e in errors:
        print(f'  - {e}')
    sys.exit(1)
else:
    print('ALL VALIDATIONS PASSED')
