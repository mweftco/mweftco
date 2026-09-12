#!/usr/bin/env python3
"""
AURELIA v4.0 - High-End Fashion Editorial Agent
Generates luxury fashion breakdown posts with carousel slides
Each post: Full Look + Jacket + Shirt + Tie + Trousers + Shoes + Fabric Specs
"""

import os
import random
import urllib.parse
from datetime import datetime
from pathlib import Path

MODELS = [
    {"name": "Male Model", "desc": "handsome male fashion model, slim athletic build"},
    {"name": "Female Model", "desc": "elegant female fashion model, graceful posture"},
]

LOOKS = [
    {
        "title": "THE CLASSIC TUXEDO",
        "subtitle": "Black Tie Perfection",
        "full_desc": "black peak lapel tuxedo, crisp white pleated dress shirt, black satin bow tie, black patent leather oxford shoes, white pocket square",
        "jacket": "black wool peak lapel tuxedo jacket, satin lapel, single button closure, jetted pockets",
        "shirt": "white pleated front tuxedo shirt, wing collar, black stud buttons, french cuffs",
        "tie": "black satin silk bow tie, classic butterfly shape, self-tie",
        "trousers": "black wool tuxedo trousers, satin side stripe, slim fit, no belt loops",
        "shoes": "black patent leather oxford shoes, closed lacing, high gloss mirror finish",
        "accessories": "white silk pocket square, black onyx cufflinks, dress watch",
        "fabric": "Jacket: 100% Super 120s Wool | Shirt: Premium Egyptian Cotton | Trousers: Wool Blend with Satin Stripe",
        "color": "Color Palette: Deep Black, Crisp White, Satin Sheen",
        "avoid": "Avoid: Brown shoes, belt instead of suspenders, short sleeves, casual watch",
        "tag": "BLACK TIE",
        "occasion": "Gala, Wedding, Award Ceremony, Formal Dinner"
    },
    {
        "title": "THE POWER NAVY SUIT",
        "subtitle": "Boardroom Dominance",
        "full_desc": "tailored navy blue business suit, white spread collar shirt, burgundy silk tie, brown leather oxford shoes, silver tie clip",
        "jacket": "navy blue tailored suit jacket, notch lapels, two-button closure, flap pockets, structured shoulders",
        "shirt": "white spread collar dress shirt, barrel cuffs, crisp cotton poplin",
        "tie": "burgundy silk tie, subtle micro pattern, standard width",
        "trousers": "navy blue flat front trousers, slim tapered fit, pressed crease",
        "shoes": "dark brown leather oxford shoes, burnished toe, leather sole",
        "accessories": "silver tie clip, leather belt matching shoes, minimalist dress watch",
        "fabric": "Jacket: Super 100s Wool | Shirt: 100% Cotton Poplin | Trousers: Wool Blend",
        "color": "Color Palette: Navy Blue, Pure White, Burgundy Accent, Brown Leather",
        "avoid": "Avoid: Black shoes with navy, loud patterns, wrinkled shirt, mismatched belt",
        "tag": "BUSINESS FORMAL",
        "occasion": "Business Meeting, Interview, Corporate Event"
    },
    {
        "title": "THE DESERT LINEN LOOK",
        "subtitle": "Summer Elegance",
        "full_desc": "beige linen suit, white linen shirt unbuttoned at collar, brown leather loafers, tortoise sunglasses, woven belt",
        "jacket": "beige unstructured linen blazer, patch pockets, half lined, relaxed fit",
        "shirt": "white linen shirt, spread collar, mother of pearl buttons, rolled sleeves",
        "tie": "no tie, open collar, casual summer style",
        "trousers": "beige linen drawstring trousers, relaxed fit, cropped length",
        "shoes": "tan leather loafers, penny style, soft leather, no socks",
        "accessories": "tortoise shell sunglasses, woven leather belt, linen pocket square",
        "fabric": "Jacket & Trousers: 100% Irish Linen | Shirt: Lightweight Linen Blend",
        "color": "Color Palette: Beige, Off-White, Tan, Tortoise Brown",
        "avoid": "Avoid: Synthetic fabrics, dark colors in heat, heavy shoes, formal tie",
        "tag": "SUMMER LUXE",
        "occasion": "Resort, Beach Wedding, Summer Party, Vacation"
    },
    {
        "title": "THE MODERN SHERWANI",
        "subtitle": "Regal Heritage",
        "full_desc": "black embroidered sherwani with gold zari work, matching churidar, black embroidered mojari shoes, pocket square",
        "jacket": "black silk sherwani, intricate gold zari embroidery, mandarin collar, front button placket",
        "shirt": "black silk inner kurta, minimal embroidery, comfortable fit",
        "tie": "no tie, mandarin collar with gold button detail",
        "trousers": "black churidar, fitted at ankle, matching embroidery at hem",
        "shoes": "black embroidered mojari, gold thread work, leather sole",
        "accessories": "gold pocket square, brooch, traditional watch",
        "fabric": "Sherwani: Silk with Zari Work | Churidar: Cotton Silk Blend | Shoes: Leather",
        "color": "Color Palette: Deep Black, Rich Gold, Subtle Cream",
        "avoid": "Avoid: Western shoes, bright clashing colors, loose fit, casual accessories",
        "tag": "ETHNIC ROYAL",
        "occasion": "Wedding, Reception, Festival, Cultural Event"
    },
    {
        "title": "THE STREET ROYALTY",
        "subtitle": "Urban Luxury",
        "full_desc": "camel wool overcoat over black hoodie, black cargo pants, white high-top sneakers, silver chain, black beanie",
        "jacket": "camel double-breasted wool overcoat, peak lapels, knee length, oversized fit",
        "shirt": "black oversized hoodie, premium cotton fleece, dropped shoulders",
        "tie": "no tie, layered streetwear aesthetic",
        "trousers": "black cargo pants, multiple pockets, tapered fit, technical fabric",
        "shoes": "white leather high-top sneakers, clean design, chunky sole",
        "accessories": "silver cuban chain, black beanie, crossbody bag, rings",
        "fabric": "Coat: Italian Wool Blend | Hoodie: Premium Fleece | Pants: Technical Cotton",
        "color": "Color Palette: Camel, Black, White, Silver",
        "avoid": "Avoid: Formal shoes, bright colors, baggy everything, clashing metals",
        "tag": "STREET LUXE",
        "occasion": "City Outing, Concert, Casual Meeting, Night Out"
    },
    {
        "title": "THE ALL BLACK EDGE",
        "subtitle": "Midnight Minimal",
        "full_desc": "black leather biker jacket, white fitted t-shirt, black raw denim jeans, black chelsea boots, silver rings",
        "jacket": "black genuine leather biker jacket, asymmetric zip, snap collar, zip pockets",
        "shirt": "white fitted crew neck t-shirt, premium cotton, muscle fit",
        "tie": "no tie, open neck casual style",
        "trousers": "black raw selvedge denim jeans, slim fit, minimal stitching",
        "shoes": "black leather chelsea boots, elastic side panels, sleek silhouette",
        "accessories": "silver signet rings, leather bracelet, aviator sunglasses",
        "fabric": "Jacket: Genuine Leather | T-Shirt: Premium Cotton | Jeans: Raw Selvedge Denim",
        "color": "Color Palette: Jet Black, Pure White, Silver Metal",
        "avoid": "Avoid: Baggy fit, colorful sneakers, logo overload, distressed jeans",
        "tag": "EDGY MINIMAL",
        "occasion": "Casual Date, Night Out, Concert, Weekend"
    },
]


def img_url(prompt, seed_offset=0):
    encoded = urllib.parse.quote(prompt)
    seed = random.randint(1, 999999) + seed_offset
    return f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&seed={seed}&nologo=true&enhance=true"


def generate_post():
    model = random.choice(MODELS)
    look = random.choice(LOOKS)
    
    now = datetime.now()
    post_num = get_next_post_number()
    slug = f"post-{post_num:03d}"
    date_str = now.strftime('%B %d, %Y')
    
    # Generate image URLs for each slide
    base = f"professional fashion photography, luxury editorial, {model['desc']}"
    
    images = {
        "full": img_url(f"{base}, full body shot, wearing {look['full_desc']}, dark studio background, dramatic lighting, 8k, haute couture"),
        "jacket": img_url(f"{base}, extreme close-up detail shot of {look['jacket']}, dark background, macro fashion photography, texture visible, 8k"),
        "shirt": img_url(f"{base}, close-up detail shot of {look['shirt']}, collar and cuff visible, dark background, fashion macro, 8k"),
        "tie": img_url(f"{base}, close-up detail shot of {look['tie']}, neck and chest area, dark background, luxury fashion detail, 8k"),
        "trousers": img_url(f"{base}, lower body shot showing {look['trousers']}, standing pose, dark studio, fashion editorial, 8k"),
        "shoes": img_url(f"{base}, close-up detail shot of feet wearing {look['shoes']}, dark reflective floor, luxury footwear photography, 8k"),
        "accessories": img_url(f"{base}, flat lay or detail shot of {look['accessories']}, dark marble surface, luxury product photography, 8k"),
    }
    
    slides_html = f'''
    <div class="carousel-container">
      <div class="carousel-track" id="track">
        
        <!-- SLIDE 1: FULL LOOK -->
        <div class="slide">
          <div class="slide-num">01</div>
          <div class="slide-label">FULL LOOK</div>
          <img src="{images['full']}" alt="Full Look" class="slide-img">
          <div class="slide-overlay">
            <div class="slide-title-overlay">{look['title']}</div>
            <div class="slide-sub-overlay">{look['subtitle']}</div>
            <div class="slide-desc">{look['full_desc']}</div>
          </div>
        </div>
        
        <!-- SLIDE 2: JACKET -->
        <div class="slide">
          <div class="slide-num">02</div>
          <div class="slide-label">JACKET / COAT</div>
          <img src="{images['jacket']}" alt="Jacket" class="slide-img">
          <div class="slide-overlay">
            <div class="detail-title">JACKET DETAIL</div>
            <div class="detail-text">{look['jacket']}</div>
          </div>
        </div>
        
        <!-- SLIDE 3: SHIRT -->
        <div class="slide">
          <div class="slide-num">03</div>
          <div class="slide-label">SHIRT / TOP</div>
          <img src="{images['shirt']}" alt="Shirt" class="slide-img">
          <div class="slide-overlay">
            <div class="detail-title">SHIRT DETAIL</div>
            <div class="detail-text">{look['shirt']}</div>
          </div>
        </div>
        
        <!-- SLIDE 4: TIE / NECK -->
        <div class="slide">
          <div class="slide-num">04</div>
          <div class="slide-label">TIE / ACCESSORY</div>
          <img src="{images['tie']}" alt="Tie" class="slide-img">
          <div class="slide-overlay">
            <div class="detail-title">NECK ACCESSORY</div>
            <div class="detail-text">{look['tie']}</div>
          </div>
        </div>
        
        <!-- SLIDE 5: TROUSERS -->
        <div class="slide">
          <div class="slide-num">05</div>
          <div class="slide-label">TROUSERS</div>
          <img src="{images['trousers']}" alt="Trousers" class="slide-img">
          <div class="slide-overlay">
            <div class="detail-title">TROUSER DETAIL</div>
            <div class="detail-text">{look['trousers']}</div>
          </div>
        </div>
        
        <!-- SLIDE 6: SHOES -->
        <div class="slide">
          <div class="slide-num">06</div>
          <div class="slide-label">FOOTWEAR</div>
          <img src="{images['shoes']}" alt="Shoes" class="slide-img">
          <div class="slide-overlay">
            <div class="detail-title">FOOTWEAR DETAIL</div>
            <div class="detail-text">{look['shoes']}</div>
          </div>
        </div>
        
        <!-- SLIDE 7: ACCESSORIES -->
        <div class="slide">
          <div class="slide-num">07</div>
          <div class="slide-label">ACCESSORIES</div>
          <img src="{images['accessories']}" alt="Accessories" class="slide-img">
          <div class="slide-overlay">
            <div class="detail-title">ACCESSORIES</div>
            <div class="detail-text">{look['accessories']}</div>
          </div>
        </div>
        
        <!-- SLIDE 8: SPECIFICATIONS -->
        <div class="slide spec-slide">
          <div class="slide-num">08</div>
          <div class="slide-label">SPECIFICATIONS</div>
          <div class="specs-panel">
            <div class="specs-title">{look['title']}</div>
            <div class="specs-sub">DETAILS & SPECIFICATIONS</div>
            <div class="specs-grid">
              <div class="spec-box">
                <div class="spec-box-title">FABRIC</div>
                <div class="spec-box-text">{look['fabric']}</div>
              </div>
              <div class="spec-box">
                <div class="spec-box-title">COLOR PALETTE</div>
                <div class="spec-box-text">{look['color']}</div>
              </div>
              <div class="spec-box">
                <div class="spec-box-title">AVOID</div>
                <div class="spec-box-text">{look['avoid']}</div>
              </div>
              <div class="spec-box">
                <div class="spec-box-title">OCCASION</div>
                <div class="spec-box-text">{look['occasion']}</div>
              </div>
            </div>
            <div class="specs-footer">A STATEMENT FOR EVERY OCCASION</div>
          </div>
        </div>
        
      </div>
      
      <button class="carousel-btn prev" onclick="move(-1)">&#10094;</button>
      <button class="carousel-btn next" onclick="move(1)">&#10095;</button>
      
      <div class="carousel-dots">
        <span class="dot active" onclick="goTo(0)"></span>
        <span class="dot" onclick="goTo(1)"></span>
        <span class="dot" onclick="goTo(2)"></span>
        <span class="dot" onclick="goTo(3)"></span>
        <span class="dot" onclick="goTo(4)"></span>
        <span class="dot" onclick="goTo(5)"></span>
        <span class="dot" onclick="goTo(6)"></span>
        <span class="dot" onclick="goTo(7)"></span>
      </div>
      
      <div class="slide-counter"><span id="current">1</span> / 8</div>
    </div>
    '''
    
    post_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{look['title']} | M&WEFTCO</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;400;500;600;700&family=Playfair+Display:wght@400;700&display=swap" rel="stylesheet">
<style>
:root {{ --bg: #02050a; --panel: rgba(10,22,45,0.98); --cyan: #00bfff; --gold: #d4af37; --text: #e0f0ff; --dim: #5a7a95; --dark: #0a1525; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ background: var(--bg); color: var(--text); font-family: 'Rajdhani', sans-serif; min-height: 100vh; }}
.container {{ max-width: 1000px; margin: 0 auto; padding: 30px 16px; }}
.topbar {{ display:flex; justify-content:space-between; align-items:center; padding: 14px 20px; background: rgba(2,5,12,0.98); border-bottom: 1px solid rgba(0,100,200,0.08); }}
.brand {{ font-family: 'Orbitron', sans-serif; font-size: 13px; color: var(--cyan); letter-spacing: 3px; text-decoration: none; }}
.back-link {{ display: inline-flex; align-items: center; gap: 8px; color: var(--cyan); text-decoration: none; font-size: 11px; letter-spacing: 1px; margin-bottom: 16px; }}
.post-header {{ text-align: center; margin-bottom: 20px; padding: 0 10px; }}
.post-date {{ font-size: 10px; color: var(--dim); letter-spacing: 3px; margin-bottom: 8px; text-transform: uppercase; }}
.post-title {{ font-family: 'Playfair Display', serif; font-size: clamp(24px, 6vw, 42px); color: #fff; letter-spacing: 4px; margin-bottom: 4px; }}
.post-subtitle {{ font-family: 'Rajdhani', sans-serif; font-size: 13px; color: var(--gold); letter-spacing: 6px; text-transform: uppercase; margin-bottom: 8px; }}
.ai-badge {{ display:inline-flex; align-items:center; gap:6px; font-size:9px; color:var(--dim); letter-spacing:2px; margin-bottom:16px; justify-content:center; width:100%; }}
.ai-badge span {{ color:var(--cyan); }}

/* CAROUSEL */
.carousel-container {{ position: relative; width: 100%; max-width: 900px; margin: 0 auto 30px; border-radius: 12px; overflow: hidden; border: 1px solid rgba(0,100,200,0.1); background: var(--dark); }}
.carousel-track {{ display: flex; transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1); }}
.slide {{ min-width: 100%; position: relative; }}
.slide-img {{ width: 100%; height: auto; max-height: 70vh; object-fit: cover; display: block; }}

/* Slide Number & Label */
.slide-num {{ position: absolute; top: 16px; left: 20px; font-family: 'Playfair Display', serif; font-size: 32px; color: rgba(255,255,255,0.15); font-weight: 700; z-index: 5; line-height: 1; }}
.slide-label {{ position: absolute; top: 22px; left: 60px; font-size: 10px; color: var(--gold); letter-spacing: 3px; text-transform: uppercase; z-index: 5; background: rgba(0,0,0,0.4); padding: 3px 10px; border-radius: 4px; border: 1px solid rgba(212,175,55,0.15); }}

/* Overlay Text */
.slide-overlay {{ position: absolute; bottom: 0; left: 0; right: 0; padding: 40px 24px 24px; background: linear-gradient(to top, rgba(2,5,10,0.95) 0%, rgba(2,5,10,0.6) 60%, transparent 100%); z-index: 4; }}
.slide-title-overlay {{ font-family: 'Playfair Display', serif; font-size: 24px; color: #fff; letter-spacing: 2px; margin-bottom: 4px; }}
.slide-sub-overlay {{ font-size: 12px; color: var(--gold); letter-spacing: 4px; text-transform: uppercase; margin-bottom: 8px; }}
.slide-desc {{ font-size: 13px; color: var(--text); line-height: 1.6; opacity: 0.9; }}
.detail-title {{ font-family: 'Orbitron', sans-serif; font-size: 11px; color: var(--gold); letter-spacing: 3px; margin-bottom: 6px; }}
.detail-text {{ font-size: 14px; color: var(--text); line-height: 1.5; }}

/* SPEC SLIDE */
.spec-slide {{ background: linear-gradient(145deg, #0a1525, #050a12); min-height: 500px; display: flex; align-items: center; justify-content: center; padding: 40px 24px; }}
.specs-panel {{ width: 100%; max-width: 700px; border: 1px solid rgba(212,175,55,0.15); border-radius: 12px; padding: 32px 28px; background: rgba(0,0,0,0.3); }}
.specs-title {{ font-family: 'Playfair Display', serif; font-size: 28px; color: #fff; text-align: center; letter-spacing: 3px; margin-bottom: 4px; }}
.specs-sub {{ font-size: 10px; color: var(--gold); text-align: center; letter-spacing: 5px; margin-bottom: 28px; text-transform: uppercase; }}
.specs-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 24px; }}
.spec-box {{ background: rgba(0,20,40,0.5); border: 1px solid rgba(0,100,200,0.08); border-radius: 8px; padding: 16px; }}
.spec-box-title {{ font-family: 'Orbitron', sans-serif; font-size: 9px; color: var(--gold); letter-spacing: 2px; margin-bottom: 8px; }}
.spec-box-text {{ font-size: 12px; color: var(--text); line-height: 1.6; }}
.specs-footer {{ text-align: center; font-size: 10px; color: var(--dim); letter-spacing: 4px; text-transform: uppercase; padding-top: 16px; border-top: 1px solid rgba(212,175,55,0.1); }}

/* Controls */
.carousel-btn {{ position: absolute; top: 50%; transform: translateY(-50%); background: rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1); color: #fff; width: 40px; height: 40px; border-radius: 50%; cursor: pointer; font-size: 14px; z-index: 10; transition: all 0.2s; display: flex; align-items: center; justify-content: center; }}
.carousel-btn:hover {{ background: rgba(212,175,55,0.2); border-color: var(--gold); }}
.carousel-btn.prev {{ left: 12px; }}
.carousel-btn.next {{ right: 12px; }}
.carousel-dots {{ display: flex; justify-content: center; gap: 8px; padding: 14px; background: rgba(0,0,0,0.4); }}
.dot {{ width: 8px; height: 8px; border-radius: 50%; background: rgba(255,255,255,0.15); cursor: pointer; transition: all 0.3s; }}
.dot.active {{ background: var(--gold); box-shadow: 0 0 8px rgba(212,175,55,0.4); }}
.slide-counter {{ position: absolute; bottom: 56px; right: 20px; font-size: 11px; color: var(--dim); letter-spacing: 1px; z-index: 5; background: rgba(0,0,0,0.4); padding: 4px 10px; border-radius: 4px; }}

/* Tags */
.tags {{ display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; margin-bottom: 30px; }}
.tag {{ padding: 5px 16px; border-radius: 20px; font-size: 9px; letter-spacing: 2px; text-transform: uppercase; }}
.tag.cat {{ background: rgba(0,100,200,0.08); border: 1px solid rgba(0,140,255,0.12); color: var(--cyan); }}
.tag.model {{ background: rgba(212,175,55,0.05); border: 1px solid rgba(212,175,55,0.1); color: var(--gold); }}

.footer {{ text-align: center; padding: 24px; font-size: 10px; color: var(--dim); letter-spacing: 2px; border-top: 1px solid rgba(0,100,200,0.05); margin-top: 20px; }}

@media (max-width: 600px) {{
  .specs-grid {{ grid-template-columns: 1fr; }}
  .slide-num {{ font-size: 24px; }}
  .slide-label {{ left: 50px; font-size: 9px; }}
  .slide-title-overlay {{ font-size: 18px; }}
  .specs-title {{ font-size: 22px; }}
}}
</style>
</head>
<body>
<div class="topbar">
  <a href="../index.html" class="brand">M&WEFTCO</a>
  <div style="font-size:9px; color:var(--dim); letter-spacing:2px;">AURELIA // EDITORIAL</div>
</div>

    <div class="container">
  <a href="../index.html" class="back-link">&#8592; Back to Home</a>
  
  <div class="post-header">
    <div class="post-date">{date_str} // AURELIA EDITORIAL #{post_num}</div>
    <div class="ai-badge"><span>&#9889;</span> AI-GENERATED FASHION EDITORIAL // {model['name'].upper()}</div>
    <div class="post-title">{look['title']}</div>
    <div class="post-subtitle">{look['subtitle']}</div>
  </div>
  
  <div class="tags">
    <span class="tag cat">#{look['tag']}</span>
    <span class="tag model">{model['name'].upper()}</span>
  </div>
  
  {slides_html}
  
</div>

<div class="footer">M&WEFTCO // CRAFTED FOR THE MODERN MAN // AURELIA AI FASHION EDITORIAL ENGINE</div>

<script>
let current = 0;
const total = 8;
    const track = document.getElementById('track');
const currentEl = document.getElementById('current');
const dots = document.querySelectorAll('.dot');

function update() {{
  track.style.transform = 'translateX(-' + (current * 100) + '%)';
  currentEl.textContent = current + 1;
  dots.forEach((d, i) => d.classList.toggle('active', i === current));
}}

function move(dir) {{
  current = (current + dir + total) % total;
  update();
}}

function goTo(idx) {{
  current = idx;
  update();
}}

// Auto-advance every 6 seconds
setInterval(() => move(1), 6000);

// Keyboard navigation
document.addEventListener('keydown', e => {{
  if (e.key === 'ArrowRight') move(1);
  if (e.key === 'ArrowLeft') move(-1);
}});

// Touch swipe
let startX = 0;
track.addEventListener('touchstart', e => startX = e.touches[0].clientX);
track.addEventListener('touchend', e => {{
  const diff = startX - e.changedTouches[0].clientX;
  if (Math.abs(diff) > 50) move(diff > 0 ? 1 : -1);
}});
</script>

</body>
</html>'''

    posts_dir = Path("posts")
    posts_dir.mkdir(exist_ok=True)
    post_path = posts_dir / f"{slug}.html"
    post_path.write_text(post_html, encoding='utf-8')
    
    update_index(look['title'], slug, date_str, images['full'], look['tag'])
    
    print(f"AURELIA v4: Editorial post created -> {post_path}")
    return look['title']

def get_next_post_number():
    posts_dir = Path("posts")
    if not posts_dir.exists():
        return 1
    existing = [f for f in posts_dir.glob("post-*.html")]
    return len(existing) + 1


def update_index(title, slug, date_str, img_url, tag):
    index_path = Path("index.html")
    if not index_path.exists():
        return
    
    content = index_path.read_text(encoding='utf-8')
    marker = '<!-- AURELIA POSTS -->'
    
    post_link = f'''<a href="posts/{slug}.html" style="display:block; background:rgba(10,22,45,0.95); border:1px solid rgba(0,100,200,0.12); border-radius:10px; overflow:hidden; text-decoration:none; color:inherit; transition:all 0.2s; margin-bottom:12px;" onmouseover="this.style.borderColor='rgba(0,180,255,0.3)'" onmouseout="this.style.borderColor='rgba(0,100,200,0.12)'">
      <div style="height:180px; background-image:url({img_url}); background-size:cover; background-position:center top;"></div>
      <div style="padding:16px;">
        <div style="font-size:10px; color:var(--dim); letter-spacing:1px; margin-bottom:4px;">{date_str} 
        EDITORIAL</div>
        <div style="font-size:15px; color:#fff; font-weight:600; margin-bottom:6px;">{title}</div>
        <span style="font-size:9px; padding:3px 10px; border-radius:12px; background:rgba(0,100,200,0.08); border:1px solid rgba(0,140,255,0.1); color:var(--cyan); letter-spacing:1px;">#{tag}</span>
      </div>
    </a>'''
    
    if marker not in content:
        section = f'''
<!-- AURELIA POSTS -->
<div style="max-width:900px; margin:40px auto; padding:0 20px;">
  <div style="font-family:'Orbitron',sans-serif; font-size:14px; color:var(--cyan); letter-spacing:3px; margin-bottom:20px;">LATEST FROM AURELIA // AI FASHION EDITORIAL</div>
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
    print("AURELIA v4.0: Generating high-end fashion editorial with 8-slide carousel...")
    title = generate_post()
    if title:
        print(f"SUCCESS: Posted editorial '{title}' with 8 slides!")
    else:
        print("ERROR: Failed to generate post")
