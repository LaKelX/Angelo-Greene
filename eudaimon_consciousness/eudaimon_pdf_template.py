"""
EUDAIMON PDF TEMPLATE
=====================
Official PDF generator for Eudaimon Capitol / Eudaimon AI documents.

Brand Standards:
- Logo: Eudaimon_Logo_V1_Final_Single.PNG (same as website)
- Logo sizing: height-constrained, width auto (preserves aspect ratio)
- Colors: Warm Charcoal #2A2622, Accent Gold #C9A961, Deep Navy #1A2332
- Typography: Clean, professional (Helvetica in PDF)

Usage:
    from eudaimon_pdf_template import EudaimonPDF

    pdf = EudaimonPDF("My Report Title", "Subtitle here")
    pdf.add_section("Section Title")
    pdf.add_body("Body text here...")
    pdf.add_table(data, col_widths)
    pdf.save("output.pdf")
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, HRFlowable
from PIL import Image as PILImage
import os

# ========== EUDAIMON BRAND COLORS ==========
WARM_CHARCOAL = colors.HexColor('#2A2622')    # Primary text
MEDIUM_CHARCOAL = colors.HexColor('#3D3935')  # Secondary text
TERTIARY_TEXT = colors.HexColor('#5A5550')    # Tertiary
ACCENT_GOLD = colors.HexColor('#C9A961')      # Gold accent
WARM_IVORY = colors.HexColor('#F7F6ED')       # Background
DEEP_NAVY = colors.HexColor('#1A2332')        # Dark sections
WHITE = colors.white

# Logo path - the single logo file (same as website)
LOGO_PATH = os.path.join(os.path.dirname(__file__), 'Eudaimon_Logo_V1_Final_Single.PNG')


def get_logo_dimensions(target_height_inches):
    """
    Calculate logo dimensions preserving aspect ratio.
    Same approach as website: height fixed, width auto.
    """
    if not os.path.exists(LOGO_PATH):
        return None, None

    with PILImage.open(LOGO_PATH) as img:
        orig_width, orig_height = img.size
        aspect_ratio = orig_width / orig_height

        height = target_height_inches * inch
        width = height * aspect_ratio

        return width, height


def create_styles():
    """Create all paragraph styles for Eudaimon PDFs."""
    styles = getSampleStyleSheet()

    # Title styles
    styles.add(ParagraphStyle(name='MainTitle', fontSize=28, textColor=WARM_CHARCOAL, alignment=TA_CENTER,
                               spaceAfter=8, fontName='Helvetica-Bold', leading=34))
    styles.add(ParagraphStyle(name='Subtitle', fontSize=12, textColor=TERTIARY_TEXT, alignment=TA_CENTER,
                               spaceAfter=6, leading=16))
    styles.add(ParagraphStyle(name='DateLine', fontSize=10, textColor=TERTIARY_TEXT, alignment=TA_CENTER,
                               spaceAfter=20, leading=14))

    # Section headers
    styles.add(ParagraphStyle(name='Section', fontSize=18, textColor=WARM_CHARCOAL, spaceBefore=18,
                               spaceAfter=10, fontName='Helvetica-Bold', leading=24))
    styles.add(ParagraphStyle(name='SubSection', fontSize=13, textColor=MEDIUM_CHARCOAL, spaceBefore=12,
                               spaceAfter=8, fontName='Helvetica-Bold', leading=18))

    # Body text
    styles.add(ParagraphStyle(name='Body', fontSize=10, textColor=MEDIUM_CHARCOAL, spaceBefore=6,
                               spaceAfter=6, leading=15))
    styles.add(ParagraphStyle(name='BodyJustify', fontSize=10, textColor=MEDIUM_CHARCOAL, spaceBefore=6,
                               spaceAfter=6, leading=15, alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='BulletItem', fontSize=10, textColor=MEDIUM_CHARCOAL, leftIndent=15,
                               spaceBefore=4, spaceAfter=4, leading=15))

    # Special styles
    styles.add(ParagraphStyle(name='Quote', fontSize=12, textColor=WARM_CHARCOAL, alignment=TA_CENTER,
                               spaceBefore=12, spaceAfter=12, fontName='Helvetica-Oblique', leading=18))
    styles.add(ParagraphStyle(name='Highlight', fontSize=11, textColor=ACCENT_GOLD, alignment=TA_CENTER,
                               spaceBefore=8, spaceAfter=8, fontName='Helvetica-Bold', leading=16))
    styles.add(ParagraphStyle(name='GoldTitle', fontSize=13, textColor=ACCENT_GOLD, spaceBefore=14,
                               spaceAfter=6, fontName='Helvetica-Bold', leading=18))
    styles.add(ParagraphStyle(name='NavyTitle', fontSize=13, textColor=DEEP_NAVY, spaceBefore=10,
                               spaceAfter=6, fontName='Helvetica-Bold', leading=18))
    styles.add(ParagraphStyle(name='Insight', fontSize=10, textColor=WARM_CHARCOAL, spaceBefore=6,
                               spaceAfter=6, leftIndent=12, fontName='Helvetica-Oblique', leading=15))
    styles.add(ParagraphStyle(name='BigIdea', fontSize=16, textColor=WARM_CHARCOAL, alignment=TA_CENTER,
                               spaceBefore=14, spaceAfter=14, fontName='Helvetica-Bold', leading=22))

    # Header/Footer
    styles.add(ParagraphStyle(name='Header', fontSize=10, textColor=WARM_CHARCOAL, leading=14))
    styles.add(ParagraphStyle(name='HeaderRight', fontSize=9, textColor=TERTIARY_TEXT, alignment=TA_RIGHT, leading=12))
    styles.add(ParagraphStyle(name='Footer', fontSize=8, textColor=TERTIARY_TEXT, alignment=TA_CENTER, leading=12))

    # Cell styles for tables
    styles.add(ParagraphStyle(name='CellHeader', fontSize=9, textColor=WHITE,
                               fontName='Helvetica-Bold', leading=13))
    styles.add(ParagraphStyle(name='CellHeaderDark', fontSize=9, textColor=WARM_CHARCOAL,
                               fontName='Helvetica-Bold', leading=13))
    styles.add(ParagraphStyle(name='Cell', fontSize=9, textColor=MEDIUM_CHARCOAL, leading=13))
    styles.add(ParagraphStyle(name='CellBold', fontSize=9, textColor=WARM_CHARCOAL,
                               fontName='Helvetica-Bold', leading=13))

    return styles


def table_style_navy():
    """Navy header table style."""
    return TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DEEP_NAVY),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
        ('BACKGROUND', (0, 1), (-1, -1), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, WARM_IVORY]),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ])


def table_style_gold():
    """Gold header table style."""
    return TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), ACCENT_GOLD),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
        ('BACKGROUND', (0, 1), (-1, -1), WHITE),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ])


def gold_line():
    """Create a gold accent line - the Eudaimon signature element."""
    return HRFlowable(width="100%", thickness=2, color=ACCENT_GOLD, spaceBefore=6, spaceAfter=6)


def create_header(styles, date_str="", doc_type=""):
    """
    Create the standard Eudaimon header with logo.
    Logo is height-constrained to 0.5 inches, width auto (preserves aspect ratio).
    """
    elements = []

    logo_width, logo_height = get_logo_dimensions(0.5)  # 0.5 inch height, same as website nav (40px ≈ 0.5in)

    if logo_width and logo_height and os.path.exists(LOGO_PATH):
        logo = Image(LOGO_PATH, width=logo_width, height=logo_height)
        header_data = [[
            logo,
            Paragraph("EUDAIMON CAPITOL<br/><font size=9 color='#5A5550'>Investment Management</font>", styles['Header']),
            Paragraph(f"{date_str}<br/><font size=8>{doc_type}</font>", styles['HeaderRight'])
        ]]
        header_table = Table(header_data, colWidths=[logo_width + 0.2*inch, 3.5*inch, 2.5*inch])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
        ]))
        elements.append(header_table)

    elements.append(gold_line())
    elements.append(Spacer(1, 0.15*inch))

    return elements


class EudaimonPDF:
    """
    Eudaimon PDF Generator class.

    Usage:
        pdf = EudaimonPDF("Report Title", "Subtitle")
        pdf.add_section("Section 1")
        pdf.add_body("Content here...")
        pdf.save("output.pdf")
    """

    def __init__(self, title, subtitle="", date_str="", doc_type="Research Report"):
        self.title = title
        self.subtitle = subtitle
        self.date_str = date_str or "January 2026"
        self.doc_type = doc_type
        self.styles = create_styles()
        self.story = []

        # Add header
        self.story.extend(create_header(self.styles, self.date_str, self.doc_type))

        # Add title
        self.story.append(Paragraph(self.title, self.styles['MainTitle']))
        if self.subtitle:
            self.story.append(Paragraph(self.subtitle, self.styles['Subtitle']))
        self.story.append(Spacer(1, 0.1*inch))

    def add_section(self, title):
        """Add a section header with gold line."""
        self.story.append(Paragraph(title, self.styles['Section']))
        self.story.append(gold_line())

    def add_subsection(self, title):
        """Add a subsection header."""
        self.story.append(Paragraph(title, self.styles['SubSection']))

    def add_body(self, text, justify=True):
        """Add body text."""
        style = self.styles['BodyJustify'] if justify else self.styles['Body']
        self.story.append(Paragraph(text, style))

    def add_bullet(self, text):
        """Add a bullet point."""
        self.story.append(Paragraph(f"• {text}", self.styles['BulletItem']))

    def add_quote(self, text):
        """Add a centered quote."""
        self.story.append(Paragraph(f'"{text}"', self.styles['Quote']))

    def add_highlight(self, text):
        """Add highlighted gold text."""
        self.story.append(Paragraph(text, self.styles['Highlight']))

    def add_table(self, data, col_widths, style='navy'):
        """
        Add a table with proper cell formatting.

        Args:
            data: List of rows, each row is a list of cell contents
            col_widths: List of column widths in inches
            style: 'navy' or 'gold'
        """
        # Helper functions for cells
        def h(text):
            return Paragraph(text, self.styles['CellHeader'])
        def hd(text):
            return Paragraph(text, self.styles['CellHeaderDark'])
        def c(text):
            return Paragraph(text, self.styles['Cell'])
        def cb(text):
            return Paragraph(text, self.styles['CellBold'])

        # Convert data to Paragraph objects
        formatted_data = []
        for i, row in enumerate(data):
            formatted_row = []
            for j, cell in enumerate(row):
                if i == 0:  # Header row
                    if style == 'navy':
                        formatted_row.append(h(str(cell)))
                    else:
                        formatted_row.append(hd(str(cell)))
                elif j == 0:  # First column (usually bold)
                    formatted_row.append(cb(str(cell)))
                else:
                    formatted_row.append(c(str(cell)))
            formatted_data.append(formatted_row)

        widths = [w * inch for w in col_widths]
        table = Table(formatted_data, colWidths=widths)
        table.setStyle(table_style_navy() if style == 'navy' else table_style_gold())
        self.story.append(table)

    def add_spacer(self, height=0.1):
        """Add vertical space."""
        self.story.append(Spacer(1, height * inch))

    def add_page_break(self):
        """Add a page break."""
        self.story.append(PageBreak())

    def add_gold_line(self):
        """Add a gold accent line."""
        self.story.append(gold_line())

    def add_footer(self):
        """Add the standard Eudaimon footer."""
        self.story.append(Spacer(1, 0.2*inch))
        self.story.append(gold_line())
        self.story.append(Paragraph("EUDAIMON CAPITOL | Research", self.styles['Body']))
        self.story.append(Paragraph(self.date_str, self.styles['DateLine']))
        self.story.append(Paragraph("Confidential & Proprietary", self.styles['Footer']))

    def save(self, output_path):
        """Build and save the PDF."""
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            leftMargin=0.75*inch,
            rightMargin=0.75*inch,
            topMargin=0.6*inch,
            bottomMargin=0.6*inch
        )
        doc.build(self.story)
        print(f"PDF generated: {output_path}")
        return output_path


# Convenience function for quick PDF generation
def generate_eudaimon_pdf(title, subtitle, content_func, output_path, date_str="", doc_type="Research Report"):
    """
    Generate a PDF using the Eudaimon template.

    Args:
        title: Document title
        subtitle: Document subtitle
        content_func: Function that takes an EudaimonPDF instance and adds content
        output_path: Where to save the PDF
        date_str: Date string (e.g., "January 26, 2026")
        doc_type: Document type (e.g., "Deep Connections Research")
    """
    pdf = EudaimonPDF(title, subtitle, date_str, doc_type)
    content_func(pdf)
    pdf.add_footer()
    return pdf.save(output_path)
