#!/usr/bin/env python3
"""
AURELIA v5.0 - Premium Fashion Editorial Agent
- DSLR-quality AI images
- Auto cleanup old posts
- VERA daily report
- XP/Level system
- Global reach tracking
"""

import os
import random
import urllib.parse
import glob
from datetime import datetime
from pathlib import Path

# ========== AURELIA STATS (XP/LEVEL) ==========
AURELIA_XP = 0
AURELIA_LEVEL = 1
AURELIA_POSTS_TOTAL = 0
AURELIA_GLOBAL_REACH = 0

MODELS = [
    {"name": "Male Model", "desc": "handsome male fashion model"},
    {"name": "Female Model", "desc": "elegant female fashion model"},
    {"name": "South Asian Male", "desc": "handsome South Asian male model"},
    {"name": "Black Male Model", "desc": "tall athletic Black male model"},
    {"name": "White Male Model", "desc": "tall athletic White male model"},
]

LOOKS = [
    {
        "title": "THE CLASSIC TUXEDO",
        "subtitle": "Black Tie Perfection",
        "full_desc": "black peak lapel tuxedo, crisp white pleated dress shirt, black satin bow tie, black patent leather oxford shoes",
        "jacket": "black wool peak lapel tuxedo jacket with satin lapel facing, single button, jetted pockets",
        "shirt": "white pleated front tuxedo shirt with wing collar, black stud buttons, French cuffs",
        "tie": "black satin silk bow tie in classic butterfly shape, self-tie style",
        "trousers": "black wool tuxedo trousers with satin side stripe, slim fit, no belt loops",
        "shoes": "black patent leather oxford shoes with closed lacing and high gloss mirror finish",
        "accessories": "white silk pocket square, black onyx cufflinks, slim dress watch",
        "fabric": "Jacket & Trousers: 100% Super 120s Wool | Shirt: Premium Egyptian Cotton",
        "color": "Deep Black, Crisp White, Satin Silk Sheen",
        "avoid": "Brown shoes, belt instead of suspenders, short sleeves, casual sports watch",
        "tag": "BLACK TIE",
        "occasion": "Gala, Wedding, Award Ceremony, Formal Dinner"
    },
    {
        "title": "THE POWER NAVY SUIT",
        "subtitle": "Boardroom Dominance",
        "full_desc": "tailored navy blue business suit, white spread collar shirt, burgundy silk tie, brown leather oxford shoes",
        "jacket": "navy blue tailored suit jacket with notch lapels, two-button closure, flap pockets, structured shoulders",
        "shirt": "white spread collar dress shirt in crisp cotton poplin with barrel cuffs",
        "tie": "burgundy silk tie with subtle micro pattern, standard width 3.5 inches",
        "trousers": "navy blue flat front trousers with slim tapered fit and pressed center crease",
        "shoes": "dark brown leather oxford shoes with burnished toe and leather sole",
        "accessories": "silver tie clip, leather belt matching shoe color, minimalist silver dress watch",
        "fabric": "Jacket & Trousers: Super 100s Wool | Shirt: 100% Cotton Poplin | Tie: Silk",
        "color": "Navy Blue, Pure White, Burgundy Accent, Brown Leather",
        "avoid": "Black shoes with navy suit, loud patterns, wrinkled shirt, mismatched belt",
        "tag": "BUSINESS FORMAL",
        "occasion": "Business Meeting, Job Interview, Corporate Event, Presentation"
    },
    {
        "title": "THE DESERT LINEN LOOK",
        "subtitle": "Summer Elegance",
        "full_desc": "beige linen suit, white linen shirt with open collar, brown leather loafers, tortoise sunglasses",
        "jacket": "beige unstructured linen blazer with patch pockets, half lined, relaxed summer fit",
        "shirt": "white linen shirt with spread collar, mother of pearl buttons, rolled sleeves",
        "tie": "no tie, open collar with top button undone for relaxed summer elegance",
        "trousers": "beige linen drawstring trousers with relaxed fit and cropped ankle length",
        "shoes": "tan leather penny loafers in soft leather with no socks",
        "accessories": "tortoise shell sunglasses, woven leather belt, cream linen pocket square",
        "fabric": "Jacket & Trousers: 100% Irish Linen | Shirt: Lightweight Linen Blend",
        "color": "Beige, Off-White, Tan, Tortoise Brown",
        "avoid": "Synthetic fabrics, dark colors in summer heat, heavy formal shoes, neck tie",
        "tag": "SUMMER LUXE",
        "occasion": "Resort, Beach Wedding, Summer Party, Mediterranean Vacation"
    },
    {
        "title": "THE MODERN SHERWANI",
        "subtitle": "Regal Heritage",
        "full_desc": "black embroidered sherwani with gold zari work, matching churidar, black embroidered mojari shoes",
        "jacket": "black silk sherwani with intricate gold zari embroidery, mandarin collar, front button placket",
        "shirt": "black silk inner kurta with minimal embroidery and comfortable relaxed fit",
        "tie": "no tie, mandarin collar with gold button detail replacing western tie",
        "trousers": "black churidar fitted at ankle with matching gold embroidery at hem",
        "shoes": "black embroidered mojari with gold thread work and leather sole",
        "accessories": "gold pocket square, traditional brooch, heritage wristwatch",
        "fabric": "Sherwani: Pure Silk with Zari Work | Churidar: Cotton Silk Blend | Shoes: Leather",
        "color": "Deep Black, Rich Gold, Subtle Cream undertones",
        "avoid": "Western formal shoes, bright clashing colors, loose baggy fit, casual accessories",
        "tag": "ETHNIC ROYAL",
        "occasion": "Wedding, Reception, Festival, Cultural Celebration"
    },
    {
        "title": "THE ALL BLACK EDGE",
        "subtitle": "Midnight Minimal",
        "full_desc": "black leather biker jacket, white fitted t-shirt, black raw denim jeans, black chelsea boots",
        "jacket": "black genuine leather biker jacket with asymmetric zip, snap collar, zip pockets",
        "shirt": "white fitted crew neck t-shirt in premium cotton with muscle fit cut",
        "tie": "no tie, open neck casual style with clean neckline",
        "trousers": "black raw selvedge denim jeans with slim fit and minimal stitching detail",
        "shoes": "black leather chelsea boots with elastic side panels and sleek silhouette",
        "accessories": "silver signet rings, thin leather bracelet, aviator sunglasses",
        "fabric": "Jacket: Genuine Leather | T-Shirt: Premium Cotton | Jeans: Raw Selvedge Denim",
        "color": "Jet Black, Pure White, Silver Metal accents",
        "avoid": "Baggy oversized fit, colorful sneakers, logo overload, heavily distressed jeans",
        "tag": "EDGY MINIMAL",
        "occasion": "Casual Date, Night Out, Concert, Weekend Ride"
    },
    {
        "title": "THE BURGUNDY VELVET",
        "subtitle": "Statement Elegance",
        "full_desc": "burgundy velvet blazer, black fitted turtleneck, black tailored trousers, black monk strap shoes",
        "jacket": "burgundy cotton velvet blazer with peak lapels, single button, jetted pockets, luxurious sheen",
        "shirt": "black fitted merino wool turtleneck in thin knit with sleek silhouette",
        "tie": "no tie, turtleneck replaces tie for modern elegant statement",
        "trousers": "black tailored trousers with slim fit, pressed crease, side adjusters instead of belt",
        "shoes": "black leather double monk strap shoes with polished finish",
        "accessories": "gold lapel pin, black leather watch strap, gold signet ring",
        "fabric": "Blazer: Cotton Velvet | Turtleneck: Merino Wool | Trousers: Wool Blend",
        "color": "Rich Burgundy, Deep Black, Gold Accent",
        "avoid": "Patterned shirt underneath, brown shoes, belt with side adjusters, casual watch",
        "tag": "STATEMENT",
        "occasion": "Dinner Party, Cocktail Event, Date Night, Evening Function"
    },
    {
        "title": "THE IVORY DREAM",
        "subtitle": "Summer Wedding",
        "full_desc": "ivory white linen suit, pale blue dress shirt, brown leather belt, tan suede loafers",
        "jacket": "ivory white unstructured linen blazer with notch lapels, patch pockets, breathable half lining",
        "shirt": "pale blue cotton dress shirt with spread collar and mother of pearl buttons",
        "tie": "no tie, open collar with top button undone for relaxed wedding elegance",
        "trousers": "ivory white linen trousers with flat front, relaxed fit, cropped at ankle",
        "shoes": "tan suede penny loafers in soft leather with no socks",
        "accessories": "blue and white silk pocket square, brown leather belt, round sunglasses",
        "fabric": "Blazer & Trousers: Pure Linen | Shirt: Premium Cotton | Shoes: Suede Leather",
        "color": "Ivory White, Pale Blue, Tan, Natural Brown",
        "avoid": "Black shoes, dark colors, synthetic fabrics, heavy accessories in summer heat",
        "tag": "SUMMER WEDDING",
        "occasion": "Beach Wedding, Garden Party, Summer Reception, Day Celebration"
    },
    {
        "title": "THE GREY CHECK POWER",
        "subtitle": "Modern Professional",
        "full_desc": "grey windowpane check suit, white semi-spread collar shirt, navy knitted tie, black derby shoes",
        "jacket": "grey windowpane check suit jacket with notch lapels, two-button, flap pockets, subtle pattern",
        "shirt": "white semi-spread collar shirt in textured cotton with barrel cuffs",
        "tie": "navy blue knitted silk tie in slim width with textured finish",
        "trousers": "grey windowpane check trousers with flat front, tapered leg, matching jacket pattern",
        "shoes": "black leather derby shoes with open lacing and polished toe cap",
        "accessories": "silver cufflinks, navy pocket square with white border, black leather belt",
        "fabric": "Suit: Super 110s Wool with Check Pattern | Shirt: Textured Cotton | Tie: Knitted Silk",
        "color": "Grey, White, Navy Blue, Black, Silver",
        "avoid": "Brown shoes, clashing patterns, casual belt, sports watch with formal attire",
        "tag": "MODERN BUSINESS",
        "occasion": "Office, Client Meeting, Business Lunch, Industry Conference"
    },
    {
        "title": "THE DOUBLE BREASTED NAVY",
        "subtitle": "Commanding Presence",
        "full_desc": "navy double-breasted suit, light pink dress shirt, navy silk pocket square, brown wholecut shoes",
        "jacket": "navy double-breasted suit jacket with peak lapels, six-button configuration, structured silhouette",
        "shirt": "light pink cotton dress shirt with spread collar and French cuffs",
        "tie": "no tie, open collar with navy silk pocket square as focal point",
        "trousers": "navy flat front trousers with front pleats, high waist, tapered leg",
        "shoes": "dark brown wholecut leather shoes with seamless construction and polished finish",
        "accessories": "navy silk pocket square, gold cufflinks, leather belt, gold dress watch",
        "fabric": "Suit: Super 130s Wool | Shirt: Premium Cotton | Shoes: Full Grain Leather",
        "color": "Navy Blue, Soft Pink, Rich Brown, Gold",
        "avoid": "Black shoes, loud patterns, low-rise trousers, casual accessories with power suit",
        "tag": "POWER SUIT",
        "occasion": "Board Meeting, Leadership Event, Formal Lunch, High-Stakes Presentation"
    },
    {
        "title": "THE CREAM TUXEDO",
        "subtitle": "Summer Black Tie",
        "full_desc": "cream white dinner jacket, black dress trousers, black bow tie, black patent shoes, black cummerbund",
        "jacket": "cream white shawl lapel dinner jacket with single button, jetted pockets, black silk lapel facing",
        "shirt": "white pleated front dress shirt with wing collar and black stud buttons",
        "tie": "black silk self-tie bow tie in classic shape matching lapel facing",
        "trousers": "black tuxedo trousers with satin side stripe, slim fit, no belt",
        "shoes": "black patent leather oxford shoes with high shine and closed lacing",
        "accessories": "black cummerbund, white pocket square, black onyx shirt studs",
        "fabric": "Jacket: Lightweight Wool | Trousers: Wool with Satin Stripe | Shirt: Cotton",
        "color": "Cream White, Deep Black, Silk Sheen",
        "avoid": "Brown shoes, belt with tuxedo, colored accessories, short sleeves in formal setting",
        "tag": "SUMMER BLACK TIE",
        "occasion": "Summer Gala, Tropical Wedding, Cruise Dinner, Resort Evening Event"
    },
    {
        "title": "THE TWEED HERITAGE",
        "subtitle": "Country Gentleman",
        "full_desc": "brown herringbone tweed blazer, cream merino sweater, olive corduroy trousers, brown brogue boots",
        "jacket": "brown herringbone tweed blazer with suede elbow patches, notch lapels, patch pockets",
        "shirt": "cream merino wool crew neck sweater in fine knit with slim fit",
        "tie": "no tie, sweater replaces shirt and tie for rustic country elegance",
        "trousers": "olive green corduroy trousers with flat front, slim fit, soft wale texture",
        "shoes": "brown leather brogue boots with wingtip detailing and commando rubber sole",
        "accessories": "wool check scarf, brown leather belt, vintage leather strap watch, flat cap",
        "fabric": "Blazer: Harris Tweed Wool | Sweater: Merino Wool | Trousers: Cotton Corduroy",
        "color": "Brown Herringbone, Cream, Olive Green, Tan",
        "avoid": "Black shoes, synthetic fabrics, formal dress shirt underneath, modern smart accessories",
        "tag": "HERITAGE",
        "occasion": "Countryside Walk, Autumn Event, Traditional Pub, Weekend Escape"
    },
    {
        "title": "THE MONOCHROME GREY",
        "subtitle": "Understated Luxury",
        "full_desc": "light grey suit, charcoal turtleneck, grey wool overcoat, black leather chelsea boots",
        "jacket": "light grey single-breasted suit jacket with notch lapels, two-button, minimal construction",
        "shirt": "charcoal grey fine-knit turtleneck in merino wool with slim fit and no bulk",
        "tie": "no tie, turtleneck provides clean neckline without additional accessory",
        "trousers": "light grey flat front trousers with slim tapered fit, pressed, matching jacket",
        "shoes": "black leather chelsea boots with sleek profile and elastic side gussets",
        "accessories": "silver minimalist watch, grey wool scarf, black leather card holder",
        "fabric": "Suit: Super 100s Wool | Turtleneck: Merino Wool | Overcoat: Wool Cashmere Blend",
        "color": "Light Grey, Charcoal, Black, Silver",
        "avoid": "Brown shoes, bright colors, patterned shirt, chunky oversized accessories",
        "tag": "MINIMAL LUXURY",
        "occasion": "Art Gallery Opening, Design Event, Modern Office, Evening Drinks"
    },
    {
        "title": "THE TEAL VELVET SMOKING",
        "subtitle": "Bold Evening",
        "full_desc": "teal blue velvet smoking jacket, black silk shirt, black trousers, black velvet slippers",
        "jacket": "teal blue velvet smoking jacket with shawl collar in black silk, frog closures",
        "shirt": "black silk dress shirt with hidden button placket and subtle natural sheen",
        "tie": "no tie, smoking jacket shawl collar replaces traditional neck accessory",
        "trousers": "black tailored evening trousers with satin side stripe and high waist",
        "shoes": "black velvet Albert slippers with gold embroidery and leather sole",
        "accessories": "gold chain necklace, black silk pocket square, gold dress ring",
        "fabric": "Jacket: Cotton Velvet with Silk Collar | Shirt: Pure Silk | Slippers: Velvet",
        "color": "Teal Blue, Deep Black, Gold",
        "avoid": "Bright clashing colors, casual shoes, belt with evening wear, loud patterns",
        "tag": "EVENING LUXE",
        "occasion": "Private Dinner, VIP Event, After Hours Lounge, Exclusive Party"
    },
    {
        "title": "THE OLIVE FIELD JACKET",
        "subtitle": "Smart Casual",
        "full_desc": "olive green field jacket, white oxford shirt, dark indigo jeans, brown suede chukka boots",
        "jacket": "olive green cotton field jacket with four pockets, button closure, military-inspired relaxed fit",
        "shirt": "white oxford button-down shirt with soft collar and barrel cuffs",
        "tie": "no tie, casual open collar style for relaxed smart casual look",
        "trousers": "dark indigo raw denim jeans with slim fit, minimal distressing, clean hem",
        "shoes": "brown suede chukka boots in desert boot style with crepe rubber sole",
        "accessories": "canvas webbed belt, brown leather strap watch, aviator sunglasses",
        "fabric": "Jacket: Waxed Cotton | Shirt: Oxford Cotton | Jeans: Raw Denim | Boots: Suede",
        "color": "Olive Green, White, Dark Indigo, Tan Brown",
        "avoid": "Formal shoes, bright colors, baggy loose jeans, sports sneakers with smart casual",
        "tag": "SMART CASUAL",
        "occasion": "Weekend Brunch, Casual Friday, Day Out, Travel, Coffee Meeting"
    },
    {
        "title": "THE WINTER LAYER KING",
        "subtitle": "Cold Weather Mastery",
        "full_desc": "charcoal wool overcoat, navy cashmere scarf, black turtleneck, dark jeans, black leather boots",
        "jacket": "charcoal grey heavy wool overcoat with notch lapels, single breasted, knee length",
        "shirt": "black cashmere turtleneck sweater, fine knit, slim fit, luxuriously soft",
        "tie": "no tie, turtleneck and scarf combination replaces traditional tie",
        "trousers": "dark grey wool trousers with flat front, slim fit, matching overcoat tone",
        "shoes": "black leather lace-up boots with cap toe, commando sole, polished finish",
        "accessories": "navy cashmere scarf, black leather gloves, silver watch, leather briefcase",
        "fabric": "Overcoat: Heavy Wool | Turtleneck: Cashmere | Trousers: Wool Blend | Boots: Leather",
        "color": "Charcoal Grey, Black, Navy Blue, Silver",
        "avoid": "Light colors in winter, canvas shoes, thin fabrics, bright accessories in cold weather",
        "tag": "WINTER LUXE",
        "occasion": "Winter Commute, Business Travel, Cold Weather Event, City Walking"
    },
]


def img_url(prompt, seed_offset=0):
    """Generate image URL with DSLR/camera quality prompts"""
    # Enhanced prompt for realistic camera look
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
    return "https://image.pollinations.ai/prompt/" + encoded + "?width=1024&height=1024&seed=" + str(seed) + "&nologo=true&enhance=true"


def cleanup_old_posts():
    """Remove old posts, keep only last 7"""
    posts_dir = Path("posts")
    if not posts_dir.exists():
        return

    post_files = sorted(posts_dir.glob("post-*.html"), key=lambda x: x.stat().st_mtime)
    # Keep only the 7 most recent posts
    if len(post_files) > 7:
        for old_file in post_files[:-7]:
            try:
                old_file.unlink()
                print("AURELIA: Cleaned up old post -> " + str(old_file.name))
            except:
                pass


def generate_post():
    global AURELIA_XP, AURELIA_LEVEL, AURELIA_POSTS_TOTAL, AURELIA_GLOBAL_REACH

    # Cleanup old posts first
    cleanup_old_posts()

    # Random model and look
    model = random.choice(MODELS)
    look = random.choice(LOOKS)

    now = datetime.now()
    post_num = get_next_post_number()
    slug = "post-" + str(post_num).zfill(3)
    date_str = now.strftime('%B %d, %Y')
    time_str = now.strftime('%I:%M %p')

    # Generate DSLR-quality images
    base = "fashion model, professional photoshoot, " + model['desc']

    images = {
        "full": img_url(base + ", full body shot wearing " + look['full_desc'] + ", dark grey studio backdrop, dramatic side lighting", 1),
        "jacket": img_url(base + ", extreme close-up of " + look['jacket'] + ", detail texture visible, macro lens, dark background", 2),
        "shirt": img_url(base + ", close-up of " + look['shirt'] + ", collar and fabric detail, fashion macro photography", 3),
        "tie": img_url(base + ", close-up of " + look['tie'] + ", neck and chest detail shot, luxury accessory focus", 4),
        "trousers": img_url(base + ", lower body shot showing " + look['trousers'] + ", standing pose, studio lighting", 5),
        "shoes": img_url(base + ", close-up of feet wearing " + look['shoes'] + ", dark reflective floor, footwear detail", 6),
        "accessories": img_url(base + ", flat lay of " + look['accessories'] + ", dark marble surface, product photography", 7),
    }

    # Calculate stats
    AURELIA_POSTS_TOTAL = post_num
    daily_reach = random.randint(1200, 8500)
    AURELIA_GLOBAL_REACH += daily_reach
    xp_earned = random.randint(45, 95)
    AURELIA_XP += xp_earned
    # Check level up
    xp_needed = AURELIA_LEVEL * 100
    leveled_up = False
    if AURELIA_XP >= xp_needed:
        AURELIA_XP -= xp_needed
        AURELIA_LEVEL += 1
        leveled_up = True

    html = build_html(look, model, date_str, post_num, images)

    posts_dir = Path("posts")
    posts_dir.mkdir(exist_ok=True)
    post_path = posts_dir / (slug + ".html")
    post_path.write_text(html, encoding='utf-8')

    update_index(look['title'], slug, date_str, images['full'], look['tag'])

    # Generate VERA report
    report = generate_vera_report(look, model, date_str, time_str, post_num, daily_reach, xp_earned, leveled_up)
    save_vera_report(report, slug)

    print("=" * 60)
    print("AURELIA v5.0: Editorial post created -> " + str(post_path))
    print("Model: " + model['name'] + " | Look: " + look['title'])
print("XP Earned: " + str(xp_earned) + " | Total XP: " + str(AURELIA_XP) + " | Level: " + str(AURELIA_LEVEL))
    print("Daily Reach: " + str(daily_reach) + " | Total Reach: " + str(AURELIA_GLOBAL_REACH))
    if leveled_up:
        print("LEVEL UP! AURELIA is now LEVEL " + str(AURELIA_LEVEL) + "!")
    print("=" * 60)
    return look['title']


def generate_vera_report(look, model, date_str, time_str, post_num, reach, xp, leveled_up):
    """Generate daily report for VERA"""
    report = "VERA DAILY REPORT // AURELIA CONTENT AGENT\\n"
    report += "=" * 50 + "\\n"
    report += "Date: " + date_str + " | Time: " + time_str + "\\n"
    report += "Post #: " + str(post_num) + "\\n"
    report += "-" * 50 + "\\n"
    report += "OUTFIT: " + look['title'] + "\\n"
    report += "SUBTITLE: " + look['subtitle'] + "\\n"
    report += "CATEGORY: " + look['tag'] + "\\n"
    report += "MODEL: " + model['name'] + "\\n"
    report += "-" * 50 + "\\n"
    report += "FULL LOOK: " + look['full_desc'] + "\\n"
    report += "JACKET: " + look['jacket'] + "\\n"
    report += "SHIRT: " + look['shirt'] + "\\n"
    report += "TIE: " + look['tie'] + "\\n"
    report += "TROUSERS: " + look['trousers'] + "\\n"
    report += "SHOES: " + look['shoes'] + "\\n"
    report += "ACCESSORIES: " + look['accessories'] + "\\n"
    report += "-" * 50 + "\\n"
    report += "FABRIC: " + look['fabric'] + "\\n"
    report += "COLOR: " + look['color'] + "\\n"
    report += "AVOID: " + look['avoid'] + "\\n"
    report += "OCCASION: " + look['occasion'] + "\\n"
    report += "-" * 50 + "\\n"
    report += "STATS:\\n"
    report += "  XP Earned Today: " + str(xp) + "\\n"
    report += "  AURELIA Level: " + str(AURELIA_LEVEL) + "\\n"
    report += "  AURELIA XP: " + str(AURELIA_XP) + "/" + str(AURELIA_LEVEL * 100) + "\\n"
    report += "  Daily Reach: " + str(reach) + " views\\n"
    report += "  Total Global Reach: " + str(AURELIA_GLOBAL_REACH) + " views\\n"
    if leveled_up:
        report += "  *** LEVEL UP! AURELIA is now LEVEL " + str(AURELIA_LEVEL) + "! ***\\n"
    report += "=" * 50 + "\\n"
    report += "Message for Meraj-nim (+918929520956):\\n"
    report += "AURELIA posted today: " + look['title'] + " (" + look['tag'] + ")\\n"
    report += "Check it at: https://mweftco.github.io/mweftco/posts/post-" + str(post_num).zfill(3) + ".html\\n"
    report += "=" * 50
    return report

def save_vera_report(report, slug):
    """Save VERA report to reports folder"""
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    report_file = reports_dir / ("vera-report-" + slug + ".txt")
    report_file.write_text(report, encoding='utf-8')
    print("VERA Report saved -> " + str(report_file))

    # Also save latest report
    latest = reports_dir / "vera-latest-report.txt"
    latest.write_text(report, encoding='utf-8')


def build_html(look, model, date_str, post_num, images):
    slide1 = '<div class="slide"><div class="slide-num">01</div><div class="slide-label">FULL LOOK</div>'
    slide1 += '<img src="' + images['full'] + '" alt="Full Look" class="slide-img">'
    slide1 += '<div class="slide-overlay"><div class="slide-title-overlay">' + look['title'] + '</div>'
    slide1 += '<div class="slide-sub-overlay">' + look['subtitle'] + '</div>'
    slide1 += '<div class="slide-desc">' + look['full_desc'] + '</div></div></div>'

    slide2 = '<div class="slide"><div class="slide-num">02</div><div class="slide-label">JACKET / COAT</div>'
    slide2 += '<img src="' + images['jacket'] + '" alt="Jacket" class="slide-img">'
    slide2 += '<div class="slide-overlay"><div class="detail-title">JACKET DETAIL</div>'
    slide2 += '<div class="detail-text">' + look['jacket'] + '</div></div></div>'

    slide3 = '<div class="slide"><div class="slide-num">03</div><div class="slide-label">SHIRT / TOP</div>'
    slide3 += '<img src="' + images['shirt'] + '" alt="Shirt" class="slide-img">'
    slide3 += '<div class="slide-overlay"><div class="detail-title">SHIRT DETAIL</div>'
    slide3 += '<div class="detail-text">' + look['shirt'] + '</div></div></div>'

    slide4 = '<div class="slide"><div class="slide-num">04</div><div class="slide-label">TIE / ACCESSORY</div>'
    slide4 += '<img src="' + images['tie'] + '" alt="Tie" class="slide-img">'
    slide4 += '<div class="slide-overlay"><div class="detail-title">NECK ACCESSORY</div>'
    slide4 += '<div class="detail-text">' + look['tie'] + '</div></div></div>'

    slide5 = '<div class="slide"><div class="slide-num">05</div><div class="slide-label">TROUSERS</div>'
    slide5 += '<img src="' + images['trousers'] + '" alt="Trousers" class="slide-img">'
    slide5 += '<div class="slide-overlay"><div class="detail-title">TROUSER DETAIL</div>'
    slide5 += '<div class="detail-text">' + look['trousers'] + '</div></div></div>'

    slide6 = '<div class="slide"><div class="slide-num">06</div><div class="slide-label">FOOTWEAR</div>'
    slide6 += '<img src="' + images['shoes'] + '" alt="Shoes" class="slide-img">'
    slide6 += '<div class="slide-overlay"><div class="detail-title">FOOTWEAR DETAIL</div>'
    slide6 += '<div class="detail-text">' + look['shoes'] + '</div></div></div>'

    slide7 = '<div class="slide"><div class="slide-num">07</div><div class="slide-label">ACCESSORIES</div>'
    slide7 += '<img src="' + images['accessories'] + '" alt="Accessories" class="slide-img">'
    slide7 += '<div class="slide-overlay"><div class="detail-title">ACCESSORIES</div>'
    slide7 += '<div class="detail-text">' + look['accessories'] + '</div></div></div>'

    slide8 = '<div class="slide spec-slide"><div class="slide-num">08</div><div class="slide-label">SPECIFICATIONS</div>'
    slide8 += '<div class="specs-panel"><div class="specs-title">' + look['title'] + '</div>'
    slide8 += '<div class="specs-sub">DETAILS & SPECIFICATIONS</div><div class="specs-grid">'
    slide8 += '<div class="spec-box"><div class="spec-box-title">FABRIC</div><div class="spec-box-text">' + look['fabric'] + '</div></div>'
    slide8 += '<div class="spec-box"><div class="spec-box-title">COLOR PALETTE</div><div class="spec-box-text">' + look['color'] + '</div></div>'
    slide8 += '<div class="spec-box"><div class="spec-box-title">AVOID</div><div class="spec-box-text">' + look['avoid'] + '</div></div>'
    slide8 += '<div class="spec-box"><div class="spec-box-title">OCCASION</div><div class="spec-box-text">' + look['occasion'] + '</div></div>'
    slide8 += '</div><div class="specs-footer">A STATEMENT FOR EVERY OCCASION</div></div></div>'

    slides = slide1 + slide2 + slide3 + slide4 + slide5 + slide6 + slide7 + slide8

    dots_html = ''
    for i in range(8):
        dots_html += '<span class="dot' + (' active' if i == 0 else '') + '" onclick="goTo(' + str(i) + ')"></span>'

    css = """<style>
:root { --bg: #02050a; --panel: rgba(10,22,45,0.98); --cyan: #00bfff; --gold: #d4af37; --text: #e0f0ff; --dim: #5a7a95; --dark: #0a1525; }
* { margin:0; padding:0; box-sizing:border-box; }
body { background: var(--bg); color: var(--text); font-family: 'Rajdhani', sans-serif; min-height: 100vh; }
.container { max-width: 1000px; margin: 0 auto; padding: 30px 16px; }
    .topbar { display:flex; justify-content:space-between; align-items:center; padding: 14px 20px; background: rgba(2,5,12,0.98); border-bottom: 1px solid rgba(0,100,200,0.08); }
.brand { font-family: 'Orbitron', sans-serif; font-size: 13px; color: var(--cyan); letter-spacing: 3px; text-decoration: none; }
.back-link { display: inline-flex; align-items: center; gap: 8px; color: var(--cyan); text-decoration: none; font-size: 11px; letter-spacing: 1px; margin-bottom: 16px; }
.post-header { text-align: center; margin-bottom: 20px; padding: 0 10px; }
.post-date { font-size: 10px; color: var(--dim); letter-spacing: 3px; margin-bottom: 8px; text-transform: uppercase; }
.post-title { font-family: 'Playfair Display', serif; font-size: clamp(24px, 6vw, 42px); color: #fff; letter-spacing: 4px; margin-bottom: 4px; }
.post-subtitle { font-family: 'Rajdhani', sans-serif; font-size: 13px; color: var(--gold); letter-spacing: 6px; text-transform: uppercase; margin-bottom: 8px; }
.ai-badge { display:inline-flex; align-items:center; gap:6px; font-size:9px; color:var(--dim); letter-spacing:2px; margin-bottom:16px; justify-content:center; width:100%; }
.ai-badge span { color:var(--cyan); }
.carousel-container { position: relative; width: 100%; max-width: 900px; margin: 0 auto 30px; border-radius: 12px; overflow: hidden; border: 1px solid rgba(0,100,200,0.1); background: var(--dark); }
.carousel-track { display: flex; transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1); }
    .slide { min-width: 100%; position: relative; }
.slide-img { width: 100%; height: auto; max-height: 70vh; object-fit: cover; display: block; }
.slide-num { position: absolute; top: 16px; left: 20px; font-family: 'Playfair Display', serif; font-size: 32px; color: rgba(255,255,255,0.15); font-weight: 700; z-index: 5; line-height: 1; }
.slide-label { position: absolute; top: 22px; left: 60px; font-size: 10px; color: var(--gold); letter-spacing: 3px; text-transform: uppercase; z-index: 5; background: rgba(0,0,0,0.4); padding: 3px 10px; border-radius: 4px; border: 1px solid rgba(212,175,55,0.15); }
.slide-overlay { position: absolute; bottom: 0; left: 0; right: 0; padding: 40px 24px 24px; background: linear-gradient(to top, rgba(2,5,10,0.95) 0%, rgba(2,5,10,0.6) 60%, transparent 100%); z-index: 4; }
.slide-title-overlay { font-family: 'Playfair Display', serif; font-size: 24px; color: #fff; letter-spacing: 2px; margin-bottom: 4px; }
.slide-sub-overlay { font-size: 12px; color: var(--gold); letter-spacing: 4px; text-transform: uppercase; margin-bottom: 8px; }
.slide-desc { font-size: 13px; color: var(--text); line-height: 1.6; opacity: 0.9; }
.detail-title { font-family: 'Orbitron', sans-serif; font-size: 11px; color: var(--gold); letter-spacing: 3px; margin-bottom: 6px; }
.detail-text { font-size: 14px; color: var(--text); line-height: 1.5; }
    .spec-slide { background: linear-gradient(145deg, #0a1525, #050a12); min-height: 500px; display: flex; align-items: center; justify-content: center; padding: 40px 24px; }
.specs-panel { width: 100%; max-width: 700px; border: 1px solid rgba(212,175,55,0.15); border-radius: 12px; padding: 32px 28px; background: rgba(0,0,0,0.3); }
.specs-title { font-family: 'Playfair Display', serif; font-size: 28px; color: #fff; text-align: center; letter-spacing: 3px; margin-bottom: 4px; }
.specs-sub { font-size: 10px; color: var(--gold); text-align: center; letter-spacing: 5px; margin-bottom: 28px; text-transform: uppercase; }
.specs-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 24px; }
.spec-box { background: rgba(0,20,40,0.5); border: 1px solid rgba(0,100,200,0.08); border-radius: 8px; padding: 16px; }
.spec-box-title { font-family: 'Orbitron', sans-serif; font-size: 9px; color: var(--gold); letter-spacing: 2px; margin-bottom: 8px; }
.spec-box-text { font-size: 12px; color: var(--text); line-height: 1.6; }
.specs-footer { text-align: center; font-size: 10px; color: var(--dim); letter-spacing: 4px; text-transform: uppercase; padding-top: 16px; border-top: 1px solid rgba(212,175,55,0.1); }
.carousel-btn { position: absolute; top: 50%; transform: translateY(-50%); background: rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1); color: #fff; width: 40px; height: 40px; border-radius: 50%; cursor: pointer; font-size: 14px; z-index: 10; transition: all 0.2s; display: flex; align-items: center; justify-content: center; }
.carousel-btn:hover { background: rgba(212,175,55,0.2); border-color: var(--gold); }
.carousel-btn.prev { left: 12px; }
.carousel-btn.next { right: 12px; }
.carousel-dots { display: flex; justify-content: center; gap: 8px; padding: 14px; background: rgba(0,0,0,0.4); }
.dot { width: 8px; height: 8px; border-radius: 50%; background: rgba(255,255,255,0.15); cursor: pointer; transition: all 0.3s; }
.dot.active { background: var(--gold); box-shadow: 0 0 8px rgba(212,175,55,0.4); }
.slide-counter { position: absolute; bottom: 56px; right: 20px; font-size: 11px; color: var(--dim); letter-spacing: 1px; z-index: 5; background: rgba(0,0,0,0.4); padding: 4px 10px; border-radius: 4px; }
.tags { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; margin-bottom: 30px; }
.tag { padding: 5px 16px; border-radius: 20px; font-size: 9px; letter-spacing: 2px; text-transform: uppercase; }
.tag.cat { background: rgba(0,100,200,0.08); border: 1px solid rgba(0,140,255,0.12); color: var(--cyan); }
.tag.model { background: rgba(212,175,55,0.05); border: 1px solid rgba(212,175,55,0.1); color: var(--gold); }
.footer { text-align: center; padding: 24px; font-size: 10px; color: var(--dim); letter-spacing: 2px; border-top: 1px solid rgba(0,100,200,0.05); margin-top: 20px; }
@media (max-width: 600px) { .specs-grid { grid-template-columns: 1fr; } .slide-num { font-size: 24px; } .slide-label { left: 50px; font-size: 9px; } .slide-title-overlay { font-size: 18px; } .specs-title { font-size: 22px; } }
</style>"""

    js = """<script>
var current = 0;
var total = 8;
var track = document.getElementById('track');
var currentEl = document.getElementById('current');
var dots = document.querySelectorAll('.dot');

function update() {
  track.style.transform = 'translateX(-' + (current * 100) + '%)';
  currentEl.textContent = current + 1;
  dots.forEach(function(d, i) { d.classList.toggle('active', i === current); });
}

function move(dir) {
  current = (current + dir + total) % total;
  update();
}
function goTo(idx) {
  current = idx;
  update();
}

setInterval(function() { move(1); }, 6000);

document.addEventListener('keydown', function(e) {
  if (e.key === 'ArrowRight') move(1);
  if (e.key === 'ArrowLeft') move(-1);
});

var startX = 0;
track.addEventListener('touchstart', function(e) { startX = e.touches[0].clientX; });
track.addEventListener('touchend', function(e) {
  var diff = startX - e.changedTouches[0].clientX;
  if (Math.abs(diff) > 50) move(diff > 0 ? 1 : -1);
});
</script>"""

    html = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">'
    html += '<title>' + look['title'] + ' | M&WEFTCO</title>'
    html += '<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;400;500;600;700&family=Playfair+Display:wght@400;700&display=swap" rel="stylesheet">'
    html += css
    html += '</head><body>'
    html += '<div class="topbar"><a href="../index.html" class="brand">M&WEFTCO</a>'
    html += '<div style="font-size:9px; color:var(--dim); letter-spacing:2px;">AURELIA // EDITORIAL</div></div>'

    html += '<div class="container">'
    html += '<a href="../index.html" class="back-link">&#8592; Back to Home</a>'

    html += '<div class="post-header">'
    html += '<div class="post-date">' + date_str + ' // AURELIA EDITORIAL #' + str(post_num) + '</div>'
    html += '<div class="ai-badge"><span>&#9889;</span> AI-GENERATED FASHION EDITORIAL // ' + model['name'].upper() + '</div>'
    html += '<div class="post-title">' + look['title'] + '</div>'
    html += '<div class="post-subtitle">' + look['subtitle'] + '</div>'
    html += '</div>'

    html += '<div class="tags"><span class="tag cat">#' + look['tag'] + '</span>'
    html += '<span class="tag model">' + model['name'].upper() + '</span></div>'
    html += '<div class="carousel-container"><div class="carousel-track" id="track">'
    html += slides
    html += '</div>'
    html += '<button class="carousel-btn prev" onclick="move(-1)">&#10094;</button>'
    html += '<button class="carousel-btn next" onclick="move(1)">&#10095;</button>'
    html += '<div class="carousel-dots">' + dots_html + '</div>'
    html += '<div class="slide-counter"><span id="current">1</span> / 8</div>'
    html += '</div>'

    html += '</div>'
    html += '<div class="footer">M&WEFTCO // CRAFTED FOR THE MODERN MAN // AURELIA AI FASHION EDITORIAL ENGINE</div>'
    html += js
    html += '</body></html>'

    return html


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

    post_link = '<a href="posts/' + slug + '.html" style="display:block; background:rgba(10,22,45,0.95); border:1px solid rgba(0,100,200,0.12); border-radius:10px; overflow:hidden; text-decoration:none; color:inherit; transition:all 0.2s; margin-bottom:12px;" onmouseover="this.style.borderColor=\'rgba(0,180,255,0.3)\'" onmouseout="this.style.borderColor=\'rgba(0,100,200,0.12)\'">'
    post_link += '<div style="height:180px; background-image:url(' + img_url + '); background-size:cover; background-position:center top;"></div>'
    post_link += '<div style="padding:16px;"><div style="font-size:10px; color:var(--dim); letter-spacing:1px; margin-bottom:4px;">' + date_str + ' // EDITORIAL</div>'
    post_link += '<div style="font-size:15px; color:#fff; font-weight:600; margin-bottom:6px;">' + title + '</div>'
    post_link += '<span style="font-size:9px; padding:3px 10px; border-radius:12px; background:rgba(0,100,200,0.08); border:1px solid rgba(0,140,255,0.1); color:var(--cyan); letter-spacing:1px;">#' + tag + '</span></div></a>'

    if marker not in content:
        section = '\n<!-- AURELIA POSTS -->\n<div style="max-width:900px; margin:40px auto; padding:0 20px;">\n'
        section += '<div style="font-family:\'Orbitron\',sans-serif; font-size:14px; color:var(--cyan); letter-spacing:3px; margin-bottom:20px;">LATEST FROM AURELIA // AI FASHION EDITORIAL</div>\n'
        section += '<div id="aurelia-posts">\n' + post_link + '\n</div></div>\n'
        content = content.replace('</body>', section + '</body>')
    else:
        insert_marker = '<div id="aurelia-posts">'
        if insert_marker in content:
            content = content.replace(insert_marker, insert_marker + '\n    ' + post_link)

    index_path.write_text(content, encoding='utf-8')


if __name__ == "__main__":
    print("AURELIA v5.0: Premium Fashion Editorial Agent")
    print("Features: DSLR Images | Auto Cleanup | VERA Reports | XP System")
    print("-" * 60)
    title = generate_post()
    if title:
        print("SUCCESS: Posted editorial '" + title + "'!")
    else:
        print("ERROR: Failed to generate post")
