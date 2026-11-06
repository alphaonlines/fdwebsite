from PIL import Image, ImageDraw, ImageFont
import sys
SRC = '/root/.claude/uploads/40078e5a-7677-5dd0-83dd-2e95124ba178/43d5e5dc-image.png'
src = Image.open(SRC).convert('RGB')
NAVY = src.getpixel((40, 560))
# paint over the torn-paper speck after 'You save even more!'
ImageDraw.Draw(src).rectangle((812, 648, 880, 660), fill=src.getpixel((850, 640)))
print('navy', NAVY)
FI = '/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf'
FR = '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf'
import glob
FI = (glob.glob('/usr/share/fonts/**/LiberationSerif-BoldItalic.ttf', recursive=True) or [FI])[0]
FR = (glob.glob('/usr/share/fonts/**/LiberationSerif-Regular.ttf', recursive=True) or [FR])[0]

def fit_cover(img, w, h, focus=(0.5, 0.5)):
    s = max(w / img.width, h / img.height)
    im = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x = round((im.width - w) * focus[0]); y = round((im.height - h) * focus[1])
    return im.crop((x, y, x + w, y + h))

LIV = src.crop((335, 690, 790, 1030))      # living room photo
BED = src.crop((1125, 690, 1374, 1030))   # bedroom photo

def build(W, H=500, x0=0, x1=1374, y0=0, strip=34, photos='both', lines=1):
    out = Image.new('RGB', (W, H), NAVY)
    stack = src.crop((x0, y0, x1, 659))
    sh = H - strip
    s = sh / stack.height
    sw = round(stack.width * s)
    if sw > W:  # scale to width instead
        s = W / stack.width; sw = W; sh = round(stack.height * s)
    stack = stack.resize((sw, sh), Image.LANCZOS)
    side = W - sw
    if photos == 'both' and side > 0:
        lw = side // 2; rw = side - lw
        out.paste(fit_cover(LIV, lw, sh, (0.55, 0.5)), (0, 0))
        out.paste(stack, (lw, 0))
        out.paste(fit_cover(BED, rw, sh, (0.6, 0.5)), (lw + sw, 0))
        d = ImageDraw.Draw(out)
        for xx in (lw, lw + sw): d.line([(xx, 0), (xx, sh)], fill=(255, 255, 255), width=3)
    elif photos == 'right' and side > 0:
        out.paste(stack, (0, 0))
        out.paste(fit_cover(BED, side, sh, (0.62, 0.5)), (sw, 0))
        ImageDraw.Draw(out).line([(sw, 0), (sw, sh)], fill=(255, 255, 255), width=3)
    else:
        out.paste(stack, ((W - sw) // 2, 0))
    # bottom strip
    d = ImageDraw.Draw(out)
    top = sh
    hgt = H - top
    if lines == 2:
        f1 = ImageFont.truetype(FR, max(14, hgt // 4)); f2 = ImageFont.truetype(FI, max(15, hgt // 3))
        t1 = 'L I V I N G   S P A C E S   F O R   A   B R I G H T E R   T O M O R R O W'
        t2 = '$1,999 minimum purchase required for offer.'
        b1 = d.textbbox((0, 0), t1, font=f1); b2 = d.textbbox((0, 0), t2, font=f2)
        gap = 6; total = (b1[3] - b1[1]) + gap + (b2[3] - b2[1]); y = top + (hgt - total) // 2
        d.text(((W - (b1[2] - b1[0])) // 2 - b1[0], y - b1[1]), t1, font=f1, fill='white')
        y += (b1[3] - b1[1]) + gap
        d.text(((W - (b2[2] - b2[0])) // 2 - b2[0], y - b2[1]), t2, font=f2, fill='white')
    else:
        f = ImageFont.truetype(FI, max(15, round(hgt * 0.55)))
        t = '$1,999 minimum purchase required for offer.'
        b = d.textbbox((0, 0), t, font=f)
        d.text(((W - (b[2] - b[0])) // 2 - b[0], top + (hgt - (b[3] - b[1])) // 2 - b[1]), t, font=f, fill='white')
    return out

specs = {
  1900: dict(photos='both', strip=36),
  1199: dict(x0=50, x1=1324, photos='right', strip=34),
  991:  dict(x0=0, x1=1374, y0=13, photos='none', strip=34),
  768:  dict(x0=70, x1=1304, photos='none', strip=84, lines=2),
}
for W, kw in specs.items():
    im = build(W, **kw)
    assert im.size == (W, 500), im.size
    im.save(f'veterans-day-{W}x500.jpg', quality=90, optimize=True, progressive=True)
    print(W, im.size)
