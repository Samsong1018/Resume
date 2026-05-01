from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import KeepTogether
from reportlab.lib.colors import HexColor
import io

# ── Colors ──────────────────────────────────────────────────────────────────
DARK     = HexColor('#141418')
PINK     = HexColor('#c73869')
PINK_LT  = HexColor('#ff4d8d')
TEXT     = HexColor('#1a1a2a')
MUTED    = HexColor('#555566')
BORDER   = HexColor('#ccccdd')
TAG_BG   = HexColor('#f0f0f5')
BLUE     = HexColor('#2a4a99')
GREEN    = HexColor('#007a4a')

W, H = letter
MARGIN_X = 0.55 * inch
MARGIN_Y = 0.5 * inch
COL_GAP  = 0.2 * inch
LEFT_W   = 3.8 * inch
RIGHT_W  = W - 2 * MARGIN_X - COL_GAP - LEFT_W

# ── Style helpers ────────────────────────────────────────────────────────────
def style(name, **kw):
    base = ParagraphStyle(name, fontName='Helvetica', fontSize=9,
                          leading=12, textColor=TEXT, spaceAfter=0, spaceBefore=0)
    for k, v in kw.items():
        setattr(base, k, v)
    return base

S_NAME     = style('name', fontName='Helvetica-Bold', fontSize=22, textColor=colors.white, leading=26)
S_TITLE    = style('title', fontSize=10, textColor=HexColor('#ffb3cc'), leading=13)
S_CONTACT  = style('contact', fontSize=7.5, textColor=HexColor('#ddddee'), leading=11)
S_SECTION  = style('section', fontName='Helvetica-Bold', fontSize=7, textColor=PINK,
                   leading=10, spaceAfter=3, spaceBefore=0)
S_JOB      = style('job', fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=TEXT)
S_SUB      = style('sub', fontSize=8, textColor=PINK, leading=11, fontName='Helvetica-Oblique')
S_BODY     = style('body', fontSize=8, textColor=MUTED, leading=11.5)
S_BULLET   = style('bullet', fontSize=8, textColor=MUTED, leading=11.5, leftIndent=8,
                   firstLineIndent=-6)
S_TAG_WRAP = style('tag_wrap', fontSize=7.5, leading=11, textColor=MUTED)

def section_header(title):
    return [
        Paragraph(title.upper(), S_SECTION),
        HRFlowable(width='100%', thickness=0.5, color=PINK, spaceAfter=4),
    ]

def tag_line(tags):
    return Paragraph(
        '  '.join(f'<font color="#888899">[</font><font color="#444466">{t}</font><font color="#888899">]</font>' for t in tags),
        S_TAG_WRAP
    )

def divider(space=4):
    return Spacer(1, space)


# ── Build document ───────────────────────────────────────────────────────────
buf = io.BytesIO()
doc = SimpleDocTemplate(
    buf,
    pagesize=letter,
    leftMargin=MARGIN_X, rightMargin=MARGIN_X,
    topMargin=0, bottomMargin=MARGIN_Y
)

story = []

# ─── HEADER ────────────────────────────────────────────────────────────────
def build_header(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(DARK)
    canvas.rect(0, H - 1.15 * inch, W, 1.15 * inch, fill=1, stroke=0)

    canvas.setFillColor(colors.white)
    canvas.setFont('Helvetica-Bold', 22)
    canvas.drawString(MARGIN_X, H - 0.5 * inch, 'Amos Horne')

    canvas.setFillColor(HexColor('#ffb3cc'))
    canvas.setFont('Helvetica', 10)
    canvas.drawString(MARGIN_X, H - 0.72 * inch, 'Cybersecurity & Development')

    # contact line right-aligned
    contact = '425-419-8720  ·  amoshorne@gmail.com  ·  github.com/Samsong1018  ·  linkedin.com/in/amos-horne-25b4693a6'
    canvas.setFillColor(HexColor('#ccccdd'))
    canvas.setFont('Helvetica', 7.5)
    canvas.drawRightString(W - MARGIN_X, H - 0.72 * inch, contact)

    canvas.setFillColor(PINK)
    canvas.rect(MARGIN_X, H - 1.12 * inch, 1.4 * inch, 2, fill=1, stroke=0)

    canvas.restoreState()

# ─── LEFT COLUMN content ────────────────────────────────────────────────────
left = []

# Summary
left += section_header('Summary')
left.append(Paragraph(
    'Aspiring cybersecurity professional and fullstack developer graduating Jun 2026 with an '
    'Associate of Arts and Sciences from Bellevue College. Self-taught across web development, '
    'systems administration, and security tooling — with hands-on experience deploying '
    'infrastructure, building CLI tools, and training AI models on local hardware.',
    S_BODY))
left.append(divider(8))

# Projects
left += section_header('Projects')

projects = [
    ('AMvpn — WireGuard VPN',
     'Self-hosted WireGuard VPN on Oracle Cloud. Replaced commercial VPN with full infrastructure '
     'control, custom tunneling, and multi-device support managed from the command line.',
     ['WireGuard', 'Oracle Cloud', 'Linux', 'Networking']),
    ('WTFlag',
     'CLI shell command explainer built as a Claude Code hook integration. Intercepts bash '
     'commands pre-execution and returns plain-English explanations from a local SQLite-indexed '
     'tldr-pages database — no API calls, instant offline lookups.',
     ['Node.js', 'SQLite', 'CLI', 'Shell Hooks']),
    ('TodoLander',
     'Fullstack web application with user authentication and personalized data persistence. '
     'Users register, log in, and manage private todo lists stored in PostgreSQL.',
     ['Express.js', 'PostgreSQL', 'Node.js', 'Auth']),
    ('Somab — Voice AI Workstation',
     'Dedicated ThinkPad AI workstation for training custom Piper TTS voices using GPU '
     'acceleration. Runs local LLM inference via Ollama with a custom-trained voice model.',
     ['Python', 'Piper TTS', 'Ollama', 'Linux', 'AI/ML']),
    ('Bumper the Band',
     'Frontend website for my band — designed and built from scratch, a real-world client '
     'project where I was both developer and client.',
     ['HTML', 'CSS', 'JavaScript']),
    ('Raspberry Pi Server',
     'Minecraft server on Raspberry Pi using tunneling over port forwarding — a deliberate '
     'security decision to avoid home-network attack vectors.',
     ['Linux', 'Networking', 'Tunneling', 'Raspberry Pi']),
]

for i, (title, desc, tags) in enumerate(projects):
    left.append(Paragraph(title, S_JOB))
    left.append(Paragraph(desc, S_BODY))
    left.append(tag_line(tags))
    if i < len(projects) - 1:
        left.append(divider(5))

left.append(divider(8))

# Education
left += section_header('Education')

edu = [
    ('Associate of Arts and Sciences', 'Bellevue College — Running Start Program',
     'Graduating Jun 2026  ·  Dual-enrollment through Cedarcrest High School Running Start'),
    ('High School Diploma', 'Cedarcrest High School — Running Start Program',
     'Graduating Jun 2026  ·  Concurrent enrollment at Bellevue College'),
]

for i, (deg, school, detail) in enumerate(edu):
    left.append(Paragraph(deg, S_JOB))
    left.append(Paragraph(school, S_SUB))
    left.append(Paragraph(detail, S_BODY))
    if i < len(edu) - 1:
        left.append(divider(4))

# ─── RIGHT COLUMN content ────────────────────────────────────────────────────
right = []

# Skills
right += section_header('Skills')

skill_groups = [
    ('Languages',        ['JavaScript', 'Python', 'HTML', 'CSS', 'SQL']),
    ('Security Tools',   ['nmap', 'Burp Suite', 'Gobuster', 'Metasploit', 'John the Ripper', 'Wireshark']),
    ('Systems & Infra',  ['Linux (Ubuntu)', 'WireGuard', 'Docker', 'Oracle Cloud', 'Self-hosting']),
    ('Web & Backend',    ['Express.js', 'PostgreSQL', 'Node.js', 'REST APIs', 'Auth / Sessions']),
    ('Dev Tools',        ['Git', 'GitHub', 'VS Code', 'SQLite', 'Postman']),
]

for group, tags in skill_groups:
    right.append(Paragraph(f'<font color="#c73869"><b>{group}</b></font>', S_BODY))
    right.append(tag_line(tags))
    right.append(divider(4))

right.append(divider(4))

# Certifications
right += section_header('Certifications')

certs = [
    ('ISC² Certified in Cybersecurity (CC)',
     'Course Complete — Exam Pending',
     BLUE,
     'All 5 domains complete. Sitting the exam soon.'),
    ('Cisco — Introduction to Cybersecurity',
     'Completed',
     GREEN,
     'Threats, defenses, data protection, incident response.'),
    ('TryHackMe — Pre-Security Path',
     'Completed',
     GREEN,
     'Networking, Linux CLI, web fundamentals, hands-on labs.'),
]

for i, (name, status, status_color, note) in enumerate(certs):
    right.append(Paragraph(f'<b>{name}</b>', S_BODY))
    right.append(Paragraph(
        f'<font color="#{status_color.hexval()[2:].upper()}">{status}</font>',
        S_BODY))
    right.append(Paragraph(note, S_BODY))
    if i < len(certs) - 1:
        right.append(divider(5))

right.append(divider(8))

# Currently studying
right += section_header('Currently Studying')
studying = [
    'ISC² CC exam preparation',
    'TryHackMe SOC Level 1 path',
    'Network Security (Domain 4 applied)',
]
for item in studying:
    right.append(Paragraph(f'▸  {item}', S_BODY))
    right.append(divider(2))

# ─── Two-column table ────────────────────────────────────────────────────────
col_data = [[left, right]]
col_table = Table(col_data, colWidths=[LEFT_W, RIGHT_W])
col_table.setStyle(TableStyle([
    ('VALIGN',      (0, 0), (-1, -1), 'TOP'),
    ('LEFTPADDING', (0, 0), (-1, -1), 0),
    ('RIGHTPADDING',(0, 0), (-1, -1), 0),
    ('TOPPADDING',  (0, 0), (-1, -1), 0),
    ('BOTTOMPADDING',(0,0), (-1, -1), 0),
    ('COLUMNPADDING',(0,0), (0, -1), 0),
    ('RIGHTPADDING',(0, 0), (0, -1), COL_GAP),
]))

story.append(Spacer(1, 1.25 * inch))  # header clearance
story.append(col_table)

doc.build(story, onFirstPage=build_header, onLaterPages=build_header)

with open('Amos_Horne_Resume.pdf', 'wb') as f:
    f.write(buf.getvalue())

print('PDF generated: Amos_Horne_Resume.pdf')
