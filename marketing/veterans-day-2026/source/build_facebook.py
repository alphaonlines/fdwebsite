# Generates one HTML file per Facebook format; render.js screenshots them at exact size.
NAVY = '#002d58'; RED = '#d0202e'; CREAM = '#fff6e0'
FINE = '$1,999 minimum purchase required for offer.'
TAG = 'LIVING SPACES FOR A BRIGHTER TOMORROW'
URL = 'FurnitureDistributors.net'
BENEFITS = [
  ('icon-sofa.png', 'FLOOR TO<br>THE DOOR', 'The price on the floor<br>is the price to your door!'),
  ('icon-tag.png', 'WE PAY YOUR<br>SALES TAX!', 'You save even more!'),
  ('icon-truck.png', 'WE PAY YOUR<br>DELIVERY!', 'Get it home for free!'),
]
BASE_CSS = f"""
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{background:{NAVY};overflow:hidden}}
body{{font-family:'Liberation Serif','Times New Roman',serif;color:#fff;position:relative}}
.abs{{position:absolute}}
.bg{{background:url(assets/title-blur.jpg) center/cover}}
.navy{{background:radial-gradient(ellipse at 50% 30%,#0a3d72 0%,{NAVY} 70%)}}
img.cover{{width:100%;height:100%;object-fit:cover;display:block}}
.ben{{display:flex;align-items:stretch;justify-content:center}}
.ben .b{{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}}
.ben .sep{{display:flex;flex-direction:column;align-items:center;justify-content:center}}
.ben .sep i{{flex:1;width:2px;background:rgba(255,255,255,.75)}}
.ben .sep b{{color:{RED};line-height:1}}
.h{{font-weight:400;letter-spacing:.01em;line-height:1.02;text-transform:uppercase}}
.s{{font-style:italic;line-height:1.15;opacity:.97}}
.fine{{font-style:italic;font-weight:700;text-align:center}}
.tag{{letter-spacing:.35em;text-align:center}}
.pill{{display:inline-block;background:{RED};color:#fff;font-weight:700;border-radius:999px;letter-spacing:.04em}}
.rule{{height:4px;background:linear-gradient(90deg,transparent,#fff 15%,#fff 85%,transparent)}}
img.feather{{-webkit-mask-image:linear-gradient(90deg,transparent 0,#000 110px,#000 calc(100% - 110px),transparent 100%);mask-image:linear-gradient(90deg,transparent 0,#000 110px,#000 calc(100% - 110px),transparent 100%)}}
.frame{{border:5px solid #fff;box-shadow:0 6px 18px rgba(0,0,0,.45);overflow:hidden;background:#000}}
"""
def benefits(icon_h, h_px, s_px, sep_star, gap=10, vertical=False):
    parts = []
    for i, (ic, h, s) in enumerate(BENEFITS):
        if i and not vertical:
            parts.append(f'<div class="sep" style="width:{sep_star*2}px"><i></i><b style="font-size:{sep_star}px">★</b><i></i></div>')
        if vertical:
            parts.append(f'<div style="display:flex;align-items:center;gap:34px;padding:0 70px"><div style="width:{icon_h*1.7}px;text-align:center"><img src="assets/{ic}" style="height:{icon_h}px"></div>'
                         f'<div><div class="h" style="font-size:{h_px}px">{h.replace("<br>"," ")}</div><div class="s" style="font-size:{s_px}px;margin-top:6px">{s.replace("<br>"," ")}</div></div></div>')
        else:
            parts.append(f'<div class="b"><img src="assets/{ic}" style="height:{icon_h}px;margin-bottom:{gap}px"><div class="h" style="font-size:{h_px}px">{h}</div><div class="s" style="font-size:{s_px}px;margin-top:{gap*0.6}px">{s}</div></div>')
    return ''.join(parts)

def page(w, h, body):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}</style></head><body style="width:{w}px;height:{h}px">{body}</body></html>'

F = {}
# 1) Square feed post 1080x1080
F['fb-post-square-1080x1080'] = (1080, 1080, f"""
<div class="abs bg" style="left:0;top:0;width:1080px;height:478px"></div>
<img class="abs" src="assets/title-1080.png" style="left:0;top:0;width:1080px">
<div class="abs navy ben" style="left:0;top:478px;width:1080px;height:250px;padding:18px 30px">{benefits(54,36,25,30)}</div>
<div class="abs frame" style="left:24px;top:728px;width:510px;height:240px;transform:rotate(-1.2deg)"><img class="cover" src="assets/living.jpg" style="object-position:0% 100%"></div>
<div class="abs frame" style="left:546px;top:728px;width:510px;height:240px;transform:rotate(1.2deg)"><img class="cover" src="assets/bedroom.jpg" style="object-position:0% 100%"></div>
<div class="abs" style="left:0;top:985px;width:1080px">
  <div class="tag" style="font-size:22px">{TAG}</div>
  <div class="fine" style="font-size:30px;margin-top:10px">{FINE}</div>
</div>""")
# 2) Portrait feed post 1080x1350 (4:5)
F['fb-post-portrait-1080x1350'] = (1080, 1350, f"""
<div class="abs bg" style="left:0;top:0;width:1080px;height:478px"></div>
<img class="abs" src="assets/title-1080.png" style="left:0;top:0;width:1080px">
<div class="abs navy ben" style="left:0;top:478px;width:1080px;height:290px;padding:26px 30px">{benefits(64,40,28,34,12)}</div>
<div class="abs frame" style="left:26px;top:775px;width:508px;height:400px;transform:rotate(-1.2deg)"><img class="cover" src="assets/living.jpg" style="object-position:0% 50%"></div>
<div class="abs frame" style="left:546px;top:775px;width:508px;height:400px;transform:rotate(1.2deg)"><img class="cover" src="assets/bedroom.jpg" style="object-position:0% 50%"></div>
<div class="abs" style="left:0;top:1196px;width:1080px;text-align:center">
  <div class="tag" style="font-size:24px">{TAG}</div>
  <div class="fine" style="font-size:32px;margin-top:10px">{FINE}</div>
  <div style="margin-top:16px"><span class="pill" style="font-size:30px;padding:10px 38px">Shop the sale · {URL}</span></div>
</div>""")
# 3) Story 1080x1920 (keeps key text out of the top ~230px and bottom ~250px app overlays)
F['fb-story-1080x1920'] = (1080, 1920, f"""
<div class="abs navy" style="left:0;top:0;width:1080px;height:1920px"></div>
<div class="abs" style="left:0;top:228px;width:1080px;height:6px;background:{RED}"></div>
<img class="abs" src="assets/title-1080.png" style="left:0;top:234px;width:1080px">
<div class="abs" style="left:0;top:770px;width:1080px;display:flex;flex-direction:column;gap:44px">{benefits(78,50,34,0,vertical=True)}</div>
<div class="abs frame" style="left:36px;top:1250px;width:496px;height:320px;transform:rotate(-1.5deg)"><img class="cover" src="assets/living.jpg" style="object-position:0% 100%"></div>
<div class="abs frame" style="left:548px;top:1250px;width:496px;height:320px;transform:rotate(1.5deg)"><img class="cover" src="assets/bedroom.jpg" style="object-position:0% 100%"></div>
<div class="abs" style="left:0;top:1600px;width:1080px;text-align:center">
  <div class="fine" style="font-size:34px">{FINE}</div>
  <div style="margin-top:22px"><span class="pill" style="font-size:32px;padding:12px 44px">Shop the sale · {URL}</span></div>
</div>""")
# 4) Link / ad image 1200x628
F['fb-link-ad-1200x628'] = (1200, 628, f"""
<img class="abs" src="assets/title-full.png" style="left:0;top:-6px;width:1200px">
<div class="abs navy ben" style="left:0;top:412px;width:1200px;height:176px;padding:12px 40px">{benefits(40,27,20,22,6)}</div>
<div class="abs" style="left:0;top:588px;width:1200px;height:40px;background:{NAVY};display:flex;align-items:center;justify-content:center"><div class="fine" style="font-size:22px">{FINE}</div></div>""")
# 5) Event cover 1920x1005
F['fb-event-cover-1920x1005'] = (1920, 1005, f"""
<div class="abs bg" style="left:0;top:0;width:1920px;height:526px"></div>
<img class="abs feather" src="assets/title-full.png" style="left:204px;top:0;width:1512px">
<div class="abs navy ben" style="left:0;top:526px;width:1920px;height:300px;padding:26px 260px">{benefits(70,44,31,36,12)}</div>
<div class="abs" style="left:0;top:842px;width:1920px;text-align:center">
  <div class="rule" style="width:1200px;margin:0 auto 18px"></div>
  <div class="tag" style="font-size:28px">{TAG}</div>
  <div class="fine" style="font-size:36px;margin-top:12px">{FINE}</div>
</div>""")
# 6) Page cover 1640x624 (key content kept in the center ~1100px that phones show)
F['fb-page-cover-1640x624'] = (1640, 624, f"""
<div class="abs bg" style="left:0;top:0;width:1640px;height:500px"></div>
<img class="abs feather" src="assets/title-full.png" style="left:127px;top:0;width:1386px">
<div class="abs navy" style="left:0;top:482px;width:1640px;height:142px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px">
  <div class="h" style="font-size:34px">Floor to the Door <b style="color:{RED}">★</b> We Pay Your Sales Tax <b style="color:{RED}">★</b> We Pay Your Delivery</div>
  <div class="fine" style="font-size:24px">{FINE}</div>
</div>""")

import json
for name, (w, h, body) in F.items():
    open(f'{name}.html', 'w').write(page(w, h, body))
json.dump({k: [v[0], v[1]] for k, v in F.items()}, open('formats.json', 'w'))
print('\n'.join(F))
