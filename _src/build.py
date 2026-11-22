#!/usr/bin/env python3
"""Builds the UTS Service site: plain static pages, one folder per URL.
Run from the repo root:  python3 _src/build.py
Two switches matter at launch:
  BASE      the address the site lives at (change to https://utsservice.ca when it moves there)
  INDEXABLE False while this is a preview, True the day it becomes the real site
"""
import os, json, html, datetime, shutil

BASE = 'https://www.utsservice.ca'
INDEXABLE = True
TODAY = datetime.date.today().isoformat()
JOBBER = 'https://clienthub.getjobber.com/client_hubs/6c2a5043-8d20-4ca8-a7c5-82753914a5b7/public/work_request/new?source=social_media'  # no longer linked
# Web3Forms access key: get one at web3forms.com for the inbox that should receive requests
W3F_KEY = 'f8b0cff3-5d5b-40ea-9d48-481d79aeeeb8'
PHONE, PHONE_TEL, PHONE2, PHONE2_TEL = '647-777-7411', '+16477777411', '647-676-4408', '+16476764408'
EMAIL = 'Admin@utsservice.ca'
MAPS = 'https://maps.app.goo.gl/TbrvcE7bR3gVnLHUA'
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
rd = lambda n: open(os.path.join(SRC, n), encoding='utf-8').read()
e = html.escape
KICK = '<svg viewBox="0 0 34 20" aria-hidden="true"><path d="M1 19V1h14v18M19 19V1h14v18"/></svg>'

REGIONS = [
 ('toronto', 'Toronto', ['Toronto', 'North York', 'Scarborough', 'Etobicoke'],
  'Toronto is home base. Our shop is at 50 Alness St in North York, so buildings across the city are close by.'),
 ('peel', 'Peel Region', ['Brampton', 'Mississauga', 'Caledon'],
  'We work across Peel Region, from Mississauga and Brampton up to Caledon.'),
 ('york', 'York Region', ['Vaughan', 'Markham', 'Richmond Hill', 'Aurora', 'Newmarket', 'East Gwillimbury', 'Georgina', 'King', 'Whitchurch-Stouffville'],
  'York Region starts just north of our shop. We cover all nine of its municipalities, from Vaughan and Markham up to Georgina.'),
 ('durham', 'Durham Region', ['Pickering', 'Ajax', 'Whitby', 'Oshawa', 'Clarington', 'Uxbridge', 'Scugog', 'Brock'],
  'East of Toronto, we cover all eight Durham municipalities, from Pickering and Ajax through Oshawa to Clarington and north to Brock.'),
 ('halton', 'Halton Region', ['Burlington', 'Oakville', 'Milton', 'Halton Hills'],
  'West of the city, we cover Oakville, Burlington, Milton and Halton Hills.'),
 ('southern-ontario', 'Beyond the GTA', ['Hamilton', 'Barrie', 'Guelph', 'Cambridge', 'Kitchener', 'Waterloo', 'St. Catharines', 'Niagara Falls', 'Brantford'],
  'For building owners and brands with sites outside the GTA, we travel to Hamilton, Niagara, Kitchener-Waterloo, Guelph, Brantford and Barrie.'),
]
ALL_CITIES = [c for r in REGIONS for c in r[2]]

SERVICES = [
 dict(slug='locksmith', name='Locksmith', img='svc-locksmith', alt='Brushed steel lock and lever on a dark commercial door',
  title='Commercial Locksmith in Toronto and the GTA | UTS Service',
  desc='Rekeys, master key systems, high-security locks and lockouts for apartment buildings and businesses across the GTA. One team for every door.',
  h1='Commercial locksmith for buildings and businesses',
  lede='Rekeys, master key systems and high-security locks, fixed right the first time.',
  answer='UTS Service is a commercial locksmith based in North York. We rekey and replace locks, build master key systems, install high-security cylinders and handle lockouts for apartment buildings, condos, stores, offices and public buildings across the GTA.',
  do=[('Rekeying', 'New pins, new keys. The old keys stop working and the hardware stays.'),
      ('Master key systems', 'One key for the manager, separate keys for each unit or department.'),
      ('High-security locks', "Cylinders that resist picking and drilling, with keys that can't be copied at a kiosk."),
      ('Lock replacement', 'Worn or damaged locks swapped for commercial-grade hardware.'),
      ('Lockouts', 'Locked out of a unit, office or storefront? We get you back in.'),
      ('Key replacement', 'Lost keys replaced. When it makes sense, the lock is rekeyed so the lost key is useless.')],
  signs=['A tenant or employee left and never returned their keys', "You don't know how many copies of a key exist", 'A lock sticks, spins or has to be jiggled', 'You manage several buildings with a different key for each', 'There was a break-in or an attempted one'],
  faqs=[('What is a master key system?', 'A master key system lets one key open many locks while every other key opens only its own door. A property manager or superintendent carries the master. Tenants, staff or departments each get a key that works on their door and nothing else.'),
        ('Should I rekey a lock or replace it?', 'Rekey when the lock works fine but you no longer trust who has keys. The pins are changed so old keys stop working, and it costs less than new hardware. Replace the lock when it is worn, damaged, or you want a higher security grade.'),
        ('What makes a lock high-security?', "A high-security cylinder is built to resist picking, drilling and forced entry. Most also use restricted keys, which can only be copied with the owner's authorization, so you know how many keys exist."),
        ('Can you rekey a whole building?', 'Yes. We rekey single units at move-out and entire buildings after a change of management, a lost master key or a break-in.')]),
 dict(slug='access-control', name='Access control', img='svc-access', alt='Wall-mounted access reader glowing blue in a lobby',
  title='Access Control Systems in Toronto and the GTA | UTS Service',
  desc='Fob, card, keypad and biometric access control for apartment buildings and businesses. Installed, managed and taken over by one team.',
  h1='Access control that tells you who gets in',
  lede='Fobs, cards, keypads and biometric readers, set up so you run every door from one place.',
  answer='Access control replaces keys with credentials you can switch on and off: fobs, cards, PIN codes or fingerprints. UTS Service designs, installs and manages these systems for apartment buildings and businesses across the GTA, and takes over systems another company installed.',
  do=[('Fob and card systems', 'The standard for apartment buildings and offices. Tap to enter.'),
      ('Keypads and PIN entry', 'Codes for staff doors, storerooms and shared spaces.'),
      ('Biometric readers', 'Fingerprint entry for rooms where a shared code is not enough.'),
      ('Fob management', 'We add, cancel and audit credentials for you, the same day.'),
      ('System takeovers', 'Inherited a system nobody understands? We sort out what you have and run it.'),
      ('Entry records', 'See which credential opened which door, and when.')],
  signs=['Lost fobs that were never cancelled', 'Former tenants or staff who can still get in', 'No record of who entered or when', 'Rekeying locks after every move-out', 'Readers that fail, or only work some of the time'],
  faqs=[('What happens when a fob is lost?', 'The lost fob is cancelled in the system and stops working right away. Nobody needs to rekey a lock or hand out new keys. A replacement fob is issued to the person who lost it.'),
        ('Fob, keypad or biometric: which is right for my building?', 'Fobs and cards suit most apartment buildings and offices because each one belongs to a person and can be cancelled alone. Keypads suit low-risk shared doors. Biometric readers suit rooms where you need to be sure of the person, not just the credential.'),
        ('Does access control keep a record of who came in?', 'Yes. Most systems log each entry with the credential used, the door and the time. That record helps after an incident and shows which fobs are still in use.'),
        ('Can you take over our existing fob system?', "Usually, yes. We'll look at what you have, tell you if it can be managed or should be replaced, and give you the price before any work starts."),
        ('What happens to the doors if the power goes out?', 'It depends on how each door is set up. Some locks release when power is lost so people can always get out, and others stay locked from the outside. Battery backup keeps readers working through short outages. We set this up door by door.')]),
 dict(slug='door-repair', name='Door repair', img='svc-repair', alt='Steel door closer and hinge on a glass entrance door',
  title='Commercial Door Repair in Toronto and the GTA | UTS Service',
  desc='Door closers, hinges, strikes, frames and panic bars repaired on commercial, storefront and apartment building doors across the GTA.',
  h1='Commercial door repair that fixes the cause',
  lede='Closers, hinges, strikes and frames that stop sticking, slamming and failing.',
  answer='Most door problems come from four parts: the closer, the hinges, the strike and the frame. UTS Service repairs and replaces all of them on commercial, storefront and apartment building doors across the GTA, so the door closes, latches and locks every time.',
  do=[('Door closers', 'Adjusted or replaced so the door shuts firmly without slamming.'),
      ('Hinges and pivots', 'Sagging doors rehung on hardware rated for the traffic.'),
      ('Strikes and latches', 'Realigned so the door latches without a pull.'),
      ('Frames and alignment', 'Bent or shifted frames corrected so the door sits square.'),
      ('Panic bars and exit hardware', 'Exit devices repaired so people can always get out.'),
      ('Door replacement', 'When a door is past repair, we replace it and its hardware.')],
  signs=["The door slams or won't close without help", "It doesn't latch unless you pull it", 'It drags on the floor or rubs the frame', 'The lock no longer lines up', 'You can see daylight around a closed door'],
  faqs=[("Why won't my door latch?", 'A door that will not latch usually has a closer that needs adjusting, hinges that have sagged, or a strike plate that no longer lines up with the latch. All three can be fixed without replacing the door.'),
        ('Should a commercial door be repaired or replaced?', 'Repair it when the door itself is sound and the problem is hardware: closer, hinges, strike or lock. Replace it when the door or frame is bent, rusted through or cracked, because new hardware on a damaged door will fail again.'),
        ('What does a door closer do?', 'A door closer is the arm at the top of the door that pulls it shut at a controlled speed. Set properly, it closes and latches the door without slamming. A leaking or worn closer is the most common reason a door slams or stays open.'),
        ('Why does it matter if a fire door latches?', 'A fire-rated door only does its job when it closes and latches by itself. If it is propped open, or the closer or latch has failed, it should be repaired promptly.')]),
 dict(slug='automatic-doors', name='Automatic doors', img='svc-auto', alt='Automatic glass sliding doors opening onto a lit lobby',
  title='Automatic Door Installation and Repair, GTA | UTS Service',
  desc='Sliding and swing automatic doors and push-button openers installed, repaired and maintained for commercial and apartment buildings across the GTA.',
  h1='Automatic doors, installed and kept working',
  lede='Sliding and swing operators, push-button openers and accessible entrances.',
  answer='UTS Service installs, repairs and maintains automatic doors for commercial properties and apartment buildings across the GTA. That covers sliding doors, swing door operators and push-button openers that make an entrance easier for everyone to use.',
  do=[('Sliding automatic doors', 'For lobbies and storefronts with steady foot traffic.'),
      ('Swing door operators', 'A motor added to a regular door so it opens by itself.'),
      ('Push-button openers', 'The accessible entrance button, installed and wired.'),
      ('Sensors and safety checks', 'Sensors tested so doors open for people and never close on them.'),
      ('Repairs', "Doors that stick, shudder or stop are diagnosed and fixed."),
      ('Scheduled maintenance', 'Regular visits that catch wear before the door fails.')],
  signs=['Doors that open slowly, partly or not at all', "Doors that don't sense people", 'Doors that close too fast', "An entrance that isn't accessible", 'A door that is noisy or shudders'],
  faqs=[('Can an existing door be made automatic?', 'Often, yes. A swing door operator can be fitted to many existing doors, with a push button or sensor to trigger it. We check the door, frame and power supply first to confirm it will work.'),
        ('Sliding or swing: which automatic door do I need?', 'Sliding doors suit wide entrances with constant traffic, like lobbies and storefronts. Swing operators suit a single existing door, and cost less because the door and frame stay.'),
        ('Do automatic doors need regular service?', 'Yes. Sensors, motors and safety features wear with use. Regular checks keep the door safe and catch problems before the entrance goes out of service.'),
        ('Do push-button openers help with accessibility?', 'Yes. A power operator with a push button is a common way to make an entrance barrier-free, which many Ontario buildings are required to provide. We install hardware that meets the code requirements for your building.')]),
]

INDUSTRIES = [
 dict(slug='apartments-condos', name='Apartments and condos', title='Locks, Fobs and Doors for Apartments and Condos | UTS Service',
  desc='Fob systems, lobby doors, unit rekeys and master keys for apartment and condo buildings across the GTA. One team for property managers and condo boards.',
  h1='Locks, fobs and doors for apartments and condos',
  lede='Fobs, intercoms, lobby doors and move-out rekeys, handled for your whole portfolio.',
  answer='UTS Service looks after the entrances of apartment and condo buildings across the GTA: fob and intercom systems, lobby and automatic doors, garage entrances, unit rekeys at move-out, and master key systems for property managers and condo boards.',
  items=[('Lost fobs and move-outs', 'A lost fob is cancelled in the system. A unit is rekeyed between tenants.'),
         ('Lobby and entrance doors', 'Closers, operators and locks kept working so the front door actually secures the building.'),
         ('Garage and common areas', 'Access readers on garages, lockers, gyms and party rooms.'),
         ('Master keys', 'The superintendent carries one key. Residents get keys that open only their own unit.')],
  faqs=[('Do you work with condo boards and superintendents?', 'Yes. We work with property managers, condo boards and on-site superintendents, and keep one record of the locks, keys and fobs for each building.'),
        ('Can you rekey a unit between tenants?', 'Yes. Rekeying at move-out means the last tenant’s keys no longer work, and it costs less than replacing the lock.'),
        ('What happens when a resident loses a fob?', 'The lost fob is cancelled in the system right away and a new one is issued. Nothing else in the building has to change.')],
  svc=['access-control', 'locksmith', 'automatic-doors', 'door-repair']),
 dict(slug='retail-franchise', name='Retail and franchise', title='Storefront Locks and Doors for Retail Chains | UTS Service',
  desc='Storefront locks, panic bars, door repair and key control for stores and franchise locations across the GTA. The same standard at every site.',
  h1='Storefront locks and doors for retail and franchises',
  lede='Same standard at every location. Storefront locks, panic bars and doors that open on time.',
  answer='UTS Service keeps storefront doors and locks working for retailers and franchise operators across the GTA. We repair and replace storefront locks, closers and panic bars, rekey after staff changes, and apply the same hardware standard at every location.',
  items=[('Storefront doors and locks', 'Glass and aluminum storefront doors that close, latch and lock at the end of the night.'),
         ('Panic bars and exit hardware', 'Exit devices that let people out and keep the door secure from outside.'),
         ('Staff turnover', 'Rekeys and restricted keys so a former employee’s key stops working.'),
         ('Every location, one vendor', 'One account and one standard across all your stores.')],
  note="Retail and franchise names we've worked for include Tim Hortons, Domino's Pizza, Pizza Pizza, Louis Vuitton, CF Toronto Eaton Centre and SmartCentres.",
  faqs=[('Can you look after all of our locations?', 'Yes. One account covers every store, with the same team and the same hardware standard at each site.'),
        ('A manager left with keys. What should we do?', 'Rekey the locks they had keys for. It is quick, costs less than new locks, and with restricted keys you control who can make copies from then on.')],
  svc=['door-repair', 'locksmith', 'automatic-doors', 'access-control']),
 dict(slug='offices', name='Offices and corporate', title='Access Control and Locks for Offices | UTS Service',
  desc='Card and fob access by floor, master key systems and entry records for offices and corporate sites across the GTA.',
  h1='Access control and locks for offices',
  lede='Card and fob access by floor, master key systems, and a record of who came in.',
  answer='UTS Service sets up and manages access for offices across the GTA: card and fob entry by floor or department, master key systems for the rooms that still use keys, and entry records that show who came in and when.',
  items=[('Access by floor or department', 'Each person gets into the areas they need and nothing more.'),
         ('Staff changes', 'A card is switched off the day someone leaves. No locks to change.'),
         ('Master key systems', 'For server rooms, storage and offices that still use keys.'),
         ('Entry records', 'A log of which credential opened which door, and when.')],
  note="Corporate names we've worked for include RBC, Amazon, WeWork, Mercedes-Benz and UPS.",
  faqs=[('Can access be limited by floor or department?', 'Yes. Each card or fob is set to open only the doors that person needs, and that can be changed at any time without touching the hardware.'),
        ('What happens when an employee leaves?', 'Their card or fob is switched off in the system. If they also held keys, the affected locks are rekeyed.')],
  svc=['access-control', 'locksmith', 'door-repair', 'automatic-doors']),
 dict(slug='public-sector', name='Public sector', title='Door Hardware and Access for Public Buildings | UTS Service',
  desc='Code-compliant locks, accessible entrances and door repair for municipal, institutional and non-profit buildings across the GTA.',
  h1='Door hardware for public buildings',
  lede='Code-compliant hardware and crews who know how to work in public buildings.',
  answer='UTS Service installs and maintains locks, access control and automatic doors in public buildings across the GTA. We use code-compliant hardware, keep entrances accessible, and work around the people who use the building every day.',
  items=[('Code-compliant hardware', 'Locks and exit devices that meet the requirements for your building.'),
         ('Accessible entrances', 'Power operators and push buttons that make an entrance barrier-free.'),
         ('High-traffic doors', 'Hardware chosen for doors that open thousands of times a week.'),
         ('Occupied buildings', 'Work planned so the building stays open and secure while we are on site.')],
  note="Public and non-profit names we've worked for include the City of Toronto, the Ontario Provincial Police, Canada Post and Fred Victor.",
  faqs=[('Is your work code compliant?', "Yes. We install hardware that meets fire code and accessibility requirements, and we'll tell you if something you have doesn't."),
        ('Can you work while the building is open?', 'Yes. We plan the work so entrances stay usable and secure while the building is occupied.')],
  svc=['automatic-doors', 'door-repair', 'access-control', 'locksmith']),
]

GENERAL_FAQS = [
 ('What does UTS Service do?', 'UTS Service is a commercial security company in North York, Ontario. We do locksmith work, access control, door repair and automatic doors for apartment buildings and businesses across the GTA.'),
 ('Do you work with property management companies?', 'Yes. Most of our work is for managers with more than one building. One account, one team, every site.'),
 ('How fast can you get here?', "Building emergencies get priority. Call and we'll give you a real arrival time on the phone."),
 ('Do you quote before starting?', "Always. You'll know the price before we touch a door."),
 ('Is the work code compliant?', "Yes. We install hardware that meets fire code and accessibility requirements, and we'll tell you if something you have doesn't."),
 ('Which areas do you cover?', 'Toronto, Peel, York, Durham and Halton regions, plus Hamilton, Niagara, Kitchener-Waterloo, Guelph, Brantford and Barrie.'),
 ('How do I request service?', 'Use the online request form, email ' + EMAIL + ', or call ' + PHONE + '.'),
]
HOME_FAQS = [GENERAL_FAQS[1], SERVICES[1]['faqs'][3], GENERAL_FAQS[2], GENERAL_FAQS[4], GENERAL_FAQS[3]]

NAV = [('Services', 'services/'), ('Buildings', 'building-program/'), ('Industries', 'industries/'), ('Areas', 'service-areas/'), ('About', 'about/'), ('FAQ', 'faq/')]

BUSINESS = {"@type": "Locksmith", "@id": BASE + "/#business", "name": "UTS Service", "url": BASE + "/", "telephone": "+1-647-777-7411", "email": EMAIL,
 "image": BASE + "/assets/hero-ending.jpg", "logo": BASE + "/assets/apple-touch-icon.png",
 "description": "Commercial locksmith, access control, door repair and automatic doors for apartment buildings and businesses across the GTA.",
 "address": {"@type": "PostalAddress", "streetAddress": "50 Alness St, Unit 1", "addressLocality": "North York", "addressRegion": "ON", "postalCode": "M3J 2G9", "addressCountry": "CA"},
 "hasMap": MAPS, "areaServed": ALL_CITIES,
 "knowsAbout": ["Commercial locksmith", "Access control systems", "Door repair", "Automatic doors", "Master key systems"]}

pages = []  # (path, lastmod)

def faq_ld(qas):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qas]}

def crumbs_ld(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + '/' + p} for i, (n, p) in enumerate(trail)]}

def shell(path, title, desc, body, ld, extra_head='', scripts=('assets/site.js',), home=False, og='assets/hero-ending.jpg'):
    depth = path.count('/'); rel = '../' * depth
    req = '#request' if path in ('', 'contact/') else rel + 'contact/#request'
    url = BASE + '/' + path
    graph = {"@context": "https://schema.org", "@graph": ld}
    nav = ''.join('<li><a href="%s%s"%s>%s</a></li>' % (rel, p, ' aria-current="page"' if path.startswith(p) else '', n) for n, p in NAV)
    mnav = ''.join('<a href="%s%s">%s</a>' % (rel, p, n) for n, p in NAV) + '<a href="%scontact/">Contact</a>' % rel
    svc_links = ''.join('<li><a href="%sservices/%s/">%s</a></li>' % (rel, s['slug'], s['name']) for s in SERVICES)
    ind_links = '<li><a href="%sbuilding-program/">Building Program</a></li>' % rel + ''.join('<li><a href="%sindustries/%s/">%s</a></li>' % (rel, s['slug'], s['name']) for s in INDUSTRIES)
    area_links = ''.join('<li><a href="%sservice-areas/%s/">%s</a></li>' % (rel, r[0], r[1]) for r in REGIONS)
    out = f'''<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{'index, follow, max-image-preview:large' if INDEXABLE else 'noindex, nofollow'}">
<meta name="theme-color" content="#0F1626">
<link rel="canonical" href="{url}">
<meta property="og:site_name" content="UTS Service">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_CA">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/{og}">
<meta name="twitter:card" content="summary_large_image">
<link rel="apple-touch-icon" href="{rel}assets/apple-touch-icon.png">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%230F1626'/%3E%3Crect x='14' y='12' width='16' height='40' rx='2' fill='none' stroke='%23EEF2F9' stroke-width='3'/%3E%3Crect x='34' y='12' width='16' height='40' rx='2' fill='none' stroke='%23EEF2F9' stroke-width='3'/%3E%3Ccircle cx='46' cy='32' r='3' fill='%234FA6FF'/%3E%3C/svg%3E">
{extra_head}
<script type="application/ld+json">{json.dumps(graph, separators=(',', ':'), ensure_ascii=False)}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@125,300;125,600&family=Hanken+Grotesk:wght@400;500&family=IBM+Plex+Mono:wght@400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{rel}assets/site.css">
</head>
<body{'' if home else ' class="inner"'}>
<a class="skip" href="#main">Skip to content</a>
<div class="env" aria-hidden="true"></div>
<nav class="nav{'' if home else ' solid'}" aria-label="Main">
  <div class="wrap">
    <a class="logo" href="{rel or './'}" aria-label="UTS Service home"><img src="{rel}assets/uts-logo.png" alt="UTS Service" width="444" height="160"></a>
    <ul>{nav}</ul>
    <div class="nav-r">
    <a class="btn btn-primary btn-sm cta-top" href="{req}">Request service</a>
    <a class="btn btn-glass btn-sm call" href="tel:{PHONE_TEL}">Call</a>
    <button class="menu-btn" id="menu-btn" type="button" aria-label="Menu" aria-expanded="false" aria-controls="mnav"><span></span></button>
    </div>
  </div>
</nav>
<div class="mnav" id="mnav">{mnav}</div>
{body}
<footer>
  <div class="wrap fwrap">
    <div class="fbrand">
      <img src="{rel}assets/uts-logo.png" alt="UTS Service" width="444" height="160" loading="lazy">
      <p>Locksmith, access control, door repair and automatic doors across Ontario.</p>
      <ul>
        <li><a href="tel:{PHONE_TEL}">{PHONE}</a></li>
        <li><a href="tel:{PHONE2_TEL}">{PHONE2}</a></li>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><a href="{MAPS}" target="_blank" rel="noopener">50 Alness St, Unit 1, North York, ON M3J 2G9</a></li>
      </ul>
    </div>
    <div><h4>Services</h4><ul>{svc_links}<li><a href="{rel}emergency-service/">Emergency service</a></li></ul></div>
    <div><h4>Who we serve</h4><ul>{ind_links}</ul></div>
    <div><h4>Service areas</h4><ul>{area_links}</ul></div>
    <div><h4>Company</h4><ul><li><a href="{rel}about/">About</a></li><li><a href="{rel}faq/">FAQ</a></li><li><a href="{rel}contact/">Contact</a></li><li><a href="{rel}contact/#request">Request service</a></li></ul></div>
    <p class="legal">© 2026 UTS Service. All rights reserved.</p>
  </div>
</footer>
<div class="sticky-call">
  <a class="btn btn-primary" href="tel:{PHONE_TEL}">Call now</a>
  <a class="btn btn-glass" href="{req}">Request service</a>
</div>
{''.join('<script src="%s%s" defer></script>' % (rel, s) for s in scripts)}
</body>
</html>
'''
    full = os.path.join(ROOT, path, 'index.html') if path != '404' else os.path.join(ROOT, '404.html')
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8').write(out)
    if path != '404': pages.append(path)

# ---------- inner page blocks ----------
def hero(rel, trail, kicker, h1, lede, img='hero-poster.jpg'):
    cr = ' <span aria-hidden="true">/</span> '.join(('<a href="%s%s">%s</a>' % (rel, p, e(n))) if i < len(trail) - 1 else '<span aria-current="page">%s</span>' % e(n) for i, (n, p) in enumerate(trail))
    return f'''<header class="phero" style="--bg:url({rel}assets/{img})">
  <div class="wrap">
    <nav class="crumbs mono" aria-label="Breadcrumb">{cr}</nav>
    <p class="kick mono in">{KICK}{e(kicker)}</p>
    <h1>{e(h1)}</h1>
    <p class="lede">{e(lede)}</p>
    <div class="row"><a class="btn btn-primary" href="{rel}contact/#request">Request service</a><a class="btn btn-glass" href="tel:{PHONE_TEL}">Call {PHONE}</a></div>
  </div>
</header>'''

def answer(text, label='The short answer'):
    return f'<section class="psec"><div class="wrap"><div class="answer reveal"><p class="mono alabel">{label}</p><p>{e(text)}</p></div></div></section>'

def cards(kicker, h2, items, cols=3, rel=''):
    c = ''.join('<article class="card reveal"><span class="ix mono">%02d</span><h3>%s</h3><p>%s</p></article>' % (i + 1, ('<a href="%s%s">%s</a>' % (rel, it[2], e(it[0]))) if len(it) > 2 else e(it[0]), e(it[1])) for i, it in enumerate(items))
    return f'<section class="psec"><div class="wrap"><p class="kick mono reveal">{KICK}{e(kicker)}</p><h2 class="h reveal">{e(h2)}</h2><div class="pgrid c{cols}">{c}</div></div></section>'

def checklist(kicker, h2, items, aside=''):
    li = ''.join('<li>%s</li>' % e(x) for x in items)
    return f'<section class="psec"><div class="wrap split2"><div><p class="kick mono reveal">{KICK}{e(kicker)}</p><h2 class="h reveal">{e(h2)}</h2><ul class="prog-list reveal">{li}</ul></div>{aside}</div></section>'

def steps(rel):
    S = [('Tell us what you have', 'Use the request form or call. A few details about the building and the doors is enough.'),
         ('We look at it', 'For anything beyond a simple fix, we walk the site and see the doors in person.'),
         ('You get a price first', "You'll know the price before we touch a door."),
         ('We do the work', 'One crew handles the lock, the reader and the door, and shows you what was done.')]
    c = ''.join('<li class="reveal"><span class="mono">%02d</span><h3>%s</h3><p>%s</p></li>' % (i + 1, e(a), e(b)) for i, (a, b) in enumerate(S))
    return f'<section class="psec"><div class="wrap"><p class="kick mono reveal">{KICK}How it works</p><h2 class="h reveal">From first call to finished door.</h2><ol class="steps">{c}</ol></div></section>'

def faq(qas, h2='Questions people ask us', open_first=True):
    d = ''.join('<details%s><summary>%s</summary><p>%s</p></details>' % (' open' if (i == 0 and open_first) else '', e(q), e(a)) for i, (q, a) in enumerate(qas))
    return f'<section class="psec"><div class="wrap"><p class="kick mono reveal">{KICK}Questions</p><h2 class="h reveal">{e(h2)}</h2><div class="faq reveal">{d}</div></div></section>'

def linkrow(rel, kicker, h2, links):
    c = ''.join('<a class="lcard reveal" href="%s%s"><span>%s</span><small>%s</small></a>' % (rel, p, e(n), e(b)) for n, p, b in links)
    return f'<section class="psec"><div class="wrap"><p class="kick mono reveal">{KICK}{e(kicker)}</p><h2 class="h reveal">{e(h2)}</h2><div class="lgrid">{c}</div></div></section>'

def cta(rel, h2='Let us through your front door.', p="Tell us about your building and we'll get back to you the same business day."):
    return f'''<section class="psec" id="request"><div class="wrap"><div class="em reveal"><p class="kick mono in">{KICK}Request service</p><h2>{e(h2)}</h2><p>{e(p)}</p><div class="row"><a class="btn btn-primary" href="{rel}contact/#request">Request service</a><a class="btn btn-glass" href="{rel}contact/">Contact details</a><a class="big-call" href="tel:{PHONE_TEL}">{PHONE}</a></div></div></div></section>'''

def pic(rel, s):
    return f'<figure class="pfig reveal"><picture><source type="image/webp" srcset="{rel}assets/{s["img"]}.webp"><img src="{rel}assets/{s["img"]}.jpg" alt="{e(s["alt"])}" loading="lazy" width="1600" height="1200"></picture></figure>'

def svc_ld(name, path, desc, area=None):
    return {"@type": "Service", "name": name, "serviceType": name, "description": desc, "url": BASE + '/' + path, "provider": {"@id": BASE + "/#business"}, "areaServed": area or ALL_CITIES}

def main(*blocks):
    return '<main id="main" tabindex="-1">' + ''.join(blocks) + '</main>'

SVC = {s['slug']: s for s in SERVICES}
svc_blurb = {'locksmith': 'Rekeys, master keys and high-security locks', 'access-control': 'Fobs, cards, keypads and biometrics', 'door-repair': 'Closers, hinges, strikes and frames', 'automatic-doors': 'Sliding and swing operators'}

def build():
    # shared assets
    open(os.path.join(ROOT, 'assets/site.css'), 'w', encoding='utf-8').write(rd('home.css') + '\n' + rd('inner.css'))
    for n in ('home.js', 'site.js'):
        open(os.path.join(ROOT, 'assets', n), 'w', encoding='utf-8').write(rd(n) + '\n' + rd('form.js'))

    # ---- home ----
    shell('', 'UTS Service | Locks, Access Control and Doors in the GTA',
          'Locksmith, access control, door repair and automatic doors for apartment buildings and businesses across the GTA. One team for every entrance.',
          rd('home.body.html').replace('{{REL}}', '').replace('{{FORM}}', rd('form.html').replace('{{W3F_KEY}}', W3F_KEY)),
          [BUSINESS, {"@type": "WebSite", "@id": BASE + "/#website", "url": BASE + "/", "name": "UTS Service", "publisher": {"@id": BASE + "/#business"}, "inLanguage": "en-CA"}, faq_ld(HOME_FAQS)],
          extra_head=rd('home.head.html'), scripts=('assets/home.js',), home=True)

    # ---- services hub ----
    rel = '../'
    T = [('Home', ''), ('Services', 'services/')]
    shell('services/', 'Locksmith, Access Control and Door Services | UTS Service',
          'Four trades from one crew: commercial locksmith, access control, door repair and automatic doors for buildings across the GTA.',
          hero(rel, T, 'Services', 'Four trades. One crew.', 'Locks, access control, door repair and automatic doors, handled by the same team.') + main(
              answer('UTS Service covers the four trades an entrance depends on: locksmith work, access control, door repair and automatic doors. Having one team do all four means the lock, the reader and the door are set up to work together, and one company answers for the result.'),
              cards('What we do', 'Pick the door problem you have.', [(s['name'], s['lede'], 'services/%s/' % s['slug']) for s in SERVICES], cols=2, rel=rel),
              steps(rel),
              linkrow(rel, 'Who we serve', 'Built for buildings, not one-off calls.', [('Building Program', 'building-program/', 'One account for every door')] + [(i['name'], 'industries/%s/' % i['slug'], i['lede']) for i in INDUSTRIES]),
              faq(GENERAL_FAQS[:5]), cta(rel)),
          [crumbs_ld(T), {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": s['name'], "url": BASE + '/services/%s/' % s['slug']} for i, s in enumerate(SERVICES)]}, faq_ld(GENERAL_FAQS[:5])])

    # ---- service pages ----
    rel = '../../'
    for s in SERVICES:
        p = 'services/%s/' % s['slug']; T = [('Home', ''), ('Services', 'services/'), (s['name'], p)]
        others = [(o['name'], 'services/%s/' % o['slug'], svc_blurb[o['slug']]) for o in SERVICES if o is not s]
        shell(p, s['title'], s['desc'],
              hero(rel, T, s['name'], s['h1'], s['lede']) + main(
                  answer(s['answer']),
                  cards('What we do', 'What is included.', s['do'], cols=3),
                  checklist('When to call', 'Signs it is time to call us.', s['signs'], pic(rel, s)),
                  steps(rel), faq(s['faqs']),
                  linkrow(rel, 'Related', 'Often done on the same visit.', others + [('Service areas', 'service-areas/', 'Where we work')]),
                  cta(rel)),
              [crumbs_ld(T), svc_ld(s['name'], p, s['desc']), faq_ld(s['faqs'])], og='assets/%s.jpg' % s['img'])

    # ---- building program ----
    rel = '../'; p = 'building-program/'; T = [('Home', ''), ('Building Program', p)]
    bp_faqs = [GENERAL_FAQS[1], SVC['access-control']['faqs'][3], ('Can one account cover several buildings?', 'Yes. One account covers every site, with the same team and the same standards at each.'), ('What does a scheduled check cover?', 'The closers, strikes, hinges, locks and readers on your main doors, looked at on a regular visit so problems are caught before a door fails.')]
    shell(p, 'Building Program for Property Managers | UTS Service',
          'One account for every lock, fob reader and door in your buildings. Fob management, master keys, scheduled checks and a priority line.',
          hero(rel, T, 'The Building Program', 'One call. Every door.', 'Most buildings juggle a locksmith, an access company and a door guy. Then nobody owns the problem. We take all of it.') + main(
              answer('The Building Program is one account for every lock, reader and door in your buildings. Instead of calling a locksmith, an access control company and a door company, you call one team that already knows your properties.'),
              cards('What is included', 'Four things you stop chasing.', [
                  ('Fob management', 'We add, cancel and audit credentials the same day.'),
                  ('Master key systems', 'Know who holds which key, and rekey when someone leaves.'),
                  ('Scheduled checks', 'Closers, strikes, hinges and readers inspected before they fail.'),
                  ('Priority line', 'Building emergencies go to the front of the queue.')], cols=2),
              checklist('Who it is for', 'A fit if this sounds familiar.', ['You manage more than one building', "You aren't sure who still has keys or fobs", 'The same door keeps getting patched', 'Three vendors each blame the other two', 'You want one invoice and one phone number']),
              linkrow(rel, 'By building type', 'See how it works for your kind of building.', [(i['name'], 'industries/%s/' % i['slug'], i['lede']) for i in INDUSTRIES]),
              steps(rel), faq(bp_faqs), cta(rel, 'Put every door on one account.')),
          [crumbs_ld(T), svc_ld('Building Program', p, 'One account for locksmith work, access control, door repair and automatic doors across a portfolio of buildings.'), faq_ld(bp_faqs)])

    # ---- industries ----
    rel = '../'; T = [('Home', ''), ('Industries', 'industries/')]
    shell('industries/', 'Who We Serve: Buildings and Businesses | UTS Service',
          'Locks, access control and doors for apartment and condo buildings, retail and franchise locations, offices and public buildings across the GTA.',
          hero(rel, T, 'Who we serve', 'Built for buildings, not one-off calls.', 'Property managers, retailers, offices and public buildings across the GTA.') + main(
              answer('UTS Service works for the people responsible for buildings: property managers and condo boards, retail and franchise operators, office and facility managers, and public sector teams. Every customer is a building or a business, and most have more than one site.'),
              cards('By building type', 'Find your kind of building.', [(i['name'], i['lede'], 'industries/%s/' % i['slug']) for i in INDUSTRIES], cols=2, rel=rel),
              linkrow(rel, 'For portfolios', 'More than one building?', [('Building Program', 'building-program/', 'One account for every door'), ('Services', 'services/', 'The four trades we cover'), ('Service areas', 'service-areas/', 'Where we work')]),
              cta(rel)),
          [crumbs_ld(T)])
    rel = '../../'
    for i in INDUSTRIES:
        p = 'industries/%s/' % i['slug']; T = [('Home', ''), ('Industries', 'industries/'), (i['name'], p)]
        note = '<section class="psec"><div class="wrap"><p class="pnote2 reveal">%s</p></div></section>' % e(i['note']) if i.get('note') else ''
        shell(p, i['title'], i['desc'],
              hero(rel, T, i['name'], i['h1'], i['lede'], img='hero-ending.jpg') + main(
                  answer(i['answer']),
                  cards('What we handle', 'The door problems this kind of building has.', i['items'], cols=2),
                  note,
                  linkrow(rel, 'Services', 'What we usually do here.', [(SVC[k]['name'], 'services/%s/' % k, svc_blurb[k]) for k in i['svc']]),
                  steps(rel), faq(i['faqs']), cta(rel)),
              [crumbs_ld(T), svc_ld('Locksmith, access control and door services for ' + i['name'].lower(), p, i['desc']), faq_ld(i['faqs'])])

    # ---- service areas ----
    rel = '../'; T = [('Home', ''), ('Service areas', 'service-areas/')]
    groups = ''.join('<div class="region reveal"><p class="mono rlabel"><a href="%s/">%s</a></p><ul class="cities">%s</ul></div>' % (r[0], e(r[1]), ''.join('<li>%s</li>' % e(c) for c in r[2])) for r in REGIONS)
    area_faqs = [GENERAL_FAQS[5], ('Where is UTS Service based?', 'Our shop is at 50 Alness St, Unit 1, in North York, Ontario.'), ('Do you travel outside the GTA?', 'Yes. We travel to Hamilton, Barrie, Guelph, Cambridge, Kitchener, Waterloo, St. Catharines, Niagara Falls and Brantford.')]
    shell('service-areas/', 'Service Areas: Toronto, the GTA and Beyond | UTS Service',
          'UTS Service covers Toronto, Peel, York, Durham and Halton regions, plus Hamilton, Niagara, Kitchener-Waterloo, Guelph, Brantford and Barrie.',
          hero(rel, T, 'Coverage', 'Across the GTA and well beyond it.', 'Based in North York. Working in %d cities and towns across southern Ontario.' % len(ALL_CITIES)) + main(
              answer('UTS Service is based at 50 Alness St in North York and works across Toronto, Peel, York, Durham and Halton regions. We also travel to Hamilton, Niagara, Kitchener-Waterloo, Guelph, Brantford and Barrie.'),
              '<section class="psec"><div class="wrap"><p class="kick mono reveal">%sBy region</p><h2 class="h reveal">Every place we work.</h2><div class="regions">%s</div></div></section>' % (KICK, groups),
              faq(area_faqs), cta(rel)),
          [crumbs_ld(T), faq_ld(area_faqs)])
    rel = '../../'
    for slug, name, cities, blurb in REGIONS:
        p = 'service-areas/%s/' % slug; T = [('Home', ''), ('Service areas', 'service-areas/'), (name, p)]
        clist = ', '.join(cities[:-1]) + ' and ' + cities[-1]
        where = 'outside the GTA' if slug == 'southern-ontario' else 'in ' + name
        h1 = 'Commercial locksmith and access control ' + ('beyond the GTA' if slug == 'southern-ontario' else 'in ' + name)
        qas = [('Does UTS Service work %s?' % where, 'Yes. We work in %s.' % clist),
               ('What do you do %s?' % where, 'The same four trades we do everywhere: locksmith work, access control, door repair and automatic doors, for apartment buildings and businesses.'),
               ('How do I book a visit?', 'Use the online request form, email %s, or call %s.' % (EMAIL, PHONE))]
        chips = '<section class="psec"><div class="wrap"><p class="kick mono reveal">%sCities and towns</p><h2 class="h reveal">Where we work %s.</h2><ul class="cities big reveal">%s</ul></div></section>' % (KICK, where, ''.join('<li>%s</li>' % e(c) for c in cities))
        others = [(r[1], 'service-areas/%s/' % r[0], ', '.join(r[2][:3]) + (' and more' if len(r[2]) > 3 else '')) for r in REGIONS if r[0] != slug]
        desc = 'Locksmith, access control, door repair and automatic doors for buildings and businesses in %s.' % clist
        if len(desc) > 158: desc = 'Locksmith, access control, door repair and automatic doors for apartment buildings and businesses across %s.' % ('southern Ontario' if slug == 'southern-ontario' else name)
        shell(p, ('Locksmith and Access Control %s | UTS Service' % ('Beyond the GTA' if slug == 'southern-ontario' else 'in ' + name)), desc,
              hero(rel, T, name, h1, blurb) + main(
                  answer('Yes, UTS Service works %s. We cover %s, handling locksmith work, access control, door repair and automatic doors for apartment buildings and businesses.' % (where, clist)),
                  chips,
                  linkrow(rel, 'Services', 'What we do %s.' % where, [(s['name'], 'services/%s/' % s['slug'], svc_blurb[s['slug']]) for s in SERVICES]),
                  faq(qas),
                  linkrow(rel, 'Other areas', 'We also work in these regions.', others),
                  cta(rel)),
              [crumbs_ld(T), svc_ld('Commercial locksmith and access control', p, desc, cities), faq_ld(qas)])

    # ---- emergency ----
    rel = '../'; p = 'emergency-service/'; T = [('Home', ''), ('Emergency service', p)]
    em_faqs = [GENERAL_FAQS[2], ('What counts as a building emergency?', 'An entrance that will not lock, a door that will not open, an automatic door stuck open or shut, an access system that is down, or a break-in that left a door unsecured.'), ('What should I do while I wait?', 'Keep someone at the unsecured door if you can, do not force a jammed automatic door, and note which door or reader has the problem so we arrive with the right parts.')]
    shell(p, 'Emergency Locksmith and Door Service, GTA | UTS Service',
          "Front door won't lock? Reader down? Automatic door stuck? Call UTS Service at 647-777-7411 for building door emergencies across the GTA.",
          hero(rel, T, 'Building emergencies', "Front door won't lock at 2 a.m.?", "Garage door stuck. Lobby door wide open. Reader dead. Call and we're on the way.") + main(
              answer("If a door won't lock, won't open, or an access system is down, call %s. Building emergencies go to the front of our queue, and we'll give you a real arrival time on the phone." % PHONE, 'What to do right now'),
              cards('What we come out for', 'The calls that cannot wait.', [
                  ('Entrance will not lock', 'A front or back door that will not secure the building.'),
                  ('Locked out', 'A unit, office or storefront nobody can get into.'),
                  ('Automatic door stuck', 'Stuck open, stuck shut, or closing on people.'),
                  ('Access system down', 'Readers dead, fobs rejected, doors not releasing.'),
                  ('After a break-in', 'Doors and locks secured, then repaired properly.'),
                  ('Lost master key', 'The affected locks rekeyed so the lost key is useless.')], cols=3),
              faq(em_faqs),
              linkrow(rel, 'Stop the next one', 'Most emergencies start as small problems.', [('Building Program', 'building-program/', 'Scheduled checks and a priority line'), ('Door repair', 'services/door-repair/', 'Fix it before it fails'), ('Automatic doors', 'services/automatic-doors/', 'Regular service')]),
              cta(rel, 'Call now: ' + PHONE, 'Or send the details through the request form and we will call you back.')),
          [crumbs_ld(T), svc_ld('Emergency locksmith and door service', p, 'Emergency door, lock and access control service for buildings across the GTA.'), faq_ld(em_faqs)])

    # ---- about ----
    p = 'about/'; T = [('Home', ''), ('About', p)]
    shell(p, 'About UTS Service | Commercial Security in North York',
          'UTS Service is a commercial security company in North York. Locksmith, access control, door repair and automatic doors for buildings across Ontario.',
          hero(rel, T, 'About us', 'The people who keep the doors working.', 'A commercial security company in North York, serving buildings and businesses across Ontario.', img='hero-ending.jpg') + main(
              answer('UTS Service is a commercial security company based at 50 Alness St in North York, Ontario. We provide locksmith services, access control systems, door repair and automatic door installation for businesses, commercial properties and apartment buildings.', 'Who we are'),
              cards('What we stand for', 'Four things we hold ourselves to.', [
                  ('Reliability', 'We do what we said we would, on time.'),
                  ('Commitment', 'Customer satisfaction and long relationships come first.'),
                  ('Quality', 'We use security products that meet industry standards.'),
                  ('Innovation', 'We keep improving how we work and what we install.')], cols=2),
              '<section class="psec"><div class="wrap"><p class="kick mono reveal">%sOur mission</p><h2 class="h reveal">Protect businesses. Give people peace of mind.</h2><p class="lede reveal">Our mission is to deliver reliable, high-quality security that protects businesses, with skilled people and proven hardware matched to what each customer needs.</p><p class="pnote2 reveal">%s</p></div></section>' % (KICK, e("Names we've worked for include Tim Hortons, Amazon, RBC, the City of Toronto, the Ontario Provincial Police, CF Toronto Eaton Centre, Louis Vuitton, Mercedes-Benz, Canada Post, UPS, WeWork, SmartCentres, Domino's Pizza, Pizza Pizza and Fred Victor.")),
              linkrow(rel, 'Explore', 'What we do and where.', [('Services', 'services/', 'The four trades we cover'), ('Building Program', 'building-program/', 'One account for every door'), ('Service areas', 'service-areas/', 'Where we work'), ('Contact', 'contact/', 'Phone, email and address')]),
              cta(rel)),
          [crumbs_ld(T), {"@type": "AboutPage", "url": BASE + '/' + p, "about": {"@id": BASE + "/#business"}}])

    # ---- faq ----
    p = 'faq/'; T = [('Home', ''), ('FAQ', p)]
    allq = list(GENERAL_FAQS)
    blocks = [faq(GENERAL_FAQS, 'About working with us')]
    for s in SERVICES:
        blocks.append(faq(s['faqs'], s['name'], open_first=False)); allq += [q for q in s['faqs'] if q not in allq]
    shell(p, 'Locksmith and Access Control FAQ | UTS Service',
          'Plain answers about commercial locks, master keys, fob systems, door repair and automatic doors from UTS Service in North York.',
          hero(rel, T, 'Questions', 'Plain answers about locks, fobs and doors.', 'What property managers and business owners ask us most.') + main(*blocks, cta(rel)),
          [crumbs_ld(T), faq_ld(allq)])

    # ---- contact ----
    p = 'contact/'; T = [('Home', ''), ('Contact', p)]
    planner = rd('form.html').replace('{{W3F_KEY}}', W3F_KEY)
    contact = f'''<section class="psec" id="request"><div class="wrap split2 top">
      <div class="reveal"><p class="kick mono in">{KICK}Reach us</p><h2 class="h">Call, email or send a request.</h2>
        <ul class="nap">
          <li><span class="mono">Phone</span><a href="tel:{PHONE_TEL}">{PHONE}</a> <a href="tel:{PHONE2_TEL}">{PHONE2}</a></li>
          <li><span class="mono">Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><span class="mono">Address</span><a href="{MAPS}" target="_blank" rel="noopener">50 Alness St, Unit 1<br>North York, ON M3J 2G9</a></li>
        </ul></div>
      {planner}
    </div></section>'''
    shell(p, 'Contact UTS Service | Request Locksmith or Door Service',
          'Call 647-777-7411, email Admin@utsservice.ca or send a service request online. UTS Service, 50 Alness St, Unit 1, North York, ON.',
          hero(rel, T, 'Contact', 'Let us through your front door.', "Fill in the form and we'll get back to you the same business day.", img='hero-ending.jpg') + main(contact, faq([GENERAL_FAQS[6], GENERAL_FAQS[2], GENERAL_FAQS[3]], 'Before you reach out')),
          [crumbs_ld(T), {"@type": "ContactPage", "url": BASE + '/' + p, "about": {"@id": BASE + "/#business"}}, faq_ld([GENERAL_FAQS[6], GENERAL_FAQS[2], GENERAL_FAQS[3]])])

    # ---- 404 ----
    body404 = f'<main id="main" tabindex="-1"><section class="psec p404"><div class="wrap"><p class="kick mono in">{KICK}404</p><h1>This door is locked.</h1><p class="lede">The page you were looking for is not here.</p><div class="row"><a class="btn btn-primary" href="{BASE}/">Back to the front entrance</a><a class="btn btn-glass" href="{BASE}/services/">Services</a></div></div></section></main>'
    out_pages = list(pages)
    shell('404', 'Page not found | UTS Service', 'This page does not exist.', body404, [])
    s404 = open(os.path.join(ROOT, '404.html'), encoding='utf-8').read()
    for a in ('href="assets/', 'src="assets/'):
        s404 = s404.replace(a, a.split('"')[0] + '"' + BASE + '/assets/')
    for n, pth in NAV: s404 = s404.replace('href="%s"' % pth, 'href="%s/%s"' % (BASE, pth))
    for extra in ['contact/', 'about/', 'faq/', 'emergency-service/', 'building-program/'] + ['services/%s/' % s['slug'] for s in SERVICES] + ['industries/%s/' % i['slug'] for i in INDUSTRIES] + ['service-areas/%s/' % r[0] for r in REGIONS]:
        s404 = s404.replace('href="%s"' % extra, 'href="%s/%s"' % (BASE, extra))
    s404 = s404.replace('href="./"', 'href="%s/"' % BASE).replace('<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">')
    open(os.path.join(ROOT, '404.html'), 'w', encoding='utf-8').write(s404)

    # ---- sitemap, robots, llms.txt ----
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join('<url><loc>%s/%s</loc><lastmod>%s</lastmod></url>\n' % (BASE, pth, TODAY) for pth in out_pages) + '</urlset>\n'
    open(os.path.join(ROOT, 'sitemap.xml'), 'w').write(sm)
    open(os.path.join(ROOT, 'robots.txt'), 'w').write('User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n' % BASE)
    L = ['# UTS Service', '', '> Commercial locksmith, access control, door repair and automatic doors for apartment buildings and businesses across the Greater Toronto Area. Based at 50 Alness St, Unit 1, North York, ON M3J 2G9. Phone %s. Email %s.' % (PHONE, EMAIL), '',
         'UTS Service works for property managers, condo boards, retail and franchise operators, offices and public sector buildings. Customers are buildings and businesses, not individual homeowners.', '', '## Services']
    L += ['- [%s](%s/services/%s/): %s' % (s['name'], BASE, s['slug'], s['answer']) for s in SERVICES]
    L += ['- [Building Program](%s/building-program/): One account for every lock, reader and door across a portfolio of buildings.' % BASE, '- [Emergency service](%s/emergency-service/): Building door, lock and access emergencies. Call %s.' % (BASE, PHONE), '', '## Who we serve']
    L += ['- [%s](%s/industries/%s/): %s' % (i['name'], BASE, i['slug'], i['answer']) for i in INDUSTRIES]
    L += ['', '## Service areas'] + ['- [%s](%s/service-areas/%s/): %s' % (r[1], BASE, r[0], ', '.join(r[2])) for r in REGIONS]
    L += ['', '## Company', '- [About](%s/about/)' % BASE, '- [FAQ](%s/faq/)' % BASE, '- [Contact](%s/contact/)' % BASE, '- [Request service](%s/contact/#request)' % BASE, '']
    open(os.path.join(ROOT, 'llms.txt'), 'w', encoding='utf-8').write('\n'.join(L))
    print('built', len(out_pages), 'pages')

if __name__ == '__main__':
    build()
