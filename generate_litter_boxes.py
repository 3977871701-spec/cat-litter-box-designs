#!/usr/bin/env python3
"""
3D Product Rendering for Cat Litter Boxes - Vietnamese Market
Creates realistic 3D isometric renders of 3 cat litter box designs
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import math
import os

# Color palettes - Modern Morandi & Macaron colors
COLORS = {
    'mint': (162, 210, 191),      # 薄荷绿
    'coral': (235, 179, 159),     # 珊瑚粉
    'lavender': (183, 167, 209),  # 薰衣草紫
    'cream': (245, 240, 230),     # 奶油白
    'gray_blue': (156, 179, 189), # 灰蓝
    'sage': (178, 190, 166),      # 鼠尾草绿
    'peach': (247, 201, 179),     # 蜜桃粉
    'dusty_pink': (219, 183, 183),# 灰粉
    'sky': (175, 207, 220),       # 天空蓝
    'warm_gray': (180, 170, 160), # 暖灰
}

def hex_to_rgb(hex_color):
    h = hex_color.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def draw_isometric_box(draw, cx, cy, width, depth, height, top_color, front_color, side_color, corner_radius=8):
    """Draw an isometric box with rounded corners"""
    w, d, h = width, depth, height
    
    # Isometric projection angles
    cos_a, sin_a = 0.866, 0.5  # 30 degrees
    
    # Calculate 8 vertices
    # Center bottom
    cbx, cby = cx, cy
    
    # Bottom face vertices
    b0 = (cbx, cby)  # center
    b1 = (cbx - w*cos_a/2, cby + w*sin_a/2)  # left-back
    b2 = (cbx + d*cos_a/2, cby + d*sin_a/2)  # right-front
    b3 = (cbx - (w-d)*cos_a/2, cby + (w+d)*sin_a/2)  # left-front
    
    # Top face vertices (at height h)
    t0 = (cbx, cby - h)
    t1 = (cbx - w*cos_a/2, cby + w*sin_a/2 - h)
    t2 = (cbx + d*cos_a/2, cby + d*sin_a/2 - h)
    t3 = (cbx - (w-d)*cos_a/2, cby + (w+d)*sin_a/2 - h)
    
    # Front face (left-facing)
    front_points = [b1, b3, t3, t1]
    draw.polygon(front_points, fill=front_color)
    
    # Side face (right-facing)  
    side_points = [b3, b2, t2, t3]
    draw.polygon(side_points, fill=side_color)
    
    # Top face
    top_points = [t0, t1, t3, t2]
    draw.polygon(top_points, fill=top_color)
    
    return True

def draw_rounded_rect(draw, xy, radius, fill):
    """Draw a rounded rectangle"""
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill)

def create_scene_background(draw, width, height, seed=0):
    """Create a lifestyle scene background"""
    # Gradient background
    for y in range(height):
        ratio = y / height
        r = int(248 + (220 - 248) * ratio)
        g = int(244 + (235 - 244) * ratio)
        b = int(240 + (230 - 240) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Add subtle floor pattern
    floor_y = int(height * 0.75)
    for y in range(floor_y, height):
        ratio = (y - floor_y) / (height - floor_y)
        r = int(220 + (180 - 220) * ratio)
        g = int(210 + (175 - 210) * ratio)
        b = int(200 + (170 - 200) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Add some decorative elements (plant, mat)
    # Plant pot
    draw.ellipse([50, height-120, 110, height-60], fill=(165, 180, 160))
    draw.polygon([(55, height-120), (80, height-180), (105, height-120)], fill=(140, 170, 130))
    draw.polygon([(65, height-130), (80, height-170), (95, height-130)], fill=(155, 185, 145))
    
    # Small mat/rug
    draw.rounded_rectangle([width-180, height-100, width-50, height-50], 10, fill=(210, 195, 180))

def render_model_A(draw, cx, cy, scale=1.0):
    """
    Model A: Three-layer top-entry splash-proof cat litter box (80×60×55cm)
    Features: Three tiers, top entry hole, splash-proof walls
    """
    # Main body - large three-layer structure
    main_w, main_d, main_h = 160 * scale, 120 * scale, 100 * scale
    
    # Colors - Mint green Morandi
    top_c = (175, 210, 195)
    front_c = (145, 185, 165)
    side_c = (125, 170, 150)
    
    # Draw main body (three-tier appearance)
    # Bottom tier
    draw_isometric_box(draw, cx, cy+30*scale, 160*scale, 120*scale, 35*scale, 
                       (180, 215, 200), (140, 180, 160), (120, 165, 145))
    
    # Middle tier
    draw_isometric_box(draw, cx, cy+10*scale, 150*scale, 112*scale, 35*scale,
                       (175, 212, 198), (138, 182, 158), (118, 168, 148))
    
    # Top tier  
    draw_isometric_box(draw, cx, cy-10*scale, 140*scale, 105*scale, 35*scale,
                       top_c, front_c, side_c)
    
    # Top entry hole (dark ellipse)
    cos_a, sin_a = 0.866, 0.5
    hole_cx, hole_cy = cx, cy - 45*scale
    hole_w, hole_d = 60*scale, 40*scale
    
    # Hole shadow
    draw.ellipse([hole_cx-hole_w/2, hole_cy-hole_d/2, 
                  hole_cx+hole_w/2, hole_cy+hole_d/2], fill=(80, 75, 70))
    # Hole inner
    draw.ellipse([hole_cx-hole_w/2+3, hole_cy-hole_d/2+2, 
                  hole_cx+hole_w/2-3, hole_cy+hole_d/2-2], fill=(60, 55, 50))
    
    # Entry rim (raised)
    rim_points = [
        (hole_cx-hole_w/2-5*scale, hole_cy-hole_d/2-5*scale),
        (hole_cx+hole_w/2+5*scale, hole_cy-hole_d/2-5*scale),
        (hole_cx+hole_w/2+5*scale, hole_cy+hole_d/2+5*scale),
        (hole_cx-hole_w/2-5*scale, hole_cy+hole_d/2+5*scale)
    ]
    draw.polygon(rim_points, fill=(160, 195, 180))
    
    # Splash-proof outer rim
    outer_rim_w = 170*scale
    outer_rim_d = 128*scale
    draw_isometric_box(draw, cx, cy-18*scale, outer_rim_w, outer_rim_d, 8*scale,
                       (185, 218, 205), (150, 188, 168), (130, 172, 155))
    
    # Side ventilation grilles
    for i in range(4):
        offset = (i - 1.5) * 25*scale
        draw.line([(cx - 70*scale + offset, cy+15*scale), 
                   (cx - 70*scale + offset, cy+25*scale)], fill=(115, 155, 138), width=3)
    
    # Decorative logo area
    draw.rounded_rectangle([cx-15*scale, cy+50*scale, cx+15*scale, cy+58*scale], 
                           3, fill=(165, 198, 180))

def render_model_B(draw, cx, cy, scale=1.0):
    """
    Model B: Single-door flip-top cat litter box with transparent skylight (60×50×50cm)
    Features: Hinged lid, transparent top window, compact design
    """
    # Colors - Coral/Peach Macaron
    main_top = (245, 205, 190)
    main_front = (220, 175, 160)
    main_side = (200, 155, 145)
    
    # Main body
    body_h = 85*scale
    draw_isometric_box(draw, cx, cy+20*scale, 120*scale, 100*scale, body_h,
                       main_top, main_front, main_side)
    
    # Flip lid (slightly raised)
    lid_offset = 8*scale
    draw_isometric_box(draw, cx, cy+20*scale-lid_offset, 124*scale, 104*scale, 12*scale,
                       (255, 215, 200), (225, 180, 165), (205, 160, 150))
    
    # Transparent skylight
    cos_a, sin_a = 0.866, 0.5
    sky_cx, sky_cy = cx, cy+20*scale-lid_offset-6*scale
    sky_w, sky_d = 80*scale, 60*scale
    
    # Skylight frame
    draw.ellipse([sky_cx-sky_w/2-4*scale, sky_cy-sky_d/2-4*scale,
                  sky_cx+sky_w/2+4*scale, sky_cy+sky_d/2+4*scale], fill=(180, 140, 130))
    # Transparent glass effect
    draw.ellipse([sky_cx-sky_w/2, sky_cy-sky_d/2,
                  sky_cx+sky_w/2, sky_cy+sky_d/2], fill=(175, 207, 220, 180))
    # Glass highlight
    draw.ellipse([sky_cx-sky_w/3, sky_cy-sky_d/3,
                  sky_cx, sky_cy], fill=(200, 230, 240, 120))
    
    # Front door (flip open indication)
    door_w = 50*scale
    door_h = 40*scale
    door_cx = cx - 30*scale
    door_cy = cy + 30*scale
    
    # Door outline
    door_pts = [
        (door_cx - door_w/2, door_cy),
        (door_cx + door_w/2, door_cy),
        (door_cx + door_w/2 + door_h*cos_a/2, door_cy + door_h*sin_a/2),
        (door_cx - door_w/2 + door_h*cos_a/2, door_cy + door_h*sin_a/2)
    ]
    draw.polygon(door_pts, outline=(180, 130, 115), width=2)
    
    # Handle
    handle_x = door_cx + 15*scale
    handle_y = door_cy + 15*scale
    draw.ellipse([handle_x-8*scale, handle_y-4*scale, handle_x+8*scale, handle_y+4*scale],
                fill=(160, 110, 95))
    
    # Paw print decoration
    center_x, center_y = cx + 35*scale, cy + 50*scale
    draw.ellipse([center_x-5*scale, center_y-4*scale, center_x+5*scale, center_y+5*scale],
                fill=(210, 165, 150))  # main pad
    draw.ellipse([center_x-10*scale, center_y-14*scale, center_x-4*scale, center_y-6*scale],
                fill=(210, 165, 150))  # toe 1
    draw.ellipse([center_x-2*scale, center_y-16*scale, center_x+4*scale, center_y-8*scale],
                fill=(210, 165, 150))  # toe 2
    draw.ellipse([center_x+4*scale, center_y-14*scale, center_x+10*scale, center_y-6*scale],
                fill=(210, 165, 150))  # toe 3

def render_model_C(draw, cx, cy, scale=1.0):
    """
    Model C: Drawer-type minimalist cat litter box with front drawer (55×45×45cm)
    Features: Pull-out drawer at front, clean minimalist lines
    """
    # Colors - Lavender Morandi
    body_top = (195, 180, 210)
    body_front = (170, 150, 185)
    body_side = (155, 135, 170)
    
    drawer_front = (185, 165, 200)
    drawer_side = (165, 145, 178)
    
    # Main basin (lower section)
    basin_h = 55*scale
    draw_isometric_box(draw, cx, cy+25*scale, 110*scale, 90*scale, basin_h,
                       (200, 185, 215), body_front, body_side)
    
    # Upper rim
    rim_h = 10*scale
    draw_isometric_box(draw, cx, cy+25*scale-basin_h, 115*scale, 95*scale, rim_h,
                       (208, 192, 220), (178, 158, 192), (162, 142, 178))
    
    # Drawer (pulled out slightly)
    drawer_pull = 15*scale  # how much drawer is pulled out
    drawer_h = 35*scale
    
    # Drawer body
    cos_a, sin_a = 0.866, 0.5
    drawer_cx = cx + drawer_pull * cos_a / 2
    drawer_cy = cy + 25*scale - basin_h - drawer_pull * sin_a / 2
    
    # Drawer front face
    d_front_pts = [
        (cx - 50*scale, cy + 25*scale - basin_h + 5*scale),
        (cx + 55*scale, cy + 25*scale - basin_h + 5*scale),
        (cx + 55*scale + 20*scale*cos_a, cy + 25*scale - basin_h + 5*scale + 20*scale*sin_a),
        (cx - 50*scale + 20*scale*cos_a, cy + 25*scale - basin_h + 5*scale + 20*scale*sin_a)
    ]
    draw.polygon(d_front_pts, fill=drawer_front)
    
    # Drawer side face
    d_side_pts = [
        (cx + 55*scale, cy + 25*scale - basin_h + 5*scale),
        (cx + 55*scale + 35*scale, cy + 25*scale - basin_h + 5*scale - 35*scale),
        (cx + 55*scale + 35*scale + 20*scale*cos_a, cy + 25*scale - basin_h + 5*scale + 20*scale*sin_a - 35*scale),
        (cx + 55*scale + 20*scale*cos_a, cy + 25*scale - basin_h + 5*scale + 20*scale*sin_a)
    ]
    draw.polygon(d_side_pts, fill=drawer_side)
    
    # Drawer handle
    handle_cx = cx + 30*scale + 10*scale*cos_a
    handle_cy = cy + 25*scale - basin_h + 5*scale + 10*scale*sin_a
    handle_len = 30*scale
    draw.line([(handle_cx - handle_len/2, handle_cy), 
               (handle_cx + handle_len/2, handle_cy)],
             fill=(140, 120, 160), width=5)
    draw.ellipse([handle_cx-4*scale, handle_cy-4*scale, handle_cx+4*scale, handle_cy+4*scale],
                fill=(130, 110, 150))
    
    # Litter indicator line on drawer
    draw.line([(cx - 45*scale + 20*scale*cos_a, cy + 25*scale - basin_h + 15*scale + 20*scale*sin_a),
               (cx + 50*scale + 20*scale*cos_a, cy + 25*scale - basin_h + 15*scale + 20*scale*sin_a)],
              fill=(160, 140, 175), width=2)

def add_shadow(draw, cx, cy, width, depth, intensity=0.3):
    """Add soft shadow under the product"""
    cos_a, sin_a = 0.866, 0.5
    shadow_pts = [
        (cx - width*cos_a/2 + 10, cy + width*sin_a/2 + 15),
        (cx + depth*cos_a/2 + 10, cy + depth*sin_a/2 + 15),
        (cx + depth*cos_a/2 - width*cos_a/2 + 20, cy + depth*sin_a/2 + width*sin_a/2 + 20)
    ]
    shadow = Image.new('RGBA', draw.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.polygon(shadow_pts, fill=(0, 0, 0, int(80 * intensity)))
    return shadow

def add_product_label(draw, x, y, text, scale=1.0):
    """Add product label text"""
    font_size = int(14 * scale)
    draw.text((x, y), text, fill=(100, 95, 90))

def render_all_models():
    """Render all three cat litter box models"""
    output_dir = os.path.expanduser("~/cat_litter_designs")
    os.makedirs(output_dir, exist_ok=True)
    
    width, height = 1200, 900
    
    models = [
        ("v2_model_1.png", render_model_A, "三层顶入式防溅猫砂盆 | 三层结构 · 顶部入口 · 防溅设计", 
         "型号A: 80×60×55cm", (162, 210, 191)),
        ("v2_model_2.png", render_model_B, "单门翻盖式猫砂盆 | 翻盖设计 · 透明天窗", 
         "型号B: 60×50×50cm", (245, 205, 190)),
        ("v2_model_3.png", render_model_C, "抽屉式简约猫砂盆 | 抽拉抽屉 · 简洁外观",
         "型号C: 55×45×45cm", (183, 167, 209)),
    ]
    
    for filename, render_func, subtitle, size_label, accent_color in models:
        # Create base image
        img = Image.new('RGB', (width, height), (248, 244, 240))
        draw = ImageDraw.Draw(img)
        
        # Create lifestyle background
        for y in range(height):
            ratio = y / height
            r = int(248 + (235 - 248) * ratio)
            g = int(244 + (232 - 244) * ratio)
            b = int(240 + (228 - 240) * ratio)
            if y > height * 0.7:
                # Floor area
                floor_ratio = (y - height * 0.7) / (height * 0.3)
                r = int(235 - (235-195) * floor_ratio)
                g = int(232 - (232-192) * floor_ratio)
                b = int(228 - (228-188) * floor_ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Add decorative elements
        # Plant in corner
        draw.ellipse([80, height-150, 150, height-80], fill=(165, 180, 160))
        draw.polygon([(90, height-150), (115, height-220), (140, height-150)], fill=(145, 170, 135))
        draw.polygon([(100, height-160), (115, height-200), (130, height-160)], fill=(160, 182, 152))
        
        # Small decorative mat
        draw.rounded_rectangle([width-220, height-120, width-80, height-60], 15, fill=(215, 200, 185))
        
        # Model position
        model_cx, model_cy = width//2, height//2 + 50
        
        # Add shadow
        shadow = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        cos_a, sin_a = 0.866, 0.5
        shadow_pts = [
            (model_cx - 100 + 15, model_cy + 80 + 20),
            (model_cx + 80 + 15, model_cy + 60 + 20),
            (model_cx + 80 - 100 + 30, model_cy + 60 + 80 + 25)
        ]
        shadow_draw.polygon(shadow_pts, fill=(0, 0, 0, 50))
        img = Image.alpha_composite(img.convert('RGBA'), shadow).convert('RGB')
        draw = ImageDraw.Draw(img)
        
        # Render the model
        render_func(draw, model_cx, model_cy, scale=1.8)
        
        # Add title and info
        title_font_size = 28
        subtitle_font_size = 16
        label_font_size = 14
        
        # Product title
        draw.text((width//2 - 200, 60), subtitle, fill=(80, 75, 70))
        
        # Size label with accent background
        label_bg_x = width//2 - 80
        draw.rounded_rectangle([label_bg_x, height-140, label_bg_x+160, height-105], 
                               10, fill=(*accent_color,))
        draw.text((label_bg_x + 15, height-132), size_label, fill=(255, 255, 255))
        
        # Brand watermark
        draw.text((width-150, 40), "CatOi Vietnam", fill=(180, 175, 170))
        
        # Vietnamese tagline
        draw.text((60, 80), "Thiết kế cho mèo Việt", fill=(150, 145, 140))
        
        # Save image
        output_path = os.path.join(output_dir, filename)
        img.save(output_path, 'PNG')
        print(f"Saved: {output_path}")
    
    return output_dir

if __name__ == "__main__":
    render_all_models()
    print("\nAll 3 cat litter box renders completed!")
