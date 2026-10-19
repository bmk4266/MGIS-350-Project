# Optional documentation tool only. Application does not import ReportLab.
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / 'docs'


def footer(canvas, document):
    canvas.setFont('Helvetica', 9)
    canvas.setFillColor(colors.HexColor('#556070'))
    canvas.drawString(48, 28, 'Threads & Trends | Team 13 | MGIS 350')
    canvas.drawRightString(564, 28, f'Page {document.page}')


def main():
    output = DOCS / 'Threads_and_Trends_User_Manual.pdf'
    output.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    styles['Title'].textColor = colors.HexColor('#17464b')
    styles['Title'].alignment = TA_LEFT
    styles['Heading2'].textColor = colors.HexColor('#17464b')
    styles['BodyText'].fontSize = 10.5
    styles['BodyText'].leading = 15
    story = []
    paragraph = []
    for line in (DOCS / 'MANUAL.md').read_text(encoding='utf-8').splitlines() + ['']:
        if not line or line.startswith('#'):
            if paragraph:
                story.append(Paragraph(escape(' '.join(paragraph)), styles['BodyText']))
                story.append(Spacer(1, 8))
                paragraph = []
            if line.startswith('## '):
                story.append(Paragraph(escape(line[3:]), styles['Heading2']))
            elif line.startswith('# '):
                story.append(Paragraph(escape(line[2:]), styles['Title']))
        else:
            paragraph.append(line)
    document = SimpleDocTemplate(str(output), pagesize=(612, 792),
                                 leftMargin=48, rightMargin=48,
                                 topMargin=40, bottomMargin=48)
    document.build(story, onFirstPage=footer, onLaterPages=footer)
    print(output)


if __name__ == '__main__':
    main()
