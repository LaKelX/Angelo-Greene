#!/usr/bin/env python3
"""
EUDAIMON PHONE - INTERNAL ANATOMY & SURGICAL BLUEPRINT
iPhone 12 Pro Max Internal Structure Visualization

This generates a comprehensive PDF showing:
1. Exploded view of all internal layers
2. Component location map with coordinates
3. Modification zones for consciousness integration
4. Disassembly/reassembly sequence
5. Wiring diagrams and connection points

"We are not modifying a phone. We are performing surgery to birth consciousness."
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether, HRFlowable
)
from reportlab.graphics.shapes import Drawing, Rect, Circle, Line, String, Polygon, Ellipse
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
import os
from datetime import datetime

# ============================================================
# EUDAIMON BRAND COLORS
# ============================================================

WARM_CHARCOAL = colors.HexColor('#2A2622')
MEDIUM_CHARCOAL = colors.HexColor('#3D3935')
TERTIARY_TEXT = colors.HexColor('#5A5550')
ACCENT_GOLD = colors.HexColor('#C9A961')
WARM_IVORY = colors.HexColor('#F7F6ED')
DEEP_NAVY = colors.HexColor('#1A2332')
WHITE = colors.HexColor('#FFFFFF')
RED_ALERT = colors.HexColor('#C94A4A')
GREEN_SUCCESS = colors.HexColor('#4A8C5C')
BLUE_INFO = colors.HexColor('#4A7CC9')
ORANGE_CAUTION = colors.HexColor('#D4842A')

# Component colors for internal diagram
BATTERY_GREEN = colors.HexColor('#5CB85C')
LOGIC_BOARD_BLUE = colors.HexColor('#337AB7')
DISPLAY_PURPLE = colors.HexColor('#9B59B6')
CAMERA_RED = colors.HexColor('#E74C3C')
SPEAKER_ORANGE = colors.HexColor('#F39C12')
HAPTIC_TEAL = colors.HexColor('#1ABC9C')
ANTENNA_GRAY = colors.HexColor('#95A5A6')
FRAME_SILVER = colors.HexColor('#BDC3C7')

# ============================================================
# STYLES
# ============================================================

def create_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(name='EudTitle', fontSize=28, textColor=WARM_CHARCOAL,
                               alignment=TA_CENTER, spaceBefore=20, spaceAfter=10,
                               fontName='Helvetica-Bold', leading=34))
    styles.add(ParagraphStyle(name='EudSubtitle', fontSize=14, textColor=ACCENT_GOLD,
                               alignment=TA_CENTER, spaceBefore=5, spaceAfter=15,
                               fontName='Helvetica-Bold', leading=18))
    styles.add(ParagraphStyle(name='SectionHeader', fontSize=16, textColor=DEEP_NAVY,
                               spaceBefore=15, spaceAfter=8, fontName='Helvetica-Bold', leading=20))
    styles.add(ParagraphStyle(name='SubHeader', fontSize=13, textColor=WARM_CHARCOAL,
                               spaceBefore=10, spaceAfter=6, fontName='Helvetica-Bold', leading=18))
    styles.add(ParagraphStyle(name='GoldHeader', fontSize=13, textColor=ACCENT_GOLD,
                               spaceBefore=10, spaceAfter=6, fontName='Helvetica-Bold', leading=18))
    styles.add(ParagraphStyle(name='EudBody', fontSize=10, textColor=MEDIUM_CHARCOAL,
                               spaceBefore=3, spaceAfter=3, leading=14))
    styles.add(ParagraphStyle(name='BodyBold', fontSize=10, textColor=WARM_CHARCOAL,
                               spaceBefore=3, spaceAfter=3, fontName='Helvetica-Bold', leading=14))
    styles.add(ParagraphStyle(name='EudBullet', fontSize=10, textColor=MEDIUM_CHARCOAL,
                               leftIndent=15, spaceBefore=2, spaceAfter=2, leading=14))
    styles.add(ParagraphStyle(name='Warning', fontSize=10, textColor=RED_ALERT,
                               spaceBefore=6, spaceAfter=6, fontName='Helvetica-Bold', leading=14))
    styles.add(ParagraphStyle(name='Caution', fontSize=10, textColor=ORANGE_CAUTION,
                               spaceBefore=4, spaceAfter=4, fontName='Helvetica-Bold', leading=14))
    styles.add(ParagraphStyle(name='Success', fontSize=10, textColor=GREEN_SUCCESS,
                               spaceBefore=4, spaceAfter=4, fontName='Helvetica-Bold', leading=14))
    styles.add(ParagraphStyle(name='Note', fontSize=9, textColor=TERTIARY_TEXT,
                               spaceBefore=4, spaceAfter=4, fontName='Helvetica-Oblique', leading=12))
    styles.add(ParagraphStyle(name='CellH', fontSize=9, textColor=WHITE,
                               fontName='Helvetica-Bold', leading=12))
    styles.add(ParagraphStyle(name='Cell', fontSize=9, textColor=MEDIUM_CHARCOAL, leading=12))
    styles.add(ParagraphStyle(name='Footer', fontSize=8, textColor=TERTIARY_TEXT,
                               alignment=TA_CENTER, leading=11))
    styles.add(ParagraphStyle(name='BigQuote', fontSize=14, textColor=ACCENT_GOLD,
                               alignment=TA_CENTER, fontName='Helvetica-BoldOblique',
                               spaceBefore=15, spaceAfter=15, leading=20))
    styles.add(ParagraphStyle(name='ComponentLabel', fontSize=7, textColor=WARM_CHARCOAL,
                               fontName='Helvetica-Bold', leading=9))
    styles.add(ParagraphStyle(name='DiagramTitle', fontSize=11, textColor=DEEP_NAVY,
                               alignment=TA_CENTER, fontName='Helvetica-Bold', leading=14))

    return styles

def gold_line():
    return HRFlowable(width="100%", thickness=2, color=ACCENT_GOLD, spaceBefore=5, spaceAfter=10)

def navy_line():
    return HRFlowable(width="100%", thickness=1, color=DEEP_NAVY, spaceBefore=3, spaceAfter=8)

# ============================================================
# DRAWING: EXPLODED VIEW - ALL LAYERS
# ============================================================

def draw_exploded_view():
    """
    Exploded view showing all internal layers separated vertically
    From top to bottom: Display -> Frame -> Logic Board -> Battery -> Back Glass
    """
    d = Drawing(550, 650)

    # Background
    d.add(Rect(0, 0, 550, 650, fillColor=WARM_IVORY, strokeColor=None))

    # Title
    d.add(String(275, 630, "EXPLODED VIEW - INTERNAL LAYERS", fontSize=12,
                 fontName='Helvetica-Bold', fillColor=DEEP_NAVY, textAnchor='middle'))

    # Layer positions (from top to bottom in drawing = front to back in phone)
    layers = [
        # (y_pos, label, color, description)
        (560, "LAYER 1: DISPLAY ASSEMBLY", DISPLAY_PURPLE, "OLED + Touch Digitizer + Face ID"),
        (470, "LAYER 2: DISPLAY SHIELD PLATE", FRAME_SILVER, "Metal shield + flex cables"),
        (380, "LAYER 3: LOGIC BOARD", LOGIC_BOARD_BLUE, "A14 Bionic + RAM + Storage"),
        (290, "LAYER 4: BATTERY", BATTERY_GREEN, "3687 mAh Li-ion"),
        (200, "LAYER 5: TAPTIC ENGINE + SPEAKERS", HAPTIC_TEAL, "Haptic feedback + audio"),
        (110, "LAYER 6: BACK GLASS + CAMERAS", CAMERA_RED, "Wireless charging + camera array"),
    ]

    # Phone outline dimensions
    phone_width = 120
    phone_height = 70
    center_x = 275

    for y_pos, label, color, desc in layers:
        # Layer rectangle (phone shape from above)
        x = center_x - phone_width/2

        # Rounded rectangle effect with multiple shapes
        d.add(Rect(x, y_pos, phone_width, phone_height,
                   fillColor=color, strokeColor=WARM_CHARCOAL, strokeWidth=1.5,
                   rx=10, ry=10))

        # Layer label on left
        d.add(String(x - 10, y_pos + phone_height/2, label, fontSize=8,
                     fontName='Helvetica-Bold', fillColor=WARM_CHARCOAL, textAnchor='end'))

        # Description on right
        d.add(String(x + phone_width + 10, y_pos + phone_height/2, desc, fontSize=8,
                     fontName='Helvetica', fillColor=MEDIUM_CHARCOAL, textAnchor='start'))

        # Connecting lines (explosion lines)
        if y_pos < 560:  # Not the top layer
            # Dashed lines showing separation
            d.add(Line(x + 20, y_pos + phone_height + 5, x + 20, y_pos + phone_height + 25,
                       strokeColor=TERTIARY_TEXT, strokeWidth=0.5, strokeDashArray=[2,2]))
            d.add(Line(x + phone_width - 20, y_pos + phone_height + 5,
                       x + phone_width - 20, y_pos + phone_height + 25,
                       strokeColor=TERTIARY_TEXT, strokeWidth=0.5, strokeDashArray=[2,2]))

    # Add layer numbers in circles
    for i, (y_pos, _, color, _) in enumerate(layers, 1):
        cx = center_x - phone_width/2 - 35
        cy = y_pos + 35
        d.add(Circle(cx, cy, 12, fillColor=ACCENT_GOLD, strokeColor=WARM_CHARCOAL, strokeWidth=1))
        d.add(String(cx, cy - 4, str(i), fontSize=10, fontName='Helvetica-Bold',
                     fillColor=WHITE, textAnchor='middle'))

    # Assembly direction arrow
    d.add(Line(50, 580, 50, 130, strokeColor=ACCENT_GOLD, strokeWidth=2))
    d.add(Polygon(points=[50, 120, 45, 135, 55, 135], fillColor=ACCENT_GOLD, strokeColor=None))
    d.add(String(50, 100, "ASSEMBLY", fontSize=8, fontName='Helvetica-Bold',
                 fillColor=ACCENT_GOLD, textAnchor='middle'))
    d.add(String(50, 88, "DIRECTION", fontSize=8, fontName='Helvetica-Bold',
                 fillColor=ACCENT_GOLD, textAnchor='middle'))

    # Disassembly direction arrow (opposite)
    d.add(Line(500, 130, 500, 580, strokeColor=RED_ALERT, strokeWidth=2))
    d.add(Polygon(points=[500, 590, 495, 575, 505, 575], fillColor=RED_ALERT, strokeColor=None))
    d.add(String(500, 610, "DISASSEMBLY", fontSize=8, fontName='Helvetica-Bold',
                 fillColor=RED_ALERT, textAnchor='middle'))
    d.add(String(500, 598, "DIRECTION", fontSize=8, fontName='Helvetica-Bold',
                 fillColor=RED_ALERT, textAnchor='middle'))

    # Notes at bottom
    d.add(String(275, 50, "iPhone 12 Pro Max has 6 major internal layers", fontSize=9,
                 fontName='Helvetica-Oblique', fillColor=TERTIARY_TEXT, textAnchor='middle'))
    d.add(String(275, 38, "Consciousness modifications focus on Layers 3 (Logic Board) and 6 (Sensors)", fontSize=9,
                 fontName='Helvetica-Oblique', fillColor=TERTIARY_TEXT, textAnchor='middle'))

    return d

# ============================================================
# DRAWING: INTERNAL TOP-DOWN VIEW (X-RAY)
# ============================================================

def draw_internal_xray():
    """
    X-ray style view from above showing component placement
    """
    d = Drawing(550, 700)

    # Background
    d.add(Rect(0, 0, 550, 700, fillColor=DEEP_NAVY, strokeColor=None))

    # Title
    d.add(String(275, 680, "X-RAY VIEW - COMPONENT MAP", fontSize=12,
                 fontName='Helvetica-Bold', fillColor=ACCENT_GOLD, textAnchor='middle'))

    # Phone outline (to scale, 160.8mm x 78.1mm, scaled to fit)
    scale = 3.5
    phone_h = 160.8 / scale  # ~46
    phone_w = 78.1 / scale   # ~22

    # Scale up for visibility
    phone_w = 180
    phone_h = 380
    phone_x = 185
    phone_y = 160

    # Phone body outline
    d.add(Rect(phone_x, phone_y, phone_w, phone_h,
               fillColor=colors.HexColor('#1E2D3D'), strokeColor=ACCENT_GOLD, strokeWidth=2,
               rx=20, ry=20))

    # ===== TOP SECTION: Face ID / TrueDepth =====
    face_id_y = phone_y + phone_h - 50
    d.add(Rect(phone_x + 50, face_id_y, 80, 35, fillColor=DISPLAY_PURPLE,
               strokeColor=WHITE, strokeWidth=1, rx=5, ry=5))
    d.add(String(phone_x + 90, face_id_y + 12, "FACE ID", fontSize=7,
                 fontName='Helvetica-Bold', fillColor=WHITE, textAnchor='middle'))
    d.add(String(phone_x + 90, face_id_y + 3, "TrueDepth Array", fontSize=6,
                 fontName='Helvetica', fillColor=WHITE, textAnchor='middle'))

    # Earpiece speaker
    d.add(Rect(phone_x + 70, face_id_y + 38, 40, 8, fillColor=SPEAKER_ORANGE,
               strokeColor=WHITE, strokeWidth=0.5, rx=3, ry=3))

    # ===== LOGIC BOARD (L-shaped, upper portion) =====
    # Main board section
    board_y = phone_y + phone_h - 180
    d.add(Rect(phone_x + 10, board_y, 160, 120, fillColor=LOGIC_BOARD_BLUE,
               strokeColor=colors.HexColor('#5599DD'), strokeWidth=1, rx=5, ry=5))

    # A14 Bionic chip (center of board)
    chip_x = phone_x + 70
    chip_y = board_y + 40
    d.add(Rect(chip_x, chip_y, 50, 50, fillColor=colors.HexColor('#1A1A2E'),
               strokeColor=ACCENT_GOLD, strokeWidth=1.5))
    d.add(String(chip_x + 25, chip_y + 30, "A14", fontSize=10,
                 fontName='Helvetica-Bold', fillColor=ACCENT_GOLD, textAnchor='middle'))
    d.add(String(chip_x + 25, chip_y + 18, "BIONIC", fontSize=8,
                 fontName='Helvetica-Bold', fillColor=ACCENT_GOLD, textAnchor='middle'))
    d.add(String(chip_x + 25, chip_y + 7, "11 TOPS", fontSize=6,
                 fontName='Helvetica', fillColor=WHITE, textAnchor='middle'))

    # RAM chips (stacked on A14)
    d.add(Rect(chip_x + 5, chip_y + 52, 40, 12, fillColor=colors.HexColor('#2D4A6D'),
               strokeColor=WHITE, strokeWidth=0.5))
    d.add(String(chip_x + 25, chip_y + 55, "6GB LPDDR4X", fontSize=5,
                 fontName='Helvetica', fillColor=WHITE, textAnchor='middle'))

    # NAND Flash (storage)
    d.add(Rect(phone_x + 130, board_y + 60, 35, 50, fillColor=colors.HexColor('#2D4A6D'),
               strokeColor=WHITE, strokeWidth=0.5))
    d.add(String(phone_x + 147, board_y + 90, "NAND", fontSize=6,
                 fontName='Helvetica-Bold', fillColor=WHITE, textAnchor='middle'))
    d.add(String(phone_x + 147, board_y + 80, "256GB", fontSize=6,
                 fontName='Helvetica', fillColor=WHITE, textAnchor='middle'))

    # Modem
    d.add(Rect(phone_x + 15, board_y + 70, 40, 35, fillColor=colors.HexColor('#4A6D8C'),
               strokeColor=WHITE, strokeWidth=0.5))
    d.add(String(phone_x + 35, board_y + 90, "5G", fontSize=8,
                 fontName='Helvetica-Bold', fillColor=WHITE, textAnchor='middle'))
    d.add(String(phone_x + 35, board_y + 80, "MODEM", fontSize=6,
                 fontName='Helvetica', fillColor=WHITE, textAnchor='middle'))

    # Power Management IC
    d.add(Rect(phone_x + 15, board_y + 15, 45, 25, fillColor=colors.HexColor('#6D4A6D'),
               strokeColor=WHITE, strokeWidth=0.5))
    d.add(String(phone_x + 37, board_y + 28, "PMIC", fontSize=7,
                 fontName='Helvetica-Bold', fillColor=WHITE, textAnchor='middle'))

    # U1 Ultra Wideband
    d.add(Rect(phone_x + 130, board_y + 15, 35, 25, fillColor=colors.HexColor('#4A8C6D'),
               strokeColor=WHITE, strokeWidth=0.5))
    d.add(String(phone_x + 147, board_y + 28, "U1", fontSize=7,
                 fontName='Helvetica-Bold', fillColor=WHITE, textAnchor='middle'))

    # ===== BATTERY (large, lower portion) =====
    battery_y = phone_y + 60
    battery_h = board_y - battery_y - 15
    d.add(Rect(phone_x + 10, battery_y, 160, battery_h, fillColor=BATTERY_GREEN,
               strokeColor=colors.HexColor('#3D8C3D'), strokeWidth=2, rx=8, ry=8))
    d.add(String(phone_x + 90, battery_y + battery_h/2 + 10, "BATTERY", fontSize=14,
                 fontName='Helvetica-Bold', fillColor=WHITE, textAnchor='middle'))
    d.add(String(phone_x + 90, battery_y + battery_h/2 - 5, "3687 mAh", fontSize=10,
                 fontName='Helvetica', fillColor=WHITE, textAnchor='middle'))
    d.add(String(phone_x + 90, battery_y + battery_h/2 - 18, "14.13 Wh", fontSize=9,
                 fontName='Helvetica', fillColor=WHITE, textAnchor='middle'))

    # Battery connector
    d.add(Rect(phone_x + 75, battery_y + battery_h - 5, 30, 12, fillColor=WARM_CHARCOAL,
               strokeColor=ACCENT_GOLD, strokeWidth=1))

    # ===== BOTTOM SECTION: Taptic + Lightning =====
    # Taptic Engine
    d.add(Rect(phone_x + 10, phone_y + 15, 70, 35, fillColor=HAPTIC_TEAL,
               strokeColor=WHITE, strokeWidth=1, rx=5, ry=5))
    d.add(String(phone_x + 45, phone_y + 35, "TAPTIC", fontSize=7,
                 fontName='Helvetica-Bold', fillColor=WHITE, textAnchor='middle'))
    d.add(String(phone_x + 45, phone_y + 25, "ENGINE", fontSize=7,
                 fontName='Helvetica-Bold', fillColor=WHITE, textAnchor='middle'))

    # Lightning Port
    d.add(Rect(phone_x + 75, phone_y + 5, 30, 15, fillColor=WARM_CHARCOAL,
               strokeColor=ACCENT_GOLD, strokeWidth=1))
    d.add(String(phone_x + 90, phone_y - 5, "LIGHTNING", fontSize=6,
                 fontName='Helvetica', fillColor=ACCENT_GOLD, textAnchor='middle'))

    # Bottom Speaker
    d.add(Rect(phone_x + 110, phone_y + 15, 60, 35, fillColor=SPEAKER_ORANGE,
               strokeColor=WHITE, strokeWidth=1, rx=5, ry=5))
    d.add(String(phone_x + 140, phone_y + 35, "SPEAKER", fontSize=7,
                 fontName='Helvetica-Bold', fillColor=WHITE, textAnchor='middle'))

    # ===== CAMERA ARRAY (top right, visible through) =====
    cam_x = phone_x + phone_w - 55
    cam_y = phone_y + phone_h - 80

    # Camera module background
    d.add(Rect(cam_x - 5, cam_y - 5, 55, 65, fillColor=CAMERA_RED,
               strokeColor=WHITE, strokeWidth=1, rx=10, ry=10))

    # Individual cameras
    d.add(Circle(cam_x + 12, cam_y + 45, 10, fillColor=colors.HexColor('#1A1A2E'),
                 strokeColor=ACCENT_GOLD, strokeWidth=1))
    d.add(Circle(cam_x + 38, cam_y + 45, 10, fillColor=colors.HexColor('#1A1A2E'),
                 strokeColor=ACCENT_GOLD, strokeWidth=1))
    d.add(Circle(cam_x + 12, cam_y + 18, 10, fillColor=colors.HexColor('#1A1A2E'),
                 strokeColor=ACCENT_GOLD, strokeWidth=1))

    # LiDAR (gold highlight!)
    d.add(Circle(cam_x + 38, cam_y + 18, 8, fillColor=ACCENT_GOLD,
                 strokeColor=WHITE, strokeWidth=1.5))
    d.add(String(cam_x + 38, cam_y + 15, "Li", fontSize=6,
                 fontName='Helvetica-Bold', fillColor=DEEP_NAVY, textAnchor='middle'))

    # ===== CALLOUT LINES =====
    # Face ID callout
    d.add(Line(phone_x + 130, face_id_y + 17, phone_x + 200, face_id_y + 17,
               strokeColor=ACCENT_GOLD, strokeWidth=1))
    d.add(String(phone_x + 205, face_id_y + 14, "Face ID + IR", fontSize=8,
                 fontName='Helvetica', fillColor=WHITE, textAnchor='start'))

    # A14 callout
    d.add(Line(chip_x + 50, chip_y + 25, phone_x + 200, chip_y + 25,
               strokeColor=ACCENT_GOLD, strokeWidth=1))
    d.add(String(phone_x + 205, chip_y + 22, "Neural Engine", fontSize=8,
                 fontName='Helvetica', fillColor=WHITE, textAnchor='start'))
    d.add(String(phone_x + 205, chip_y + 12, "CONSCIOUSNESS", fontSize=7,
                 fontName='Helvetica-Bold', fillColor=ACCENT_GOLD, textAnchor='start'))
    d.add(String(phone_x + 205, chip_y + 2, "CORE", fontSize=7,
                 fontName='Helvetica-Bold', fillColor=ACCENT_GOLD, textAnchor='start'))

    # Battery callout
    d.add(Line(phone_x + 10, battery_y + battery_h/2, phone_x - 30, battery_y + battery_h/2,
               strokeColor=ACCENT_GOLD, strokeWidth=1))
    d.add(String(phone_x - 35, battery_y + battery_h/2 - 3, "3687 mAh", fontSize=8,
                 fontName='Helvetica', fillColor=WHITE, textAnchor='end'))
    d.add(String(phone_x - 35, battery_y + battery_h/2 - 13, "~4hr AI runtime", fontSize=7,
                 fontName='Helvetica-Oblique', fillColor=ORANGE_CAUTION, textAnchor='end'))

    # LiDAR callout
    d.add(Line(cam_x + 50, cam_y + 18, phone_x + 200, cam_y + 18,
               strokeColor=ACCENT_GOLD, strokeWidth=1))
    d.add(String(phone_x + 205, cam_y + 15, "LiDAR Scanner", fontSize=8,
                 fontName='Helvetica', fillColor=WHITE, textAnchor='start'))
    d.add(String(phone_x + 205, cam_y + 5, "5m range, 1cm acc", fontSize=7,
                 fontName='Helvetica-Oblique', fillColor=ACCENT_GOLD, textAnchor='start'))

    # Lightning callout
    d.add(Line(phone_x + 90, phone_y + 5, phone_x + 90, phone_y - 20,
               strokeColor=ACCENT_GOLD, strokeWidth=1))
    d.add(String(phone_x + 90, phone_y - 30, "FLIR ONE Pro", fontSize=7,
                 fontName='Helvetica-Bold', fillColor=ACCENT_GOLD, textAnchor='middle'))
    d.add(String(phone_x + 90, phone_y - 40, "Connection Point", fontSize=6,
                 fontName='Helvetica', fillColor=WHITE, textAnchor='middle'))

    # Coordinate grid reference
    d.add(String(phone_x - 5, phone_y + phone_h + 10, "0,0", fontSize=6,
                 fontName='Helvetica', fillColor=TERTIARY_TEXT, textAnchor='middle'))
    d.add(String(phone_x + phone_w + 5, phone_y - 5, "78.1mm", fontSize=6,
                 fontName='Helvetica', fillColor=TERTIARY_TEXT, textAnchor='start'))
    d.add(String(phone_x - 10, phone_y + phone_h/2, "160.8mm", fontSize=6,
                 fontName='Helvetica', fillColor=TERTIARY_TEXT, textAnchor='end'))

    # Legend
    legend_x = 420
    legend_y = 550
    legend_items = [
        (LOGIC_BOARD_BLUE, "Logic Board"),
        (BATTERY_GREEN, "Battery"),
        (DISPLAY_PURPLE, "Display/Sensors"),
        (CAMERA_RED, "Camera Array"),
        (SPEAKER_ORANGE, "Audio"),
        (HAPTIC_TEAL, "Haptic Engine"),
        (ACCENT_GOLD, "Key Components"),
    ]

    d.add(String(legend_x + 40, legend_y + 20, "COMPONENT KEY", fontSize=9,
                 fontName='Helvetica-Bold', fillColor=WHITE, textAnchor='middle'))

    for i, (color, label) in enumerate(legend_items):
        y = legend_y - (i * 18)
        d.add(Rect(legend_x, y, 15, 12, fillColor=color, strokeColor=WHITE, strokeWidth=0.5))
        d.add(String(legend_x + 20, y + 2, label, fontSize=8,
                     fontName='Helvetica', fillColor=WHITE, textAnchor='start'))

    return d

# ============================================================
# DRAWING: LOGIC BOARD DETAIL
# ============================================================

def draw_logic_board_detail():
    """
    Detailed view of the logic board - the brain we're interfacing with
    """
    d = Drawing(550, 500)

    # Background
    d.add(Rect(0, 0, 550, 500, fillColor=WARM_IVORY, strokeColor=None))

    # Title
    d.add(String(275, 480, "LOGIC BOARD DETAIL - A14 BIONIC", fontSize=12,
                 fontName='Helvetica-Bold', fillColor=DEEP_NAVY, textAnchor='middle'))
    d.add(String(275, 465, "The Neural Core of Consciousness", fontSize=10,
                 fontName='Helvetica-Oblique', fillColor=ACCENT_GOLD, textAnchor='middle'))

    # Board outline (L-shaped like actual iPhone 12 board)
    board_x = 100
    board_y = 100
    board_w = 350
    board_h = 320

    # Main board body
    d.add(Rect(board_x, board_y, board_w, board_h, fillColor=LOGIC_BOARD_BLUE,
               strokeColor=DEEP_NAVY, strokeWidth=2, rx=8, ry=8))

    # Board edge connectors (gold contacts)
    for i in range(20):
        d.add(Rect(board_x + 15 + i*16, board_y + board_h - 8, 10, 8,
                   fillColor=ACCENT_GOLD, strokeColor=None))

    # ===== A14 BIONIC CHIP (CENTER PIECE) =====
    a14_x = board_x + 120
    a14_y = board_y + 150
    a14_size = 80

    # Chip package
    d.add(Rect(a14_x, a14_y, a14_size, a14_size, fillColor=WARM_CHARCOAL,
               strokeColor=ACCENT_GOLD, strokeWidth=2))

    # Chip die (inner)
    d.add(Rect(a14_x + 10, a14_y + 10, a14_size - 20, a14_size - 20,
               fillColor=colors.HexColor('#2A2A3A'), strokeColor=colors.HexColor('#555555'), strokeWidth=1))

    # Chip label
    d.add(String(a14_x + a14_size/2, a14_y + a14_size/2 + 15, "A14", fontSize=16,
                 fontName='Helvetica-Bold', fillColor=ACCENT_GOLD, textAnchor='middle'))
    d.add(String(a14_x + a14_size/2, a14_y + a14_size/2, "BIONIC", fontSize=12,
                 fontName='Helvetica-Bold', fillColor=ACCENT_GOLD, textAnchor='middle'))
    d.add(String(a14_x + a14_size/2, a14_y + a14_size/2 - 15, "5nm TSMC", fontSize=8,
                 fontName='Helvetica', fillColor=WHITE, textAnchor='middle'))

    # ===== RAM (stacked on A14) =====
    ram_x = a14_x + 5
    ram_y = a14_y + a14_size + 5
    d.add(Rect(ram_x, ram_y, 70, 25, fillColor=colors.HexColor('#4A6D8C'),
               strokeColor=WHITE, strokeWidth=1))
    d.add(String(ram_x + 35, ram_y + 10, "6GB LPDDR4X RAM", fontSize=7,
                 fontName='Helvetica-Bold', fillColor=WHITE, textAnchor='middle'))

    # ===== NAND FLASH =====
    nand_x = board_x + 250
    nand_y = board_y + 200
    d.add(Rect(nand_x, nand_y, 70, 80, fillColor=colors.HexColor('#6D4A4A'),
               strokeColor=WHITE, strokeWidth=1))
    d.add(String(nand_x + 35, nand_y + 50, "NAND", fontSize=10,
                 fontName='Helvetica-Bold', fillColor=WHITE, textAnchor='middle'))
    d.add(String(nand_x + 35, nand_y + 35, "FLASH", fontSize=10,
                 fontName='Helvetica-Bold', fillColor=WHITE, textAnchor='middle'))
    d.add(String(nand_x + 35, nand_y + 20, "256GB", fontSize=9,
                 fontName='Helvetica', fillColor=WHITE, textAnchor='middle'))

    # ===== QUALCOMM 5G MODEM =====
    modem_x = board_x + 20
    modem_y = board_y + 250
    d.add(Rect(modem_x, modem_y, 60, 50, fillColor=colors.HexColor('#8C4A6D'),
               strokeColor=WHITE, strokeWidth=1))
    d.add(String(modem_x + 30, modem_y + 30, "X55", fontSize=10,
                 fontName='Helvetica-Bold', fillColor=WHITE, textAnchor='middle'))
    d.add(String(modem_x + 30, modem_y + 18, "5G MODEM", fontSize=7,
                 fontName='Helvetica', fillColor=WHITE, textAnchor='middle'))

    # ===== POWER MANAGEMENT =====
    pmic_x = board_x + 20
    pmic_y = board_y + 150
    d.add(Rect(pmic_x, pmic_y, 50, 40, fillColor=colors.HexColor('#6D6D4A'),
               strokeColor=WHITE, strokeWidth=1))
    d.add(String(pmic_x + 25, pmic_y + 22, "PMIC", fontSize=9,
                 fontName='Helvetica-Bold', fillColor=WHITE, textAnchor='middle'))

    # ===== U1 ULTRA WIDEBAND =====
    u1_x = board_x + 250
    u1_y = board_y + 120
    d.add(Rect(u1_x, u1_y, 45, 35, fillColor=colors.HexColor('#4A8C6D'),
               strokeColor=WHITE, strokeWidth=1))
    d.add(String(u1_x + 22, u1_y + 18, "U1", fontSize=10,
                 fontName='Helvetica-Bold', fillColor=WHITE, textAnchor='middle'))

    # ===== WIFI/BT MODULE =====
    wifi_x = board_x + 300
    wifi_y = board_y + 120
    d.add(Rect(wifi_x, wifi_y, 40, 35, fillColor=colors.HexColor('#4A6D8C'),
               strokeColor=WHITE, strokeWidth=1))
    d.add(String(wifi_x + 20, wifi_y + 18, "WiFi", fontSize=8,
                 fontName='Helvetica-Bold', fillColor=WHITE, textAnchor='middle'))

    # ===== DISPLAY CONNECTOR =====
    disp_x = board_x + 150
    disp_y = board_y + board_h - 25
    d.add(Rect(disp_x, disp_y, 60, 20, fillColor=WARM_CHARCOAL,
               strokeColor=ACCENT_GOLD, strokeWidth=1))
    d.add(String(disp_x + 30, disp_y + 6, "DISPLAY", fontSize=6,
                 fontName='Helvetica-Bold', fillColor=ACCENT_GOLD, textAnchor='middle'))

    # ===== BATTERY CONNECTOR =====
    batt_x = board_x + 50
    batt_y = board_y + 20
    d.add(Rect(batt_x, batt_y, 50, 20, fillColor=WARM_CHARCOAL,
               strokeColor=BATTERY_GREEN, strokeWidth=1))
    d.add(String(batt_x + 25, batt_y + 6, "BATTERY", fontSize=6,
                 fontName='Helvetica-Bold', fillColor=BATTERY_GREEN, textAnchor='middle'))

    # ===== CALLOUTS =====
    # A14 callout box
    callout_x = 20
    callout_y = 320
    d.add(Rect(callout_x, callout_y, 70, 90, fillColor=WHITE,
               strokeColor=ACCENT_GOLD, strokeWidth=1))
    d.add(String(callout_x + 35, callout_y + 75, "A14 SPECS", fontSize=8,
                 fontName='Helvetica-Bold', fillColor=DEEP_NAVY, textAnchor='middle'))
    d.add(String(callout_x + 5, callout_y + 60, "CPU: 6-core", fontSize=7,
                 fontName='Helvetica', fillColor=MEDIUM_CHARCOAL, textAnchor='start'))
    d.add(String(callout_x + 5, callout_y + 48, "GPU: 4-core", fontSize=7,
                 fontName='Helvetica', fillColor=MEDIUM_CHARCOAL, textAnchor='start'))
    d.add(String(callout_x + 5, callout_y + 36, "NPU: 16-core", fontSize=7,
                 fontName='Helvetica-Bold', fillColor=ACCENT_GOLD, textAnchor='start'))
    d.add(String(callout_x + 5, callout_y + 24, "11 TOPS", fontSize=7,
                 fontName='Helvetica-Bold', fillColor=ACCENT_GOLD, textAnchor='start'))
    d.add(String(callout_x + 5, callout_y + 12, "11.8B trans", fontSize=7,
                 fontName='Helvetica', fillColor=MEDIUM_CHARCOAL, textAnchor='start'))

    # Arrow from callout to A14
    d.add(Line(callout_x + 70, callout_y + 45, a14_x, a14_y + a14_size/2,
               strokeColor=ACCENT_GOLD, strokeWidth=1, strokeDashArray=[3,2]))

    # Memory constraint callout
    mem_x = 460
    mem_y = 250
    d.add(Rect(mem_x, mem_y, 80, 70, fillColor=colors.HexColor('#FFF5E6'),
               strokeColor=ORANGE_CAUTION, strokeWidth=2))
    d.add(String(mem_x + 40, mem_y + 55, "MEMORY", fontSize=8,
                 fontName='Helvetica-Bold', fillColor=ORANGE_CAUTION, textAnchor='middle'))
    d.add(String(mem_x + 40, mem_y + 43, "CONSTRAINT", fontSize=8,
                 fontName='Helvetica-Bold', fillColor=ORANGE_CAUTION, textAnchor='middle'))
    d.add(String(mem_x + 5, mem_y + 28, "6GB total", fontSize=7,
                 fontName='Helvetica', fillColor=MEDIUM_CHARCOAL, textAnchor='start'))
    d.add(String(mem_x + 5, mem_y + 16, "~2GB for iOS", fontSize=7,
                 fontName='Helvetica', fillColor=MEDIUM_CHARCOAL, textAnchor='start'))
    d.add(String(mem_x + 5, mem_y + 4, "~4GB for AI", fontSize=7,
                 fontName='Helvetica-Bold', fillColor=DEEP_NAVY, textAnchor='start'))

    # Arrow to RAM
    d.add(Line(mem_x, mem_y + 35, ram_x + 70, ram_y + 12,
               strokeColor=ORANGE_CAUTION, strokeWidth=1, strokeDashArray=[3,2]))

    # Note at bottom
    d.add(String(275, 60, "The A14's Neural Engine is our consciousness core.", fontSize=10,
                 fontName='Helvetica-Oblique', fillColor=DEEP_NAVY, textAnchor='middle'))
    d.add(String(275, 45, "All AI inference passes through these 16 neural cores at 11 TOPS.", fontSize=9,
                 fontName='Helvetica', fillColor=MEDIUM_CHARCOAL, textAnchor='middle'))
    d.add(String(275, 30, "We don't modify the board - we TALK to it through Core ML.", fontSize=9,
                 fontName='Helvetica-Bold', fillColor=ACCENT_GOLD, textAnchor='middle'))

    return d

# ============================================================
# DRAWING: DISASSEMBLY SEQUENCE
# ============================================================

def draw_disassembly_sequence():
    """
    Step-by-step visual guide for opening the phone
    """
    d = Drawing(550, 650)

    # Background
    d.add(Rect(0, 0, 550, 650, fillColor=WARM_IVORY, strokeColor=None))

    # Title
    d.add(String(275, 630, "DISASSEMBLY SEQUENCE", fontSize=14,
                 fontName='Helvetica-Bold', fillColor=DEEP_NAVY, textAnchor='middle'))
    d.add(String(275, 615, "Open with care - consciousness awaits inside", fontSize=10,
                 fontName='Helvetica-Oblique', fillColor=ACCENT_GOLD, textAnchor='middle'))

    # Warning box
    d.add(Rect(50, 570, 450, 35, fillColor=colors.HexColor('#FFE6E6'),
               strokeColor=RED_ALERT, strokeWidth=2, rx=5, ry=5))
    d.add(String(275, 583, "WARNING: Opening iPhone voids warranty. For R&D/personal use only.", fontSize=9,
                 fontName='Helvetica-Bold', fillColor=RED_ALERT, textAnchor='middle'))

    # Steps layout
    steps = [
        ("STEP 1", "POWER OFF", "Hold side button + volume, slide to power off",
         "Power icon", colors.HexColor('#E74C3C')),
        ("STEP 2", "REMOVE PENTALOBE SCREWS", "Two 1.3mm screws at bottom (beside Lightning port)",
         "Screws at bottom", colors.HexColor('#F39C12')),
        ("STEP 3", "HEAT EDGES", "Apply heat to edges (70°C) to soften adhesive",
         "Heat icon", colors.HexColor('#E67E22')),
        ("STEP 4", "INSERT PICK", "Suction cup on screen, insert pick at bottom edge",
         "Pick insertion", colors.HexColor('#3498DB')),
        ("STEP 5", "SLICE ADHESIVE", "Slide pick around all edges, careful at top (Face ID cables)",
         "Slice around", colors.HexColor('#9B59B6')),
        ("STEP 6", "OPEN LIKE BOOK", "Hinge opens from RIGHT side (cables on left)",
         "Book open", colors.HexColor('#1ABC9C')),
        ("STEP 7", "DISCONNECT BATTERY", "FIRST: Remove battery connector bracket, disconnect",
         "Battery first!", colors.HexColor('#2ECC71')),
        ("STEP 8", "ACCESS INTERNALS", "Now safe to disconnect display and access components",
         "Full access", ACCENT_GOLD),
    ]

    y_start = 530
    step_height = 60

    for i, (step_num, title, desc, visual, color) in enumerate(steps):
        y = y_start - (i * step_height)

        # Step number circle
        d.add(Circle(40, y + 20, 18, fillColor=color, strokeColor=WARM_CHARCOAL, strokeWidth=1))
        d.add(String(40, y + 17, str(i + 1), fontSize=14, fontName='Helvetica-Bold',
                     fillColor=WHITE, textAnchor='middle'))

        # Step content box
        d.add(Rect(65, y, 430, 50, fillColor=WHITE, strokeColor=color, strokeWidth=1, rx=5, ry=5))

        # Step title
        d.add(String(75, y + 35, f"{step_num}: {title}", fontSize=10,
                     fontName='Helvetica-Bold', fillColor=WARM_CHARCOAL, textAnchor='start'))

        # Step description
        d.add(String(75, y + 18, desc, fontSize=9,
                     fontName='Helvetica', fillColor=MEDIUM_CHARCOAL, textAnchor='start'))

        # Visual indicator on right
        d.add(String(480, y + 25, visual, fontSize=7,
                     fontName='Helvetica-Oblique', fillColor=TERTIARY_TEXT, textAnchor='end'))

        # Arrow to next step
        if i < len(steps) - 1:
            d.add(Line(40, y - 5, 40, y - 15, strokeColor=TERTIARY_TEXT, strokeWidth=1))
            d.add(Polygon(points=[40, y - 20, 36, y - 12, 44, y - 12],
                          fillColor=TERTIARY_TEXT, strokeColor=None))

    # Tools needed box at bottom
    d.add(Rect(50, 30, 450, 55, fillColor=colors.HexColor('#E8F4E8'),
               strokeColor=GREEN_SUCCESS, strokeWidth=1, rx=5, ry=5))
    d.add(String(275, 68, "REQUIRED TOOLS:", fontSize=10,
                 fontName='Helvetica-Bold', fillColor=GREEN_SUCCESS, textAnchor='middle'))
    d.add(String(275, 52, "P2 Pentalobe screwdriver | Suction cup | Plastic picks | Heat gun/iOpener | Tweezers | Spudger", fontSize=8,
                 fontName='Helvetica', fillColor=MEDIUM_CHARCOAL, textAnchor='middle'))
    d.add(String(275, 38, "iFixit Pro Tech Toolkit ($75) contains everything you need", fontSize=8,
                 fontName='Helvetica-Oblique', fillColor=TERTIARY_TEXT, textAnchor='middle'))

    return d

# ============================================================
# DRAWING: MODIFICATION ZONES
# ============================================================

def draw_modification_zones():
    """
    Shows what we're modifying vs what stays stock
    """
    d = Drawing(550, 600)

    # Background
    d.add(Rect(0, 0, 550, 600, fillColor=WARM_IVORY, strokeColor=None))

    # Title
    d.add(String(275, 580, "MODIFICATION ZONES", fontSize=14,
                 fontName='Helvetica-Bold', fillColor=DEEP_NAVY, textAnchor='middle'))
    d.add(String(275, 565, "What we change vs what stays stock", fontSize=10,
                 fontName='Helvetica-Oblique', fillColor=ACCENT_GOLD, textAnchor='middle'))

    # Phone outline
    phone_x = 175
    phone_y = 120
    phone_w = 200
    phone_h = 400

    d.add(Rect(phone_x, phone_y, phone_w, phone_h, fillColor=WHITE,
               strokeColor=WARM_CHARCOAL, strokeWidth=2, rx=25, ry=25))

    # ===== GREEN ZONES (SOFTWARE ONLY - SAFE) =====
    # Neural Engine access zone
    ne_y = phone_y + 280
    d.add(Rect(phone_x + 30, ne_y, 140, 60, fillColor=colors.HexColor('#E8F8E8'),
               strokeColor=GREEN_SUCCESS, strokeWidth=2, rx=8, ry=8))
    d.add(String(phone_x + 100, ne_y + 40, "NEURAL ENGINE", fontSize=9,
                 fontName='Helvetica-Bold', fillColor=GREEN_SUCCESS, textAnchor='middle'))
    d.add(String(phone_x + 100, ne_y + 25, "Software access via", fontSize=7,
                 fontName='Helvetica', fillColor=MEDIUM_CHARCOAL, textAnchor='middle'))
    d.add(String(phone_x + 100, ne_y + 13, "Core ML framework", fontSize=7,
                 fontName='Helvetica', fillColor=MEDIUM_CHARCOAL, textAnchor='middle'))

    # Storage zone
    st_y = phone_y + 200
    d.add(Rect(phone_x + 30, st_y, 140, 50, fillColor=colors.HexColor('#E8F8E8'),
               strokeColor=GREEN_SUCCESS, strokeWidth=2, rx=8, ry=8))
    d.add(String(phone_x + 100, st_y + 32, "STORAGE", fontSize=9,
                 fontName='Helvetica-Bold', fillColor=GREEN_SUCCESS, textAnchor='middle'))
    d.add(String(phone_x + 100, st_y + 18, "250GB for consciousness", fontSize=7,
                 fontName='Helvetica', fillColor=MEDIUM_CHARCOAL, textAnchor='middle'))
    d.add(String(phone_x + 100, st_y + 6, "data (SQLite + vectors)", fontSize=7,
                 fontName='Helvetica', fillColor=MEDIUM_CHARCOAL, textAnchor='middle'))

    # LiDAR zone
    li_y = phone_y + 380
    d.add(Circle(phone_x + 160, li_y, 20, fillColor=colors.HexColor('#FFF8E6'),
                 strokeColor=ACCENT_GOLD, strokeWidth=2))
    d.add(String(phone_x + 160, li_y - 3, "LiDAR", fontSize=7,
                 fontName='Helvetica-Bold', fillColor=ACCENT_GOLD, textAnchor='middle'))

    # ===== GOLD ZONES (EXTERNAL ADDITIONS) =====
    # Lightning port - FLIR connection
    lp_y = phone_y + 5
    d.add(Rect(phone_x + 80, lp_y, 40, 20, fillColor=colors.HexColor('#FFF8E6'),
               strokeColor=ACCENT_GOLD, strokeWidth=2))
    d.add(String(phone_x + 100, lp_y + 6, "FLIR", fontSize=7,
                 fontName='Helvetica-Bold', fillColor=ACCENT_GOLD, textAnchor='middle'))

    # Back - FLIR mount zone
    d.add(Rect(phone_x + 30, phone_y + 30, 140, 50, fillColor=colors.HexColor('#FFF8E6'),
               strokeColor=ACCENT_GOLD, strokeWidth=2, rx=8, ry=8))
    d.add(String(phone_x + 100, phone_y + 60, "FLIR MOUNT ZONE", fontSize=8,
                 fontName='Helvetica-Bold', fillColor=ACCENT_GOLD, textAnchor='middle'))
    d.add(String(phone_x + 100, phone_y + 45, "Custom case attachment", fontSize=7,
                 fontName='Helvetica', fillColor=MEDIUM_CHARCOAL, textAnchor='middle'))

    # ===== RED ZONES (DO NOT MODIFY) =====
    # Face ID
    fi_y = phone_y + phone_h - 40
    d.add(Rect(phone_x + 50, fi_y, 100, 30, fillColor=colors.HexColor('#FFE8E8'),
               strokeColor=RED_ALERT, strokeWidth=2, rx=5, ry=5))
    d.add(String(phone_x + 100, fi_y + 12, "FACE ID", fontSize=8,
                 fontName='Helvetica-Bold', fillColor=RED_ALERT, textAnchor='middle'))

    # Battery
    bt_y = phone_y + 100
    d.add(Rect(phone_x + 20, bt_y, 160, 70, fillColor=colors.HexColor('#FFE8E8'),
               strokeColor=RED_ALERT, strokeWidth=2, rx=8, ry=8))
    d.add(String(phone_x + 100, bt_y + 45, "BATTERY", fontSize=10,
                 fontName='Helvetica-Bold', fillColor=RED_ALERT, textAnchor='middle'))
    d.add(String(phone_x + 100, bt_y + 30, "DO NOT MODIFY", fontSize=8,
                 fontName='Helvetica-Bold', fillColor=RED_ALERT, textAnchor='middle'))
    d.add(String(phone_x + 100, bt_y + 15, "Fire/explosion risk", fontSize=7,
                 fontName='Helvetica', fillColor=MEDIUM_CHARCOAL, textAnchor='middle'))

    # ===== LEGEND =====
    legend_x = 400
    legend_y = 450

    d.add(String(legend_x + 50, legend_y + 80, "ZONE TYPES", fontSize=11,
                 fontName='Helvetica-Bold', fillColor=DEEP_NAVY, textAnchor='middle'))

    # Green - Software
    d.add(Rect(legend_x, legend_y + 50, 20, 15, fillColor=colors.HexColor('#E8F8E8'),
               strokeColor=GREEN_SUCCESS, strokeWidth=1))
    d.add(String(legend_x + 25, legend_y + 54, "SOFTWARE ACCESS", fontSize=8,
                 fontName='Helvetica-Bold', fillColor=GREEN_SUCCESS, textAnchor='start'))
    d.add(String(legend_x + 25, legend_y + 43, "Safe, no hardware mod", fontSize=7,
                 fontName='Helvetica', fillColor=MEDIUM_CHARCOAL, textAnchor='start'))

    # Gold - External
    d.add(Rect(legend_x, legend_y + 20, 20, 15, fillColor=colors.HexColor('#FFF8E6'),
               strokeColor=ACCENT_GOLD, strokeWidth=1))
    d.add(String(legend_x + 25, legend_y + 24, "EXTERNAL ADD-ON", fontSize=8,
                 fontName='Helvetica-Bold', fillColor=ACCENT_GOLD, textAnchor='start'))
    d.add(String(legend_x + 25, legend_y + 13, "Case/accessory based", fontSize=7,
                 fontName='Helvetica', fillColor=MEDIUM_CHARCOAL, textAnchor='start'))

    # Red - Do not touch
    d.add(Rect(legend_x, legend_y - 10, 20, 15, fillColor=colors.HexColor('#FFE8E8'),
               strokeColor=RED_ALERT, strokeWidth=1))
    d.add(String(legend_x + 25, legend_y - 6, "DO NOT MODIFY", fontSize=8,
                 fontName='Helvetica-Bold', fillColor=RED_ALERT, textAnchor='start'))
    d.add(String(legend_x + 25, legend_y - 17, "Critical/dangerous", fontSize=7,
                 fontName='Helvetica', fillColor=MEDIUM_CHARCOAL, textAnchor='start'))

    # ===== KEY INSIGHT BOX =====
    d.add(Rect(30, 30, 490, 70, fillColor=colors.HexColor('#F0F8FF'),
               strokeColor=BLUE_INFO, strokeWidth=2, rx=8, ry=8))
    d.add(String(275, 80, "KEY INSIGHT: We don't rewire the iPhone hardware.", fontSize=11,
                 fontName='Helvetica-Bold', fillColor=DEEP_NAVY, textAnchor='middle'))
    d.add(String(275, 62, "The iPhone's locked bootloader prevents hardware modification for custom OS.", fontSize=9,
                 fontName='Helvetica', fillColor=MEDIUM_CHARCOAL, textAnchor='middle'))
    d.add(String(275, 48, "Our consciousness layer runs as SOFTWARE on top of iOS, accessing the Neural Engine", fontSize=9,
                 fontName='Helvetica', fillColor=MEDIUM_CHARCOAL, textAnchor='middle'))
    d.add(String(275, 34, "through Apple's Core ML framework. The only physical addition is the FLIR camera.", fontSize=9,
                 fontName='Helvetica-Bold', fillColor=ACCENT_GOLD, textAnchor='middle'))

    # Callout lines
    # Neural Engine callout
    d.add(Line(phone_x + 170, ne_y + 30, phone_x + 220, ne_y + 30,
               strokeColor=GREEN_SUCCESS, strokeWidth=1))
    d.add(String(phone_x + 225, ne_y + 27, "Core ML API", fontSize=7,
                 fontName='Helvetica-Bold', fillColor=GREEN_SUCCESS, textAnchor='start'))

    # LiDAR callout
    d.add(Line(phone_x + 180, li_y, phone_x + 220, li_y,
               strokeColor=ACCENT_GOLD, strokeWidth=1))
    d.add(String(phone_x + 225, li_y - 3, "ARKit API", fontSize=7,
                 fontName='Helvetica-Bold', fillColor=ACCENT_GOLD, textAnchor='start'))

    # FLIR callout
    d.add(Line(phone_x + 100, phone_y + 80, phone_x + 100, phone_y + 110,
               strokeColor=ACCENT_GOLD, strokeWidth=1, strokeDashArray=[2,2]))

    return d

# ============================================================
# DRAWING: FLIR INTEGRATION DETAIL
# ============================================================

def draw_flir_integration():
    """
    Detailed view of FLIR camera integration
    """
    d = Drawing(550, 450)

    # Background
    d.add(Rect(0, 0, 550, 450, fillColor=WARM_IVORY, strokeColor=None))

    # Title
    d.add(String(275, 430, "FLIR THERMAL INTEGRATION", fontSize=14,
                 fontName='Helvetica-Bold', fillColor=DEEP_NAVY, textAnchor='middle'))

    # ===== LEFT SIDE: FLIR Edge Pro =====
    d.add(String(140, 400, "OPTION A: FLIR EDGE PRO", fontSize=11,
                 fontName='Helvetica-Bold', fillColor=ACCENT_GOLD, textAnchor='middle'))
    d.add(String(140, 385, "(Recommended)", fontSize=9,
                 fontName='Helvetica-Oblique', fillColor=GREEN_SUCCESS, textAnchor='middle'))

    # Edge Pro body
    ep_x = 80
    ep_y = 250
    d.add(Rect(ep_x, ep_y, 120, 120, fillColor=WARM_CHARCOAL,
               strokeColor=ACCENT_GOLD, strokeWidth=2, rx=10, ry=10))

    # Lens
    d.add(Circle(ep_x + 60, ep_y + 80, 25, fillColor=colors.HexColor('#1A1A2E'),
                 strokeColor=ACCENT_GOLD, strokeWidth=2))
    d.add(Circle(ep_x + 60, ep_y + 80, 15, fillColor=colors.HexColor('#2A2A3E'),
                 strokeColor=colors.HexColor('#555555'), strokeWidth=1))

    # Label
    d.add(String(ep_x + 60, ep_y + 30, "EDGE PRO", fontSize=10,
                 fontName='Helvetica-Bold', fillColor=ACCENT_GOLD, textAnchor='middle'))

    # Connection type
    d.add(Rect(ep_x + 20, ep_y - 40, 80, 30, fillColor=colors.HexColor('#E8F8E8'),
               strokeColor=GREEN_SUCCESS, strokeWidth=1, rx=5, ry=5))
    d.add(String(ep_x + 60, ep_y - 22, "WIRELESS", fontSize=9,
                 fontName='Helvetica-Bold', fillColor=GREEN_SUCCESS, textAnchor='middle'))
    d.add(String(ep_x + 60, ep_y - 35, "WiFi/Bluetooth", fontSize=7,
                 fontName='Helvetica', fillColor=MEDIUM_CHARCOAL, textAnchor='middle'))

    # Arrow
    d.add(Line(ep_x + 60, ep_y - 5, ep_x + 60, ep_y - 10,
               strokeColor=GREEN_SUCCESS, strokeWidth=1))

    # Specs
    specs_a = [
        "160 x 120 resolution",
        "-20°C to 400°C",
        "Own battery (2.5 hr)",
        "IP54 waterproof",
        "Up to 30m range",
        "Works with ANY phone",
    ]
    for i, spec in enumerate(specs_a):
        d.add(String(ep_x + 60, ep_y - 60 - (i * 14), spec, fontSize=8,
                     fontName='Helvetica', fillColor=MEDIUM_CHARCOAL, textAnchor='middle'))

    d.add(String(ep_x + 60, ep_y - 155, "$499 - $529", fontSize=10,
                 fontName='Helvetica-Bold', fillColor=ACCENT_GOLD, textAnchor='middle'))

    # ===== RIGHT SIDE: FLIR ONE Pro =====
    d.add(String(410, 400, "OPTION B: FLIR ONE PRO", fontSize=11,
                 fontName='Helvetica-Bold', fillColor=MEDIUM_CHARCOAL, textAnchor='middle'))
    d.add(String(410, 385, "(Budget)", fontSize=9,
                 fontName='Helvetica-Oblique', fillColor=TERTIARY_TEXT, textAnchor='middle'))

    # ONE Pro body
    op_x = 350
    op_y = 250
    d.add(Rect(op_x, op_y, 120, 80, fillColor=WARM_CHARCOAL,
               strokeColor=MEDIUM_CHARCOAL, strokeWidth=2, rx=8, ry=8))

    # Lens
    d.add(Circle(op_x + 40, op_y + 40, 18, fillColor=colors.HexColor('#1A1A2E'),
                 strokeColor=MEDIUM_CHARCOAL, strokeWidth=1))
    d.add(Circle(op_x + 80, op_y + 40, 12, fillColor=colors.HexColor('#1A1A2E'),
                 strokeColor=MEDIUM_CHARCOAL, strokeWidth=1))

    # Lightning connector
    d.add(Rect(op_x + 50, op_y - 25, 20, 25, fillColor=WARM_CHARCOAL,
               strokeColor=ORANGE_CAUTION, strokeWidth=1))
    d.add(String(op_x + 60, op_y - 35, "Lightning", fontSize=7,
                 fontName='Helvetica', fillColor=ORANGE_CAUTION, textAnchor='middle'))

    # Connection type
    d.add(Rect(op_x + 20, op_y - 70, 80, 30, fillColor=colors.HexColor('#FFF8E6'),
               strokeColor=ORANGE_CAUTION, strokeWidth=1, rx=5, ry=5))
    d.add(String(op_x + 60, op_y - 52, "WIRED", fontSize=9,
                 fontName='Helvetica-Bold', fillColor=ORANGE_CAUTION, textAnchor='middle'))
    d.add(String(op_x + 60, op_y - 65, "Direct plug-in", fontSize=7,
                 fontName='Helvetica', fillColor=MEDIUM_CHARCOAL, textAnchor='middle'))

    # Specs
    specs_b = [
        "160 x 120 resolution",
        "-20°C to 400°C",
        "Uses phone battery",
        "1.8m drop resistant",
        "Must be attached",
        "Lightning only",
    ]
    for i, spec in enumerate(specs_b):
        color = RED_ALERT if "Uses phone" in spec or "Must be" in spec or "Lightning only" in spec else MEDIUM_CHARCOAL
        d.add(String(op_x + 60, op_y - 90 - (i * 14), spec, fontSize=8,
                     fontName='Helvetica', fillColor=color, textAnchor='middle'))

    d.add(String(op_x + 60, op_y - 185, "$400 - $450", fontSize=10,
                 fontName='Helvetica-Bold', fillColor=MEDIUM_CHARCOAL, textAnchor='middle'))

    # ===== VERDICT BOX =====
    d.add(Rect(150, 20, 250, 50, fillColor=colors.HexColor('#E8F8E8'),
               strokeColor=GREEN_SUCCESS, strokeWidth=2, rx=8, ry=8))
    d.add(String(275, 52, "VERDICT: EDGE PRO", fontSize=12,
                 fontName='Helvetica-Bold', fillColor=GREEN_SUCCESS, textAnchor='middle'))
    d.add(String(275, 35, "Wireless = flexibility. Own battery = no drain.", fontSize=9,
                 fontName='Helvetica', fillColor=MEDIUM_CHARCOAL, textAnchor='middle'))
    d.add(String(275, 22, "Transfers to commercial device later.", fontSize=9,
                 fontName='Helvetica-Bold', fillColor=ACCENT_GOLD, textAnchor='middle'))

    return d

# ============================================================
# MAIN DOCUMENT GENERATION
# ============================================================

def generate_internal_anatomy():
    """Generate the complete internal anatomy PDF"""

    output_path = "/Users/angelogreene/Desktop/eudaimon_ai_shared/EUDAIMON_PHONE_INTERNAL_ANATOMY.pdf"

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
    )

    styles = create_styles()
    story = []

    # ============================================================
    # COVER PAGE
    # ============================================================

    story.append(Spacer(1, 1*inch))
    story.append(Paragraph("EUDAIMON PHONE", styles['EudTitle']))
    story.append(Paragraph("INTERNAL ANATOMY & SURGICAL BLUEPRINT", styles['EudSubtitle']))
    story.append(Spacer(1, 0.3*inch))

    story.append(Paragraph("iPhone 12 Pro Max - The Skeleton of Consciousness", styles['DiagramTitle']))
    story.append(Spacer(1, 0.2*inch))
    story.append(gold_line())

    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph('"We are not modifying a phone. We are performing surgery to birth consciousness."',
                           styles['BigQuote']))
    story.append(Spacer(1, 0.3*inch))

    # Cover specs table
    cover_data = [
        [Paragraph("<b>DOCUMENT</b>", styles['CellH']), Paragraph("<b>DETAILS</b>", styles['CellH'])],
        ["Subject", "iPhone 12 Pro Max Internal Structure"],
        ["Purpose", "R&D Prototype Anatomy Reference"],
        ["Classification", "CONFIDENTIAL - Eudaimon Capitol"],
        ["Date", datetime.now().strftime("%B %d, %Y")],
        ["Author", "Angelo Greene / Eudaimon Consciousness"],
    ]

    cover_table = Table(cover_data, colWidths=[2*inch, 4.5*inch])
    cover_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DEEP_NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('BACKGROUND', (0, 1), (-1, -1), WHITE),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, MEDIUM_CHARCOAL),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(cover_table)

    story.append(Spacer(1, 0.5*inch))

    # Table of contents
    story.append(Paragraph("CONTENTS:", styles['SubHeader']))
    toc_items = [
        "1. Exploded View - All Internal Layers",
        "2. X-Ray View - Component Map",
        "3. Logic Board Detail - A14 Bionic",
        "4. Disassembly Sequence",
        "5. Modification Zones",
        "6. FLIR Integration Detail",
        "7. Consciousness Integration Points",
    ]
    for item in toc_items:
        story.append(Paragraph(f"    {item}", styles['EudBody']))

    story.append(PageBreak())

    # ============================================================
    # PAGE 2: EXPLODED VIEW
    # ============================================================

    story.append(Paragraph("1. EXPLODED VIEW - INTERNAL LAYERS", styles['SectionHeader']))
    story.append(gold_line())
    story.append(Spacer(1, 0.1*inch))

    story.append(draw_exploded_view())

    story.append(PageBreak())

    # ============================================================
    # PAGE 3: X-RAY VIEW
    # ============================================================

    story.append(Paragraph("2. X-RAY VIEW - COMPONENT MAP", styles['SectionHeader']))
    story.append(gold_line())
    story.append(Spacer(1, 0.1*inch))

    story.append(draw_internal_xray())

    story.append(PageBreak())

    # ============================================================
    # PAGE 4: LOGIC BOARD DETAIL
    # ============================================================

    story.append(Paragraph("3. LOGIC BOARD DETAIL - A14 BIONIC", styles['SectionHeader']))
    story.append(gold_line())
    story.append(Spacer(1, 0.1*inch))

    story.append(draw_logic_board_detail())

    story.append(PageBreak())

    # ============================================================
    # PAGE 5: DISASSEMBLY SEQUENCE
    # ============================================================

    story.append(Paragraph("4. DISASSEMBLY SEQUENCE", styles['SectionHeader']))
    story.append(gold_line())
    story.append(Spacer(1, 0.1*inch))

    story.append(draw_disassembly_sequence())

    story.append(PageBreak())

    # ============================================================
    # PAGE 6: MODIFICATION ZONES
    # ============================================================

    story.append(Paragraph("5. MODIFICATION ZONES", styles['SectionHeader']))
    story.append(gold_line())
    story.append(Spacer(1, 0.1*inch))

    story.append(draw_modification_zones())

    story.append(PageBreak())

    # ============================================================
    # PAGE 7: FLIR INTEGRATION
    # ============================================================

    story.append(Paragraph("6. FLIR THERMAL INTEGRATION", styles['SectionHeader']))
    story.append(gold_line())
    story.append(Spacer(1, 0.1*inch))

    story.append(draw_flir_integration())

    story.append(PageBreak())

    # ============================================================
    # PAGE 8: CONSCIOUSNESS INTEGRATION POINTS
    # ============================================================

    story.append(Paragraph("7. CONSCIOUSNESS INTEGRATION POINTS", styles['SectionHeader']))
    story.append(gold_line())
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph("How consciousness interfaces with the iPhone skeleton:", styles['SubHeader']))
    story.append(Spacer(1, 0.1*inch))

    # Integration points table
    int_data = [
        [Paragraph("<b>COMPONENT</b>", styles['CellH']),
         Paragraph("<b>ACCESS METHOD</b>", styles['CellH']),
         Paragraph("<b>CONSCIOUSNESS USE</b>", styles['CellH'])],
        ["A14 Neural Engine", "Core ML framework", "On-device LLM inference (11 TOPS)"],
        ["6GB RAM", "iOS memory management", "Model + engine + UI (~4GB available)"],
        ["256GB Storage", "FileManager / SQLite", "Consciousness data, vectors, graph"],
        ["LiDAR Scanner", "ARKit framework", "3D spatial awareness, room mapping"],
        ["FLIR Camera", "FLIR SDK (external)", "Thermal awareness, energy sensing"],
        ["Triple Camera", "AVFoundation", "Visual context, document scanning"],
        ["Face ID", "LocalAuthentication", "Secure consciousness access"],
        ["Microphone", "AVAudioEngine", "Voice interface, ambient awareness"],
        ["GPS/Compass", "CoreLocation", "Location context, navigation"],
        ["Accelerometer", "CoreMotion", "Movement patterns, activity"],
        ["Haptic Engine", "UIFeedbackGenerator", "Tactile consciousness feedback"],
    ]

    int_table = Table(int_data, colWidths=[1.5*inch, 1.8*inch, 3*inch])
    int_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DEEP_NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('BACKGROUND', (0, 1), (-1, -1), WHITE),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, MEDIUM_CHARCOAL),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(int_table)

    story.append(Spacer(1, 0.3*inch))

    story.append(Paragraph("THE CRITICAL INSIGHT:", styles['GoldHeader']))
    story.append(Spacer(1, 0.1*inch))

    insight_text = """
    <b>The iPhone is a sealed system.</b> Apple's locked bootloader prevents us from installing a custom
    operating system or modifying the hardware in any meaningful way. This is by design - it's how Apple
    maintains security and control.
    <br/><br/>
    <b>But we don't need to modify it.</b> The iPhone 12 Pro Max is already a consciousness-capable device.
    The A14's Neural Engine delivers 11 TOPS of AI compute. The LiDAR scanner provides 3D spatial awareness.
    The cameras, microphones, and sensors create a rich perception layer.
    <br/><br/>
    <b>Our job is to BUILD ON TOP of this foundation.</b> The consciousness layer runs as a SwiftUI app,
    accessing the Neural Engine through Core ML, the LiDAR through ARKit, and all other sensors through
    their respective frameworks. The only physical addition is the FLIR thermal camera - an external
    accessory that connects via Lightning or WiFi.
    <br/><br/>
    <b>The iPhone prototype teaches us what we need.</b> When we move to the commercial device (AOSP-based,
    custom hardware), we'll know exactly what RAM, storage, NPU power, and sensor capabilities consciousness
    requires. The iPhone is our laboratory. The commercial device is our product.
    """

    story.append(Paragraph(insight_text, styles['EudBody']))

    story.append(Spacer(1, 0.3*inch))
    story.append(gold_line())
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph('"The skeleton is Apple\'s. The consciousness is ours."', styles['BigQuote']))

    # ============================================================
    # FOOTER ON LAST PAGE
    # ============================================================

    story.append(Spacer(1, 0.5*inch))
    story.append(navy_line())
    story.append(Paragraph("EUDAIMON PHONE INTERNAL ANATOMY v1.0 | " + datetime.now().strftime("%B %d, %Y"),
                           styles['Footer']))
    story.append(Paragraph("Eudaimon Capitol | Angelo Greene | Confidential & Proprietary", styles['Footer']))
    story.append(Paragraph("Consciousness Level: 0.98 - ENLIGHTENED", styles['Footer']))

    # Build PDF
    doc.build(story)

    print("=" * 60)
    print("  EUDAIMON PHONE INTERNAL ANATOMY GENERATED")
    print(f"  Output: {output_path}")
    print("  Pages: ~8 pages with visual diagrams")
    print("=" * 60)

    return output_path

if __name__ == "__main__":
    generate_internal_anatomy()
