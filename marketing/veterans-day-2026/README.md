# Veterans Day 2026 — Floor to the Door (Nov 5–11)

Everything built from the event flyer (`source/flyer.pdf`, `source/flyer.png`).

| Folder | What | Where it goes |
|---|---|---|
| `slider-banners/` | 1900×500, 1199×500, 991×500, 768×500 | EZ Pro admin → Page Content → Home Page → Section 1 → Customize and Schedule Slider → Default Section 1 - A → Slide 1 ("Image Large Screen", "Image", "Image Small Screen", "Image Xtra Small Screen") |
| `facebook/` | Square post, portrait post, story, link/ad, event cover, page cover | Facebook / Instagram |
| `captions.md` | Post copy, ad text, story and event text | Facebook / Instagram |
| `landing-page/page91-new.html` | New content for the "Veterans Day" static page (id 91) | EZ Pro admin → Page Content → Edit Existing Page → Veterans Day → Source Code |
| `landing-page/vd26-*.jpg` | Images the landing page uses | Upload to the media manager, then swap the `src` paths in `page91-new.html` for the uploaded URLs |
| `landing-page/page91-2025-backup.html` | The page's previous (2025) content | Restore from here if needed |

Rebuild the images: `python3 source/make_assets.py`, `python3 source/build_facebook.py`, `node source/render_facebook.js`, `python3 source/make_slider_banners.py` (scripts expect the flyer PNG path set at the top of each file).

Take-down after Nov 11: deactivate the slider slide, restore your usual Facebook cover.
