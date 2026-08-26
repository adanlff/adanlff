import base64

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

char_w   = 8.235
dot_step = 7.5
FONT     = "'JetBrains Mono',Consolas,'Courier New',monospace"

ROWS = [
    ('· Role:',                    'Full-Stack & Front-End Developer'),
    ('· Location:',                'Sidoarjo, East Java, Indonesia'),
    ('· Education:',               'B.Sc. Informatics — Telkom University'),
    ('· GPA:',                     '3.77 / 4.00 (Fresh Graduate)'),
    ('· IDE & Tools:',             'VS Code, Figma, Git, Vercel'),
    None,
    ('__SECTION__', 'Tech Stack'),
    ('· Languages.Code:',          'TypeScript, JavaScript, PHP, Python'),
    ('· Languages.Web:',           'HTML5, CSS3, SQL, JSON, Markdown'),
    ('· Frameworks:',              'Next.js, React.js, Vue.js, Astro, Laravel'),
    ('· UI & Motion:',             'Tailwind CSS, Shadcn UI, Framer Motion, GSAP'),
    ('· Database & BaaS:',         'PostgreSQL, MySQL, SQLite, Prisma, Supabase'),
    None,
    ('__SECTION__', 'Experience & Projects'),
    ('· Work Experience:',         'CoE MOSHEE (Intern) · MIN 1 Sidoarjo'),
    ('· Featured Projects:',       'MagangHab Tracker, BISINDO Detection'),
    ('· UI/UX Focus:',             'Clean UI · Micro-Interactions · Accessibility'),
    None,
    ('__SECTION__', 'Contact'),
    ('· Email:',                   'achdany14@gmail.com'),
    ('· Portfolio:',               'adann.my.id'),
    ('· LinkedIn:',                '/in/achmaddanyalfansyah'),
    ('· Instagram:',               '@adanlff'),
]


def make_svg(bg, hc, kc, dc, vc, nc, sc):
    X0 = 20
    X1 = 810
    DG = 10
    RH = 18

    def xml(s):
        return s.replace('&', '&amp;').replace('<', '&lt;')

    out = []

    def t(x, y, content, color, anchor='start', bold=False, size=13.5):
        w  = ' font-weight="bold"' if bold else ''
        a  = f' text-anchor="{anchor}"' if anchor != 'start' else ''
        sz = f' font-size="{size}"' if size != 13.5 else ''
        out.append(f'<text x="{x:.1f}" y="{y}"{a}{w}{sz} fill="{color}">{xml(content)}</text>')

    def hline(x1, x2, y, color, width=0.7):
        out.append(f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y:.1f}" stroke="{color}" stroke-width="{width}"/>')

    def dots(x1, x2, y, color):
        if x2 - x1 < dot_step:
            return
        out.append(f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y:.1f}" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-dasharray="0.001 {dot_step}"/>')

    def data_row(y, key, val):
        dx1 = X0 + len(key) * char_w + DG
        dx2 = X1 - len(val) * char_w - DG
        t(X0, y, key, kc)
        dots(dx1, dx2, y - 4, dc)
        t(X1, y, val, vc, anchor='end')

    def section_header(y, label):
        prefix   = '─ '
        prefix_w = len(prefix) * char_w
        line_x1  = X0 + prefix_w + len(label) * char_w + DG
        t(X0, y, prefix, sc)
        t(X0 + prefix_w, y, label, nc)
        hline(line_x1, X1, y - 4, sc)

    svg_h = 50 + len(ROWS) * RH + 24

    out.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="830" height="{svg_h}" viewBox="0 0 830 {svg_h}">')
    out.append(FONT_FACE)
    out.append(f'<rect width="830" height="{svg_h}" rx="8" fill="{bg}" stroke="{sc}" stroke-width="1.5"/>')
    out.append(f'<g font-family={FONT!r} font-size="13.5">')

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
    bg='#1c2128',
    hc='#e6edf3', kc='#ffa657', dc='#484f58',
    vc='#79c0ff', nc='#c9d1d9', sc='#30363d',
)
light = make_svg(
    bg='#f0f6ff',
    hc='#1f2328', kc='#953800', dc='#b9c5d0',
    vc='#0a3069', nc='#57606a', sc='#c2cfde',
)

with open('dark.svg', 'w', encoding='utf-8') as f:
    f.write(dark)
with open('light.svg', 'w', encoding='utf-8') as f:
    f.write(light)

print(f'dark.svg:  {len(dark.encode())/1024:.1f} KB')
print(f'light.svg: {len(light.encode())/1024:.1f} KB')
