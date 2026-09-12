#!/usr/bin/env python3
"""
AURELIA v2.0 - AI Fashion Content Agent with Image Generation
Generates daily fashion posts with AI-generated model images for M&WEFTCO
Uses Pollinations.ai (free, no API key needed) for image generation
"""

import os
import json
import random
import urllib.request
from datetime import datetime
from pathlib import Path

# ========== MODELS & OUTFITS ==========
MODELS = [
    {"name": "Female Model", "desc": "elegant female fashion model", "id": "female"},
    {"name": "Black Male Model", "desc": "tall athletic Black male fashion model, 6ft3", "id": "black_male"},
    {"name": "White Male Model", "desc": "tall athletic White male fashion model, 6ft3", "id": "white_male"},
    {"name": "South Asian Male Model", "desc": "handsome South Asian male fashion model", "id": "south_asian_male"},
]

OUTFITS = [
    {
        "title": "The Power Navy Suit",
        "outfit": "tailored navy blue business suit with white dress shirt, black leather oxford shoes, silver watch",
        "desc": "Command the room with this sharp navy power suit. Perfect for meetings, presentations, and making a statement.",
        "tag": "FORMAL"
    },
    {
        "title": "Midnight Black Elegance",
        "outfit": "slim-fit all-black suit with black turtleneck, black Chelsea boots, minimalist silver accessories",
        "desc": "All black never goes out of style. Sleek, mysterious, and undeniably powerful.",
        "tag": "FORMAL"
    },
    {
        "title": "Casual Luxe Friday",
        "outfit": "cream oversized blazer, black fitted t-shirt, dark denim jeans, white leather sneakers",
        "desc": "Relaxed but refined. The perfect balance between comfort and high fashion.",
        "tag": "SMART CASUAL"
    },
    {
        "title": "Desert Beige Statement",
        "outfit": "beige linen suit with open-collar white shirt, brown leather loafers, gold accent watch",
        "desc": "Light, breathable, and effortlessly stylish. Beige is the new power color.",
        "tag": "SUMMER FORMAL"
    },
    {
        "title": "Street Royalty",
        "outfit": "black oversized hoodie under camel wool coat, black cargo pants, high-top white sneakers, chain necklace",
        "desc": "Streetwear meets luxury. For the modern man who writes his own rules.",
        "tag": "STREETWEAR"
    },
    {
        "title": "The Classic Tuxedo",
        "outfit": "black peak lapel tuxedo, crisp white pleated shirt, black bow tie, patent leather shoes",
        "desc": "When the occasion demands perfection. Timeless black-tie elegance.",
        "tag": "BLACK TIE"
    },
    {
        "title": "Monochrome Minimal",
        "outfit": "grey wool overcoat, light grey turtleneck sweater, charcoal trousers, black leather boots",
        "desc": "Less is more. Shades of grey create a sophisticated, modern silhouette.",
        "tag": "MINIMAL"
    },
    {
        "title": "Bold in Burgundy",
        "outfit": "burgundy velvet blazer, black fitted shirt, black tailored trousers, black dress shoes",
        "desc": "Stand out without shouting. Burgundy adds richness and depth to any wardrobe.",
        "tag": "STATEMENT"
    },
    {
        "title": "Summer Linen Dream",
        "outfit": "white linen shirt unbuttoned at collar, beige linen trousers, brown leather sandals, sunglasses",
        "desc": "Beat the heat in style. Linen is the ultimate summer luxury fabric.",
        "tag": "SUMMER"
    },
    {
        "title": "The Modern Sherwani",
        "outfit": "black embroidered sherwani with gold detailing, matching churidar, black traditional shoes",
        "desc": "Where tradition meets contemporary fashion. Perfect for weddings and celebrations.",
        "tag": "ETHNIC"
    },
    {
        "title": "Leather & Denim Edge",
        "outfit": "black leather jacket, white crew neck tee, dark blue raw denim jeans, black combat boots",
        "desc": "Rebel with a cause. This look is bold, confident, and unapologetic.",
        "tag": "EDGY"
    },
    {
        "title": "Office to Evening",
        "outfit": "charcoal grey three-piece suit, light blue shirt, burgundy tie, brown brogue shoes",
        "desc": "From boardroom to bar. One outfit that works from 9 AM to midnight.",
        "tag": "VERSATILE"
    },
    {
        "title": "Resort Luxe",
        "outfit": "floral print silk shirt, white tailored shorts, leather boat shoes, aviator sunglasses",
        "desc": "Vacation mode activated. Luxury resort wear for the modern gentleman.",
        "tag": "RESORT"
    },
    {
        "title": "Winter Layer King",
        "outfit": "navy wool peacoat, grey cashmere scarf, black turtleneck, dark jeans, black leather boots",
        "desc": "Master the art of layering. Warmth and style in perfect harmony.",
        "tag": "WINTER"
    },
    {
        "title": "Athleisure Elite",
        "outfit": "black fitted tracksuit with white side stripes, white running shoes, crossbody bag, cap",
        "desc": "Gym to street in seconds. Because style should never slow you down.",
        "tag": "ATHLEISURE"
    },
]


def generate_image(model, outfit):
    """Generate AI fashion image using Pollinations.ai (free, no API key)"""
    
    prompt = (
        f"Professional fashion photography, full body shot, "
        f"{model['desc']}, wearing {outfit['outfit']}, "
        f"luxury studio background with soft lighting, "
        f"high-end fashion editorial style, "
        f"8k quality, sharp details, M&WEFTCO branding aesthetic, "
        f"dark moody background with gold accents"
    )
    
    # URL-encode the prompt
    import urllib.parse
    encoded_prompt = urllib.parse.quote(prompt)
    
    # Pollinations.ai - free, no API key needed
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&seed={random.randint(1,999999)}&nologo=true"
    
    # Download the image
    img_filename = f"aurelia_post_{datetime.now().strftime('%Y%m%d')}.jpg"
    img_path = Path("posts/images") / img_filename
    img_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        urllib.request.urlretrieve(image_url, img_path)
        print(f"AURELIA: Image generated -> {img_path}")
        return f"posts/images/{img_filename}"
    except Exception as e:
        print(f"Image generation failed: {e}")
        return None


def generate_post():
    """Generate a complete fashion post with AI image"""
    
    model = random.choice(MODELS)
    outfit = random.choice(OUTFITS)
    
    now = datetime.now()
    post_num = get_next_post_number()
    slug = f"post-{post_num:03d}"
    date_str = now.strftime('%B %d, %Y')
    
    # Generate AI image
    img_path = generate_image(model, outfit)
    
    # Build HTML
    img_html = f'<img src="../{img_path}" alt="{outfit["title"]}" style="width:100%;border-radius:12px;margin-bottom:20px;">' if img_path else ''
    
    post_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{outfit['title']} | M&WEFTCO</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@400;600&display=swap" rel="stylesheet">
<style>
:root {{ --bg: #02050a; --panel: rgba(10,22,45,0.95); --cyan: #00bfff; --gold: #d4af37; --text: #e0f0ff; --dim: #5a7a95; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ background: var(--bg); color: var(--text); font-family: 'Rajdhani', sans-serif; min-height: 100vh; }}
.container {{ max-width: 900px; margin: 0 auto; padding: 40px 20px; }}
.topbar {{ display:flex; justify-content:space-between; align-items:center; padding: 16px 24px; background: rgba(2,5,12,0.95); border-bottom: 1px solid rgba(0,100,200,0.1); }}
.brand {{ font-family: 'Orbitron', sans-serif; font-size: 14px; color: var(--cyan); letter-spacing: 3px; text-decoration: none; }}
.post-card {{ background: var(--panel); border: 1px solid rgba(0,100,200,0.12); border-radius: 12px; padding: 32px; margin-top: 30px; }}
.post-date {{ font-size: 11px; color: var(--dim); letter-spacing: 2px; margin-bottom: 12px; text-transform: uppercase; }}
.post-title {{ font-family: 'Orbitron', sans-serif; font-size: 28px; color: #fff; margin-bottom: 8px; line-height: 1.3; }}
.post-subtitle {{ font-size: 14px; color: var(--gold); letter-spacing: 1px; margin-bottom: 20px; }}
.post-body {{ font-size: 15px; line-height: 1.8; color: var(--text); margin-bottom: 20px; }}
.post-body p {{ margin-bottom: 16px; }}
.post-tag {{ display: inline-block; padding: 4px 14px; border-radius: 20px; background: rgba(0,100,200,0.1); border: 1px solid rgba(0,100,200,0.15); color: var(--cyan); font-size: 10px; letter-spacing: 2px; margin-top: 10px; text-transform: uppercase; }}
.model-tag {{ display: inline-block; padding: 4px 14px; border-radius: 20px; background: rgba(212,175,55,0.08); border: 1px solid rgba(212,175,55,0.15); color: var(--gold); font-size: 10px; letter-spacing: 2px; margin-top: 10px; margin-left: 8px; text-transform: uppercase; }}
.footer {{ text-align: center; padding: 30px; font-size: 11px; color: var(--dim); letter-spacing: 2px; margin-top: 40px; border-top: 1px solid rgba(0,100,200,0.05); }}
.back-link {{ display: inline-flex; align-items: center; gap: 8px; color: var(--cyan); text-decoration: none; font-size: 12px; letter-spacing: 1px; margin-bottom: 20px; }}
.back-link:hover {{ text-decoration: underline; }}
.ai-badge {{ display:inline-flex; align-items:center; gap:6px; font-size:9px; color:var(--dim); letter-spacing:1px; margin-bottom:16px; }}
.ai-badge span {{ color:var(--cyan); }}
</style>
</head>
<body>
<div class="topbar">
  <a href="../index.html" class="brand">M&WEFTCO</a>
  <div style="font-size:10px; color:var(--dim); letter-spacing:2px;">AURELIA // AI FASHION AGENT</div>
</div>
<div class="container">
  <a href="../index.html" class="back-link">&#8592; Back to Home</a>
  <div class="post-card">
    <div class="post-date">{date_str} // AURELIA FASHION POST #{post_num}</div>
    <div class="ai-badge"><span>&#9889;</span> AI-GENERATED LOOK // {model['name'].upper()}</div>
    <div class="post-title">{outfit['title']}</div>
    <div class="post-subtitle">{outfit['outfit']}</div>
    {img_html}
    <div class="post-body"><p>{outfit['desc']}</p><p>Curated by <b>AURELIA</b> - M&WEFTCO's AI Fashion Agent. Every day, a new look. Every day, a new statement.</p></div>
    <div style="margin-top:8px;">
      <span class="post-tag">#{outfit['tag']}</span>
      <span class="model-tag">{model['name'].upper()}</span>
    </div>
  </div>
</div>
<div class="footer">M&WEFTCO // CRAFTED FOR THE MODERN MAN // AURELIA AI FASHION ENGINE</div>
</body>
</html>'''

    posts_dir = Path("posts")
    posts_dir.mkdir(exist_ok=True)
    post_path = posts_dir / f"{slug}.html"
    post_path.write_text(post_html, encoding='utf-8')
    
    update_index(outfit['title'], slug, date_str, img_path)
    
    print(f"AURELIA: Post created -> {post_path}")
    return outfit['title']


def get_next_post_number():
    posts_dir = Path("posts")
    if not posts_dir.exists():
        return 1
    existing = [f for f in posts_dir.glob("post-*.html")]
    return len(existing) + 1


def update_index(title, slug, date_str, img_path):
    index_path = Path("index.html")
    if not index_path.exists():
        return
    
    content = index_path.read_text(encoding='utf-8')
    
    marker = '<!-- AURELIA POSTS -->'
    img_attr = f'background-image:url({img_path});background-size:cover;background-position:center;' if img_path else ''
    
    post_link = f'''<a href="posts/{slug}.html" style="display:block; background:rgba(10,22,45,0.95); border:1px solid rgba(0,100,200,0.12); border-radius:10px; overflow:hidden; text-decoration:none; color:inherit; transition:all 0.2s; margin-bottom:12px;" onmouseover="this.style.borderColor='rgba(0,180,255,0.3)'" onmouseout="this.style.borderColor='rgba(0,100,200,0.12)'">
      <div style="height:140px; {img_attr} background-color:#0a1a35;"></div>
      <div style="padding:16px;">
        <div style="font-size:10px; color:var(--dim); letter-spacing:1px; margin-bottom:4px;">{date_str}</div>
        <div style="font-size:15px; color:#fff; font-weight:600;">{title}</div>
      </div>
    </a>'''
    
    if marker not in content:
        section = f'''
<!-- AURELIA POSTS -->
<div style="max-width:900px; margin:40px auto; padding:0 20px;">
  <div style="font-family:'Orbitron',sans-serif; font-size:14px; color:var(--cyan); letter-spacing:3px; margin-bottom:20px;">LATEST FROM AURELIA // AI FASHION</div>
  <div id="aurelia-posts">
    {post_link}
  </div>
</div>
'''
        content = content.replace('</body>', section + '</body>')
    else:
        insert_marker = '<div id="aurelia-posts">'
        if insert_marker in content:
            content = content.replace(insert_marker, insert_marker + '\n    ' + post_link)
    
    index_path.write_text(content, encoding='utf-8')


if __name__ == "__main__":
    print("AURELIA v2.0: Generating AI fashion post with model image...")
    title = generate_post()
    if title:
        print(f"SUCCESS: Posted '{title}' with AI-generated image!")
    else:
        print("ERROR: Failed to generate post")
