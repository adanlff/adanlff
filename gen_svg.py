def make_svg(bg, hc, kc, dc, vc, nc, sc, rx):
    rows_data = [
        ('OS',          'Windows, Linux, shell'),
        ('Uptime',      'fresh graduate'),
        ('Host',        'Telkom University Surabaya'),
        ('Kernel',      'Full-Stack & Front-End Dev'),
        ('IDE',         'VS Code, Figma'),
        None,
        ('Languages.Programming', 'TypeScript, JavaScript, Python'),
        ('Languages.Computer',    'HTML, CSS, JSON, SQL, Markdown'),
        ('Languages.Real',        'Indonesian, English'),
        ('__CONTACT__',),
        ('Email',       'achdany14@gmail.com'),
        ('Instagram',   '@adanlff'),
        ('LinkedIn',    '/in/achmaddanyalfansyah'),
        ('Website',     'adann.my.id'),
        ('__STATS__',),
        ('GPA',         '3.77 / 4.00 - Informatics'),
        ('Stack',       'Next.js, React, TypeScript'),
    ]

    def xml_escape(s):
        return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="830" height="360" viewBox="0 0 830 360">')
    lines.append(f'<rect width="830" height="360" rx="{rx}" fill="{bg}"/>')
    lines.append(f"<g font-family=\"Consolas,'Courier New',monospace\" font-size=\"13.5\">")

    # Header
    head_txt = 'adanlff@github '   # 15 chars
    head_dashes = '\u2500' * 81     # U+2500 BOX DRAWINGS LIGHT HORIZONTAL, 81 chars -> total 96
    lines.append(f'<text x="20" y="28" xml:space="preserve" font-weight="bold"><tspan fill="{hc}">{head_txt}</tspan><tspan fill="{sc}" font-weight="normal">{head_dashes}</tspan></text>')

    y = 50
    for r in rows_data:
        if r is None:
            y += 18  # blank gap line
            continue
        if r[0] == '__CONTACT__':
            label = 'Contact'
            dashes = '\u2500' * (93 - len(label))  # 2('- ') + len(label) + 1(' ') + dashes = 96
            lines.append(f'<text x="20" y="{y}" xml:space="preserve"><tspan fill="{sc}">\u2500 </tspan><tspan fill="{nc}">{label}</tspan><tspan fill="{sc}"> {dashes}</tspan></text>')
            y += 18
            continue
        if r[0] == '__STATS__':
            label = 'GitHub Stats'
            dashes = '\u2500' * (93 - len(label))
            lines.append(f'<text x="20" y="{y}" xml:space="preserve"><tspan fill="{sc}">\u2500 </tspan><tspan fill="{nc}">{label}</tspan><tspan fill="{sc}"> {dashes}</tspan></text>')
            y += 18
            continue

        key_raw, val_raw = r
        # Format key: "· key_raw:" left-padded to 25 chars
        key_label = f'\u00b7 {key_raw}:'   # middle dot + space + key + colon
        key_field = key_label.ljust(25)
        dots_field = '.' * 35
        val_field = xml_escape(val_raw).rjust(36)

        assert len(key_field) == 25, f"key_field len={len(key_field)} for {key_raw!r}"
        assert len(dots_field) == 35
        # val_field may have extra chars from xml escaping but visual length should be 36
        
        # For the tspan text: key in orange, dots in dim, val in blue
        line = f'<text x="20" y="{y}" xml:space="preserve"><tspan fill="{kc}">{key_field}</tspan><tspan fill="{dc}">{dots_field}</tspan><tspan fill="{vc}">{val_field}</tspan></text>'
        lines.append(line)
        y += 18

    lines.append('</g></svg>')
    return '\n'.join(lines)

dark = make_svg(
    bg='#0d1117', hc='#e6edf3', kc='#ffa657', dc='#3d444d',
    vc='#79c0ff', nc='#c9d1d9', sc='#3d444d', rx=8
)
light = make_svg(
    bg='#f6f8fa', hc='#1f2328', kc='#953800', dc='#bec8d1',
    vc='#0a3069', nc='#57606a', sc='#bec8d1', rx=8
)

with open('dark_mode.svg', 'w', encoding='utf-8') as f:
    f.write(dark)
with open('light_mode.svg', 'w', encoding='utf-8') as f:
    f.write(light)

print('Done!')
print(f'Total rows in dark SVG: {dark.count(chr(10))+1}')
# Spot-check one row
for line in dark.split('\n'):
    if 'OS:' in line and 'tspan' in line:
        print('OS row preview:', line[:160])
        break
