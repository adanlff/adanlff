import base64, os

# ── Font embedding ──────────────────────────────────────────────────────────
def load_font_b64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('ascii')

regular_b64 = load_font_b64('JetBrainsMono-Regular.ttf')
bold_b64    = load_font_b64('JetBrainsMono-Bold.ttf')

FONT_FACE = f"""<style>
  @font-face {{
    font-family: 'JetBrains Mono';
    src: url('data:font/ttf;base64,{regular_b64}') format('truetype');
    font-weight: normal;
  }}
  @font-face {{
    font-family: 'JetBrains Mono';
    src: url('data:font/ttf;base64,{bold_b64}') format('truetype');
    font-weight: bold;
  }}
</style>"""

# ── Config ───────────────────────────────────────────────────────────────────
# JetBrains Mono advance width: 610 units / 1000 em → at 13.5px = 8.235px/char
char_w   = 8.235
dot_step = 7.5   # px per dot in the dotted SVG line
FONT     = "'JetBrains Mono',Consolas,'Courier New',monospace"

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
    X0 = 20    # left padding
    X1 = 810   # right edge
    DG = 10    # gap between key end and dots, and dots end and value
    RH = 18    # row height

    def xml(s):
        return s.replace('&', '&amp;').replace('<', '&lt;')

    out = []

    def t(x, y, content, color, anchor='start', bold=False, size=13.5):
        w  = ' font-weight="bold"' if bold else ''
        a  = f' text-anchor="{anchor}"' if anchor != 'start' else ''
        sz = f' font-size="{size}"' if size != 13.5 else ''
        out.append(
            f'<text x="{x:.1f}" y="{y}"{a}{w}{sz} fill="{color}">{xml(content)}</text>'
        )

    def hline(x1, x2, y, color, width=0.7):
        out.append(
            f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y:.1f}" '
            f'stroke="{color}" stroke-width="{width}"/>'
        )

    def dots(x1, x2, y, color):
        if x2 - x1 < dot_step:
            return
        out.append(
            f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y:.1f}" '
            f'stroke="{color}" stroke-width="1.8" stroke-linecap="round" '
            f'stroke-dasharray="0.001 {dot_step}"/>'
        )

    def data_row(y, key, val):
        kw   = len(key) * char_w
        vw   = len(val) * char_w
        dx1  = X0 + kw + DG
        dx2  = X1 - vw - DG
        t(X0, y, key, kc)
        dots(dx1, dx2, y - 4, dc)
        t(X1, y, val, vc, anchor='end')

    def section_header(y, label):
        prefix    = '─ '
        prefix_w  = len(prefix) * char_w
        label_w   = len(label) * char_w
        line_x1   = X0 + prefix_w + label_w + DG
        t(X0, y, prefix, sc)
        t(X0 + prefix_w, y, label, nc)
        hline(line_x1, X1, y - 4, sc)

    # Calculate SVG height
    svg_h = 50 + sum(RH if r is not None else RH for r in ROWS) + 24

    out.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="830" height="{svg_h}" viewBox="0 0 830 {svg_h}">')
    out.append(FONT_FACE)
    out.append(f'<rect width="830" height="{svg_h}" rx="8" fill="{bg}"/>')
    out.append(f'<g font-family={FONT!r} font-size="13.5">')

    # Header row
    t(X0, 28, 'adanlff@github', hc, bold=True, size=14)
    hline(X0 + len('adanlff@github') * char_w + DG, X1, 24, sc)

    y = 50
    for row in ROWS:
        if row is None:
            y += RH
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

kb = len(dark.encode()) / 1024
print(f'Done! dark_mode.svg: {kb:.1f} KB')
print(f'      light_mode.svg: {len(light.encode())/1024:.1f} KB')
