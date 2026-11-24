#!/usr/bin/env python3
"""Generates the static pages (shared header/footer) into the repo root.
Run:  python3 tools/make_pages.py
Car stock and reviews live in data.js; everything else is in this file."""
import json, os, html, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.loads(open(os.path.join(ROOT, 'data.js'), encoding='utf8').read().split('=', 1)[1].rstrip().rstrip(';'))
e = html.escape
V = '5'  # bump to bust the browser cache for css/js

PH = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 4h4l2 5-2.500 1.500a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg>'
WAI = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.600 15.100L2 22l5-1.300A10 10 0 1 0 12 2zm5.800 14.200c-.200.700-1.400 1.300-1.900 1.400-.500.100-1.100.100-1.800-.100-.400-.100-1-.300-1.600-.600-2.900-1.200-4.700-4.100-4.900-4.300-.100-.200-1.200-1.500-1.200-2.900s.700-2.100 1-2.400c.300-.300.600-.300.800-.300h.500c.200 0 .400-.100.700.500l.900 2.200c.100.200.100.400 0 .600l-.300.500-.500.500c-.200.200-.300.300-.100.600.200.300.800 1.300 1.700 2.100 1.200 1 2.100 1.400 2.400 1.500.300.100.500.100.600-.100l.800-1c.200-.300.400-.200.700-.100l2 1c.300.100.500.200.600.300.100.300.100.800-.100 1.400z"/></svg>'
PIN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 21s7-6.200 7-11.500A7 7 0 0 0 5 9.500C5 14.800 12 21 12 21z"/><circle cx="12" cy="9.500" r="2.500"/></svg>'
CLK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'
CAL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="4" y="5" width="16" height="16" rx="2"/><path d="M4 10h16M9 3v4M15 3v4"/></svg>'
GOOG = '<svg viewBox="0 0 24 24"><path fill="#4285F4" d="M22.500 12.200c0-.800-.100-1.500-.200-2.200H12v4.200h5.900a5 5 0 0 1-2.200 3.300v2.700h3.500c2.100-1.900 3.300-4.700 3.300-8z"/><path fill="#34A853" d="M12 23c3 0 5.500-1 7.300-2.700l-3.500-2.700c-1 .700-2.300 1.100-3.800 1.100-2.900 0-5.300-1.900-6.200-4.600H2.200v2.800A11 11 0 0 0 12 23z"/><path fill="#FBBC05" d="M5.800 14.100a6.600 6.600 0 0 1 0-4.200V7.100H2.200a11 11 0 0 0 0 9.800l3.600-2.800z"/><path fill="#EA4335" d="M12 5.400c1.600 0 3.100.600 4.200 1.600l3.100-3.100A11 11 0 0 0 2.200 7.100l3.600 2.800C6.700 7.300 9.100 5.400 12 5.400z"/></svg>'

ICONS = {
 'gear':'<circle cx="12" cy="12" r="3.200"/><path d="M12 2.500v3M12 18.500v3M2.500 12h3M18.500 12h3M5.300 5.300l2.100 2.100M16.600 16.600l2.100 2.100M5.300 18.700l2.100-2.100M16.600 7.400l2.100-2.100"/>',
 'susp':'<path d="M8 3h8M8 21h8M12 3v2M12 19v2M8 6.500l8 2.500-8 2.500 8 2.500-8 2.500"/>',
 'exh':'<path d="M2 13h4l2-2h8v6H8l-2-2H2zM16 12.500h4M16 15.500h4M21 9c1 0 1-2 0-2.500M18.500 9c1 0 1-2 0-2.500"/>',
 'fuel':'<path d="M4 21V5a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v16M3 21h12M6.500 7h5v4h-5zM14 9l4 3v6a1.500 1.500 0 0 0 3 0v-8l-3-3"/>',
 'diag':'<rect x="3" y="4" width="18" height="12" rx="1.500"/><path d="M6 11h3l1.500-3 2.500 5 1.500-2H18M9 20h6M12 16v4"/>',
 'eng':'<path d="M7 9V6h6v3M9 6V4h2M4 12v5M4 14.500h3M7 9h9l2 3h2v6h-2l-1 2H9l-2-2z"/>',
 'brake':'<circle cx="12" cy="12" r="8.500"/><circle cx="12" cy="12" r="3"/><path d="M12 3.500v2M12 18.500v2M3.500 12h2M18.500 12h2"/>',
 'batt':'<rect x="3" y="7" width="18" height="12" rx="1.500"/><path d="M7 7V5M17 7V5M6.500 13h3M15 13h3M16.500 11.500v3"/>',
 'nct':'<path d="M9 4h6l1 2h3v15H5V6h3zM8.500 13l2.500 2.500 4.500-5"/>',
 'belt':'<circle cx="7" cy="8" r="3.500"/><circle cx="17" cy="16" r="3.500"/><path d="M4.500 10.500l10 8M9.500 5.500l10 8"/>',
 'oil':'<path d="M3 11h5l2-3h4v3l6-2-3 9H8l-1-3H3zM20.500 14c.800 1.200 1.200 1.900 1.200 2.600a1.200 1.200 0 0 1-2.400 0c0-.700.400-1.400 1.200-2.600z"/>',
}
SERVICES = [
 ('Gearbox / Transmission Repair','gear','Expert gearbox repair services with fast turnaround, high-quality parts, and experienced technicians to get your vehicle back on the road smoothly and efficiently.','Gearbox/Transmission'),
 ('Suspension Repair','susp','If you’re experiencing a bumpy ride or unusual handling, your suspension system may be in need of repair. Let our experts diagnose and fix the issue.','Suspension'),
 ('Exhaust System Services','exh','A faulty exhaust system can lead to decreased performance and even dangerous emissions. We offer a range of exhaust system services to keep you safe and on the road.','Other'),
 ('Fuel System Services','fuel','If you’re experiencing issues with your fuel system, such as poor fuel economy or difficulty starting your vehicle, let us diagnose and fix the issue.','Other'),
 ('Diagnostic Services','diag','If you’re not sure what’s wrong with your vehicle, bring it in for our diagnostic services. Our experts will diagnose the issue and recommend the necessary repairs.','Diagnostic & Routine Maintenance'),
 ('Engine Repair','eng','Our skilled technicians can diagnose and repair any engine problem. From oil changes to complete engine overhauls, we have you covered.','Engine'),
 ('Brake Services','brake','Don’t neglect your brakes. Let us keep them in top condition. Our brake services include brake pad and rotor replacement, brake line repair, and more.','Brakes'),
 ('Battery','batt','Reliable car batteries with long-lasting performance, quick installation, and warranties to keep your vehicle powered in any condition.','Battery'),
 ('Pre / Post NCT','nct','Comprehensive pre- and post-NCT checks to ensure your car passes inspection with ease, addressing issues beforehand and verifying everything is road-ready afterward.','Pre NCT'),
 ('Timing Belt','belt','Professional timing belt replacement to ensure your engine runs smoothly, preventing costly damage with quality parts and expert installation.','Timing Belt'),
 ('Routine Maintenance','oil','Regular maintenance is the key to keeping your vehicle running smoothly and avoiding costly repairs. Let us handle your oil changes, tune-ups, and more.','Interim Service'),
]
APPT = ['Pre NCT','Post NCT','Diagnostic & Routine Maintenance','Brakes','Suspension','Engine','Transmission','Battery','Interim Service','Timing Belt','Gearbox/Transmission','Other']
FAQ_GARAGE = [
 ('How often should I get my oil changed?','We recommend getting your oil changed every 5,000 miles or every six months, whichever comes first. This can help keep your engine running smoothly and prevent damage.'),
 ('Do I need to schedule an appointment?','While we do accept walk-ins, we highly recommend scheduling an appointment to ensure timely service. You can book an appointment by calling us or through the booking form on this website.'),
 ('How long will my repair take?','The time required for repairs depends on the complexity of the issue. Simple services like oil changes and tyre rotations can often be completed within an hour, while more complex repairs may take several hours or even a full day. We will provide you with an estimated timeline when you bring your vehicle in.'),
 ('How much will my repair cost?','Repair costs vary depending on the type of service and the parts required. After diagnosing the issue, we will provide you with a detailed estimate before any work begins. We strive to offer competitive pricing and ensure transparency with no hidden fees.'),
 ('Are you certified to work on my make and model?','Our technicians are certified and experienced in working on a wide range of vehicle makes and models, including domestic and foreign brands. We undergo regular training to stay up-to-date with the latest automotive technology and repair techniques.'),
 ('Do you offer emergency or after-hours services?','We understand that car trouble can happen at any time. While we do not offer 24/7 services, we can assist with towing and provide emergency repairs during business hours. For after-hours emergencies, please contact a local towing service to bring your vehicle to our garage, and we will attend to it as soon as we open.'),
 ('What payment methods do you accept?','We accept a variety of payment methods, including cash, major credit cards, and debit cards. If you need to discuss alternative payment options, please let us know in advance.'),
 ('How can I check the status of my repair?','You can call us at any time during business hours to check the status of your repair. We’ll provide you with updates and let you know when your vehicle is ready for pickup. Additionally, we may offer text or email updates for your convenience.'),
 ('How do I contact you?','You can reach us by phone, email, WhatsApp or through this website. See the Contact page for our phone numbers, email address, and business hours. We’re always happy to answer any questions or assist with scheduling an appointment.'),
]
FAQ_SALES = [
 ('What types of cars do you sell?','We sell a wide range of cars including saloons, SUVs, trucks, and sports cars.'),
 ('Do you offer financing options?','Yes, we offer financing options through various banks and financing companies. Contact us for more information.'),
 ('Do you accept trade-ins?','Yes, we accept trade-ins. Contact us with information on your current vehicle and we’ll provide a trade-in value.'),
 ('Can I schedule a test drive?','Of course! Test drives are available by appointment. Reach out to book yours today.'),
 ('Do you deliver cars?','Yes, we offer delivery options for your convenience. Contact us to learn more.'),
]
NAV = [('services','Car Clinic'),('cars','Cars for Sale'),('about','About'),('reviews','Reviews'),('faq','FAQ'),('contact','Contact')]
MON = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
from urllib.parse import quote

def ico(k): return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.600" stroke-linecap="round" stroke-linejoin="round">{ICONS[k]}</svg>'
def svc_cards(items, start=0):
    return ''.join(f'<a class="card rvl" style="--d:{(i%4)*.06}s" href="contact?type=service&amp;service={quote(s[3])}"><span class="no">{start+i+1:02d}</span><div class="ico">{ico(s[1])}</div><h3>{e(s[0])}</h3><p>{e(s[2])}</p><span class="link">Book this job</span></a>' for i, s in enumerate(items))
def review(r):
    y, m, _ = r['date'].split('-'); body = re.sub(r'^[⭐\s]+', '', r['body'])
    return f'<figure class="rv rvl"><div class="stars" aria-label="5 out of 5 stars">★★★★★</div><blockquote>{e(body)}</blockquote><figcaption><span class="av">{e(r["name"][0].upper())}</span><span><b>{e(r["name"])}</b><small>Google review · {MON[int(m)-1]} {y}</small></span></figcaption></figure>'
def faq(items): return ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in items)
def band(h, p, a, b):
    return f'''<section class="tight"><div class="wrap"><div class="band rvl"><div><h2 class="sil">{h}</h2><p>{p}</p></div><div class="cta">{a}{b}</div></div></div></section>'''
BOOK = '<a class="btn btn-red" href="contact?type=service">Book a service <span class="ar">→</span></a>'
VIEW = '<a class="btn btn-ghost" href="cars">View cars</a>'
CALL = f'<a class="btn btn-ghost" href="tel:+353857553430">{PH}085 755 3430</a>'

def hero_small(eyebrow, h1, lead, media=''):
    return f'''<div class="hero sm"><div class="media" aria-hidden="true">{media}</div><div class="wrap"><span class="eyebrow">{eyebrow}</span><h1 class="sil">{h1}</h1><p class="lead">{lead}</p></div></div>'''

def page(slug, title, desc, body, intro=False):
    nav = ''.join(f'<a href="{s}"{" aria-current=\"page\"" if s == slug else ""}>{n}</a>' for s, n in NAV)
    intro_html = '''<div class="intro" aria-hidden="true"><div class="in"><img src="img/logo.webp" alt="" width="720" height="254"><span class="beam"></span><div class="bar"><i></i></div><small>Greenhills Road · Dublin 12</small></div><button class="sk" type="button">Skip</button></div>''' if intro else ''
    return f'''<!doctype html>
<html lang="en-IE" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#0a0a0b">
<meta property="og:type" content="website"><meta property="og:locale" content="en_IE"><meta property="og:site_name" content="Starline Motors">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:image" content="img/og.jpg">
<link rel="icon" href="img/icon-48.png" sizes="48x48"><link rel="apple-touch-icon" href="img/icon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/site.css?v={V}">
<script>document.documentElement.classList.remove('no-js')</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{intro_html}
<div class="top"><div class="wrap">
  <div class="grp"><span class="i">{PIN}<a href="contact">Greenhills Road, Dublin 12 · D12 K303</a></span></div>
  <div class="grp hide"><span class="i">{CLK}Car Clinic 09:00 – 18:00 · Sales 09:00 – 17:00</span><span class="i">{PH}<a href="tel:+353857553430">085 755 3430</a></span></div>
</div></div>
<header class="nav"><div class="wrap">
  <a class="brand" href="./" aria-label="Starline Motors home"><img src="img/logo.webp" alt="Starline Motors" width="720" height="254"></a>
  <button class="burger" aria-label="Menu" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
  <nav class="links" id="menu" aria-label="Main">{nav}</nav>
  <a class="btn btn-red btn-sm call" href="contact?type=service">Book in</a>
</div></header>
<main id="main">
{body}
</main>
<footer><div class="wrap">
  <div class="fg">
    <div>
      <div class="logos"><img src="img/logo.webp" alt="Starline Motors" width="720" height="254" loading="lazy"><img src="img/car-clinic.webp" alt="Car Clinic at Starline Motors" width="760" height="331" loading="lazy"></div>
      <p>Quality used cars &amp; commercials, with expert servicing and repairs at the Car Clinic on-site.</p>
      <div class="soc">
        <a href="https://www.facebook.com/p/Starline-Motors-61555278196141/" target="_blank" rel="noopener" aria-label="Starline Motors on Facebook"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M14 9V7c0-1 .300-1.500 1.600-1.500H17V2h-2.600C11.300 2 10 3.800 10 6.500V9H7.500v3.500H10V22h4v-9.500h2.700L17 9z"/></svg></a>
        <a href="https://www.instagram.com/starline_motors_sales/" target="_blank" rel="noopener" aria-label="Starline Motors on Instagram"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.500" cy="6.500" r="1" fill="currentColor"/></svg></a>
        <a href="https://wa.me/353857553430" target="_blank" rel="noopener" aria-label="WhatsApp">{WAI}</a>
      </div>
    </div>
    <div><h4>EXPLORE</h4><ul><li><a href="services">Car Clinic services</a></li><li><a href="cars">Cars for sale</a></li><li><a href="about">About us</a></li><li><a href="reviews">Reviews</a></li><li><a href="faq">FAQ</a></li></ul></div>
    <div><h4>CONTACT</h4><ul><li><a href="tel:+353857553430">085 755 3430</a></li><li><a href="tel:+353852258335">Sales: 085 225 8335</a></li><li><a href="mailto:starlinemotorssales@gmail.com">starlinemotorssales@gmail.com</a></li><li><a href="contact">Book in</a></li></ul></div>
    <div><h4>VISIT</h4><ul><li>Greenhills Road, Kilnamanagh</li><li>Dublin 12, D12 K303</li><li>Car Clinic 09:00 – 18:00</li><li>Sales 09:00 – 17:00</li></ul></div>
  </div>
  <div class="legal"><span>Copyright © <span data-yr>2026</span> Starline Motors. All rights reserved.</span><span>Website by <a href="https://almlabmarketing.com/" target="_blank" rel="noopener">AlmLab</a></span></div>
</div></footer>
<a class="fab" href="https://wa.me/353857553430" target="_blank" rel="noopener" aria-label="Message us on WhatsApp">{WAI}</a>
<div class="dock"><a href="tel:+353857553430">{PH}Call</a><a href="https://wa.me/353857553430" target="_blank" rel="noopener">{WAI}WhatsApp</a><a class="r" href="contact?type=service">{CAL}Book in</a></div>
<script src="data.js?v={V}"></script>
<script src="js/site.js?v={V}"></script>
</body>
</html>
'''

VID = lambda n: f'<video muted loop playsinline preload="none" poster="img/{n}.webp" data-src="video/{n}.mp4"></video>'
RATING = f'''<a class="gpill" href="reviews"><span class="g">{GOOG}</span><b data-n="rating">{DATA["rating"]}</b><span class="stars" aria-hidden="true">★★★★★</span><span><span data-n="total">{DATA["total"]}</span> Google reviews</span></a>'''

# ---------------- HOME ----------------
home = f'''
<div class="hero"><div class="media" aria-hidden="true">{VID("hero")}</div>
  <div class="wrap">
    <span class="eyebrow">Greenhills Road · Dublin 12</span>
    <h1 class="sil">Fixed right. <em>Sold honest.</em></h1>
    <p class="lead">Starline Motors and the Car Clinic under one roof. Expert servicing and repairs, and quality used cars and commercials you can trust.</p>
    <div class="cta">{BOOK}{VIEW}{CALL}</div>
    {RATING}
    <div class="ticks"><span>10+ years of auto repair</span><span>OE standard parts</span><span>3 months warranty on cars</span></div>
  </div>
  <span class="scroll" aria-hidden="true">Scroll</span>
</div>

<section class="tight"><div class="wrap">
  <div class="doors">
    <a class="door rvl" href="services">{VID("clinic")}<div class="c"><img class="lg" src="img/car-clinic.webp" alt="Car Clinic at Starline Motors" width="760" height="331" loading="lazy"><h3>The Car Clinic</h3><p>Servicing, diagnostics, NCT prep, brakes, gearbox, timing belts and major repairs.</p><span class="go">Explore services <i>→</i></span></div></a>
    <a class="door rvl" style="--d:.1s" href="cars"><img class="bg" id="door-car" src="img/hero.webp" alt="" loading="lazy"><div class="c"><h3>Cars for sale</h3><p><span data-n="stock">16</span> cars and commercials in stock. Fully motor checked, serviced and ready to go.</p><span class="go">Browse the stock <i>→</i></span></div></a>
  </div>
</div></section>

<section class="light"><div class="wrap">
  <div class="sec-h rvl"><div><span class="eyebrow">The Car Clinic</span><h2>Quality auto <em>repair services</em></h2></div><p>Our skilled technicians use the latest tools and technology to make sure your car performs at its best.</p></div>
  <div class="svc mini">{svc_cards([SERVICES[4],SERVICES[8],SERVICES[6],SERVICES[0]])}</div>
  <p style="margin:34px 0 0" class="rvl"><a class="btn btn-dark" href="services">All 11 services <span class="ar">→</span></a></p>
</div></section>

<div class="mq" aria-hidden="true"><div>{"".join("<span>"+t+"</span>" for t in ["Servicing","Diagnostics","Pre &amp; Post NCT","Brakes","Gearbox","Timing Belts","Used Cars","Commercials"]*2)}</div></div>

<section class="ink2"><div class="wrap">
  <div class="sec-h rvl"><div><span class="eyebrow">Just in</span><h2 class="sil">Find your <em>dream car</em></h2></div><a class="btn btn-ghost" href="cars">See all cars <span class="ar">→</span></a></div>
  <div class="grid dark-cars hscroll" id="featured"></div>
</div></section>

<section class="light"><div class="wrap">
  <div class="sec-h rvl"><div><span class="eyebrow">See what our clients say</span><h2>Word of <em>mouth</em></h2></div>
    <div class="rate"><b data-n="rating">{DATA["rating"]}</b><div><div class="stars" aria-hidden="true">★★★★★</div><small>from <span data-n="total">{DATA["total"]}</span> reviews on Google</small></div></div></div>
  <div class="rv3 hscroll">{"".join(review(r) for r in [DATA["reviews"][5],DATA["reviews"][2],DATA["reviews"][6]])}</div>
  <p style="margin:34px 0 0" class="rvl"><a class="btn btn-dark" href="reviews">Read more reviews <span class="ar">→</span></a></p>
</div></section>
{band("Ready when <em>you are</em>","Book a service, a viewing or a test drive. We reply fast and quote before any work begins.",BOOK,'<a class="btn btn-ghost" href="contact?type=viewing">Book a test drive</a>')}
'''

# ---------------- SERVICES ----------------
services = f'''
{hero_small("The Car Clinic","Quality auto <em>repair services</em>","Experience excellence in car repair and maintenance with Car Clinic. Routine servicing, diagnostics or major repairs, handled with professionalism and precision.",VID("clinic"))}
<section class="light"><div class="wrap">
  <div class="sec-h rvl"><div><span class="eyebrow">What we do</span><h2>Everything your car <em>needs</em></h2></div><p>From oil changes and brake inspections to engine tune-ups and more. Pick a job to book it in.</p></div>
  <div class="svc">{svc_cards(SERVICES)}</div>
</div></section>
<section class="ink2"><div class="wrap">
  <div class="sec-h rvl"><div><span class="eyebrow">Online appointments</span><h2 class="sil">Book a <em>bay</em></h2></div><p>Every appointment starts with a one hour bay booking. Price varies by vehicle, and we quote before any work begins.</p></div>
  <ul class="appt rvl">{"".join(f'<li><a href="contact?type=service&amp;service={quote(a)}"><span><b>{e(a)}</b><small>1 hr · Price varies</small></span><i>→</i></a></li>' for a in APPT)}</ul>
</div></section>
<section class="light"><div class="wrap"><div class="two">
  <div class="rvl"><span class="eyebrow">Why the Car Clinic</span><h2 style="font-size:clamp(36px,4.6vw,58px);font-weight:800;margin:16px 0 22px">Back on the road, <em>fast</em></h2>
    <p>The Car Clinic is your go-to solution for all maintenance and repair needs, whether it’s routine servicing, diagnostics, or major repairs. Our team of skilled technicians uses the latest tools and technology to ensure your car performs at its best.</p>
    <p>We are conveniently located on Greenhills Road (D12 K303). Stop by or give us a call today to schedule an appointment and experience the Car Clinic difference.</p>
    <div class="cta" style="margin-top:22px"><a class="btn btn-red" href="contact?type=service">Book a service <span class="ar">→</span></a><a class="btn btn-out" href="faq">Garage FAQ</a></div></div>
  <div class="pill rvl" style="--d:.1s">
    <article><h3>Our story</h3><p>At Car Clinic, we have been providing top-quality auto repair services to the community for over 10 years. Our experienced technicians are committed to delivering exceptional customer service and ensuring your vehicle is running smoothly.</p></article>
    <article><h3>Our guarantee</h3><p>We offer an outstanding turnaround, making sure you are not without your vehicle for a long period of time. Warranty varies on all parts fitted. OE standard, always.</p></article>
    <article><h3>State-of-the-art equipment</h3><p>Our team uses state-of-the-art equipment to diagnose and fix any issues with your vehicle quickly and efficiently.</p></article>
  </div>
</div></div></section>
{band("Something not <em>right?</em>","Tell us what the car is doing and we will get it booked in.",BOOK,CALL)}
'''

# ---------------- CARS ----------------
cars = f'''
{hero_small("Quality used cars &amp; commercials","Find your <em>dream car</em>","Every car is fully motor checked, serviced and ready to go. Finance available, trade-ins welcome, viewing by appointment.",'<img src="img/hero.webp" alt="">')}
<section class="light"><div class="wrap">
  <div class="tools">
    <input type="search" id="q" placeholder="Search make or model" aria-label="Search cars">
    <div class="seg" role="group" aria-label="Availability"><button data-st="avail" aria-pressed="true">In stock</button><button data-st="sold" aria-pressed="false">Sold</button><button data-st="all" aria-pressed="false">All</button></div>
    <select id="sort" aria-label="Sort cars"><option value="new">Newest listed</option><option value="lo">Price: low to high</option><option value="hi">Price: high to low</option><option value="yr">Year: newest</option></select>
  </div>
  <div class="chips" id="makes" role="group" aria-label="Filter by make"></div>
  <div class="count" id="count" aria-live="polite"></div>
  <div class="grid" id="grid"></div>
</div></section>
{band("Can’t see <em>the one?</em>","Stock changes every week. Tell us what you are after and your budget, and we will keep an eye out.",'<a class="btn btn-red" href="contact?type=viewing">Tell us what you want <span class="ar">→</span></a>','<a class="btn btn-ghost" href="tel:+353852258335">Sales: 085 225 8335</a>')}
'''

car = f'''
<section class="light" style="padding-top:44px"><div class="wrap">
  <div id="detail"></div>
</div></section>
<section class="ink2"><div class="wrap">
  <div class="sec-h rvl"><div><span class="eyebrow">Keep looking</span><h2 class="sil">More from <em>the forecourt</em></h2></div><a class="btn btn-ghost" href="cars">See all cars <span class="ar">→</span></a></div>
  <div class="grid dark-cars hscroll" id="more"></div>
</div></section>
'''

# ---------------- ABOUT ----------------
about = f'''
{hero_small("About us","More than just <em>a dealership</em>","Proudly located on Greenhills Road. Your trusted partner for all your automotive needs.",VID("hero"))}
<section class="light"><div class="wrap"><div class="two">
  <div class="rvl">
    <p>Welcome to Starline Motors, proudly located on Greenhills Road, where we are dedicated to being more than just a car dealership. We’re your trusted partner for all your automotive needs. With a reputation for excellence, we offer an extensive range of high-quality vehicles, catering to every lifestyle and budget. Whether you want to buy cars for daily use or family outings, we have you covered.</p>
    <p>At Starline Motors, customer satisfaction is our top priority. Our experienced and approachable team is here to guide you through every step of the process, from selecting the perfect vehicle to exploring competitive car financing solutions tailored just for you. We pride ourselves on transparency, ensuring you get clear and honest advice without any unnecessary pressure.</p>
    <p>But our commitment doesn’t stop at the sale. We offer comprehensive after-sales support, including servicing, repairs, and maintenance, to keep your vehicle in peak condition. Our modern facilities, equipped with state-of-the-art tools, ensure your car receives the best care possible.</p>
    <p>We don’t just sell cars. We create lasting relationships built on trust, quality, and unmatched service. Experience the excitement of a test drive in Dublin and discover why we are Greenhills Road’s favourite car dealership.</p>
    <div class="cta" style="margin-top:24px"><a class="btn btn-red" href="contact?type=viewing">Book a viewing <span class="ar">→</span></a><a class="btn btn-out" href="cars">View cars</a></div>
  </div>
  <div class="rvl" style="--d:.1s">
    <div class="frame" style="margin-bottom:14px">{VID("clinic")}</div>
    <div class="pill">
      <article><h3>Starline Car Clinic</h3><p>Alongside our vehicles we proudly offer the Car Clinic, a dedicated service within Starline Motors designed to provide expert care for your vehicle.</p></article>
      <article><h3>All under one roof</h3><p>With the Car Clinic on-site, you can trust us not only to help you find your dream car but also to keep it in perfect condition for years to come.</p></article>
    </div>
  </div>
</div></div></section>
<section><div class="wrap">
  <div class="stats rvl">
    <div><b><span data-n="rating">{DATA["rating"]}</span><i>★</i></b><span><span data-n="total">{DATA["total"]}</span> Google reviews</span></div>
    <div><b>10<i>+</i></b><span>Years of auto repair</span></div>
    <div><b>OE</b><span>Standard parts, always</span></div>
    <div><b data-n="stock">16</b><span>Cars in stock now</span></div>
  </div>
</div></section>
{band("Come and <em>see us</em>","We love our customers, so feel free to visit during normal business hours.",'<a class="btn btn-red" href="contact">Get in touch <span class="ar">→</span></a>','<a class="btn btn-ghost" href="services">Car Clinic</a>')}
'''

# ---------------- REVIEWS ----------------
reviews = f'''
{hero_small("See what our clients say","Word of <em>mouth</em>",f'Rated {DATA["rating"]} out of 5 from {DATA["total"]} reviews on Google. Here is what customers say about buying from us and having their cars looked after.','<img src="img/clinic.webp" alt="">')}
<section class="light"><div class="wrap">
  <div class="sec-h rvl"><div class="rate"><b data-n="rating">{DATA["rating"]}</b><div><div class="stars" aria-hidden="true">★★★★★</div><small>from <span data-n="total">{DATA["total"]}</span> reviews on Google</small></div></div>
    <a class="btn btn-dark" href="https://www.google.com/maps/search/?api=1&amp;query=Starline+Motors+Greenhills+Road+Dublin" target="_blank" rel="noopener">See us on Google <span class="ar">→</span></a></div>
  <div class="rvm">{"".join(review(r) for r in DATA["reviews"])}</div>
</div></section>
{band("Join the <em>regulars</em>","Book your car in or come and view one of ours.",BOOK,VIEW)}
'''

# ---------------- FAQ ----------------
faq_page = f'''
{hero_small("Frequently asked questions","Straight <em>answers</em>","Can’t find an answer to your question? Reach us at starlinemotorssales@gmail.com or give us a call.",'<img src="img/clinic.webp" alt="">')}
<section class="light"><div class="wrap"><div class="faq">
  <div class="rvl"><h3>Garage &amp; repairs</h3>{faq(FAQ_GARAGE)}</div>
  <div class="rvl" style="--d:.1s"><h3>Buying a car</h3>{faq(FAQ_SALES)}</div>
</div></div></section>
{band("Still have <em>a question?</em>","Ask us directly. We are always happy to help.",'<a class="btn btn-red" href="contact?type=general">Ask us <span class="ar">→</span></a>',CALL)}
'''

# ---------------- CONTACT ----------------
contact = f'''
{hero_small("Get in touch","Book a service or <em>a test drive</em>","Drop us a line, or better yet, see us in person. We love our customers, so feel free to visit during normal business hours.",'<img src="img/hero.webp" alt="">')}
<section class="light"><div class="wrap">
  <div class="contact">
    <form id="form" novalidate class="rvl">
      <div class="types full" role="radiogroup" aria-label="What do you need?">
        <label><input type="radio" name="type" value="service" checked><span>Service / repair</span></label>
        <label><input type="radio" name="type" value="viewing"><span>Viewing / test drive</span></label>
        <label><input type="radio" name="type" value="general"><span>General enquiry</span></label>
      </div>
      <label>Name<input name="name" autocomplete="name" required></label>
      <label>Phone<input name="phone" type="tel" autocomplete="tel" inputmode="tel" required></label>
      <label class="full">Email<input name="email" type="email" autocomplete="email"></label>
      <label id="l-svc">Service needed<select name="service"><option value="">Choose a service</option>{"".join(f"<option>{e(a)}</option>" for a in APPT)}</select></label>
      <label id="l-reg">Your car (make, model, reg)<input name="vehicle" placeholder="e.g. Ford Focus 191-D-12345"></label>
      <label id="l-car" class="full" hidden>Car you’re interested in<select name="car"></select></label>
      <label class="full">Preferred day<input name="day" type="date"></label>
      <label class="full">Message<textarea name="msg" placeholder="Tell us what’s going on with the car, or what you’re looking for"></textarea></label>
      <div class="send full"><button class="btn btn-wa" type="submit" data-via="wa">{WAI}Send on WhatsApp</button><button class="btn btn-dark" type="submit" data-via="mail">Send by email</button></div>
      <p class="hint full" id="hint">Your message opens in WhatsApp or your email app, ready to send.</p>
    </form>
    <div class="side rvl" style="--d:.1s">
      <div class="box"><h3>CALL US</h3><small>Garage &amp; general</small><a class="big" href="tel:+353857553430">085 755 3430</a><small style="margin-top:18px">Sales team · 9am to 7pm</small><a class="big" href="tel:+353852258335">085 225 8335</a>
        <div class="cta" style="margin-top:22px"><a class="btn btn-wa btn-sm" href="https://wa.me/353857553430" target="_blank" rel="noopener">{WAI}Message us on WhatsApp</a></div></div>
      <div class="box lt"><h3>HOURS</h3><dl><dt>Car Clinic</dt><dd>09:00 – 18:00</dd><dt>Car sales</dt><dd>09:00 – 17:00</dd><dt>Viewings</dt><dd>By appointment</dd></dl></div>
      <div class="box lt"><h3>FIND US</h3><p style="margin-bottom:16px;color:var(--dark)">Starline Motors &amp; Car Clinic<br>Greenhills Road, Kilnamanagh,<br>Dublin 12, D12 K303, Ireland</p><a class="btn btn-dark btn-sm" href="https://www.google.com/maps/dir/?api=1&amp;destination=Starline+Car+Clinic%2C+Greenhills+Rd%2C+Dublin+D12+K303" target="_blank" rel="noopener">Get directions <span class="ar">→</span></a></div>
    </div>
  </div>
  <div class="map rvl"><iframe title="Map showing Starline Motors on Greenhills Road" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=Starline+Car+Clinic,+Greenhills+Rd,+Dublin+D12+K303&amp;z=15&amp;output=embed"></iframe></div>
</div></section>
'''

T = ' | Starline Motors & Car Clinic, Dublin 12'
PAGES = [
 ('index','Starline Motors & Car Clinic | Garage, NCT Repairs & Used Cars, Greenhills Road Dublin 12','Starline Motors and the Car Clinic on Greenhills Road, Dublin 12. Servicing, diagnostics, pre and post NCT, brakes, gearbox, timing belts and quality used cars and commercials.',home,True),
 ('services','Car Clinic: Servicing, Repairs & NCT Prep'+T,'Car servicing, diagnostics, pre and post NCT checks, brakes, suspension, gearbox, timing belts and engine repair at the Car Clinic on Greenhills Road.',services,False),
 ('cars','Used Cars & Commercials for Sale'+T,'Quality used cars and commercials for sale on Greenhills Road, Dublin 12. Fully motor checked and serviced, with warranty. Finance available.',cars,False),
 ('car','Car details'+T,'Photos, spec and price for this car at Starline Motors, Greenhills Road, Dublin 12.',car,False),
 ('about','About Starline Motors'+T,'More than just a car dealership: quality used cars and expert after-sales care at the on-site Car Clinic on Greenhills Road.',about,False),
 ('reviews','Customer Reviews'+T,'Read Google reviews from Starline Motors and Car Clinic customers in Dublin.',reviews,False),
 ('faq','FAQ'+T,'Answers to common questions about servicing, repairs, finance, trade-ins and test drives at Starline Motors.',faq_page,False),
 ('contact','Contact & Booking'+T,'Book a service, viewing or test drive at Starline Motors and the Car Clinic, Greenhills Road, Dublin 12. Call 085 755 3430.',contact,False),
]
for slug, title, desc, body, intro in PAGES:
    out = page('' if slug == 'index' else slug, title, desc, body, intro)
    out = re.sub(r'(\d)\.(\d)00\b', r'\1.\2', out)  # tidy svg numbers
    open(os.path.join(ROOT, slug + '.html'), 'w', encoding='utf8').write(out)
    print('wrote', slug + '.html', len(out))
