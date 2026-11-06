# Veterans Day 2026 — Floor to the Door (Nov 5–11) — Facebook / Instagram status

Assets and approved copy: branch `claude/eloquent-darwin-l2mib5`, folder `marketing/veterans-day-2026/` (`captions.md`, `facebook/`).

- Facebook Page "Furniture Distributors": `95489941835`
- Linked Instagram business account: `17841407136660336`

## COVER RESTORE (after Nov 11)

**Previous (usual) Page cover photo ID: `1684697493667601`**

Switch back to it on Nov 12, 2026:

```
POST https://graph.facebook.com/v21.0/95489941835
  cover=1684697493667601
  no_feed_story=true
```

Needs a Page access token with `pages_manage_metadata`. Not yet approved to run automatically.

## Done

| Date | What | ID |
|---|---|---|
| 2026-11-06 | Facebook feed post (portrait graphic, main caption) | `95489941835_1696125465858137` |
| 2026-11-06 | Instagram feed post (same) | `18146379544608912` |
| 2026-11-06 | Veterans Day cover uploaded to the Page as an unpublished photo | `1696127209191296` |

## Blocked

**Switch the Page cover to `1696127209191296`.** Not done yet.
On 2026-11-06 every Graph API request reached Facebook with no access token
(`/me` → code 2500 "An active access token must be used", the cover photo → code 104 "An access token is required",
the Page → code 200 "Provide valid app ID"). The session's stored graph.facebook.com credential
(Authorization header) is not giving Facebook a usable token: it is empty, expired, or saved wrong.
Needed: a fresh, long-lived **Page** access token for Page `95489941835` with `pages_manage_metadata`
(plus `pages_read_engagement`; `pages_manage_posts` too if the reminder posts get approved),
saved as `Authorization: Bearer <token>` for graph.facebook.com.

## Waiting for approval (not done)

- Scheduled reminder post "Still time!", Mon Nov 9, 2026 10:00 AM ET (15:00 UTC), square graphic
- Scheduled reminder post "Last day", Wed Nov 11, 2026 9:00 AM ET (14:00 UTC), square graphic
- Facebook event with the event cover graphic
- Cover switch back to `1684697493667601` on Nov 12

## Owner does these by hand

- Story with a "SHOP THE SALE" link sticker → landing page (`facebook/fb-story-1080x1920.jpg`)
- Website slider banners (`slider-banners/`, four sizes) and landing page (`landing-page/page91-new.html`), entered through the EZ Pro admin.
  The landing page's images already load from `fwaimages.blob.core.windows.net/s36/Banners/VeteransDay2026/` (checked 2026-11-06), so no `src` swap is needed.
