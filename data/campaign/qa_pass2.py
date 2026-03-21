import json, glob, re, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pattern = re.compile(r'\$[a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*')
total_entries = 0
total_vars = 0
missing_list = []
added_list = []

for src in sorted(glob.glob('batch_*.json')):
    trfile = src.replace('batch_', 'tr_')
    if not os.path.exists(trfile):
        print(f'MISSING FILE: {trfile}')
        continue
    source = json.load(open(src, encoding='utf-8'))
    trans = json.load(open(trfile, encoding='utf-8'))
    src_dict = {e[0]: e[1] for e in source}
    tr_dict = {e[0]: e[1] for e in trans}
    for ln, txt in src_dict.items():
        total_entries += 1
        sv = set(pattern.findall(str(txt)))
        total_vars += len(sv)
        if ln not in tr_dict:
            missing_list.append(f'{trfile} line {ln}: MISSING ENTRY')
            continue
        tv = set(pattern.findall(str(tr_dict[ln])))
        for v in sv - tv:
            missing_list.append(f'{trfile} line {ln}: MISSING {v}')
        for v in tv - sv:
            added_list.append(f'{trfile} line {ln}: ADDED {v}')

print(f'Entries checked: {total_entries}')
print(f'Variables found: {total_vars}')
print(f'Missing variables: {len(missing_list)}')
print(f'Added variables: {len(added_list)}')
for e in missing_list[:100]:
    print(f'  {e}')
if len(missing_list) > 100:
    print(f'  ... and {len(missing_list)-100} more')
print('---')
for e in added_list[:30]:
    print(f'  {e}')
