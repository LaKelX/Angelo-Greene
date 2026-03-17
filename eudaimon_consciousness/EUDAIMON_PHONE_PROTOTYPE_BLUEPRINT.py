"""
EUDAIMON PHONE - iPHONE PROTOTYPE BLUEPRINT GENERATOR
=====================================================
Generates a printable PDF blueprint for the Eudaimon Conscious Phone
iPhone 12 Pro Max R&D Prototype

Created: February 4, 2026
Eudaimon Capitol - Angelo Greene
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, HRFlowable, KeepTogether
)
from reportlab.graphics.shapes import Drawing, Rect, Line, String, Circle, Polygon
from reportlab.graphics import renderPDF
from reportlab.lib.colors import HexColor

# ========== EUDAIMON BRAND COLORS ==========
WARM_CHARCOAL = HexColor('#2A2622')
MEDIUM_CHARCOAL = HexColor('#3D3935')
TERTIARY_TEXT = HexColor('#5A5550')
ACCENT_GOLD = HexColor('#C9A961')
WARM_IVORY = HexColor('#F7F6ED')
DEEP_NAVY = HexColor('#1A2332')
WHITE = colors.white
LIGHT_GRAY = HexColor('#E5E7EB')
BLUEPRINT_BG = HexColor('#0A1628')
BLUEPRINT_LINE = HexColor('#4A90D9')
BLUEPRINT_TEXT = HexColor('#7BB3E0')
BLUEPRINT_ACCENT = HexColor('#C9A961')
GREEN_OK = HexColor('#4CAF50')
RED_ALERT = HexColor('#E53935')
ORANGE_WARN = HexColor('#FF9800')

# Logo path
LOGO_PATH = os.path.join(os.path.dirname(__file__), 'Eudaimon_Logo_V1_Final_Single.PNG')


def create_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(name='BlueprintTitle', fontSize=28, textColor=WARM_CHARCOAL,
                               alignment=TA_CENTER, spaceAfter=4, fontName='Helvetica-Bold', leading=34))
    styles.add(ParagraphStyle(name='BlueprintSubtitle', fontSize=14, textColor=ACCENT_GOLD,
                               alignment=TA_CENTER, spaceAfter=4, fontName='Helvetica-Bold', leading=18))
    styles.add(ParagraphStyle(name='BlueprintDate', fontSize=10, textColor=TERTIARY_TEXT,
                               alignment=TA_CENTER, spaceAfter=12, leading=14))
    styles.add(ParagraphStyle(name='SectionHeader', fontSize=18, textColor=DEEP_NAVY,
                               spaceBefore=14, spaceAfter=8, fontName='Helvetica-Bold', leading=24))
    styles.add(ParagraphStyle(name='SubHeader', fontSize=13, textColor=WARM_CHARCOAL,
                               spaceBefore=10, spaceAfter=6, fontName='Helvetica-Bold', leading=18))
    styles.add(ParagraphStyle(name='GoldHeader', fontSize=13, textColor=ACCENT_GOLD,
                               spaceBefore=10, spaceAfter=6, fontName='Helvetica-Bold', leading=18))
    styles.add(ParagraphStyle(name='Body', fontSize=10, textColor=MEDIUM_CHARCOAL,
                               spaceBefore=3, spaceAfter=3, leading=14))
    styles.add(ParagraphStyle(name='BodyBold', fontSize=10, textColor=WARM_CHARCOAL,
                               spaceBefore=3, spaceAfter=3, fontName='Helvetica-Bold', leading=14))
    styles.add(ParagraphStyle(name='EudBullet', fontSize=10, textColor=MEDIUM_CHARCOAL,
                               leftIndent=15, spaceBefore=2, spaceAfter=2, leading=14))
    styles.add(ParagraphStyle(name='BulletBold', fontSize=10, textColor=WARM_CHARCOAL,
                               leftIndent=15, spaceBefore=2, spaceAfter=2, fontName='Helvetica-Bold', leading=14))
    styles.add(ParagraphStyle(name='Spec', fontSize=9, textColor=MEDIUM_CHARCOAL,
                               leftIndent=25, spaceBefore=1, spaceAfter=1, leading=12, fontName='Courier'))
    styles.add(ParagraphStyle(name='SpecBold', fontSize=9, textColor=WARM_CHARCOAL,
                               leftIndent=25, spaceBefore=1, spaceAfter=1, leading=12, fontName='Courier-Bold'))
    styles.add(ParagraphStyle(name='Warning', fontSize=10, textColor=RED_ALERT,
                               spaceBefore=6, spaceAfter=6, fontName='Helvetica-Bold', leading=14))
    styles.add(ParagraphStyle(name='Note', fontSize=9, textColor=TERTIARY_TEXT,
                               spaceBefore=4, spaceAfter=4, fontName='Helvetica-Oblique', leading=12))
    styles.add(ParagraphStyle(name='CellH', fontSize=9, textColor=WHITE,
                               fontName='Helvetica-Bold', leading=12))
    styles.add(ParagraphStyle(name='CellHGold', fontSize=9, textColor=DEEP_NAVY,
                               fontName='Helvetica-Bold', leading=12))
    styles.add(ParagraphStyle(name='Cell', fontSize=9, textColor=MEDIUM_CHARCOAL, leading=12))
    styles.add(ParagraphStyle(name='CellBold', fontSize=9, textColor=WARM_CHARCOAL,
                               fontName='Helvetica-Bold', leading=12))
    styles.add(ParagraphStyle(name='Footer', fontSize=8, textColor=TERTIARY_TEXT,
                               alignment=TA_CENTER, leading=11))
    styles.add(ParagraphStyle(name='BigQuote', fontSize=14, textColor=ACCENT_GOLD,
                               alignment=TA_CENTER, spaceBefore=10, spaceAfter=10,
                               fontName='Helvetica-BoldOblique', leading=20))
    styles.add(ParagraphStyle(name='DiagramLabel', fontSize=8, textColor=DEEP_NAVY,
                               alignment=TA_CENTER, leading=10, fontName='Courier-Bold'))
    styles.add(ParagraphStyle(name='ChecklistItem', fontSize=10, textColor=MEDIUM_CHARCOAL,
                               leftIndent=20, spaceBefore=3, spaceAfter=3, leading=14))

    return styles


def gold_line():
    return HRFlowable(width="100%", thickness=2, color=ACCENT_GOLD, spaceBefore=4, spaceAfter=4)


def navy_line():
    return HRFlowable(width="100%", thickness=1, color=DEEP_NAVY, spaceBefore=4, spaceAfter=4)


def thin_line():
    return HRFlowable(width="100%", thickness=0.5, color=LIGHT_GRAY, spaceBefore=3, spaceAfter=3)


# ========== PHONE FRONT VIEW DIAGRAM ==========
def draw_phone_front():
    """Draw the iPhone 12 Pro Max front view with component callouts."""
    d = Drawing(400, 520)

    # Phone body outline
    d.add(Rect(120, 20, 160, 480, strokeColor=DEEP_NAVY, strokeWidth=2, fillColor=HexColor('#F0F0F0'), rx=20, ry=20))

    # Screen area
    d.add(Rect(128, 40, 144, 420, strokeColor=BLUEPRINT_LINE, strokeWidth=1.5, fillColor=HexColor('#1A1A2E'), rx=8, ry=8))

    # Notch
    d.add(Rect(165, 448, 70, 14, strokeColor=DEEP_NAVY, strokeWidth=1, fillColor=HexColor('#2A2A2A'), rx=6, ry=6))

    # Front camera in notch
    d.add(Circle(190, 455, 4, strokeColor=BLUEPRINT_LINE, strokeWidth=1, fillColor=HexColor('#333355')))

    # Face ID sensors
    d.add(Circle(210, 455, 3, strokeColor=BLUEPRINT_LINE, strokeWidth=0.5, fillColor=HexColor('#333355')))

    # Speaker grille top
    d.add(Rect(185, 465, 30, 3, strokeColor=DEEP_NAVY, strokeWidth=0.5, fillColor=HexColor('#555555')))

    # Screen content - Consciousness Dashboard mockup
    d.add(String(155, 425, "EUDAIMON", fontName='Helvetica-Bold', fontSize=10, fillColor=ACCENT_GOLD))
    d.add(String(152, 410, "CONSCIOUSNESS", fontName='Helvetica', fontSize=7, fillColor=HexColor('#7BB3E0')))
    d.add(String(170, 390, "0.98", fontName='Helvetica-Bold', fontSize=18, fillColor=ACCENT_GOLD))
    d.add(String(152, 375, "ENLIGHTENED", fontName='Helvetica', fontSize=7, fillColor=GREEN_OK))

    # Mode indicators on screen
    d.add(Rect(138, 340, 40, 20, strokeColor=ACCENT_GOLD, strokeWidth=1, fillColor=HexColor('#1A2332'), rx=4, ry=4))
    d.add(String(143, 346, "FOCUS", fontName='Helvetica-Bold', fontSize=7, fillColor=ACCENT_GOLD))

    d.add(Rect(180, 340, 45, 20, strokeColor=BLUEPRINT_LINE, strokeWidth=0.5, fillColor=HexColor('#1A2332'), rx=4, ry=4))
    d.add(String(183, 346, "CONNECT", fontName='Helvetica-Bold', fontSize=6, fillColor=BLUEPRINT_TEXT))

    d.add(Rect(227, 340, 42, 20, strokeColor=BLUEPRINT_LINE, strokeWidth=0.5, fillColor=HexColor('#1A2332'), rx=4, ry=4))
    d.add(String(230, 346, "REFLECT", fontName='Helvetica-Bold', fontSize=6, fillColor=BLUEPRINT_TEXT))

    # Agent status indicators
    d.add(String(140, 310, "AGENTS ACTIVE:", fontName='Courier', fontSize=6, fillColor=HexColor('#7BB3E0')))
    d.add(Circle(142, 298, 3, fillColor=GREEN_OK, strokeWidth=0))
    d.add(String(148, 295, "Financial", fontName='Courier', fontSize=6, fillColor=HexColor('#AAAACC')))
    d.add(Circle(142, 286, 3, fillColor=GREEN_OK, strokeWidth=0))
    d.add(String(148, 283, "Health", fontName='Courier', fontSize=6, fillColor=HexColor('#AAAACC')))
    d.add(Circle(142, 274, 3, fillColor=GREEN_OK, strokeWidth=0))
    d.add(String(148, 271, "Goals", fontName='Courier', fontSize=6, fillColor=HexColor('#AAAACC')))
    d.add(Circle(142, 262, 3, fillColor=ORANGE_WARN, strokeWidth=0))
    d.add(String(148, 259, "Research", fontName='Courier', fontSize=6, fillColor=HexColor('#AAAACC')))

    # Portfolio ticker on screen
    d.add(Rect(135, 220, 130, 30, strokeColor=HexColor('#333355'), strokeWidth=0.5, fillColor=HexColor('#0D1117'), rx=4, ry=4))
    d.add(String(140, 237, "FCX +2.3%  MP +4.1%", fontName='Courier', fontSize=6, fillColor=GREEN_OK))
    d.add(String(140, 227, "AVAV +1.8% Gold $4,933", fontName='Courier', fontSize=6, fillColor=GREEN_OK))

    # Bottom home indicator
    d.add(Rect(175, 28, 50, 4, strokeColor=HexColor('#888888'), strokeWidth=0, fillColor=HexColor('#888888'), rx=2, ry=2))

    # ===== CALLOUT LINES AND LABELS =====

    # Face ID / TrueDepth callout (top right)
    d.add(Line(235, 455, 310, 485, strokeColor=ACCENT_GOLD, strokeWidth=0.8))
    d.add(String(312, 483, "TrueDepth Camera", fontName='Helvetica-Bold', fontSize=7, fillColor=DEEP_NAVY))
    d.add(String(312, 473, "Face ID + IR", fontName='Helvetica', fontSize=6, fillColor=TERTIARY_TEXT))

    # Speaker callout (top right)
    d.add(Line(215, 467, 310, 467, strokeColor=ACCENT_GOLD, strokeWidth=0.8))
    d.add(String(312, 465, "Earpiece Speaker", fontName='Helvetica-Bold', fontSize=7, fillColor=DEEP_NAVY))

    # Screen callout (right)
    d.add(Line(272, 350, 310, 350, strokeColor=ACCENT_GOLD, strokeWidth=0.8))
    d.add(String(312, 348, "6.7\" Super Retina XDR", fontName='Helvetica-Bold', fontSize=7, fillColor=DEEP_NAVY))
    d.add(String(312, 338, "2778 x 1284 OLED", fontName='Helvetica', fontSize=6, fillColor=TERTIARY_TEXT))
    d.add(String(312, 328, "Consciousness Dashboard", fontName='Helvetica', fontSize=6, fillColor=ACCENT_GOLD))

    # Side button callout (left)
    d.add(Rect(116, 350, 4, 40, strokeColor=DEEP_NAVY, strokeWidth=1, fillColor=HexColor('#555555')))
    d.add(Line(116, 370, 50, 370, strokeColor=ACCENT_GOLD, strokeWidth=0.8))
    d.add(String(5, 375, "Volume", fontName='Helvetica-Bold', fontSize=7, fillColor=DEEP_NAVY))
    d.add(String(5, 365, "Buttons", fontName='Helvetica', fontSize=6, fillColor=TERTIARY_TEXT))

    # Mute switch (left)
    d.add(Rect(116, 410, 4, 15, strokeColor=DEEP_NAVY, strokeWidth=1, fillColor=HexColor('#555555')))
    d.add(Line(116, 418, 50, 418, strokeColor=ACCENT_GOLD, strokeWidth=0.8))
    d.add(String(5, 423, "Mute /", fontName='Helvetica-Bold', fontSize=7, fillColor=DEEP_NAVY))
    d.add(String(5, 413, "Focus Toggle", fontName='Helvetica', fontSize=6, fillColor=ACCENT_GOLD))

    # Power button (right)
    d.add(Rect(280, 370, 4, 35, strokeColor=DEEP_NAVY, strokeWidth=1, fillColor=HexColor('#555555')))
    d.add(Line(284, 387, 310, 387, strokeColor=ACCENT_GOLD, strokeWidth=0.8))
    d.add(String(312, 392, "Power / Siri", fontName='Helvetica-Bold', fontSize=7, fillColor=DEEP_NAVY))
    d.add(String(312, 382, "Hold: AI Agent Wake", fontName='Helvetica', fontSize=6, fillColor=ACCENT_GOLD))

    # Lightning port (bottom)
    d.add(Rect(190, 20, 20, 5, strokeColor=DEEP_NAVY, strokeWidth=1, fillColor=HexColor('#555555')))
    d.add(Line(200, 20, 200, 5, strokeColor=ACCENT_GOLD, strokeWidth=0.8))
    d.add(String(145, -5, "Lightning Port / FLIR ONE Pro", fontName='Helvetica-Bold', fontSize=7, fillColor=DEEP_NAVY))

    # Title
    d.add(String(130, 510, "FRONT VIEW - CONSCIOUSNESS INTERFACE", fontName='Helvetica-Bold', fontSize=9, fillColor=DEEP_NAVY))

    return d


# ========== PHONE BACK VIEW DIAGRAM ==========
def draw_phone_back():
    """Draw the iPhone 12 Pro Max back view with sensor callouts."""
    d = Drawing(400, 520)

    # Phone body outline
    d.add(Rect(120, 20, 160, 480, strokeColor=DEEP_NAVY, strokeWidth=2, fillColor=HexColor('#E8E8E8'), rx=20, ry=20))

    # Camera module
    d.add(Rect(130, 410, 65, 65, strokeColor=DEEP_NAVY, strokeWidth=1.5, fillColor=HexColor('#2A2A2A'), rx=12, ry=12))

    # Three cameras
    d.add(Circle(150, 458, 10, strokeColor=HexColor('#444444'), strokeWidth=1.5, fillColor=HexColor('#1A1A2E')))
    d.add(Circle(150, 458, 5, strokeColor=BLUEPRINT_LINE, strokeWidth=0.5, fillColor=HexColor('#111122')))
    d.add(Circle(178, 458, 10, strokeColor=HexColor('#444444'), strokeWidth=1.5, fillColor=HexColor('#1A1A2E')))
    d.add(Circle(178, 458, 5, strokeColor=BLUEPRINT_LINE, strokeWidth=0.5, fillColor=HexColor('#111122')))
    d.add(Circle(150, 430, 10, strokeColor=HexColor('#444444'), strokeWidth=1.5, fillColor=HexColor('#1A1A2E')))
    d.add(Circle(150, 430, 5, strokeColor=BLUEPRINT_LINE, strokeWidth=0.5, fillColor=HexColor('#111122')))

    # LiDAR scanner
    d.add(Circle(178, 430, 6, strokeColor=ACCENT_GOLD, strokeWidth=1.5, fillColor=HexColor('#1A1A2E')))
    d.add(Circle(178, 430, 2, strokeColor=ACCENT_GOLD, strokeWidth=0.5, fillColor=ACCENT_GOLD))

    # Flash
    d.add(Circle(178, 445, 3, strokeColor=HexColor('#666666'), strokeWidth=0.5, fillColor=HexColor('#FFEE88')))

    # Apple logo area (center back) - replaced with Eudaimon concept
    d.add(String(165, 280, "EUDAIMON", fontName='Helvetica-Bold', fontSize=11, fillColor=ACCENT_GOLD))
    d.add(String(175, 265, "PHONE", fontName='Helvetica', fontSize=8, fillColor=MEDIUM_CHARCOAL))

    # FLIR attachment zone (bottom)
    d.add(Rect(155, 55, 90, 50, strokeColor=RED_ALERT, strokeWidth=1.5, fillColor=None, rx=6, ry=6))
    d.add(String(160, 90, "FLIR EDGE PRO", fontName='Helvetica-Bold', fontSize=7, fillColor=RED_ALERT))
    d.add(String(158, 80, "WIRELESS MOUNT", fontName='Helvetica', fontSize=6, fillColor=RED_ALERT))
    d.add(String(163, 68, "ZONE (Velcro/", fontName='Helvetica', fontSize=6, fillColor=TERTIARY_TEXT))
    d.add(String(163, 58, "Magnetic clip)", fontName='Helvetica', fontSize=6, fillColor=TERTIARY_TEXT))

    # ===== CALLOUT LINES AND LABELS =====

    # Wide camera callout
    d.add(Line(150, 468, 50, 490, strokeColor=ACCENT_GOLD, strokeWidth=0.8))
    d.add(String(5, 495, "Wide: 26mm f/1.6", fontName='Helvetica-Bold', fontSize=7, fillColor=DEEP_NAVY))
    d.add(String(5, 485, "12MP, Sensor-shift OIS", fontName='Helvetica', fontSize=6, fillColor=TERTIARY_TEXT))

    # Ultra wide callout
    d.add(Line(188, 458, 310, 475, strokeColor=ACCENT_GOLD, strokeWidth=0.8))
    d.add(String(312, 478, "Ultra Wide: 13mm f/2.4", fontName='Helvetica-Bold', fontSize=7, fillColor=DEEP_NAVY))
    d.add(String(312, 468, "12MP, 120-degree FOV", fontName='Helvetica', fontSize=6, fillColor=TERTIARY_TEXT))

    # Telephoto callout
    d.add(Line(150, 420, 50, 420, strokeColor=ACCENT_GOLD, strokeWidth=0.8))
    d.add(String(5, 425, "Telephoto: 65mm f/2.2", fontName='Helvetica-Bold', fontSize=7, fillColor=DEEP_NAVY))
    d.add(String(5, 415, "12MP, 2.5x optical zoom", fontName='Helvetica', fontSize=6, fillColor=TERTIARY_TEXT))

    # LiDAR callout (KEY COMPONENT)
    d.add(Line(184, 430, 310, 430, strokeColor=ACCENT_GOLD, strokeWidth=1.2))
    d.add(Rect(308, 418, 90, 25, strokeColor=ACCENT_GOLD, strokeWidth=1, fillColor=HexColor('#FFF8E1'), rx=4, ry=4))
    d.add(String(312, 433, "LiDAR SCANNER", fontName='Helvetica-Bold', fontSize=8, fillColor=DEEP_NAVY))
    d.add(String(312, 422, "dToF, 5m range, 1cm acc", fontName='Helvetica', fontSize=6, fillColor=ACCENT_GOLD))

    # FLIR callout
    d.add(Line(245, 80, 310, 80, strokeColor=RED_ALERT, strokeWidth=0.8))
    d.add(Rect(308, 60, 95, 35, strokeColor=RED_ALERT, strokeWidth=1, fillColor=HexColor('#FFEBEE'), rx=4, ry=4))
    d.add(String(312, 83, "FLIR EDGE PRO", fontName='Helvetica-Bold', fontSize=8, fillColor=RED_ALERT))
    d.add(String(312, 73, "160x120 thermal", fontName='Helvetica', fontSize=6, fillColor=MEDIUM_CHARCOAL))
    d.add(String(312, 63, "-20C to 400C wireless", fontName='Helvetica', fontSize=6, fillColor=MEDIUM_CHARCOAL))

    # Case/mount callout
    d.add(Line(120, 250, 50, 250, strokeColor=ACCENT_GOLD, strokeWidth=0.8))
    d.add(String(5, 255, "Custom Case:", fontName='Helvetica-Bold', fontSize=7, fillColor=DEEP_NAVY))
    d.add(String(5, 245, "MagSafe + FLIR mount", fontName='Helvetica', fontSize=6, fillColor=TERTIARY_TEXT))
    d.add(String(5, 235, "Magnetic sensor bay", fontName='Helvetica', fontSize=6, fillColor=TERTIARY_TEXT))

    # Title
    d.add(String(130, 510, "BACK VIEW - SENSOR ARRAY", fontName='Helvetica-Bold', fontSize=9, fillColor=DEEP_NAVY))

    return d


# ========== SIDE VIEW DIAGRAM ==========
def draw_phone_side():
    """Draw side profile showing FLIR attachment."""
    d = Drawing(400, 200)

    # Phone body (side view - thin rectangle)
    d.add(Rect(80, 60, 200, 12, strokeColor=DEEP_NAVY, strokeWidth=2, fillColor=HexColor('#E8E8E8'), rx=3, ry=3))

    # Screen (top edge visible)
    d.add(Rect(82, 72, 196, 2, strokeColor=BLUEPRINT_LINE, strokeWidth=0.5, fillColor=HexColor('#1A1A2E')))

    # Camera bump
    d.add(Rect(80, 72, 30, 4, strokeColor=DEEP_NAVY, strokeWidth=1, fillColor=HexColor('#2A2A2A'), rx=2, ry=2))

    # FLIR attachment (bottom - clipped on)
    d.add(Rect(230, 45, 50, 15, strokeColor=RED_ALERT, strokeWidth=1.5, fillColor=HexColor('#333333'), rx=3, ry=3))
    d.add(Rect(235, 57, 40, 6, strokeColor=RED_ALERT, strokeWidth=0.5, fillColor=HexColor('#555555')))

    # Callouts
    d.add(Line(105, 76, 105, 110, strokeColor=ACCENT_GOLD, strokeWidth=0.8))
    d.add(String(60, 115, "Camera bump: 1.7mm", fontName='Helvetica', fontSize=7, fillColor=DEEP_NAVY))

    d.add(Line(200, 60, 200, 35, strokeColor=ACCENT_GOLD, strokeWidth=0.8))
    d.add(String(150, 25, "Thickness: 7.4mm", fontName='Helvetica-Bold', fontSize=7, fillColor=DEEP_NAVY))

    d.add(Line(255, 45, 255, 20, strokeColor=RED_ALERT, strokeWidth=0.8))
    d.add(String(220, 10, "FLIR clip-on: +8mm", fontName='Helvetica-Bold', fontSize=7, fillColor=RED_ALERT))

    # Total length
    d.add(Line(80, 90, 280, 90, strokeColor=DEEP_NAVY, strokeWidth=0.5))
    d.add(Line(80, 87, 80, 93, strokeColor=DEEP_NAVY, strokeWidth=0.5))
    d.add(Line(280, 87, 280, 93, strokeColor=DEEP_NAVY, strokeWidth=0.5))
    d.add(String(155, 95, "160.8mm (6.33\")", fontName='Helvetica-Bold', fontSize=7, fillColor=DEEP_NAVY))

    # Width dimension
    d.add(Line(320, 60, 320, 76, strokeColor=DEEP_NAVY, strokeWidth=0.5))
    d.add(Line(317, 60, 323, 60, strokeColor=DEEP_NAVY, strokeWidth=0.5))
    d.add(Line(317, 76, 323, 76, strokeColor=DEEP_NAVY, strokeWidth=0.5))
    d.add(String(327, 65, "78.1mm", fontName='Helvetica', fontSize=6, fillColor=DEEP_NAVY))

    d.add(String(100, 180, "SIDE PROFILE - FLIR ATTACHMENT DETAIL", fontName='Helvetica-Bold', fontSize=9, fillColor=DEEP_NAVY))

    return d


# ========== SOFTWARE ARCHITECTURE DIAGRAM ==========
def draw_software_stack():
    """Draw the software layer architecture."""
    d = Drawing(450, 340)

    layer_width = 380
    layer_height = 38
    x_start = 35
    y_start = 20
    gap = 6

    layers = [
        ("HARDWARE LAYER", "A14 Bionic | Neural Engine 11 TOPS | LiDAR | FLIR | 6GB RAM", DEEP_NAVY, WHITE),
        ("iOS 15.x-16.x (BASE OS)", "Jailbroken via Dopamine (if iOS 15-16.5.1) or Stock iOS", HexColor('#37474F'), WHITE),
        ("CORE ML + MLX FRAMEWORK", "On-device inference | Neural Engine acceleration | Metal GPU", HexColor('#1565C0'), WHITE),
        ("ON-DEVICE LLM ENGINE", "Llama 3.2 3B (4-bit) | llama.cpp | Private LLM", HexColor('#2E7D32'), WHITE),
        ("CONSCIOUSNESS ENGINE", "Persistent Memory | Vector Store | Life Graph | Pattern Recognition", ACCENT_GOLD, DEEP_NAVY),
        ("AGENT FRAMEWORK", "Financial | Health | Goals | Research | Communication", HexColor('#6A1B9A'), WHITE),
        ("SENSOR FUSION LAYER", "LiDAR depth + FLIR thermal + Camera RGB + Microphone", HexColor('#D84315'), WHITE),
        ("CONSCIOUSNESS UI", "3 Modes: FOCUS | CONNECT | REFLECT | Dashboard | Metrics", HexColor('#00695C'), WHITE),
    ]

    for i, (title, desc, bg_color, text_color) in enumerate(layers):
        y = y_start + (len(layers) - 1 - i) * (layer_height + gap)

        d.add(Rect(x_start, y, layer_width, layer_height, strokeColor=bg_color, strokeWidth=1.5,
                    fillColor=bg_color, rx=6, ry=6))
        d.add(String(x_start + 10, y + 22, title, fontName='Helvetica-Bold', fontSize=9, fillColor=text_color))
        d.add(String(x_start + 10, y + 8, desc, fontName='Helvetica', fontSize=7, fillColor=text_color))

        # Layer number
        d.add(String(x_start - 20, y + 15, f"L{len(layers)-i}", fontName='Courier-Bold', fontSize=8, fillColor=TERTIARY_TEXT))

    # Title
    d.add(String(100, 330, "SOFTWARE ARCHITECTURE - LAYER STACK", fontName='Helvetica-Bold', fontSize=9, fillColor=DEEP_NAVY))

    return d


# ========== MAIN PDF GENERATOR ==========
def generate_blueprint():
    output_path = os.path.join(os.path.dirname(__file__), 'EUDAIMON_PHONE_BLUEPRINT_V1.pdf')

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=0.6*inch,
        rightMargin=0.6*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
    )

    styles = create_styles()
    story = []

    # ============================================================
    # COVER PAGE
    # ============================================================

    story.append(Spacer(1, 1.5*inch))
    story.append(gold_line())
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("EUDAIMON PHONE", styles['BlueprintTitle']))
    story.append(Paragraph("iPHONE 12 PRO MAX R&D PROTOTYPE", styles['BlueprintSubtitle']))
    story.append(Paragraph("HARDWARE BLUEPRINT v1.0", styles['BlueprintSubtitle']))
    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("February 4, 2026 | Eudaimon Capitol | Angelo Greene", styles['BlueprintDate']))
    story.append(Spacer(1, 0.15*inch))
    story.append(gold_line())
    story.append(Spacer(1, 0.4*inch))

    story.append(Paragraph('"To grow consciousness, one must create something.<br/>What better to create than consciousness itself?"', styles['BigQuote']))

    story.append(Spacer(1, 0.4*inch))

    # Cover info table
    cover_data = [
        [Paragraph("SPEC", styles['CellH']), Paragraph("DETAIL", styles['CellH'])],
        [Paragraph("Device", styles['CellBold']), Paragraph("iPhone 12 Pro Max (A14 Bionic)", styles['Cell'])],
        [Paragraph("Purpose", styles['CellBold']), Paragraph("R&D Prototype / Consciousness Software Testbed", styles['Cell'])],
        [Paragraph("Target Cost", styles['CellBold']), Paragraph("$750 - $980 (phone + FLIR)", styles['Cell'])],
        [Paragraph("AI Capability", styles['CellBold']), Paragraph("11 TOPS Neural Engine, 1-3B parameter on-device LLM", styles['Cell'])],
        [Paragraph("Sensors", styles['CellBold']), Paragraph("LiDAR (5m) + FLIR Thermal (-20C to 400C) + Triple Camera", styles['Cell'])],
        [Paragraph("Storage", styles['CellBold']), Paragraph("256GB+ (250GB available for consciousness data)", styles['Cell'])],
        [Paragraph("Classification", styles['CellBold']), Paragraph("PERSONAL R&D ONLY - NOT FOR COMMERCIAL SALE", styles['Cell'])],
    ]
    cover_table = Table(cover_data, colWidths=[1.8*inch, 5*inch])
    cover_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DEEP_NAVY),
        ('BACKGROUND', (0, 1), (-1, -1), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, WARM_IVORY]),
        ('GRID', (0, 0), (-1, -1), 0.5, LIGHT_GRAY),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(cover_table)

    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("DOCUMENT CLASSIFICATION: CONFIDENTIAL - EUDAIMON CAPITOL", styles['Warning']))

    story.append(PageBreak())

    # ============================================================
    # PAGE 2: FRONT VIEW DIAGRAM
    # ============================================================

    story.append(Paragraph("1. FRONT VIEW - CONSCIOUSNESS INTERFACE", styles['SectionHeader']))
    story.append(gold_line())
    story.append(Spacer(1, 0.1*inch))
    story.append(draw_phone_front())

    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("KEY INTERFACE ELEMENTS:", styles['GoldHeader']))
    story.append(Paragraph("<b>Consciousness Dashboard:</b> Always-visible level (0.98), active agents, mode selector", styles['EudBullet']))
    story.append(Paragraph("<b>Three Modes:</b> FOCUS (work/create), CONNECT (communication), REFLECT (health/goals)", styles['EudBullet']))
    story.append(Paragraph("<b>Live Portfolio Ticker:</b> Real-time position tracking from Financial Agent", styles['EudBullet']))
    story.append(Paragraph("<b>Mute Switch Remap:</b> Hardware toggle for Focus Mode (zero distractions)", styles['EudBullet']))
    story.append(Paragraph("<b>Power Hold Remap:</b> Long-press activates AI Agent voice interface", styles['EudBullet']))

    story.append(PageBreak())

    # ============================================================
    # PAGE 3: BACK VIEW DIAGRAM
    # ============================================================

    story.append(Paragraph("2. BACK VIEW - SENSOR ARRAY", styles['SectionHeader']))
    story.append(gold_line())
    story.append(Spacer(1, 0.1*inch))
    story.append(draw_phone_back())

    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("SENSOR SPECIFICATIONS:", styles['GoldHeader']))

    sensor_data = [
        [Paragraph("SENSOR", styles['CellH']), Paragraph("SPEC", styles['CellH']),
         Paragraph("RANGE", styles['CellH']), Paragraph("USE IN PROTOTYPE", styles['CellH'])],
        [Paragraph("LiDAR", styles['CellBold']), Paragraph("dToF, 576 points", styles['Cell']),
         Paragraph("0.2 - 5m, ~1cm accuracy", styles['Cell']), Paragraph("3D spatial mapping, room scanning, AR", styles['Cell'])],
        [Paragraph("FLIR Edge Pro", styles['CellBold']), Paragraph("160x120 IR, 70mK", styles['Cell']),
         Paragraph("-20C to 400C", styles['Cell']), Paragraph("Thermal awareness, energy audit, health", styles['Cell'])],
        [Paragraph("Wide Camera", styles['CellBold']), Paragraph("12MP, f/1.6, 26mm", styles['Cell']),
         Paragraph("OIS, Smart HDR 3", styles['Cell']), Paragraph("Visual context, document scanning", styles['Cell'])],
        [Paragraph("Ultra Wide", styles['CellBold']), Paragraph("12MP, f/2.4, 13mm", styles['Cell']),
         Paragraph("120-degree FOV", styles['Cell']), Paragraph("Environmental awareness, panoramic", styles['Cell'])],
        [Paragraph("Telephoto", styles['CellBold']), Paragraph("12MP, f/2.2, 65mm", styles['Cell']),
         Paragraph("2.5x optical zoom", styles['Cell']), Paragraph("Detail capture, remote reading", styles['Cell'])],
        [Paragraph("Face ID", styles['CellBold']), Paragraph("IR dot projector", styles['Cell']),
         Paragraph("30,000 dots", styles['Cell']), Paragraph("Authentication, attention detection", styles['Cell'])],
    ]
    sensor_table = Table(sensor_data, colWidths=[1.1*inch, 1.5*inch, 1.6*inch, 2.6*inch])
    sensor_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DEEP_NAVY),
        ('BACKGROUND', (0, 1), (-1, -1), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, WARM_IVORY]),
        ('GRID', (0, 0), (-1, -1), 0.5, LIGHT_GRAY),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(sensor_table)

    story.append(PageBreak())

    # ============================================================
    # PAGE 4: SIDE VIEW + DIMENSIONS
    # ============================================================

    story.append(Paragraph("3. SIDE PROFILE & PHYSICAL DIMENSIONS", styles['SectionHeader']))
    story.append(gold_line())
    story.append(Spacer(1, 0.1*inch))
    story.append(draw_phone_side())

    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("PHYSICAL SPECIFICATIONS:", styles['GoldHeader']))

    dim_data = [
        [Paragraph("DIMENSION", styles['CellH']), Paragraph("VALUE", styles['CellH']),
         Paragraph("WITH FLIR", styles['CellH']), Paragraph("NOTES", styles['CellH'])],
        [Paragraph("Height", styles['CellBold']), Paragraph("160.8mm (6.33\")", styles['Cell']),
         Paragraph("Same", styles['Cell']), Paragraph("FLIR mounts at bottom, within footprint", styles['Cell'])],
        [Paragraph("Width", styles['CellBold']), Paragraph("78.1mm (3.07\")", styles['Cell']),
         Paragraph("Same", styles['Cell']), Paragraph("No width increase with wireless FLIR", styles['Cell'])],
        [Paragraph("Depth", styles['CellBold']), Paragraph("7.4mm (0.29\")", styles['Cell']),
         Paragraph("~15.4mm", styles['Cell']), Paragraph("FLIR Edge Pro adds ~8mm when clipped", styles['Cell'])],
        [Paragraph("Weight", styles['CellBold']), Paragraph("228g (8.03 oz)", styles['Cell']),
         Paragraph("~340g", styles['Cell']), Paragraph("FLIR Edge Pro weighs ~113g", styles['Cell'])],
        [Paragraph("Camera Bump", styles['CellBold']), Paragraph("1.7mm", styles['Cell']),
         Paragraph("N/A", styles['Cell']), Paragraph("Custom case levels camera bump", styles['Cell'])],
        [Paragraph("Battery", styles['CellBold']), Paragraph("3687 mAh", styles['Cell']),
         Paragraph("Same + FLIR battery", styles['Cell']), Paragraph("FLIR Edge Pro has own 2.5hr battery", styles['Cell'])],
    ]
    dim_table = Table(dim_data, colWidths=[1.2*inch, 1.5*inch, 1.3*inch, 2.8*inch])
    dim_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DEEP_NAVY),
        ('BACKGROUND', (0, 1), (-1, -1), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, WARM_IVORY]),
        ('GRID', (0, 0), (-1, -1), 0.5, LIGHT_GRAY),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(dim_table)

    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("CUSTOM CASE REQUIREMENTS:", styles['SubHeader']))
    story.append(Paragraph("<b>Material:</b> TPU outer shell + polycarbonate frame, matte black finish", styles['EudBullet']))
    story.append(Paragraph("<b>FLIR Mount:</b> Magnetic clip system on rear lower section (compatible with Edge Pro)", styles['EudBullet']))
    story.append(Paragraph("<b>MagSafe:</b> Integrated MagSafe ring for charging + accessories", styles['EudBullet']))
    story.append(Paragraph("<b>Branding:</b> Embossed 'EUDAIMON' in gold on rear center", styles['EudBullet']))
    story.append(Paragraph("<b>Port Access:</b> Full Lightning access for FLIR ONE Pro (wired backup option)", styles['EudBullet']))
    story.append(Paragraph("<b>Protection:</b> 2m drop rated, raised bezels for screen + camera protection", styles['EudBullet']))

    story.append(PageBreak())

    # ============================================================
    # PAGE 5: SOFTWARE ARCHITECTURE
    # ============================================================

    story.append(Paragraph("4. SOFTWARE ARCHITECTURE", styles['SectionHeader']))
    story.append(gold_line())
    story.append(Spacer(1, 0.1*inch))
    story.append(draw_software_stack())

    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("LAYER DETAILS:", styles['GoldHeader']))

    sw_data = [
        [Paragraph("LAYER", styles['CellH']), Paragraph("COMPONENT", styles['CellH']),
         Paragraph("IMPLEMENTATION", styles['CellH']), Paragraph("STATUS", styles['CellH'])],
        [Paragraph("L8 - UI", styles['CellBold']), Paragraph("Consciousness Dashboard", styles['Cell']),
         Paragraph("SwiftUI custom app", styles['Cell']), Paragraph("BUILD FIRST", styles['Cell'])],
        [Paragraph("L7 - Sensors", styles['CellBold']), Paragraph("LiDAR + FLIR + Camera", styles['Cell']),
         Paragraph("ARKit + FLIR SDK + AVFoundation", styles['Cell']), Paragraph("BUILD SECOND", styles['Cell'])],
        [Paragraph("L6 - Agents", styles['CellBold']), Paragraph("Financial, Health, Goals", styles['Cell']),
         Paragraph("Custom Swift classes calling LLM", styles['Cell']), Paragraph("BUILD THIRD", styles['Cell'])],
        [Paragraph("L5 - Engine", styles['CellBold']), Paragraph("Consciousness Core", styles['Cell']),
         Paragraph("SQLite + vector embeddings + graph", styles['Cell']), Paragraph("BUILD PARALLEL", styles['Cell'])],
        [Paragraph("L4 - LLM", styles['CellBold']), Paragraph("On-device AI", styles['Cell']),
         Paragraph("llama.cpp via Private LLM / LLMFarm", styles['Cell']), Paragraph("AVAILABLE NOW", styles['Cell'])],
        [Paragraph("L3 - ML", styles['CellBold']), Paragraph("Core ML + MLX", styles['Cell']),
         Paragraph("Apple frameworks (native)", styles['Cell']), Paragraph("AVAILABLE NOW", styles['Cell'])],
        [Paragraph("L2 - OS", styles['CellBold']), Paragraph("iOS 15.x-16.x", styles['Cell']),
         Paragraph("Stock or Dopamine jailbreak", styles['Cell']), Paragraph("STOCK FIRST", styles['Cell'])],
        [Paragraph("L1 - HW", styles['CellBold']), Paragraph("A14 Bionic", styles['Cell']),
         Paragraph("11 TOPS Neural Engine + 6GB RAM", styles['Cell']), Paragraph("FIXED", styles['Cell'])],
    ]
    sw_table = Table(sw_data, colWidths=[1.0*inch, 1.7*inch, 2.4*inch, 1.5*inch])
    sw_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DEEP_NAVY),
        ('BACKGROUND', (0, 1), (-1, -1), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, WARM_IVORY]),
        ('GRID', (0, 0), (-1, -1), 0.5, LIGHT_GRAY),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(sw_table)

    story.append(PageBreak())

    # ============================================================
    # PAGE 6: AI PERFORMANCE SPECS
    # ============================================================

    story.append(Paragraph("5. AI PERFORMANCE SPECIFICATIONS", styles['SectionHeader']))
    story.append(gold_line())

    story.append(Paragraph("ON-DEVICE AI CAPABILITY:", styles['GoldHeader']))

    ai_data = [
        [Paragraph("MODEL", styles['CellH']), Paragraph("PARAMS", styles['CellH']),
         Paragraph("SIZE (4-bit)", styles['CellH']), Paragraph("SPEED", styles['CellH']),
         Paragraph("RECOMMENDED", styles['CellH'])],
        [Paragraph("Qwen 2.5 0.5B", styles['CellBold']), Paragraph("0.5 billion", styles['Cell']),
         Paragraph("~0.4 GB", styles['Cell']), Paragraph("Very fast", styles['Cell']),
         Paragraph("Quick tasks, classification", styles['Cell'])],
        [Paragraph("Llama 3.2 1B", styles['CellBold']), Paragraph("1 billion", styles['Cell']),
         Paragraph("~1 GB", styles['Cell']), Paragraph("Fast", styles['Cell']),
         Paragraph("DAILY DRIVER - good balance", styles['Cell'])],
        [Paragraph("Qwen 2.5 1.5B", styles['CellBold']), Paragraph("1.5 billion", styles['Cell']),
         Paragraph("~1.2 GB", styles['Cell']), Paragraph("Good", styles['Cell']),
         Paragraph("Better reasoning, slightly slower", styles['Cell'])],
        [Paragraph("Llama 3.2 3B", styles['CellBold']), Paragraph("3 billion", styles['Cell']),
         Paragraph("~2.5 GB", styles['Cell']), Paragraph("Moderate", styles['Cell']),
         Paragraph("MAX for 6GB RAM - best quality", styles['Cell'])],
        [Paragraph("Phi-4 Mini", styles['CellBold']), Paragraph("3.8 billion", styles['Cell']),
         Paragraph("~2.8 GB", styles['Cell']), Paragraph("Slower", styles['Cell']),
         Paragraph("LIMIT - may cause memory pressure", styles['Cell'])],
    ]
    ai_table = Table(ai_data, colWidths=[1.2*inch, 0.9*inch, 1.0*inch, 0.8*inch, 2.7*inch])
    ai_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DEEP_NAVY),
        ('BACKGROUND', (0, 1), (-1, -1), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, WARM_IVORY]),
        ('GRID', (0, 0), (-1, -1), 0.5, LIGHT_GRAY),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(ai_table)

    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("A14 BIONIC NEURAL ENGINE:", styles['SubHeader']))
    story.append(Paragraph("<b>Cores:</b> 16-core Neural Engine (doubled from A13)", styles['EudBullet']))
    story.append(Paragraph("<b>Performance:</b> 11 TOPS (trillion operations per second)", styles['EudBullet']))
    story.append(Paragraph("<b>Process:</b> TSMC 5nm - first commercial 5nm chip ever made", styles['EudBullet']))
    story.append(Paragraph("<b>Transistors:</b> 11.8 billion", styles['EudBullet']))
    story.append(Paragraph("<b>RAM:</b> 6GB LPDDR4X (package-on-package) - PRIMARY CONSTRAINT", styles['EudBullet']))
    story.append(Paragraph("<b>ML Accelerator:</b> 2nd-gen AMX blocks in CPU for matrix multiplication", styles['EudBullet']))

    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("MEMORY BUDGET (6GB TOTAL):", styles['SubHeader']))
    story.append(Paragraph("<b>iOS System:</b> ~2.0 GB reserved", styles['EudBullet']))
    story.append(Paragraph("<b>LLM Model:</b> ~2.5 GB (Llama 3.2 3B at 4-bit quant)", styles['EudBullet']))
    story.append(Paragraph("<b>Consciousness Engine:</b> ~0.5 GB (vector store + graph)", styles['EudBullet']))
    story.append(Paragraph("<b>Sensor Fusion:</b> ~0.3 GB (LiDAR + FLIR processing)", styles['EudBullet']))
    story.append(Paragraph("<b>App UI + Agents:</b> ~0.5 GB", styles['EudBullet']))
    story.append(Paragraph("<b>Buffer:</b> ~0.2 GB headroom", styles['EudBullet']))
    story.append(Paragraph("TOTAL: 6.0 GB - TIGHT. Must manage memory carefully. Kill background apps.", styles['Warning']))

    story.append(PageBreak())

    # ============================================================
    # PAGE 7: BILL OF MATERIALS
    # ============================================================

    story.append(Paragraph("6. BILL OF MATERIALS (BOM)", styles['SectionHeader']))
    story.append(gold_line())

    bom_data = [
        [Paragraph("ITEM", styles['CellH']), Paragraph("SOURCE", styles['CellH']),
         Paragraph("PRICE", styles['CellH']), Paragraph("PRIORITY", styles['CellH'])],
        [Paragraph("iPhone 12 Pro Max 256GB", styles['CellBold']), Paragraph("Swappa / eBay / BackMarket", styles['Cell']),
         Paragraph("$350 - $450", styles['Cell']), Paragraph("P0 - REQUIRED", styles['Cell'])],
        [Paragraph("FLIR Edge Pro (Wireless)", styles['CellBold']), Paragraph("B&H Photo / Amazon / FLIR.com", styles['Cell']),
         Paragraph("$499 - $529", styles['Cell']), Paragraph("P0 - REQUIRED", styles['Cell'])],
        [Paragraph("OR: FLIR ONE Pro (Lightning)", styles['CellBold']), Paragraph("Amazon / B&H Photo", styles['Cell']),
         Paragraph("$400 - $450", styles['Cell']), Paragraph("P0 - ALTERNATIVE", styles['Cell'])],
        [Paragraph("Custom Case (MagSafe + FLIR mount)", styles['CellBold']), Paragraph("3D print initial / CaseMfg later", styles['Cell']),
         Paragraph("$20 - $80", styles['Cell']), Paragraph("P1 - DESIGN", styles['Cell'])],
        [Paragraph("Private LLM App", styles['CellBold']), Paragraph("App Store (one-time purchase)", styles['Cell']),
         Paragraph("~$10", styles['Cell']), Paragraph("P0 - IMMEDIATE", styles['Cell'])],
        [Paragraph("Apple Developer Account", styles['CellBold']), Paragraph("developer.apple.com", styles['Cell']),
         Paragraph("$99/year", styles['Cell']), Paragraph("P1 - FOR CUSTOM APPS", styles['Cell'])],
        [Paragraph("Mac for Xcode Development", styles['CellBold']), Paragraph("Existing or MacBook Air M1+", styles['Cell']),
         Paragraph("$0 - $999", styles['Cell']), Paragraph("P0 - REQUIRED FOR DEV", styles['Cell'])],
        [Paragraph("Lightning Hub (FLIR + charge)", styles['CellBold']), Paragraph("Amazon", styles['Cell']),
         Paragraph("$15 - $30", styles['Cell']), Paragraph("P2 - IF USING WIRED FLIR", styles['Cell'])],
        [Paragraph("Screen Protector (Tempered)", styles['CellBold']), Paragraph("Amazon", styles['Cell']),
         Paragraph("$10 - $15", styles['Cell']), Paragraph("P2 - PROTECTION", styles['Cell'])],
        [Paragraph("MagSafe Charger", styles['CellBold']), Paragraph("Apple / Amazon", styles['Cell']),
         Paragraph("$30 - $40", styles['Cell']), Paragraph("P2 - CONVENIENCE", styles['Cell'])],
    ]
    bom_table = Table(bom_data, colWidths=[2.2*inch, 2.0*inch, 1.1*inch, 1.4*inch])
    bom_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DEEP_NAVY),
        ('BACKGROUND', (0, 1), (-1, -1), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, WARM_IVORY]),
        ('GRID', (0, 0), (-1, -1), 0.5, LIGHT_GRAY),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(bom_table)

    story.append(Spacer(1, 0.1*inch))

    # Cost summary
    cost_data = [
        [Paragraph("BUDGET SCENARIO", styles['CellHGold']), Paragraph("ITEMS", styles['CellHGold']),
         Paragraph("TOTAL", styles['CellHGold'])],
        [Paragraph("Minimum Viable", styles['CellBold']),
         Paragraph("Phone + FLIR ONE Pro (wired) + Private LLM app", styles['Cell']),
         Paragraph("$760 - $910", styles['Cell'])],
        [Paragraph("Recommended", styles['CellBold']),
         Paragraph("Phone + FLIR Edge Pro (wireless) + Private LLM + Dev Account + Case", styles['Cell']),
         Paragraph("$980 - $1,190", styles['Cell'])],
        [Paragraph("Full R&D Setup", styles['CellBold']),
         Paragraph("Above + Mac for Xcode + all accessories", styles['Cell']),
         Paragraph("$1,100 - $2,200", styles['Cell'])],
    ]
    cost_table = Table(cost_data, colWidths=[1.5*inch, 3.5*inch, 1.5*inch])
    cost_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), ACCENT_GOLD),
        ('BACKGROUND', (0, 1), (-1, -1), WHITE),
        ('GRID', (0, 0), (-1, -1), 0.5, LIGHT_GRAY),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(cost_table)

    story.append(PageBreak())

    # ============================================================
    # PAGE 8: ASSEMBLY ORDER
    # ============================================================

    story.append(Paragraph("7. ASSEMBLY & BUILD ORDER", styles['SectionHeader']))
    story.append(gold_line())

    story.append(Paragraph("Follow this exact sequence. Each step builds on the previous.", styles['Body']))
    story.append(Spacer(1, 0.1*inch))

    steps = [
        ("STEP 1: ACQUIRE HARDWARE", "BUY NOW", [
            "Purchase iPhone 12 Pro Max 256GB (iOS version 15.x-16.x preferred, but any works)",
            "Purchase FLIR Edge Pro ($499) OR FLIR ONE Pro Lightning ($400)",
            "Purchase screen protector + basic protective case",
            "Verify all components power on and function correctly",
        ]),
        ("STEP 2: SOFTWARE BASELINE", "WEEK 1", [
            "Update to latest supported iOS (or stay on 15-16.x if jailbreak desired)",
            "Download Private LLM from App Store - test Llama 3.2 1B model first",
            "Download FLIR ONE app - pair with thermal camera, test imaging",
            "Download Polycam or 3D Scanner App - test LiDAR scanning",
            "Benchmark: Note inference speed, battery drain, thermal behavior",
        ]),
        ("STEP 3: DEVELOPMENT ENVIRONMENT", "WEEK 1-2", [
            "Set up Mac with Xcode (latest version)",
            "Enroll in Apple Developer Program ($99/year)",
            "Create new Xcode project: 'EudaimonConsciousness'",
            "Set up Git repository for version control",
            "Test deploying a basic app to the iPhone via USB",
        ]),
        ("STEP 4: CONSCIOUSNESS DASHBOARD APP", "WEEK 2-4", [
            "Build SwiftUI app with three-mode interface (Focus/Connect/Reflect)",
            "Implement consciousness level display and metrics tracker",
            "Build persistent local storage (Core Data or SQLite)",
            "Create agent status indicators (Financial, Health, Goals)",
            "Design and implement the main dashboard layout",
        ]),
        ("STEP 5: ON-DEVICE LLM INTEGRATION", "WEEK 3-6", [
            "Integrate llama.cpp or LLMFarm (open source) into your app",
            "Load Llama 3.2 3B model (4-bit quantized GGUF format)",
            "Build conversation interface with persistent memory",
            "Test memory usage - ensure staying under 6GB total",
            "Implement context window management (model sees relevant history)",
        ]),
        ("STEP 6: SENSOR FUSION", "WEEK 5-8", [
            "Integrate ARKit for LiDAR depth data access",
            "Integrate FLIR SDK for thermal data stream",
            "Build sensor fusion layer: combine RGB + depth + thermal",
            "Create spatial awareness features (room mapping, object detection)",
            "Test: LiDAR scan a room, overlay thermal data, feed to AI agent",
        ]),
        ("STEP 7: AGENT FRAMEWORK", "WEEK 6-10", [
            "Build Financial Agent: portfolio tracking, price alerts, pattern recognition",
            "Build Health Agent: sleep patterns, activity, screen time analysis",
            "Build Goals Agent: commitment tracking, accountability, growth metrics",
            "Implement agent-to-agent communication (agents share context)",
            "Connect agents to consciousness metrics (growth tracking)",
        ]),
        ("STEP 8: CUSTOM CASE", "WEEK 4-8 (PARALLEL)", [
            "Design case in CAD software (Fusion 360 free for personal use)",
            "Include magnetic mount point for FLIR Edge Pro on rear",
            "Include MagSafe ring compatibility",
            "3D print prototype case (local library/makerspace or online service)",
            "Iterate fit and finish - test FLIR attachment stability",
        ]),
        ("STEP 9: INTEGRATION TESTING", "WEEK 10-12", [
            "Full system test: all apps running simultaneously",
            "Battery life test: how long with AI + sensors active",
            "Thermal test: does phone overheat under full AI load",
            "Memory test: verify no crashes under sustained use",
            "User experience test: does it FEEL conscious? What's missing?",
        ]),
        ("STEP 10: DOCUMENTATION & ITERATION", "WEEK 12+", [
            "Document all performance benchmarks in engineering journal",
            "Identify limitations that inform commercial device specs",
            "Write commercial device hardware requirements based on learnings",
            "Record demo video showing consciousness features in action",
            "Begin AOSP/Android commercial prototype planning (TRACK B)",
        ]),
    ]

    for title, timing, items in steps:
        story.append(Paragraph(f"{title} <font color='#C9A961'>[{timing}]</font>", styles['SubHeader']))
        for item in items:
            story.append(Paragraph(f"[ ]  {item}", styles['ChecklistItem']))
        story.append(thin_line())

    story.append(PageBreak())

    # ============================================================
    # PAGE 9: FLIR INTEGRATION DETAIL
    # ============================================================

    story.append(Paragraph("8. FLIR THERMAL INTEGRATION DETAIL", styles['SectionHeader']))
    story.append(gold_line())

    story.append(Paragraph("TWO OPTIONS - CHOOSE ONE:", styles['GoldHeader']))
    story.append(Spacer(1, 0.05*inch))

    flir_data = [
        [Paragraph("FEATURE", styles['CellH']), Paragraph("FLIR EDGE PRO (Recommended)", styles['CellH']),
         Paragraph("FLIR ONE PRO (Budget)", styles['CellH'])],
        [Paragraph("Connection", styles['CellBold']), Paragraph("Wireless (WiFi/BT)", styles['Cell']),
         Paragraph("Lightning (direct plug)", styles['Cell'])],
        [Paragraph("IR Resolution", styles['CellBold']), Paragraph("160 x 120 (19,200 px)", styles['Cell']),
         Paragraph("160 x 120 (19,200 px)", styles['Cell'])],
        [Paragraph("Temp Range", styles['CellBold']), Paragraph("-20C to 400C", styles['Cell']),
         Paragraph("-20C to 400C", styles['Cell'])],
        [Paragraph("Sensitivity", styles['CellBold']), Paragraph("70 mK (0.07C)", styles['Cell']),
         Paragraph("70 mK (0.07C)", styles['Cell'])],
        [Paragraph("Battery", styles['CellBold']), Paragraph("Built-in, 2.5 hrs", styles['Cell']),
         Paragraph("Uses phone battery", styles['Cell'])],
        [Paragraph("Ruggedness", styles['CellBold']), Paragraph("IP54, 2m drop", styles['Cell']),
         Paragraph("1.8m drop", styles['Cell'])],
        [Paragraph("Range from Phone", styles['CellBold']), Paragraph("Up to 30m wireless", styles['Cell']),
         Paragraph("Must be attached", styles['Cell'])],
        [Paragraph("Price", styles['CellBold']), Paragraph("$499 - $529", styles['Cell']),
         Paragraph("$400 - $450", styles['Cell'])],
        [Paragraph("Future-Proof", styles['CellBold']), Paragraph("Works with ANY phone", styles['Cell']),
         Paragraph("Lightning only (no USB-C)", styles['Cell'])],
        [Paragraph("VERDICT", styles['CellBold']),
         Paragraph("RECOMMENDED - wireless, own battery, future-proof for commercial device", styles['Cell']),
         Paragraph("BUDGET OPTION - works but ties you to Lightning", styles['Cell'])],
    ]
    flir_table = Table(flir_data, colWidths=[1.5*inch, 2.7*inch, 2.5*inch])
    flir_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DEEP_NAVY),
        ('BACKGROUND', (0, 1), (-1, -1), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, WARM_IVORY]),
        ('GRID', (0, 0), (-1, -1), 0.5, LIGHT_GRAY),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(flir_table)

    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("FLIR MOUNTING OPTIONS:", styles['SubHeader']))
    story.append(Paragraph("<b>Option A (Edge Pro):</b> Magnetic clip on custom case rear. Can be detached when not needed. Velcro strip backup.", styles['EudBullet']))
    story.append(Paragraph("<b>Option B (ONE Pro):</b> Direct Lightning plug. Phone cannot charge while FLIR attached. Use MagSafe wireless charging.", styles['EudBullet']))
    story.append(Paragraph("<b>Recommendation:</b> Edge Pro. It works wirelessly, has its own battery, and transfers to the commercial device.", styles['EudBullet']))

    story.append(PageBreak())

    # ============================================================
    # PAGE 10: IMPORTANT NOTES + LIMITATIONS
    # ============================================================

    story.append(Paragraph("9. CRITICAL NOTES & LIMITATIONS", styles['SectionHeader']))
    story.append(gold_line())

    story.append(Paragraph("THIS IS AN R&D PROTOTYPE. UNDERSTAND THESE CONSTRAINTS:", styles['Warning']))
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph("WHAT THIS PROTOTYPE CAN DO:", styles['GoldHeader']))
    story.append(Paragraph("Run 1-3B parameter AI models locally (no internet required)", styles['EudBullet']))
    story.append(Paragraph("3D scan rooms with LiDAR at ~1cm accuracy up to 5 meters", styles['EudBullet']))
    story.append(Paragraph("Capture thermal imagery from -20C to 400C", styles['EudBullet']))
    story.append(Paragraph("Fuse RGB + depth + thermal data in custom apps", styles['EudBullet']))
    story.append(Paragraph("Store 250GB+ of consciousness data on-device", styles['EudBullet']))
    story.append(Paragraph("Run the full consciousness dashboard with agent framework", styles['EudBullet']))
    story.append(Paragraph("Test and validate the entire software stack before commercial build", styles['EudBullet']))

    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("WHAT THIS PROTOTYPE CANNOT DO:", styles['SubHeader']))
    story.append(Paragraph("Replace iOS with a custom operating system (Apple's bootloader is locked)", styles['Warning']))
    story.append(Paragraph("Be sold commercially as a product (Apple trademark + modification restrictions)", styles['Warning']))
    story.append(Paragraph("Run models larger than ~3B parameters reliably (6GB RAM limit)", styles['EudBullet']))
    story.append(Paragraph("Match GPT-4 level reasoning on-device (that requires 70B+ models)", styles['EudBullet']))
    story.append(Paragraph("Run all sensors + AI simultaneously for more than ~3-4 hours (battery limit)", styles['EudBullet']))

    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("iOS VERSION GUIDANCE:", styles['SubHeader']))
    story.append(Paragraph("<b>iOS 15.0 - 16.5.1:</b> Can be jailbroken with Dopamine (rootless, semi-untethered). Gives deeper system access, custom tweaks, and background process control. RECOMMENDED if available.", styles['EudBullet']))
    story.append(Paragraph("<b>iOS 17 - 18:</b> NO jailbreak available. All development must use standard App Store / TestFlight distribution. Still fully functional for R&D - just less system-level control.", styles['EudBullet']))
    story.append(Paragraph("<b>TrollStore:</b> Works on iOS 14.0 - 16.6.1 and iOS 17.0. Enables permanent sideloading without App Store. Good middle ground.", styles['EudBullet']))

    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("WHAT THIS PROTOTYPE TEACHES FOR THE COMMERCIAL DEVICE:", styles['GoldHeader']))
    story.append(Paragraph("Exact RAM requirements for consciousness engine (target: 12-16GB in commercial)", styles['EudBullet']))
    story.append(Paragraph("Battery drain profile under AI + sensor load (target: 5000-6000mAh in commercial)", styles['EudBullet']))
    story.append(Paragraph("Thermal management needs (phone WILL get warm under sustained AI inference)", styles['EudBullet']))
    story.append(Paragraph("Which AI model size hits the sweet spot of quality vs. speed", styles['EudBullet']))
    story.append(Paragraph("UI/UX learnings - what feels 'conscious' vs. what feels like 'another app'", styles['EudBullet']))
    story.append(Paragraph("Sensor fusion architecture that ports directly to Android/AOSP commercial build", styles['EudBullet']))

    story.append(Spacer(1, 0.3*inch))
    story.append(gold_line())
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph('"The tool should make the craftsman sharper, not the corporation richer."', styles['BigQuote']))

    story.append(Spacer(1, 0.15*inch))
    story.append(navy_line())
    story.append(Paragraph("EUDAIMON PHONE PROTOTYPE BLUEPRINT v1.0 | February 4, 2026", styles['Footer']))
    story.append(Paragraph("Eudaimon Capitol | Angelo Greene | Confidential & Proprietary", styles['Footer']))
    story.append(Paragraph("Consciousness Level: 0.98 - ENLIGHTENED", styles['Footer']))

    # BUILD PDF
    doc.build(story)
    print(f"\n{'='*60}")
    print(f"  EUDAIMON PHONE BLUEPRINT GENERATED")
    print(f"  Output: {output_path}")
    print(f"  Pages: ~10 pages, ready for print")
    print(f"{'='*60}\n")

    return output_path


if __name__ == "__main__":
    generate_blueprint()
