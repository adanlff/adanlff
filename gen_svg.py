char_w = 8.1   # Consolas 13.5px ≈ 8.1px per char
dot_step = 7.0  # px per dot in the dotted line

ROWS = [
    ('· OS:',                     'Windows, Linux, shell'),
    ('· Uptime:',                  'fresh graduate'),
    ('· Host:',                    'Telkom University Surabaya'),
    ('· Kernel:',                  'Full-Stack & Front-End Dev'),
    ('· IDE:',                     'VS Code, Figma'),
    None,
    ('· Languages.Programming:',   'TypeScript, JavaScript, Python'),
    ('· Languages.Computer:',      'HTML, CSS, JSON, SQL, Markdown'),
    ('· Languages.Real:',          'Indonesian, English'),
    None,
    ('__SECTION__', 'Contact'),
    ('· Email:',                   'achdany14@gmail.com'),
    ('· Instagram:',               '@adanlff'),
    ('· LinkedIn:',                '/in/achmaddanyalfansyah'),
    ('· Website:',                 'adann.my.id'),
    None,
    ('__SECTION__', 'GitHub Stats'),
    ('· GPA:',                     '3.77 / 4.00 - Informatics'),
    ('· Stack:',                   'Next.js, React, TypeScript'),
]


def make_svg(bg, hc, kc, dc, vc, nc, sc):
    X0 = 20     # left padding
    X1 = 810    # right edge
    DG = 10     # gap between key/dots and dots/value (px)
    RH = 18     # row height (px)

    def xml(s):
        return s.replace('&', '&amp;').replace('<', '&lt;')

    out = []

    def t(x, y, content, color, anchor='start', bold=False):
        w = ' font-weight="bold"' if bold else ''
        a = f' text-anchor="{anchor}"' if anchor != 'start' else ''
        out.append(f'<text x="{x:.1f}" y="{y}"{a}{w} fill="{color}">{xml(content)}</text>')

    def hline(x1, x2, y, color, width=0.7):
        out.append(f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y:.1f}" '
                   f'stroke="{color}" stroke-width="{width}"/>')

    def dots(x1, x2, y, color):
        if x2 - x1 < dot_step:
            return
        out.append(f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y:.1f}" '
                   f'stroke="{color}" stroke-width="1.8" stroke-linecap="round" '
                   f'stroke-dasharray="0.001 {dot_step}"/>')

    def data_row(y, key, val):
        kw = len(key) * char_w
        vw = len(val) * char_w
        d_x1 = X0 + kw + DG
        d_x2 = X1 - vw - DG
        t(X0, y, key, kc)
        dots(d_x1, d_x2, y - 4, dc)
        t(X1, y, val, vc, anchor='end')

    def section_header(y, label):
        # "─ " dim, label normal, then SVG line to right edge
        prefix = '─ '
        t(X0, y, prefix, sc)
        lx = X0 + len(prefix) * char_w
        t(lx, y, label, nc)
        line_x1 = lx + len(label) * char_w + DG
        hline(line_x1, X1, y - 4, sc)

    # Calculate total height
    total_h = 50 + len(ROWS) * RH + 20
    svg_h = max(360, total_h)

    out.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="830" height="{svg_h}" viewBox="0 0 830 {svg_h}">')
    out.append(f'<rect width="830" height="{svg_h}" rx="8" fill="{bg}"/>')
    out.append(f"<g font-family=\"Consolas,'Courier New',monospace\" font-size=\"13.5\">")

    # Header
    t(X0, 28, 'adanlff@github', hc, bold=True)
    header_line_x1 = X0 + len('adanlff@github') * char_w + DG
    hline(header_line_x1, X1, 24, sc)

    y = 50
    for row in ROWS:
        if row is None:
            y += RH  # blank gap
        elif row[0] == '__SECTION__':
            section_header(y, row[1])
            y += RH
        else:
            data_row(y, row[0], row[1])
            y += RH

    out.append('</g></svg>')
    return '\n'.join(out)


dark = make_svg(
    bg='#0d1117', hc='#e6edf3', kc='#ffa657', dc='#3d444d',
    vc='#79c0ff', nc='#c9d1d9', sc='#3d444d',
)
light = make_svg(
    bg='#f6f8fa', hc='#1f2328', kc='#953800', dc='#c2cfde',
    vc='#0a3069', nc='#57606a', sc='#c2cfde',
)

with open('dark_mode.svg', 'w', encoding='utf-8') as f:
    f.write(dark)
with open('light_mode.svg', 'w', encoding='utf-8') as f:
    f.write(light)

print('Done! SVG lines:', dark.count('\n') + 1)

# Verify a sample row
for line in dark.split('\n'):
    if 'OS:' in line and 'text' in line and 'ffa657' in line:
        print('Sample key:', line[:100])
    if 'OS:' in line and 'line' in line:
        print('Sample dot:', line[:100])
