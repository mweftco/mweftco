#!/usr/bin/env python3
"""
AURELIA - Autonomous Content Agent for M&WEFTCO
Posts daily content to the GitHub Pages website
"""

import os
import json
import random
from datetime import datetime
from pathlib import Path

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

CATEGORIES = [
    "style_tips", "fashion_trends", "outfit_ideas", "grooming",
    "confidence", "lifestyle", "seasonal_style", "wardrobe"
]

CONTENT_TEMPLATES = {
    "style_tips": [
        {
            "title": "5 Style Rules Every Man Should Know",
            "body": "<p>Style is not about expensive clothes. It is about the right fit, right color, and right attitude.</p><ul><li><b>Fit is everything</b> - A cheap well-fitted shirt looks better than an expensive loose one.</li><li><b>Neutral foundation</b> - Build your wardrobe around black, white, navy, and grey.</li><li><b>One statement piece</b> - Let one item shine. Keep the rest simple.</li><li><b>Shoes matter</b> - People notice your shoes. Keep them clean.</li><li><b>Confidence</b> - The best outfit is confidence. Wear it daily.</li></ul>"
        },
        {
            "title": "How to Dress for Your Body Type",
            "body": "<p>Understanding your body type is the first step to great style.</p><ul><li><b>Slim build:</b> Layer up. Structured jackets add mass.</li><li><b>Athletic:</b> Tailored fits work best. Avoid overly tight clothes.</li><li><b>Broad build:</b> Vertical stripes and dark colors create balance.</li><li><b>Tall:</b> Horizontal stripes and layered looks add proportion.</li></ul>"
        },
        {
            "title": "The Power of Minimal Wardrobe",
            "body": "<p>Less is more. A minimal wardrobe saves time and always keeps you sharp.</p><ul><li>2 white shirts</li><li>2 black t-shirts</li><li>1 navy blazer</li><li>1 pair dark jeans</li><li>1 pair chinos</li><li>White sneakers + Black formal shoes</li></ul><p>Mix and match. You now have 20+ outfits.</p>"
        }
    ],
    "fashion_trends": [
        {
            "title": "Trending: The Return of Classic Cuts",
            "body": "<p>Fashion is cyclical. Classic cuts are making a strong comeback this season.</p><p>Structured blazers, straight-fit trousers, and clean silhouettes are dominating runways. The message is clear: timeless beats trendy.</p><p>Invest in pieces that never go out of style. Trends fade. Classics remain.</p>"
        },
        {
            "title": "Color of the Season: Deep Navy",
            "body": "<p>Deep navy is the new black. It is versatile, elegant, and works in every setting.</p><p>Pair navy with white for a clean look. With beige for warmth. With black for edge.</p><p>One navy blazer can transform your entire wardrobe.</p>"
        }
    ],
    "outfit_ideas": [
        {
            "title": "Monday Power Look",
            "body": "<p>Start your week with authority.</p><ul><li>Navy tailored blazer</li><li>White crisp shirt</li><li>Dark slim-fit jeans or trousers</li><li>Black leather shoes</li><li>Minimal watch</li></ul><p>Clean. Sharp. Unstoppable.</p>"
        },
        {
            "title": "Casual Friday Done Right",
            "body": "<p>Casual does not mean careless.</p><ul><li>Fitted polo or crew neck tee</li><li>Well-fitted chinos</li><li>Clean white sneakers</li><li>Leather strap watch</li></ul><p>Relaxed but refined. That is the M&WEFTCO way.</p>"
        }
    ],
    "grooming": [
        {
            "title": "The 5-Minute Grooming Routine",
            "body": "<p>Looking sharp takes minutes, not hours.</p><ul><li><b>Cleanse</b> - Wash your face. Fresh skin is confident skin.</li><li><b>Trim</b> - Keep beard or stubble neat. Lines matter.</li><li><b>Moisturize</b> - Hydrated skin looks younger and healthier.</li><li><b>Style hair</b> - Find one hairstyle that works. Stick to it.</li><li><b>Fragrance</b> - One spray. Let it be subtle.</li></ul>"
        }
    ],
    "confidence": [
        {
            "title": "Dress Well, Feel Unstoppable",
            "body": "<p>There is a direct link between how you dress and how you feel.</p><p>When you look good, you carry yourself differently. You speak clearer. You walk taller. You think sharper.</p><p>Style is not vanity. It is self-respect.</p><p>Every morning, choose to show up as your best version.</p>"
        },
        {
            "title": "Your Style is Your Signature",
            "body": "<p>Before you speak, your style speaks for you.</p><p>People form opinions in seconds. Make sure your style tells the right story.</p><p>Consistency in style builds trust. Reliability. Presence.</p><p>What does your style say about you?</p>"
        }
    ],
    "lifestyle": [
        {
            "title": "The Modern Man's Lifestyle",
            "body": "<p>Style extends beyond clothes. It is a lifestyle.</p><ul><li><b>Discipline</b> - Wake up early. Plan your day.</li><li><b>Fitness</b> - A good body makes every outfit look better.</li><li><b>Reading</b> - Knowledge is the ultimate accessory.</li><li><b>Etiquette</b> - Manners never go out of style.</li></ul><p>Be the man who turns heads and earns respect.</p>"
        }
    ],
    "seasonal_style": [
        {
            "title": "Summer Style Essentials",
            "body": "<p>Beat the heat without losing the edge.</p><ul><li>Lightweight linen shirts</li><li>Breathable cotton tees</li><li>Beige and white color palette</li><li>Sunglasses that fit your face</li><li>Leather sandals or canvas shoes</li></ul><p>Stay cool. Stay sharp.</p>"
        },
        {
            "title": "Winter Layering Guide",
            "body": "<p>Winter is the best season for style. Layers add depth.</p><ul><li>Base: Fitted tee or thermal</li><li>Middle: Sweater or cardigan</li><li>Outer: Wool coat or leather jacket</li><li>Accessories: Scarf, gloves, beanie</li></ul><p>Layer with purpose. Every piece should earn its place.</p>"
        }
    ],
    "wardrobe": [
        {
            "title": "Building a Capsule Wardrobe",
            "body": "<p>Quality over quantity. Always.</p><ul><li>3 t-shirts (white, black, grey)</li><li>2 shirts (white, light blue)</li><li>1 blazer (navy or black)</li><li>2 trousers (black, beige)</li><li>1 pair jeans (dark wash)</li><li>2 pairs shoes (white sneakers, black formal)</li></ul><p>11 pieces. Infinite combinations.</p>"
        }
    ]
}


def generate_content_with_api():
    api_key = os.environ.get('GEMINI_API_KEY', '')
    if not api_key or not HAS_REQUESTS:
        return None
    
    category = random.choice(CATEGORIES)
    
    prompt = """Write a short fashion/style blog post for a men's fashion brand called M&WEFTCO.
Category: """ + category.replace('_', ' ').title() + """
Write an engaging title and HTML body content (2-3 paragraphs or a short list).
Keep it under 200 words. Tone: confident, modern, empowering.
Return ONLY JSON in this format:
{"title": "...", "body": "<p>...</p>"}"""

    try:
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=" + api_key
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.8}
        }
        resp = requests.post(url, headers=headers, json=data, timeout=30)
        resp.raise_for_status()
        result = resp.json()
        text = result['candidates'][0]['content']['parts'][0]['text']
        start = text.find('{')
        end = text.rfind('}') + 1
        if start >= 0 and end > start:
            return json.loads(text[start:end])
    except Exception as e:
        print("API generation failed:", e)
    return None


def generate_local_content():
    category = random.choice(CATEGORIES)
    templates = CONTENT_TEMPLATES.get(category, CONTENT_TEMPLATES["style_tips"])
    return random.choice(templates)


def get_next_post_number():
    posts_dir = Path("posts")
    if not posts_dir.exists():
        return 1
    existing = [f for f in posts_dir.glob("*.html")]
    return len(existing) + 1


def create_post():
    content = generate_content_with_api()
    if not content:
        content = generate_local_content()
    
    now = datetime.now()
    post_num = get_next_post_number()
    slug = "post-" + str(post_num).zfill(3)
    date_str = now.strftime('%B %d, %Y')
    tag = random.choice(CATEGORIES).replace('_', '').upper()
    
    post_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>""" + content['title'] + """ | M&WEFTCO</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@400;600&display=swap" rel="stylesheet">
<style>
:root { --bg: #02050a; --panel: rgba(10,22,45,0.95); --cyan: #00bfff; --gold: #d4af37; --text: #e0f0ff; --dim: #5a7a95; }
* { margin:0; padding:0; box-sizing:border-box; }
body { background: var(--bg); color: var(--text); font-family: 'Rajdhani', sans-serif; min-height: 100vh; }
.container { max-width: 800px; margin: 0 auto; padding: 40px 20px; }
.topbar { display:flex; justify-content:space-between; align-items:center; padding: 16px 24px; background: rgba(2,5,12,0.95); border-bottom: 1px solid rgba(0,100,200,0.1); }
.brand { font-family: 'Orbitron', sans-serif; font-size: 14px; color: var(--cyan); letter-spacing: 3px; text-decoration: none; }
.post-card { background: var(--panel); border: 1px solid rgba(0,100,200,0.12); border-radius: 12px; padding: 32px; margin-top: 30px; }
.post-date { font-size: 11px; color: var(--dim); letter-spacing: 2px; margin-bottom: 12px; text-transform: uppercase; }
.post-title { font-family: 'Orbitron', sans-serif; font-size: 24px; color: #fff; margin-bottom: 20px; line-height: 1.3; }
.post-body { font-size: 15px; line-height: 1.8; color: var(--text); }
.post-body p { margin-bottom: 16px; }
.post-body ul { margin: 16px 0; padding-left: 20px; }
.post-body li { margin-bottom: 10px; }
.post-body b { color: var(--gold); }
.post-tag { display: inline-block; padding: 4px 12px; border-radius: 12px; background: rgba(0,100,200,0.1); border: 1px solid rgba(0,100,200,0.1); color: var(--cyan); font-size: 10px; letter-spacing: 1px; margin-top: 20px; }
.footer { text-align: center; padding: 30px; font-size: 11px; color: var(--dim); letter-spacing: 2px; margin-top: 40px; border-top: 1px solid rgba(0,100,200,0.05); }
.back-link { display: inline-flex; align-items: center; gap: 8px; color: var(--cyan); text-decoration: none; font-size: 12px; letter-spacing: 1px; margin-bottom: 20px; }
.back-link:hover { text-decoration: underline; }
</style>
</head>
<body>
<div class="topbar">
  <a href="../index.html" class="brand">M&WEFTCO</a>
  <div style="font-size:10px; color:var(--dim); letter-spacing:2px;">AURELIA // CONTENT AGENT</div>
</div>
<div class="container">
  <a href="../index.html" class="back-link">&#8592; Back to Home</a>
  <div class="post-card">
    <div class="post-date">""" + date_str + """ // AURELIA POST #""" + str(post_num) + """</div>
    <div class="post-title">""" + content['title'] + """</div>
    <div class="post-body">""" + content['body'] + """</div>
    <div class="post-tag">#""" + tag + """</div>
  </div>
</div>
<div class="footer">M&WEFTCO // CRAFTED FOR THE MODERN MAN // AURELIA AUTONOMOUS CONTENT</div>
</body>
</html>"""

    posts_dir = Path("posts")
    posts_dir.mkdir(exist_ok=True)
    post_path = posts_dir / (slug + ".html")
    post_path.write_text(post_html, encoding='utf-8')
    
    update_index(content['title'], slug, date_str)
    
    print("AURELIA posted:", content['title'], "->", post_path)
    return content['title']


def update_index(title, slug, date_str):
    index_path = Path("index.html")
    if not index_path.exists():
        return
    
    content = index_path.read_text(encoding='utf-8')
    
    marker = '<!-- AURELIA POSTS -->'
    post_link = '<a href="posts/' + slug + '.html" style="display:block; background:rgba(10,22,45,0.95); border:1px solid rgba(0,100,200,0.12); border-radius:10px; padding:16px; margin-bottom:10px; text-decoration:none; color:inherit; transition:all 0.2s;" onmouseover="this.style.borderColor=\'rgba(0,180,255,0.3)\'" onmouseout="this.style.borderColor=\'rgba(0,100,200,0.12)\'">\n      <div style="font-size:10px; color:var(--dim); letter-spacing:1px; margin-bottom:4px;">' + date_str + '</div>\n      <div style="font-size:14px; color:#fff; font-weight:600;">' + title + '</div>\n    </a>'
    
    if marker not in content:
        section = '\n<!-- AURELIA POSTS -->\n<div style="max-width:800px; margin:40px auto; padding:0 20px;">\n  <div style="font-family:\'Orbitron\',sans-serif; font-size:14px; color:var(--cyan); letter-spacing:3px; margin-bottom:20px;">LATEST FROM AURELIA</div>\n  <div id="aurelia-posts">\n    ' + post_link + '\n  </div>\n</div>\n'
        content = content.replace('</body>', section + '</body>')
    else:
        insert_marker = '<div id="aurelia-posts">'
        if insert_marker in content:
            content = content.replace(insert_marker, insert_marker + '\n    ' + post_link)
    
    index_path.write_text(content, encoding='utf-8')


if __name__ == "__main__":
    print("AURELIA: Starting daily content generation...")
    title = create_post()
    if title:
        print("SUCCESS: Posted '" + title + "'")
    else:
        print("ERROR: Failed to generate content")
