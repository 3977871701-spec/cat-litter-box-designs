#!/usr/bin/env python3
"""
Cat Litter Box V3 - Vietnamese Market
Based on e-commerce reference images (Pinduoduo hot sellers)
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

# Output directory
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

# Color palettes matching reference images
PALETTES = {
    'A': {  # Model A: Full-enclosed luxury, gray-beige + dark gray
        'name': 'Model A - Full Enclosed',
        'top': (200, 195, 185),
        'mid': (180, 175, 165),
        'front': (160, 155, 145),
        'side': (140, 135, 125),
        'dark': (100, 95, 88),
        'base': (90, 88, 82),
        'litter': (215, 208, 198),
    },
    'B': {  # Model B: Corridor type, white + light gray
        'name': 'Model B - Corridor Style',
        'top': (245, 242, 238),
        'mid': (230, 228, 224),
        'front': (215, 212, 208),
        'side': (195, 192, 188),
        'dark': (165, 162, 158),
        'base': (200, 198, 195),
        'litter': (230, 225, 218),
    },
    'C': {  # Model C: Cute fresh, milk white + light pink
        'name': 'Model C - Cute Fresh',
        'top': (252, 248, 245),
        'mid': (248, 240, 238),
        'front': (240, 232, 230),
        'side': (225, 218, 215),
        'dark': (195, 182, 178),
        'base': (238, 225, 222),
        'litter': (245, 238, 232),
    },
}

def draw_iso_box(draw, cx, cy, w, h, d, palette, top_visible=True):
    """Draw an isometric box (3 visible faces)"""
    sw, sh = 1.0, 0.6  # isometric scale factors
    
    # 8 corners of the box
    # Top face parallelogram
    tl = (cx - w*sw, cy - h*sh)
    tr = (cx + w*sw, cy - h*sh)
    br = (cx + w*sw, cy)
    bl = (cx - w*sw, cy)
    
    # Bottom face (offset down by depth)
    bo_tl = (cx - w*sw, cy + d*sh)
    bo_tr = (cx + w*sw, cy + d*sh)
    bo_br = (cx + w*sw, cy + d)
    bo_bl = (cx - w*sw, cy + d)
    
    # Left face (front-left)
    lf_tl = (cx - w*sw, cy)
    lf_tr = (cx, cy + h*sh)
    lf_br = (cx, cy + h*sh + d)
    lf_bl = (cx - w*sw, cy + d)
    
    # Right face (front-right)  
    rf_tl = (cx, cy + h*sh)
    rf_tr = (cx + w*sw, cy)
    rf_br = (cx + w*sw, cy + d)
    rf_bl = (cx, cy + h*sh + d)
    
    if top_visible:
        # Top face
        draw.polygon([tl, tr, br, bl], fill=palette['top'])
    
    # Front-left face
    draw.polygon([lf_tl, lf_tr, lf_br, lf_bl], fill=palette['front'])
    
    # Front-right face  
    draw.polygon([rf_tl, rf_tr, rf_br, rf_bl], fill=palette['side'])
    
    return {
        'top': (tl, tr, br, bl),
        'front_left': (lf_tl, lf_tr, lf_br, lf_bl),
        'front_right': (rf_tl, rf_tr, rf_br, rf_bl),
    }

def create_scene(width=1200, height=900):
    """Create background scene"""
    img = Image.new('RGB', (width, height), (250, 246, 242))
    draw = ImageDraw.Draw(img)
    
    # Background gradient
    for y in range(height):
        ratio = y / height
        if y < height * 0.72:
            r = int(250 - (5) * ratio * 0.5)
            g = int(246 - (5) * ratio * 0.5)
            b = int(242 - (5) * ratio * 0.5)
        else:
            floor_r = (y - height * 0.72) / (height * 0.28)
            r = int(238 - 38 * floor_r)
            g = int(232 - 37 * floor_r)
            b = int(225 - 35 * floor_r)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Simple plant decoration
    draw.ellipse([80, height-200, 160, height-110], fill=(165, 180, 162))
    draw.polygon([(90, height-195), (120, height-280), (150, height-195)], fill=(145, 168, 148))
    
    return img, draw

def load_font(size=20):
    """Try to load a suitable font"""
    font_paths = [
        '/System/Library/Fonts/PingFang.ttc',
        '/System/Library/Fonts/STHeiti Light.ttc',
        '/Library/Fonts/Arial.ttf',
        '/System/Library/Fonts/Helvetica.ttc',
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except:
                pass
    return ImageFont.load_default()

def add_label(draw, text, x, y, font, color=(80, 75, 70)):
    """Add text label"""
    draw.text((x, y), text, fill=color, font=font)

def draw_model_A(draw, cx, cy, scale=1.0):
    """Model A: Full-enclosed luxury cat litter box - 80x60x55cm"""
    p = PALETTES['A']
    w, h, d = 160 * scale, 110 * scale, 90 * scale
    
    # Draw base/drawer at bottom
    base_h = 20 * scale
    draw_iso_box(draw, cx, cy + h + d - base_h, w, base_h*0.6, d, {
        'top': p['base'],
        'front': p['dark'],
        'side': p['dark'],
    })
    
    # Main body
    draw_iso_box(draw, cx, cy + d, w, h, d, {
        'top': p['top'],
        'mid': p['mid'],
        'front': p['front'],
        'side': p['side'],
    })
    
    # Top dome/hood
    dome_h = 60 * scale
    dome_top = cy + d - h*0.3
    # Draw dome shape using ellipses
    dome_cx = cx
    dome_cy = dome_top
    dome_w = w * 1.05
    dome_h_vert = dome_h * 0.8
    
    # Dome top surface
    draw.ellipse([dome_cx - dome_w, dome_cy - dome_h_vert*0.3,
                  dome_cx + dome_w, dome_cy + dome_h_vert*0.5],
                 fill=p['top'])
    
    # Dome front curve (using arc)
    draw.arc([dome_cx - dome_w, dome_cy - dome_h_vert,
              dome_cx + dome_w, dome_cy + dome_h_vert*1.5],
             0, 180, fill=p['front'], width=3)
    
    # Entry hole on top
    hole_w, hole_h = w*0.5, h*0.25
    draw.ellipse([dome_cx - hole_w, dome_cy - hole_h*0.3 - dome_h_vert*0.2,
                  dome_cx + hole_w, dome_cy + hole_h*0.7 - dome_h_vert*0.2],
                 fill=(50, 48, 45))
    
    # Cat inside silhouette
    cat_y = dome_cy + 20
    draw.ellipse([dome_cx - 30, cat_y - 25, dome_cx + 30, cat_y + 20], fill=(60, 58, 55))
    
    return cx, cy

def draw_model_B(draw, cx, cy, scale=1.0):
    """Model B: Corridor style - 62cm long corridor, white + gray"""
    p = PALETTES['B']
    
    # Main body
    body_w, body_h, body_d = 130 * scale, 80 * scale, 100 * scale
    draw_iso_box(draw, cx, cy + body_d, body_w, body_h, body_d, {
        'top': p['top'],
        'front': p['front'],
        'side': p['side'],
    })
    
    # Corridor (long tunnel entrance)
    corr_w, corr_h, corr_d = 60 * scale, 50 * scale, 100 * scale
    corr_x = cx - body_w * 0.8
    draw_iso_box(draw, corr_x, cy + corr_d, corr_w, corr_h, corr_d, {
        'top': p['mid'],
        'front': p['front'],
        'side': p['dark'],
    })
    
    # Corridor entrance hole
    hole_cx = corr_x
    hole_cy = cy + corr_d - corr_h * 0.3
    hole_rx = corr_w * 0.8
    hole_ry = corr_h * 0.4
    draw.ellipse([hole_cx - hole_rx, hole_cy - hole_ry,
                  hole_cx + hole_rx, hole_cy + hole_ry],
                 fill=(60, 58, 56))
    
    # Drawer at bottom
    drawer_h = 18 * scale
    drawer_y = cy + body_d - drawer_h
    dw = body_w * 1.1
    draw_iso_box(draw, cx, drawer_y, dw, drawer_h*0.5, body_d * 0.8, {
        'top': p['base'],
        'front': p['dark'],
        'side': p['dark'],
    })
    
    # Litter in main body (visible through translucent effect)
    lit_cx = cx + 10
    lit_cy = cy + body_d - 5
    draw.ellipse([lit_cx - 60, lit_cy - 15, lit_cx + 60, lit_cy + 10],
                 fill=p['litter'])
    
    return cx, cy

def draw_model_C(draw, cx, cy, scale=1.0):
    """Model C: Cute fresh style - milk white + light pink, compact"""
    p = PALETTES['C']
    
    # Rounded body (approximate with standard box)
    body_w, body_h, body_d = 110 * scale, 75 * scale, 85 * scale
    
    # Draw with rounded corners effect
    draw_iso_box(draw, cx, cy + body_d, body_w, body_h, body_d, {
        'top': p['top'],
        'front': p['front'],
        'side': p['side'],
    })
    
    # Soft top cover
    cover_h = 35 * scale
    cover_cy = cy + body_d - body_h * 0.2
    cover_w = body_w * 1.1
    
    # Rounded top
    draw.ellipse([cx - cover_w, cover_cy - cover_h,
                  cx + cover_w, cover_cy + cover_h * 0.6],
                 fill=p['mid'])
    
    # Entry hole with pink rim
    hole_cx = cx
    hole_cy = cover_cy - cover_h * 0.1
    hole_rx = body_w * 0.45
    hole_ry = cover_h * 0.5
    draw.ellipse([hole_cx - hole_rx, hole_cy - hole_ry,
                  hole_cx + hole_rx, hole_cy + hole_ry],
                 fill=(50, 48, 45))
    # Pink rim
    draw.ellipse([hole_cx - hole_rx - 4, hole_cy - hole_ry - 4,
                  hole_cx + hole_rx + 4, hole_cy + hole_ry + 4],
                 fill=p['dark'])
    draw.ellipse([hole_cx - hole_rx, hole_cy - hole_ry,
                  hole_cx + hole_rx, hole_cy + hole_ry],
                 fill=(50, 48, 45))
    
    # Cute handle on front
    handle_x = cx + body_w * 0.6
    handle_y = cy + body_d + body_h * 0.3
    draw.rounded_rectangle([handle_x - 15, handle_y - 8,
                            handle_x + 15, handle_y + 8],
                           6, fill=p['base'])
    
    # Drawer
    drawer_h = 15 * scale
    drawer_y = cy + body_d - drawer_h
    dw = body_w * 1.05
    draw_iso_box(draw, cx, drawer_y, dw, drawer_h*0.5, body_d*0.7, {
        'top': p['base'],
        'front': p['dark'],
        'side': p['dark'],
    })
    
    # Pink accent stripe
    stripe_y = cy + body_d + body_h * 0.15
    draw.rectangle([cx - body_w*0.9, stripe_y, cx + body_w*0.9, stripe_y + 6],
                   fill=p['base'])
    
    return cx, cy

def render_model(model_id):
    """Render a single model"""
    width, height = 1200, 900
    img, draw = create_scene(width, height)
    font = load_font(24)
    font_sm = load_font(18)
    
    cx, cy = width // 2, height // 2 - 50
    
    if model_id == 'A':
        draw_model_A(draw, cx, cy, scale=1.2)
        # Labels
        add_label(draw, "Hộp cát mèo kín full", cx - 130, height - 200, font, (60, 58, 55))
        add_label(draw, "80×60×55cm · Khử mùi", cx - 130, height - 170, font_sm, (100, 98, 92))
        add_label(draw, "Chống văng · Ngăn kéo", cx - 130, height - 145, font_sm, (100, 98, 92))
        add_label(draw, "CaiOi Vietnam", width - 200, 70, font, (120, 115, 108))
        add_label(draw, "Cỡ lớn", width - 200, 100, font_sm, (140, 135, 128))
        
    elif model_id == 'B':
        draw_model_B(draw, cx, cy, scale=1.1)
        add_label(draw, "Hành lang kín full", cx - 130, height - 200, font, (60, 58, 55))
        add_label(draw, "62cm siêu dài", cx - 130, height - 170, font_sm, (100, 98, 92))
        add_label(draw, "Chống văng · Khử mùi", cx - 130, height - 145, font_sm, (100, 98, 92))
        add_label(draw, "CaiOi Vietnam", width - 200, 70, font, (120, 115, 108))
        add_label(draw, "Siêu bền", width - 200, 100, font_sm, (140, 135, 128))
        
    elif model_id == 'C':
        draw_model_C(draw, cx, cy, scale=1.15)
        add_label(draw, "Hộp cát bé xinh", cx - 130, height - 200, font, (60, 58, 55))
        add_label(draw, "55×45×45cm · Dễ sạch", cx - 130, height - 170, font_sm, (100, 98, 92))
        add_label(draw, "10 giây xúc cát", cx - 130, height - 145, font_sm, (100, 98, 92))
        add_label(draw, "CaiOi Vietnam", width - 200, 70, font, (120, 115, 108))
        add_label(draw, "Hồng nhạt", width - 200, 100, font_sm, (140, 135, 128))
    
    # Model number badge
    draw.rounded_rectangle([50, 50, 110, 95], 10, fill=(180, 175, 168))
    add_label(draw, f"Model", 58, 55, font_sm, (255, 255, 255))
    add_label(draw, f"{model_id}", 68, 75, font, (255, 255, 255))
    
    return img

# Generate all 3 models
for model_id in ['A', 'B', 'C']:
    print(f"Generating Model {model_id}...")
    img = render_model(model_id)
    out_path = os.path.join(OUT_DIR, f'v3_model_{model_id.lower()}.png')
    img.save(out_path, 'PNG', quality=95)
    print(f"  Saved: {out_path} ({img.size})")

print("\nDone! All 3 models generated.")
for model_id in ['A', 'B', 'C']:
    p = os.path.join(OUT_DIR, f'v3_model_{model_id.lower()}.png')
    if os.path.exists(p):
        print(f"  ✓ v3_model_{model_id.lower()}.png")