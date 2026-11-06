from PIL import Image, ImageFilter, ImageDraw
SRC = '/root/.claude/uploads/40078e5a-7677-5dd0-83dd-2e95124ba178/43d5e5dc-image.png'
src = Image.open(SRC).convert('RGB')
A = 'assets/'
# title art (flag, Honor/Appreciate/Serve, Veterans Day, Floor to the Door, dates ribbon)
title = src.crop((0, 0, 1374, 478)); title.save(A + 'title-full.png')
src.crop((150, 0, 1230, 478)).save(A + 'title-1080.png')
# soft flag/sky background for extending the title art
bg = title.resize((687, 239)).filter(ImageFilter.GaussianBlur(10)).resize((1374, 478), Image.LANCZOS)
bg.save(A + 'title-blur.jpg', quality=88)
# showroom photos incl. their script labels
src.crop((0, 672, 790, 1035)).save(A + 'living.jpg', quality=92)
src.crop((776, 672, 1374, 1035)).save(A + 'bedroom.jpg', quality=92)
# icons -> white on transparent
def icon(box, name):
    im = src.crop(box).convert('L')
    navy_l = 45
    a = im.point(lambda v: 0 if v <= navy_l + 25 else min(255, int((v - navy_l - 25) * 255 / (255 - navy_l - 25) * 1.15)))
    out = Image.new('RGBA', im.size, (255, 255, 255, 0)); out.putalpha(a)
    out.save(A + name)
icon((186, 490, 296, 562), 'icon-sofa.png')
icon((646, 490, 720, 562), 'icon-tag.png')
icon((1067, 490, 1190, 562), 'icon-truck.png')
print('ok')
