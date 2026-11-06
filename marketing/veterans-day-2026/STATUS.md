# Veterans Day 2026 — Floor to the Door (Nov 5–11): Facebook / Instagram status

Assets and approved copy: branch `claude/eloquent-darwin-l2mib5`, folder `marketing/veterans-day-2026/` (`captions.md`, `facebook/`).

## IDs

| What | ID |
|---|---|
| Facebook Page "Furniture Distributors" | 95489941835 |
| Linked Instagram business account | 17841407136660336 |
| **Previous (normal) Page cover photo — restore after Nov 11** | **1684697493667601** |
| Veterans Day cover photo (uploaded unpublished, from `fb-page-cover-1640x624.jpg`) | 1696127209191296 |

## Done

- 2026-11-06 — Facebook main feed post, portrait graphic + main caption: `95489941835_1696125465858137`
- 2026-11-06 — Instagram main post: media `18146379544608912`
- 2026-11-06 — Veterans Day cover uploaded as unpublished photo `1696127209191296`

## Blocked

- **Switch Page cover to Veterans Day image.** Not applied yet.
  Call: `POST /95489941835` with `cover=1696127209191296`, `no_feed_story=true`, `offset_y=50` (centered).
  Last attempt 2026-11-06 08:43 PST failed: `OAuthException` code 190 / subcode 463, "Session has expired on Friday, 06-Nov-26 08:00:00 PST".
  Needs a fresh **Page** access token for Page 95489941835 that includes `pages_manage_metadata` (plus `pages_show_list`, `pages_read_engagement`), saved as the graph.facebook.com credential.

## Waiting for owner approval (not done)

- Scheduled FB reminder "Still time!" — Mon Nov 9, 10:00 AM ET, square graphic
- Scheduled FB reminder "Last day" — Wed Nov 11, 9:00 AM ET, square graphic
- Facebook event with `fb-event-cover-1920x1005.jpg`
- Cover switch-back to `1684697493667601` on Nov 12

## Owner doing manually

- Story with "SHOP THE SALE" link sticker → `facebook/fb-story-1080x1920.jpg`
- Website slider banners (`slider-banners/`, 4 sizes) and landing page (`landing-page/page91-new.html`) via EZ Pro admin.
  The landing page's image `src` URLs already point to `fwaimages.blob.core.windows.net/s36/Banners/VeteransDay2026/` and all three return 200 (checked 2026-11-06), so no path swap is needed.

## Take-down after Nov 11

- Restore Page cover: `POST /95489941835` with `cover=1684697493667601`, `no_feed_story=true`
- Deactivate the slider slide in EZ Pro
