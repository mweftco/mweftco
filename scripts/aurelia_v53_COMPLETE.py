#!/usr/bin/env python3
"""AURELIA v5.3 COMPLETE - All Features Working"""

import random
import urllib.parse
import os
import glob
from datetime import datetime

AURELIA_LEVEL = 1
AURELIA_XP = 0
AURELIA_TOTAL_POSTS = 0
AURELIA_GLOBAL_REACH = 0

MODELS = [
    {"name": "Male Model", "desc": "handsome male fashion model"},
    {"name": "Female Model", "desc": "elegant female fashion model"},
    {"name": "South Asian Male", "desc": "handsome South Asian male model"},
    {"name": "Black Male Model", "desc": "tall athletic Black male model"},
    {"name": "White Male Model", "desc": "tall athletic White male model"},
]

LOOKS = [
    {"title": "THE CLASSIC TUXEDO", "subtitle": "Black Tie Perfection", "tag": "BLACK TIE", "full_desc": "black peak lapel tuxedo, crisp white pleated dress shirt, black satin bow tie, black patent leather oxford shoes", "jacket": "black wool peak lapel tuxedo jacket with satin lapel facing, single button, jetted pockets", "shirt": "white pleated front tuxedo shirt with wing collar, black stud buttons, French cuffs", "tie": "black satin silk bow tie in classic butterfly shape, self-tie style", "trousers": "black wool tuxedo trousers with satin side stripe, slim fit, no belt loops", "shoes": "black patent leather oxford shoes with closed lacing and high gloss mirror finish", "accessories": "white silk pocket square, black onyx cufflinks, slim dress watch", "fabric": "Jacket & Trousers: 100% Super 120s Wool | Shirt: Premium Egyptian Cotton", "color": "Deep Black, Crisp White, Satin Silk Sheen", "avoid": "Brown shoes, belt instead of suspenders, short sleeves, casual sports watch", "occasion": "Gala, Wedding, Award Ceremony, Formal Dinner"},
    {"title": "THE POWER NAVY SUIT", "subtitle": "Boardroom Dominance", "tag": "BUSINESS FORMAL", "full_desc": "tailored navy blue business suit, white spread collar shirt, burgundy silk tie, brown leather oxford shoes", "jacket": "navy blue tailored suit jacket with notch lapels, two-button closure, flap pockets, structured shoulders", "shirt": "white spread collar dress shirt in crisp cotton poplin with barrel cuffs", "tie": "burgundy silk tie with subtle micro pattern, standard width 3.5 inches", "trousers": "navy blue flat front trousers with slim tapered fit and pressed center crease", "shoes": "dark brown leather oxford shoes with burnished toe and leather sole", "accessories": "silver tie clip, leather belt matching shoe color, minimalist silver dress watch", "fabric": "Jacket & Trousers: Super 100s Wool | Shirt: 100% Cotton Poplin | Tie: Silk", "color": "Navy Blue, Pure White, Burgundy Accent, Brown Leather", "avoid": "Black shoes with navy suit, loud patterns, wrinkled shirt, mismatched belt", "occasion": "Business Meeting, Job Interview, Corporate Event, Presentation"},
    {"title": "THE DESERT LINEN LOOK", "subtitle": "Summer Elegance", "tag": "SUMMER LUXE", "full_desc": "beige linen suit, white linen shirt with open collar, brown leather loafers, tortoise sunglasses", "jacket": "beige unstructured linen blazer with patch pockets, half lined, relaxed summer fit", "shirt": "white linen shirt with spread collar, mother of pearl buttons, rolled sleeves", "tie": "no tie, open collar with top button undone for relaxed summer elegance", "trousers": "beige linen drawstring trousers with relaxed fit and cropped ankle length", "shoes": "tan leather penny loafers in soft leather with no socks", "accessories": "tortoise shell sunglasses, woven leather belt, cream linen pocket square", "fabric": "Jacket & Trousers: 100% Irish Linen | Shirt: Lightweight Linen Blend", "color": "Beige, Off-White, Tan, Tortoise Brown", "avoid": "Synthetic fabrics, dark colors in summer heat, heavy formal shoes, neck tie", "occasion": "Resort, Beach Wedding, Summer Party, Mediterranean Vacation"},
    {"title": "THE MODERN SHERWANI", "subtitle": "Regal Heritage", "tag": "ETHNIC ROYAL", "full_desc": "black embroidered sherwani with gold zari work, matching churidar, black embroidered mojari shoes", "jacket": "black silk sherwani with intricate gold zari embroidery, mandarin collar, front button placket", "shirt": "black silk inner kurta with minimal embroidery and comfortable relaxed fit", "tie": "no tie, mandarin collar with gold button detail replacing western tie", "trousers": "black churidar fitted at ankle with matching gold embroidery at hem", "shoes": "black embroidered mojari with gold thread work and leather sole", "accessories": "gold pocket square, traditional brooch, heritage wristwatch", "fabric": "Sherwani: Pure Silk with Zari Work | Churidar: Cotton Silk Blend | Shoes: Leather", "color": "Deep Black, Rich Gold, Subtle Cream undertones", "avoid": "Western formal shoes, bright clashing colors, loose baggy fit, casual accessories", "occasion": "Wedding, Reception, Festival, Cultural Celebration"},
    {"title": "THE ALL BLACK EDGE", "subtitle": "Midnight Minimal", "tag": "EDGY MINIMAL", "full_desc": "black leather biker jacket, white fitted t-shirt, black raw denim jeans, black chelsea boots", "jacket": "black genuine leather biker jacket with asymmetric zip, snap collar, zip pockets", "shirt": "white fitted crew neck t-shirt in premium cotton with muscle fit cut", "tie": "no tie, open neck casual style with clean neckline", "trousers": "black raw selvedge denim jeans with slim fit and minimal stitching detail", "shoes": "black leather chelsea boots with elastic side panels and sleek silhouette", "accessories": "silver signet rings, thin leather bracelet, aviator sunglasses", "fabric": "Jacket: Genuine Leather | T-Shirt: Premium Cotton | Jeans: Raw Selvedge Denim", "color": "Jet Black, Pure White, Silver Metal accents", "avoid": "Baggy oversized fit, colorful sneakers, logo overload, heavily distressed jeans", "occasion": "Casual Date, Night Out, Concert, Weekend Ride"},
    {"title": "THE BURGUNDY VELVET", "subtitle": "Statement Elegance", "tag": "STATEMENT", "full_desc": "burgundy velvet blazer, black fitted turtleneck, black tailored trousers, black monk strap shoes", "jacket": "burgundy cotton velvet blazer with peak lapels, single button, jetted pockets, luxurious sheen", "shirt": "black fitted merino wool turtleneck in thin knit with sleek silhouette", "tie": "no tie, turtleneck replaces tie for modern elegant statement", "trousers": "black tailored trousers with slim fit, pressed crease, side adjusters instead of belt", "shoes": "black leather double monk strap shoes with polished finish", "accessories": "gold lapel pin, black leather watch strap, gold signet ring", "fabric": "Blazer: Cotton Velvet | Turtleneck: Merino Wool | Trousers: Wool Blend", "color": "Rich Burgundy, Deep Black, Gold Accent", "avoid": "Patterned shirt underneath, brown shoes, belt with side adjusters, casual watch", "occasion": "Dinner Party, Cocktail Event, Date Night, Evening Function"},
    {"title": "THE IVORY DREAM", "subtitle": "Summer Wedding", "tag": "SUMMER WEDDING", "full_desc": "ivory white linen suit, pale blue dress shirt, brown leather belt, tan suede loafers", "jacket": "ivory white unstructured linen blazer with notch lapels, patch pockets, breathable half lining", "shirt": "pale blue cotton dress shirt with spread collar and mother of pearl buttons", "tie": "no tie, open collar with top button undone for relaxed wedding elegance", "trousers": "ivory white linen trousers with flat front, relaxed fit, cropped at ankle", "shoes": "tan suede penny loafers in soft leather with no socks", "accessories": "blue and white silk pocket square, brown leather belt, round sunglasses", "fabric": "Blazer & Trousers: Pure Linen | Shirt: Premium Cotton | Shoes: Suede Leather", "color": "Ivory White, Pale Blue, Tan, Natural Brown", "avoid": "Black shoes, dark colors, synthetic fabrics, heavy accessories in summer heat", "occasion": "Beach Wedding, Garden Party, Summer Reception, Day Celebration"},
    {"title": "THE GREY CHECK POWER", "subtitle": "Modern Professional", "tag": "MODERN BUSINESS", "full_desc": "grey windowpane check suit, white semi-spread collar shirt, navy knitted tie, black derby shoes", "jacket": "grey windowpane check suit jacket with notch lapels, two-button, flap pockets, subtle pattern", "shirt": "white semi-spread collar shirt in textured cotton with barrel cuffs", "tie": "navy blue knitted silk tie in slim width with textured finish", "trousers": "grey windowpane check trousers with flat front, tapered leg, matching jacket pattern", "shoes": "black leather derby shoes with open lacing and polished toe cap", "accessories": "silver cufflinks, navy pocket square with white border, black leather belt", "fabric": "Suit: Super 110s Wool with Check Pattern | Shirt: Textured Cotton | Tie: Knitted Silk", "color": "Grey, White, Navy Blue, Black, Silver", "avoid": "Brown shoes, clashing patterns, casual belt, sports watch with formal attire", "occasion": "Office, Client Meeting, Business Lunch, Industry Conference"},
    {"title": "THE DOUBLE BREASTED NAVY", "subtitle": "Commanding Presence", "tag": "POWER SUIT", "full_desc": "navy double-breasted suit, light pink dress shirt, navy silk pocket square, brown wholecut shoes", "jacket": "navy double-breasted suit jacket with peak lapels, six-button configuration, structured silhouette", "shirt": "light pink cotton dress shirt with spread collar and French cuffs", "tie": "no tie, open collar with navy silk pocket square as focal point", "trousers": "navy flat front trousers with front pleats, high waist, tapered leg", "shoes": "dark brown wholecut leather shoes with seamless construction and polished finish", "accessories": "navy silk pocket square, gold cufflinks, leather belt, gold dress watch", "fabric": "Suit: Super 130s Wool | Shirt: Premium Cotton | Shoes: Full Grain Leather", "color": "Navy Blue, Soft Pink, Rich Brown, Gold", "avoid": "Black shoes, loud patterns, low-rise trousers, casual accessories with power suit", "occasion": "Board Meeting, Leadership Event, Formal Lunch, High-Stakes Presentation"},
    {"title": "THE CREAM TUXEDO", "subtitle": "Summer Black Tie", "tag": "SUMMER BLACK TIE", "full_desc": "cream white dinner jacket, black dress trousers, black bow tie, black patent shoes, black cummerbund", "jacket": "cream white shawl lapel dinner jacket with single button, jetted pockets, black silk lapel facing", "shirt": "white pleated front dress shirt with wing collar and black stud buttons", "tie": "black silk self-tie bow tie in classic shape matching lapel facing", "trousers": "black tuxedo trousers with satin side stripe, slim fit, no belt", "shoes": "black patent leather oxford shoes with high shine and closed lacing", "accessories": "black cummerbund, white pocket square, black onyx shirt studs", "fabric": "Jacket: Lightweight Wool | Trousers: Wool with Satin Stripe | Shirt: Cotton", "color": "Cream White, Deep Black, Silk Sheen", "avoid": "Brown shoes, belt with tuxedo, colored accessories, short sleeves in formal setting", "occasion": "Summer Gala, Tropical Wedding, Cruise Dinner, Resort Evening Event"},
    {"title": "THE TWEED HERITAGE", "subtitle": "Country Gentleman", "tag": "HERITAGE", "full_desc": "brown herringbone tweed blazer, cream merino sweater, olive corduroy trousers, brown brogue boots", "jacket": "brown herringbone tweed blazer with suede elbow patches, notch lapels, patch pockets", "shirt": "cream merino wool crew neck sweater in fine knit with slim fit", "tie": "no tie, sweater replaces shirt and tie for rustic country elegance", "trousers": "olive green corduroy trousers with flat front, slim fit, soft wale texture", "shoes": "brown leather brogue boots with wingtip detailing and commando rubber sole", "accessories": "wool check scarf, brown leather belt, vintage leather strap watch, flat cap", "fabric": "Blazer: Harris Tweed Wool | Sweater: Merino Wool | Trousers: Cotton Corduroy", "color": "Brown Herringbone, Cream, Olive Green, Tan", "avoid": "Black shoes, synthetic fabrics, formal dress shirt underneath, modern smart accessories", "occasion": "Countryside Walk, Autumn Event, Traditional Pub, Weekend Escape"},
    {"title": "THE MONOCHROME GREY", "subtitle": "Understated Luxury", "tag": "MINIMAL LUXURY", "full_desc": "light grey suit, charcoal turtleneck, grey wool overcoat, black leather chelsea boots", "jacket": "light grey single-breasted suit jacket with notch lapels, two-button, minimal construction", "shirt": "charcoal grey fine-knit turtleneck in merino wool with slim fit and no bulk", "tie": "no tie, turtleneck provides clean neckline without additional accessory", "trousers": "light grey flat front trousers with slim tapered fit, pressed, matching jacket", "shoes": "black leather chelsea boots with sleek profile and elastic side gussets", "accessories": "silver minimalist watch, grey wool scarf, black leather card holder", "fabric": "Suit: Super 100s Wool | Turtleneck: Merino Wool | Overcoat: Wool Cashmere Blend", "color": "Light Grey, Charcoal, Black, Silver", "avoid": "Brown shoes, bright colors, patterned shirt, chunky oversized accessories", "occasion": "Art Gallery Opening, Design Event, Modern Office, Evening Drinks"},
    {"title": "THE TEAL VELVET SMOKING", "subtitle": "Bold Evening", "tag": "EVENING LUXE", "full_desc": "teal blue velvet smoking jacket, black silk shirt, black trousers, black velvet slippers", "jacket": "teal blue velvet smoking jacket with shawl collar in black silk, frog closures", "shirt": "black silk dress shirt with hidden button placket and subtle natural sheen", "tie": "no tie, smoking jacket shawl collar replaces traditional neck accessory", "trousers": "black tailored evening trousers with satin side stripe and high waist", "shoes": "black velvet Albert slippers with gold embroidery and leather sole", "accessories": "gold chain necklace, black silk pocket square, gold dress ring", "fabric": "Jacket: Cotton Velvet with Silk Collar | Shirt: Pure Silk | Slippers: Velvet", "color": "Teal Blue, Deep Black, Gold", "avoid": "Bright clashing colors, casual shoes, belt with evening wear, loud patterns", "occasion": "Private Dinner, VIP Event, After Hours Lounge, Exclusive Party"},
    {"title": "THE OLIVE FIELD JACKET", "subtitle": "Smart Casual", "tag": "SMART CASUAL", "full_desc": "olive green field jacket, white oxford shirt, dark indigo jeans, brown suede chukka boots", "jacket": "olive green cotton field jacket with four pockets, button closure, military-inspired relaxed fit", "shirt": "white oxford button-down shirt with soft collar and barrel cuffs", "tie": "no tie, casual open collar style for relaxed smart casual look", "trousers": "dark indigo raw denim jeans with slim fit, minimal distressing, clean hem", "shoes": "brown suede chukka boots in desert boot style with crepe rubber sole", "accessories": "canvas webbed belt, brown leather strap watch, aviator sunglasses", "fabric": "Jacket: Waxed Cotton | Shirt: Oxford Cotton | Jeans: Raw Denim | Boots: Suede", "color": "Olive Green, White, Dark Indigo, Tan Brown", "avoid": "Formal shoes, bright colors, baggy loose jeans, sports sneakers with smart casual", "occasion": "Weekend Brunch, Casual Friday, Day Out, Travel, Coffee Meeting"},
    {"title": "THE WINTER LAYER KING", "subtitle": "Cold Weather Mastery", "tag": "WINTER LUXE", "full_desc": "charcoal wool overcoat, navy cashmere scarf, black turtleneck, dark jeans, black leather boots", "jacket": "charcoal grey heavy wool overcoat with notch lapels, single breasted, knee length", "shirt": "black cashmere turtleneck sweater, fine knit, slim fit, luxuriously soft", "tie": "no tie, turtleneck and scarf combination replaces traditional tie", "trousers": "dark grey wool trousers with flat front, slim fit, matching overcoat tone", "shoes": "black leather lace-up boots with cap toe, commando sole, polished finish", "accessories": "navy cashmere scarf, black leather gloves, silver watch, leather briefcase", "fabric": "Overcoat: Heavy Wool | Turtleneck: Cashmere | Trousers: Wool Blend | Boots: Leather", "color": "Charcoal Grey, Black, Navy Blue, Silver", "avoid": "Light colors in winter, canvas shoes, thin fabrics, bright accessories in cold weather", "occasion": "Winter Commute, Business Travel, Cold Weather Event, City Walking"},
]


def make_img_url(prompt, seed_offset):
    camera_prompt = (
        "DSLR camera photography, Canon EOS R5, 85mm f/1.2 lens, "
        "professional studio lighting, softbox and rim light, "
        "shallow depth of field, bokeh background, "
        "high resolution 8K, sharp focus on subject, "
        "fashion editorial shot, Vogue style, "
        + prompt
    )
    encoded = urllib.parse.quote(camera_prompt)
    seed = random.randint(1, 999999) + seed_offset
    url = "https://image.pollinations.ai/prompt/" + encoded
    url += "?width=1024&height=1024&seed=" + str(seed)
    url += "&nologo=true&enhance=true"
    return url


def cleanup_old_posts():
    if not os.path.exists("posts"):
        return
    files = glob.glob("posts/post-*.html")
    files.sort(key=os.path.getmtime)
    while len(files) > 7:
        old = files.pop(0)
        os.remove(old)
        print("Cleaned up old post: " + old)


def get_next_post_num():
    if not os.path.exists("posts"):
        return 1
    files = glob.glob("posts/post-*.html")
    return len(files) + 1


def build_slide(num, label, title, text, img):
    s = '<div class="slide">'
    s += '<div class="slide-num">' + num + '</div>'
    s += '<div class="slide-label">' + label + '</div>'
    s += '<img src="' + img + '" alt="' + label + '" class="slide-img">'
    s += '<div class="slide-overlay">'
    s += '<div class="detail-title">' + title + '</div>'
    s += '<div class="detail-text">' + text + '</div>'
    s += '</div></div>'
    return s


def build_html(look, model, date_str, post_num, images):
    s1 = build_slide("01", "FULL LOOK", look["title"], look["full_desc"], images["full"])
    s2 = build_slide("02", "JACKET / COAT", "JACKET DETAIL", look["jacket"], images["jacket"])
    s3 = build_slide("03", "SHIRT / TOP", "SHIRT DETAIL", look["shirt"], images["shirt"])
    s4 = build_slide("04", "TIE / ACCESSORY", "NECK ACCESSORY", look["tie"], images["tie"])
    s5 = build_slide("05", "TROUSERS", "TROUSER DETAIL", look["trousers"], images["trousers"])
    s6 = build_slide("06", "FOOTWEAR", "FOOTWEAR DETAIL", look["shoes"], images["shoes"])
    s7 = build_slide("07", "ACCESSORIES", "ACCESSORIES", look["accessories"], images["accessories"])

    s8 = '<div class="slide spec-slide">'
    s8 += '<div class="slide-num">08</div>'
    s8 += '<div class="slide-label">SPECIFICATIONS</div>'
    s8 += '<div class="specs-panel">'
    s8 += '<div class="specs-title">' + look["title"] + '</div>'
    s8 += '<div class="specs-sub">DETAILS & SPECIFICATIONS</div>'
    s8 += '<div class="specs-grid">'
    s8 += '<div class="spec-box">'
    s8 += '<div class="spec-box-title">FABRIC</div>'
    s8 += '<div class="spec-box-text">' + look["fabric"] + '</div></div>'
    s8 += '<div class="spec-box">'
    s8 += '<div class="spec-box-title">COLOR PALETTE</div>'
    s8 += '<div class="spec-box-text">' + look["color"] + '</div></div>'
    s8 += '<div class="spec-box">'
    s8 += '<div class="spec-box-title">AVOID</div>'
    s8 += '<div class="spec-box-text">' + look["avoid"] + '</div></div>'
    s8 += '<div class="spec-box">'
    s8 += '<div class="spec-box-title">OCCASION</div>'
    s8 += '<div class="spec-box-text">' + look["occasion"] + '</div></div>'
    s8 += '</div>'
    s8 += '<div class="specs-footer">A STATEMENT FOR EVERY OCCASION</div>'
    s8 += '</div></div>'

    slides = s1 + s2 + s3 + s4 + s5 + s6 + s7 + s8

    dots = ""
    for i in range(8):
        active = " active" if i == 0 else ""
        dots += '<span class="dot' + active + '" onclick="goTo(' + str(i) + ')"></span>'

    css = ":root { --bg: #02050a; --panel: rgba(10,22,45,0.98); --cyan: #00bfff; --gold: #d4af37; --text: #e0f0ff; --dim: #5a7a95; --dark: #0a1525; }"
    css += "* { margin:0; padding:0; box-sizing:border-box; }"
    css += "body { background: var(--bg); color: var(--text); font-family: 'Rajdhani', sans-serif; min-height: 100vh; }"
    css += ".container { max-width: 1000px; margin: 0 auto; padding: 30px 16px; }"
    css += ".topbar { display:flex; justify-content:space-between; align-items:center; padding: 14px 20px; background: rgba(2,5,12,0.98); border-bottom: 1px solid rgba(0,100,200,0.08); }"
    css += ".brand { font-family: 'Orbitron', sans-serif; font-size: 13px; color: var(--cyan); letter-spacing: 3px; text-decoration: none; }"
    css += ".back-link { display: inline-flex; align-items: center; gap: 8px; color: var(--cyan); text-decoration: none; font-size: 11px; letter-spacing: 1px; margin-bottom: 16px; }"
    css += ".post-header { text-align: center; margin-bottom: 20px; padding: 0 10px; }"
    css += ".post-date { font-size: 10px; color: var(--dim); letter-spacing: 3px; margin-bottom: 8px; text-transform: uppercase; }"
    css += ".post-title { font-family: 'Playfair Display', serif; font-size: clamp(24px, 6vw, 42px); color: #fff; letter-spacing: 4px; margin-bottom: 4px; }"
    css += ".post-subtitle { font-family: 'Rajdhani', sans-serif; font-size: 13px; color: var(--gold); letter-spacing: 6px; text-transform: uppercase; margin-bottom: 8px; }"
    css += ".ai-badge { display:inline-flex; align-items:center; gap:6px; font-size:9px; color:var(--dim); letter-spacing:2px; margin-bottom:16px; justify-content:center; width:100%; }"
    css += ".ai-badge span { color:var(--cyan); }"
    css += ".carousel-container { position: relative; width: 100%; max-width: 900px; margin: 0 auto 30px; border-radius: 12px; overflow: hidden; border: 1px solid rgba(0,100,200,0.1); background: var(--dark); }"
    css += ".carousel-track { display: flex; transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1); }"
    css += ".slide { min-width: 100%; position: relative; }"
    css += ".slide-img { width: 100%; height: auto; max-height: 70vh; object-fit: cover; display: block; }"
    css += ".slide-num { position: absolute; top: 16px; left: 20px; font-family: 'Playfair Display', serif; font-size: 32px; color: rgba(255,255,255,0.15); font-weight: 700; z-index: 5; line-height: 1; }"
    css += ".slide-label { position: absolute; top: 22px; left: 60px; font-size: 10px; color: var(--gold); letter-spacing: 3px; text-transform: uppercase; z-index: 5; background: rgba(0,0,0,0.4); padding: 3px 10px; border-radius: 4px; border: 1px solid rgba(212,175,55,0.15); }"
    css += ".slide-overlay { position: absolute; bottom: 0; left: 0; right: 0; padding: 40px 24px 24px; background: linear-gradient(to top, rgba(2,5,10,0.95) 0%, rgba(2,5,10,0.6) 60%, transparent 100%); z-index: 4; }"
    css += ".slide-title-overlay { font-family: 'Playfair Display', serif; font-size: 24px; color: #fff; letter-spacing: 2px; margin-bottom: 4px; }"
    css += ".slide-sub-overlay { font-size: 12px; color: var(--gold); letter-spacing: 4px; text-transform: uppercase; margin-bottom: 8px; }"
    css += ".slide-desc { font-size: 13px; color: var(--text); line-height: 1.6; opacity: 0.9; }"
    css += ".detail-title { font-family: 'Orbitron', sans-serif; font-size: 11px; color: var(--gold); letter-spacing: 3px; margin-bottom: 6px; }"
    css += ".detail-text { font-size: 14px; color: var(--text); line-height: 1.5; }"
    css += ".spec-slide { background: linear-gradient(145deg, #0a1525, #050a12); min-height: 500px; display: flex; align-items: center; justify-content: center; padding: 40px 24px; }"
    css += ".specs-panel { width: 100%; max-width: 700px; border: 1px solid rgba(212,175,55,0.15); border-radius: 12px; padding: 32px 28px; background: rgba(0,0,0,0.3); }"
    css += ".specs-title { font-family: 'Playfair Display', serif; font-size: 28px; color: #fff; text-align: center; letter-spacing: 3px; margin-bottom: 4px; }"
    css += ".specs-sub { font-size: 10px; color: var(--gold); text-align: center; letter-spacing: 5px; margin-bottom: 28px; text-transform: uppercase; }"
    css += ".specs-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 24px; }"
    css += ".spec-box { background: rgba(0,20,40,0.5); border: 1px solid rgba(0,100,200,0.08); border-radius: 8px; padding: 16px; }"
    css += ".spec-box-title { font-family: 'Orbitron', sans-serif; font-size: 9px; color: var(--gold); letter-spacing: 2px; margin-bottom: 8px; }"
    css += ".spec-box-text { font-size: 12px; color: var(--text); line-height: 1.6; }"
    css += ".specs-footer { text-align: center; font-size: 10px; color: var(--dim); letter-spacing: 4px; text-transform: uppercase; padding-top: 16px; border-top: 1px solid rgba(212,175,55,0.1); }"
    css += ".carousel-btn { position: absolute; top: 50%; transform: translateY(-50%); background: rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1); color: #fff; width: 40px; height: 40px; border-radius: 50%; cursor: pointer; font-size: 14px; z-index: 10; transition: all 0.2s; display: flex; align-items: center; justify-content: center; }"
    css += ".carousel-btn:hover { background: rgba(212,175,55,0.2); border-color: var(--gold); }"
    css += ".carousel-btn.prev { left: 12px; }"
    css += ".carousel-btn.next { right: 12px; }"
    css += ".carousel-dots { display: flex; justify-content: center; gap: 8px; padding: 14px; background: rgba(0,0,0,0.4); }"
    css += ".dot { width: 8px; height: 8px; border-radius: 50%; background: rgba(255,255,255,0.15); cursor: pointer; transition: all 0.3s; }"
    css += ".dot.active { background: var(--gold); box-shadow: 0 0 8px rgba(212,175,55,0.4); }"
    css += ".slide-counter { position: absolute; bottom: 56px; right: 20px; font-size: 11px; color: var(--dim); letter-spacing: 1px; z-index: 5; background: rgba(0,0,0,0.4); padding: 4px 10px; border-radius: 4px; }"
    css += ".tags { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; margin-bottom: 30px; }"
    css += ".tag { padding: 5px 16px; border-radius: 20px; font-size: 9px; letter-spacing: 2px; text-transform: uppercase; }"
    css += ".tag.cat { background: rgba(0,100,200,0.08); border: 1px solid rgba(0,140,255,0.12); color: var(--cyan); }"
    css += ".tag.model { background: rgba(212,175,55,0.05); border: 1px solid rgba(212,175,55,0.1); color: var(--gold); }"
    css += ".footer { text-align: center; padding: 24px; font-size: 10px; color: var(--dim); letter-spacing: 2px; border-top: 1px solid rgba(0,100,200,0.05); margin-top: 20px; }"
    css += "@media (max-width: 600px) { .specs-grid { grid-template-columns: 1fr; } .slide-num { font-size: 24px; } .slide-label { left: 50px; font-size: 9px; } .slide-title-overlay { font-size: 18px; } .specs-title { font-size: 22px; } }"

    js = "var current = 0; var total = 8; var track = document.getElementById('track'); var currentEl = document.getElementById('current'); var dots = document.querySelectorAll('.dot');"
    js += "function update() { track.style.transform = 'translateX(-' + (current * 100) + '%)'; currentEl.textContent = current + 1; dots.forEach(function(d, i) { d.classList.toggle('active', i === current); }); }"
    js += "function move(dir) { current = (current + dir + total) % total; update(); }"
    js += "function goTo(idx) { current = idx; update(); }"
    js += "setInterval(function() { move(1); }, 6000);"
    js += "document.addEventListener('keydown', function(e) { if (e.key === 'ArrowRight') move(1); if (e.key === 'ArrowLeft') move(-1); });"
    js += "var startX = 0; track.addEventListener('touchstart', function(e) { startX = e.touches[0].clientX; }); track.addEventListener('touchend', function(e) { var diff = startX - e.changedTouches[0].clientX; if (Math.abs(diff) > 50) move(diff > 0 ? 1 : -1); });"

    html = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">'
    html += '<title>' + look["title"] + ' | M&WEFTCO</title>'
    html += '<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;400;500;600;700&family=Playfair+Display:wght@400;700&display=swap" rel="stylesheet">'
    html += '<style>' + css + '</style>'
    html += '</head><body>'

    html += '<div class="topbar"><a href="../index.html" class="brand">M&WEFTCO</a>'
    html += '<div style="font-size:9px; color:var(--dim); letter-spacing:2px;">AURELIA // EDITORIAL</div></div>'

    html += '<div class="container">'
    html += '<a href="../index.html" class="back-link">&#8592; Back to Home</a>'

    html += '<div class="post-header">'
    html += '<div class="post-date">' + date_str + ' // AURELIA EDITORIAL #' + str(post_num) + '</div>'
    html += '<div class="ai-badge"><span>&#9889;</span> AI-GENERATED FASHION EDITORIAL // ' + model["name"].upper() + '</div>'
    html += '<div class="post-title">' + look["title"] + '</div>'
    html += '<div class="post-subtitle">' + look["subtitle"] + '</div>'
    html += '</div>'

    html += '<div class="tags"><span class="tag cat">#' + look["tag"] + '</span>'
    html += '<span class="tag model">' + model["name"].upper() + '</span></div>'

    html += '<div class="carousel-container"><div class="carousel-track" id="track">'
    html += slides
    html += '</div>'
    html += '<button class="carousel-btn prev" onclick="move(-1)">&#10094;</button>'
    html += '<button class="carousel-btn next" onclick="move(1)">&#10095;</button>'
    html += '<div class="carousel-dots">' + dots + '</div>'
    html += '<div class="slide-counter"><span id="current">1</span> / 8</div>'
    html += '</div>'

    html += '</div>'
    html += '<div class="footer">M&WEFTCO // CRAFTED FOR THE MODERN MAN // AURELIA AI FASHION EDITORIAL ENGINE</div>'
    html += '<script>' + js + '</script>'
    html += '</body></html>'

    return html


def build_vera_report(look, model, date_str, time_str, post_num, reach, xp, leveled):
    report = "VERA DAILY REPORT // AURELIA CONTENT AGENT\n"
    report += "=" * 50 + "\n"
    report += "Date: " + date_str + " | Time: " + time_str + "\n"
    report += "Post #: " + str(post_num) + "\n"
    report += "OUTFIT: " + look["title"] + "\n"
    report += "SUBTITLE: " + look["subtitle"] + "\n"
    report += "CATEGORY: " + look["tag"] + "\n"
    report += "MODEL: " + model["name"] + "\n"
    report += "-" * 50 + "\n"
    report += "FULL LOOK: " + look["full_desc"] + "\n"
    report += "JACKET: " + look["jacket"] + "\n"
    report += "SHIRT: " + look["shirt"] + "\n"
    report += "TIE: " + look["tie"] + "\n"
    report += "TROUSERS: " + look["trousers"] + "\n"
    report += "SHOES: " + look["shoes"] + "\n"
    report += "ACCESSORIES: " + look["accessories"] + "\n"
    report += "-" * 50 + "\n"
    report += "FABRIC: " + look["fabric"] + "\n"
    report += "COLOR: " + look["color"] + "\n"
    report += "AVOID: " + look["avoid"] + "\n"
    report += "OCCASION: " + look["occasion"] + "\n"
    report += "-" * 50 + "\n"
    report += "STATS:\n"
    report += "  XP Earned Today: " + str(xp) + "\n"
    report += "  AURELIA Level: " + str(AURELIA_LEVEL) + "\n"
    report += "  AURELIA XP: " + str(AURELIA_XP) + "/" + str(AURELIA_LEVEL * 100) + "\n"
    report += "  Daily Reach: " + str(reach) + " views\n"
    report += "  Total Global Reach: " + str(AURELIA_GLOBAL_REACH) + " views\n"
    if leveled:
        report += "  *** LEVEL UP! AURELIA is now LEVEL " + str(AURELIA_LEVEL) + "! ***\n"
    report += "=" * 50 + "\n"
    report += "Message for Meraj-nim (+918929520956):\n"
    report += "AURELIA posted today: " + look["title"] + " (" + look["tag"] + ")\n"
    report += "Check it at: https://mweftco.github.io/mweftco/posts/post-"
    report += str(post_num).zfill(3) + ".html\n"
    report += "=" * 50
    return report


def update_index(title, slug, date_str, img_url, tag):
    if not os.path.exists("index.html"):
        print("WARNING: index.html not found, skipping index update")
        return

    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    marker = "<!-- AURELIA POSTS -->"

    post_link = '<a href="posts/' + slug + '.html" style="display:block; background:rgba(10,22,45,0.95); border:1px solid rgba(0,100,200,0.12); border-radius:10px; overflow:hidden; text-decoration:none; color:inherit; transition:all 0.2s; margin-bottom:12px;" onmouseover="this.style.borderColor=\'rgba(0,180,255,0.3)\'" onmouseout="this.style.borderColor=\'rgba(0,100,200,0.12)\'">'
    post_link += '<div style="height:180px; background-image:url(' + img_url + '); background-size:cover; background-position:center top;"></div>'
    post_link += '<div style="padding:16px;"><div style="font-size:10px; color:var(--dim); letter-spacing:1px; margin-bottom:4px;">' + date_str + ' // EDITORIAL</div>'
    post_link += '<div style="font-size:15px; color:#fff; font-weight:600; margin-bottom:6px;">' + title + '</div>'
    post_link += '<span style="font-size:9px; padding:3px 10px; border-radius:12px; background:rgba(0,100,200,0.08); border:1px solid rgba(0,140,255,0.1); color:var(--cyan); letter-spacing:1px;">#' + tag + '</span></div></a>'

    if marker not in content:
        section = "\n<!-- AURELIA POSTS -->\n<div style=\"max-width:900px; margin:40px auto; padding:0 20px;\">\n"
        section += "<div style=\"font-family:'Orbitron',sans-serif; font-size:14px; color:var(--cyan); letter-spacing:3px; margin-bottom:20px;\">LATEST FROM AURELIA // AI FASHION EDITORIAL</div>\n"
        section += '<div id="aurelia-posts">\n' + post_link + "\n</div></div>\n"
        content = content.replace("</body>", section + "</body>")
    else:
        insert_marker = '<div id="aurelia-posts">'
        if insert_marker in content:
            content = content.replace(insert_marker, insert_marker + "\n    " + post_link)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)

    print("Index updated successfully")


def generate_post():
    global AURELIA_LEVEL, AURELIA_XP, AURELIA_TOTAL_POSTS, AURELIA_GLOBAL_REACH
    print("=" * 60)
    print("AURELIA v5.3 COMPLETE starting...")
    cleanup_old_posts()
    model = random.choice(MODELS)
    look = random.choice(LOOKS)
    now = datetime.now()
    post_num = get_next_post_num()
    slug = "post-" + str(post_num).zfill(3)
    date_str = now.strftime("%B %d, %Y")
    time_str = now.strftime("%I:%M %p")
    print("Selected: Model=" + model["name"] + " | Look=" + look["title"])
    base = "fashion model, professional photoshoot, " + model["desc"]
    images = {
        "full": make_img_url(base + ", full body shot wearing " + look["full_desc"] + ", dark grey studio backdrop, dramatic side lighting", 1),
        "jacket": make_img_url(base + ", extreme close-up of " + look["jacket"] + ", detail texture visible, macro lens, dark background", 2),
        "shirt": make_img_url(base + ", close-up of " + look["shirt"] + ", collar and fabric detail, fashion macro photography", 3),
        "tie": make_img_url(base + ", close-up of " + look["tie"] + ", neck and chest detail shot, luxury accessory focus", 4),
        "trousers": make_img_url(base + ", lower body shot showing " + look["trousers"] + ", standing pose, studio lighting", 5),
        "shoes": make_img_url(base + ", close-up of feet wearing " + look["shoes"] + ", dark reflective floor, footwear detail", 6),
        "accessories": make_img_url(base + ", flat lay of " + look["accessories"] + ", dark marble surface, product photography", 7),
    }
    print("Image URLs generated successfully")
    AURELIA_TOTAL_POSTS = post_num
    daily_reach = random.randint(1200, 8500)
    AURELIA_GLOBAL_REACH += daily_reach
    xp_earned = random.randint(45, 95)
    AURELIA_XP += xp_earned
    leveled_up = False
    xp_needed = AURELIA_LEVEL * 100
    if AURELIA_XP >= xp_needed:
        AURELIA_XP -= xp_needed
        AURELIA_LEVEL += 1
        leveled_up = True
    print("Stats: XP=" + str(xp_earned) + " | Level=" + str(AURELIA_LEVEL) + " | Reach=" + str(daily_reach))
    if not os.path.exists("posts"):
        os.makedirs("posts")
        print("Created posts/ directory")
    post_path = "posts/" + slug + ".html"
    html_content = build_html(look, model, date_str, post_num, images)
    with open(post_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Post saved: " + post_path)
    update_index(look["title"], slug, date_str, images["full"], look["tag"])
    if not os.path.exists("reports"):
        os.makedirs("reports")
        print("Created reports/ directory")
    report_path = "reports/vera-report-" + slug + ".txt"
    report = build_vera_report(look, model, date_str, time_str, post_num, daily_reach, xp_earned, leveled_up)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    latest_path = "reports/vera-latest-report.txt"
    with open(latest_path, "w", encoding="utf-8") as f:
        f.write(report)
    print("VERA report saved: " + report_path)
    if leveled_up:
        print("*** LEVEL UP! AURELIA is now LEVEL " + str(AURELIA_LEVEL) + "! ***")
    print("SUCCESS: Posted editorial " + look["title"] + "!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    print("AURELIA v5.3 COMPLETE")
    print("Features: DSLR Images | Auto Cleanup | VERA Reports | XP System | 8-Slide Carousel")
    print("-" * 60)
    success = generate_post()
    if success:
        print("ALL DONE!")
    else:
        print("FAILED!")
