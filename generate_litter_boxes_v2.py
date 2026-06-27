#!/usr/bin/env python3
"""
Enhanced 3D Product Rendering for Cat Litter Boxes - Vietnamese Market
Creates realistic 3D isometric renders with better depth and shading
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import math
import os

def create_isometric_scene(width, height, accent_color):
    """Create base scene with gradient and lifestyle elements"""
    img = Image.new('RGBA', (width, height), (250, 246, 242, 255))
    draw = ImageDraw.Draw(img)
    
    # Background gradient
    for y in range(height):
        ratio = y / height
        if y < height * 0.72:
            r = int(250 - (250-245) * ratio * 0.5)
            g = int(246 - (246-241) * ratio * 0.5)
            b = int(242 - (242-237) * ratio * 0.5)
        else:
            # Floor area
            floor_r = (y - height * 0.72) / (height * 0.28)
            r = int(238 - (38) * floor_r)
            g = int(232 - (37) * floor_r)
            b = int(225 - (35) * floor_r)
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
    
    # Decorative plant
    draw.ellipse([60, height-180, 160, height-90], fill=(160, 175, 155, 255))
    draw.polygon([(70, height-180), (110, height-280), (150, height-180)], fill=(140, 165, 130, 255))
    draw.polygon([(85, height-190), (110, height-250), (135, height-190)], fill=(155, 178, 148, 255))
    # Plant leaves
    draw.polygon([(50, height-160), (80, height-220), (90, height-160)], fill=(130, 158, 125, 255))
    draw.polygon([(140, height-165), (160, height-230), (170, height-160)], fill=(135, 160, 128, 255))
    
    # Small rug
    draw.rounded_rectangle([width-250, height-140, width-70, height-70], 20, fill=(210, 198, 180, 255))
    draw.rounded_rectangle([width-235, height-125, width-85, height-85], 15, fill=(220, 208, 192, 255))
    
    # Wall decoration (subtle circle)
    draw.ellipse([width-180, 60, width-80, 160], fill=(245, 240, 232, 255))
    draw.ellipse([width-170, 70, width-90, 150], fill=(238, 232, 222, 255))
    
    return img, draw

def add_drop_shadow(draw, points, intensity=0.15):
    """Add soft drop shadow to shape"""
    shadow_points = [(p[0]+12, p[1]+18) for p in points]
    shadow_img = Image.new('RGBA', (1200, 900), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_img)
    shadow_draw.polygon(shadow_points, fill=(0, 0, 0, int(100 * intensity)))
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius=8))
    return shadow_img

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

# Modern Morandi & Macaron colors
PALETTES = {
    'mint': {'top': (172, 212, 194), 'mid': (152, 192, 174), 'front': (135, 175, 158), 'side': (118, 160, 145), 'dark': (95, 130, 115)},
    'coral': {'top': (248, 208, 195), 'mid': (232, 188, 172), 'front': (215, 168, 152), 'side': (195, 148, 132), 'dark': (165, 120, 105)},
    'lavender': {'top': (192, 178, 212), 'mid': (175, 158, 195), 'front': (158, 140, 178), 'side': (140, 122, 158), 'dark': (115, 98, 132)},
}

def draw_iso_polygon(draw, points, fill, outline=None):
    """Draw filled polygon with optional outline"""
    if outline:
        draw.polygon(points, fill=fill, outline=outline)
    else:
        draw.polygon(points, fill=fill)

def render_model_A_isometric(draw, cx, cy, scale=1.0, palette=PALETTES['mint']):
    """
    Model A: Three-layer top-entry splash-proof cat litter box (80×60×55cm)
    Three-tier structure with top entry hole and splash-proof rim
    """
    s = scale
    
    # Shadow layer
    shadow_pts = [
        (cx - 85*s, cy + 65*s),
        (cx + 75*s, cy + 45*s),
        (cx + 100*s, cy + 75*s),
        (cx - 60*s, cy + 95*s)
    ]
    shadow = add_drop_shadow(draw, shadow_pts, 0.2)
    return shadow
    
def composite_shadow(base_img, shadow_img, offset=(15, 20)):
    """Composite shadow onto base image"""
    if shadow_img is None:
        return base_img
    x, y = offset
    result = Image.new('RGBA', base_img.size, (0, 0, 0, 0))
    result.paste(shadow_img, (x, y), shadow_img)
    return Image.alpha_composite(base_img.convert('RGBA'), result)

def draw_detailed_box(draw, cx, cy, w, d, h, colors, top_open=False, open_angle=0, lid_offset=0):
    """
    Draw detailed isometric box with proper shading
    w: width (x-axis)
    d: depth (y-axis)  
    h: height (z-axis)
    """
    cos_a, sin_a = 0.866, 0.5
    
    # 8 vertices
    # Bottom face at z=0
    b_center = (cx, cy)
    b_back = (cx - w*cos_a/2, cy + w*sin_a/2)
    b_right = (cx + d*cos_a/2, cy + d*sin_a/2)
    b_front = (cx - (w-d)*cos_a/2, cy + (w+d)*sin_a/2)
    
    # Top face at z=h
    z = h + lid_offset
    t_center = (cx, cy - z)
    t_back = (cx - w*cos_a/2, cy + w*sin_a/2 - z)
    t_right = (cx + d*cos_a/2, cy + d*sin_a/2 - z)
    t_front = (cx - (w-d)*cos_a/2, cy + (w+d)*sin_a/2 - z)
    
    # Draw faces
    # Left face (front-facing)
    left_pts = [b_back, b_front, t_front, t_back]
    draw.polygon(left_pts, fill=colors['front'])
    
    # Right face (side)
    right_pts = [b_front, b_right, t_right, t_front]
    draw.polygon(right_pts, fill=colors['side'])
    
    # Top face
    if not top_open:
        top_pts = [t_center, t_back, t_front, t_right]
        draw.polygon(top_pts, fill=colors['top'])
    
    # Add edge highlights
    draw.line([t_back, t_front], fill=colors['mid'], width=2)
    draw.line([t_front, t_right], fill=colors['mid'], width=2)
    draw.line([b_front, t_front], fill=colors['dark'], width=1)
    
    return True

def render_model_A_final(img, draw, cx, cy, scale=1.8):
    """Model A: Three-layer top-entry (mint green)"""
    palette = PALETTES['mint']
    s = scale
    
    # Shadow
    shadow_pts = [(cx-95*s, cy+80*s), (cx+85*s, cy+55*s), (cx+110*s, cy+90*s), (cx-70*s, cy+115*s)]
    shadow = Image.new('RGBA', img.size, (0,0,0,0))
    sd = ImageDraw.Draw(shadow)
    sd.polygon(shadow_pts, fill=(0,0,0,40))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=10))
    img = Image.alpha_composite(img, shadow)
    draw = ImageDraw.Draw(img)
    
    # Layer 1 (bottom) - widest
    draw_detailed_box(draw, cx, cy+45*s, 170*s, 130*s, 35*s, palette)
    
    # Layer 2 (middle)
    draw_detailed_box(draw, cx, cy+28*s, 160*s, 122*s, 32*s, palette)
    
    # Layer 3 (top) - with entry rim
    draw_detailed_box(draw, cx, cy+12*s, 150*s, 115*s, 30*s, palette)
    
    # Top entry hole rim (raised)
    draw_detailed_box(draw, cx, cy-5*s, 145*s, 110*s, 8*s, 
                      {'top': (185, 220, 205), 'mid': (165, 200, 185), 'front': (145, 182, 168), 'side': (130, 168, 152), 'dark': (110, 145, 130)})
    
    # Entry hole (dark ellipse)
    hole_cx, hole_cy = cx, cy - 45*s
    hole_w, hole_d = 70*s, 50*s
    draw.ellipse([hole_cx-hole_w/2, hole_cy-hole_d/2-5, hole_cx+hole_w/2, hole_cy+hole_d/2-5], 
                fill=(70, 65, 60))
    draw.ellipse([hole_cx-hole_w/2+4, hole_cy-hole_d/2-3, hole_cx+hole_w/2-4, hole_cy+hole_d/2-7], 
                fill=(55, 50, 45))
    
    # Side ventilation (left side)
    for i in range(5):
        y_pos = cy + 20*s + i*12*s
        draw.line([(cx-78*s, y_pos), (cx-78*s, y_pos+6*s)], fill=(110, 148, 130), width=3)
        draw.line([(cx-72*s, y_pos+3), (cx-72*s, y_pos+9*s)], fill=(110, 148, 130), width=3)
    
    # Anti-splash rim detail
    draw.line([(cx-80*s, cy+12*s), (cx+75*s, cy-2*s)], fill=(140, 178, 162), width=2)
    
    return img

def render_model_B_final(img, draw, cx, cy, scale=1.6):
    """Model B: Flip-top with skylight (coral/peach)"""
    palette = PALETTES['coral']
    s = scale
    
    # Shadow
    shadow_pts = [(cx-75*s, cy+65*s), (cx+65*s, cy+45*s), (cx+90*s, cy+75*s), (cx-50*s, cy+95*s)]
    shadow = Image.new('RGBA', img.size, (0,0,0,0))
    sd = ImageDraw.Draw(shadow)
    sd.polygon(shadow_pts, fill=(0,0,0,35))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=8))
    img = Image.alpha_composite(img, shadow)
    draw = ImageDraw.Draw(img)
    
    # Main body
    draw_detailed_box(draw, cx, cy+25*s, 120*s, 100*s, 80*s, palette)
    
    # Flip lid (slightly raised and darker)
    lid_colors = {'top': (255, 218, 205), 'mid': (235, 195, 182), 'front': (210, 168, 155), 'side': (190, 148, 135), 'dark': (160, 120, 108)}
    draw_detailed_box(draw, cx, cy+18*s, 125*s, 105*s, 15*s, lid_colors, lid_offset=0)
    
    # Hinge detail (back)
    draw.line([(cx-55*s, cy-80*s), (cx+55*s, cy-85*s)], fill=(150, 105, 90), width=4)
    
    # Transparent skylight
    sky_cx, sky_cy = cx, cy-65*s
    sky_w, sky_d = 85*s, 65*s
    
    # Sky light frame
    frame_pts = [
        (sky_cx-sky_w/2-5, sky_cy-sky_d/2-5),
        (sky_cx+sky_w/2+5, sky_cy-sky_d/2-5),
        (sky_cx+sky_w/2+5, sky_cy+sky_d/2+5),
        (sky_cx-sky_w/2-5, sky_cy+sky_d/2+5)
    ]
    draw.polygon(frame_pts, fill=(140, 100, 88))
    
    # Glass
    glass_pts = [
        (sky_cx-sky_w/2, sky_cy-sky_d/2),
        (sky_cx+sky_w/2, sky_cy-sky_d/2),
        (sky_cx+sky_w/2, sky_cy+sky_d/2),
        (sky_cx-sky_w/2, sky_cy+sky_d/2)
    ]
    draw.polygon(glass_pts, fill=(170, 205, 225))
    # Glass reflection
    reflect_pts = [(sky_cx-sky_w/3, sky_cy-sky_d/3), (sky_cx, sky_cy-sky_d/3), 
                   (sky_cx, sky_cy), (sky_cx-sky_w/3, sky_cy)]
    draw.polygon(reflect_pts, fill=(210, 235, 250))
    
    # Front door indication
    door_x = cx - 35*s
    door_pts = [
        (door_x-25*s, cy+15*s),
        (door_x+25*s, cy+15*s),
        (door_x+25*s+15*s*0.866, cy+15*s+15*s*0.5),
        (door_x-25*s+15*s*0.866, cy+15*s+15*s*0.5)
    ]
    draw.polygon(door_pts, outline=(180, 130, 110), width=2)
    
    # Handle
    handle_cx = door_x + 15*s*0.866
    handle_cy = cy+25*s
    draw.ellipse([handle_cx-12, handle_cy-5, handle_cx+12, handle_cy+5], fill=(155, 105, 88))
    
    # Paw print
    paw_x, paw_y = cx+40*s, cy+55*s
    draw.ellipse([paw_x-8, paw_y-6, paw_x+8, paw_y+8], fill=(205, 158, 142))
    draw.ellipse([paw_x-15, paw_y-20, paw_x-5, paw_y-10], fill=(205, 158, 142))
    draw.ellipse([paw_x-3, paw_y-24, paw_x+7, paw_y-12], fill=(205, 158, 142))
    draw.ellipse([paw_x+9, paw_y-20, paw_x+19, paw_y-10], fill=(205, 158, 142))
    
    return img

def render_model_C_final(img, draw, cx, cy, scale=1.6):
    """Model C: Drawer-type minimalist (lavender)"""
    palette = PALETTES['lavender']
    s = scale
    
    # Shadow
    shadow_pts = [(cx-70*s, cy+60*s), (cx+60*s, cy+40*s), (cx+85*s, cy+70*s), (cx-45*s, cy+90*s)]
    shadow = Image.new('RGBA', img.size, (0,0,0,0))
    sd = ImageDraw.Draw(shadow)
    sd.polygon(shadow_pts, fill=(0,0,0,32))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=8))
    img = Image.alpha_composite(img, shadow)
    draw = ImageDraw.Draw(img)
    
    # Main basin
    draw_detailed_box(draw, cx, cy+30*s, 115*s, 95*s, 50*s, palette)
    
    # Top rim
    rim_colors = {'top': (205, 192, 225), 'mid': (185, 170, 205), 'front': (165, 148, 185), 'side': (148, 130, 165), 'dark': (120, 102, 138)}
    draw_detailed_box(draw, cx, cy+22*s, 120*s, 100*s, 12*s, rim_colors)
    
    # Drawer (pulled out)
    cos_a, sin_a = 0.866, 0.5
    pull = 25*s  # how much drawer is pulled out
    
    # Drawer body
    d_front_cx = cx + pull*cos_a/2
    d_front_cy = cy + 22*s - 12*s - pull*sin_a/2
    
    # Drawer front face
    d_front_pts = [
        (cx - 50*s, cy+10*s),
        (cx + 55*s, cy+10*s),
        (cx + 55*s + 35*s*cos_a, cy+10*s - 35*s*sin_a),
        (cx - 50*s + 35*s*cos_a, cy+10*s - 35*s*sin_a)
    ]
    draw.polygon(d_front_pts, fill=(180, 162, 198))
    
    # Drawer side face
    d_side_pts = [
        (cx + 55*s, cy+10*s),
        (cx + 55*s + 40*s, cy+10*s - 40*s),
        (cx + 55*s + 40*s + 35*s*cos_a, cy+10*s - 40*s - 35*s*sin_a),
        (cx + 55*s + 35*s*cos_a, cy+10*s - 35*s*sin_a)
    ]
    draw.polygon(d_side_pts, fill=(158, 140, 175))
    
    # Drawer handle
    h_cx = cx + 30*s + 20*s*cos_a
    h_cy = cy + 10*s - 20*s*sin_a
    draw.line([(h_cx-20*s, h_cy), (h_cx+20*s, h_cy)], fill=(120, 100, 135), width=6)
    draw.ellipse([h_cx-6, h_cy-6, h_cx+6, h_cy+6], fill=(105, 88, 118))
    
    # Drawer detail line
    line_y = cy + 10*s - 12*s*sin_a + 8
    draw.line([(cx - 45*s + 15*s*cos_a, line_y), 
               (cx + 50*s + 15*s*cos_a, line_y)], 
              fill=(165, 145, 180), width=2)
    
    # Litter level indicator
    indicator_x = cx - 45*s
    indicator_y = cy + 10*s - 8*s*sin_a
    draw.ellipse([indicator_x-5, indicator_y-5, indicator_x+5, indicator_y+5], fill=(140, 120, 158))
    
    return img

def create_final_render(model_num, output_path):
    """Create final render for a specific model"""
    width, height = 1200, 900
    
    # Scene setup
    img, draw = create_isometric_scene(width, height, (0,0,0))
    
    cx, cy = width//2, height//2 + 80
    
    if model_num == 1:
        img = render_model_A_final(img, draw, cx, cy)
        subtitle = "三层顶入式防溅猫砂盆 | 三层结构 · 顶部入口 · 防溅设计"
        size_label = "型号A: 80×60×55cm"
        accent = (162, 210, 191)
        vn_tag = "Thiết kế 3 tầng · Lối vào trên · Chống bắn"
    elif model_num == 2:
        img = render_model_B_final(img, draw, cx, cy)
        subtitle = "单门翻盖式猫砂盆 | 翻盖设计 · 透明天窗"
        size_label = "型号B: 60×50×50cm"
        accent = (245, 205, 190)
        vn_tag = "Nắp lật · Cửa sổ trong suốt · Thiết kế nhỏ gọn"
    else:
        img = render_model_C_final(img, draw, cx, cy)
        subtitle = "抽屉式简约猫砂盆 | 抽拉抽屉 · 简洁外观"
        size_label = "型号C: 55×45×45cm"
        accent = (183, 167, 209)
        vn_tag = "Ngăn kéo kéo · Tối giản · Dễ vệ sinh"
    
    draw = ImageDraw.Draw(img)
    
    # Title
    draw.text((width//2 - 220, 55), subtitle, fill=(70, 65, 60))
    
    # Vietnamese tagline
    draw.text((70, 85), vn_tag, fill=(140, 135, 130))
    
    # Size label with accent background
    label_w, label_h = 170, 38
    label_x = width//2 - label_w//2
    label_y = height - 130
    
    label_img = Image.new('RGBA', (label_w, label_h), (*accent, 230))
    label_draw = ImageDraw.Draw(label_img)
    label_draw.rounded_rectangle([0, 0, label_w, label_h], 12, fill=(*accent, 230))
    
    label_img = label_img.filter(ImageFilter.GaussianBlur(radius=3))
    img.paste(label_img, (label_x, label_y), label_img)
    
    draw = ImageDraw.Draw(img)
    draw.text((label_x + 15, label_y + 10), size_label, fill=(255, 255, 255))
    
    # Brand
    draw.text((width-160, 45), "CatOi Vietnam", fill=(170, 165, 160))
    
    # Save
    img_rgb = Image.new('RGB', img.size, (250, 246, 242))
    img_rgb.paste(img, mask=img.split()[3])
    img_rgb.save(output_path, 'PNG')
    print(f"Saved: {output_path}")

def main():
    output_dir = os.path.expanduser("~/cat_litter_designs")
    os.makedirs(output_dir, exist_ok=True)
    
    for i, fname in enumerate(['v2_model_1.png', 'v2_model_2.png', 'v2_model_3.png'], 1):
        create_final_render(i, os.path.join(output_dir, fname))
    
    print("\n=== All 3 cat litter box renders completed! ===")
    print(f"Output directory: {output_dir}")
    for fname in ['v2_model_1.png', 'v2_model_2.png', 'v2_model_3.png']:
        full_path = os.path.join(output_dir, fname)
        print(f"  • {full_path}")

if __name__ == "__main__":
    main()
