# Naismith's Rule Calculator

A free, mobile-friendly hiking time estimator based on Naismith's Rule. Live at [naismithsrule.com](https://naismithsrule.com).

## What it does

Enter a hike's distance, elevation gain, elevation loss, and track difficulty — the calculator returns an estimated hiking time in hours/minutes, total minutes, and decimal hours.

## The formula

The calculator extends the original 1892 Naismith's Rule with two improvements:

- **Descent** — based on Eric Langmuir's 1984 refinement: subtract 10 minutes for every 300 m of descent
- **Track grade** — a five-level scale that adjusts the base walking speed:

| Grade | Description | Speed |
|-------|-------------|-------|
| 1 | Light easy going — vehicle track | 5 km/h |
| 2 | Easy going — well formed bush track | 3 km/h |
| 3 | Medium going | 2 km/h |
| 4 | Bush track, sometimes obscure | 1.5 km/h |
| 5 | Thick bush — heavy going | 0.5 km/h |

Climb adds 1 hour per 600 m of ascent (the original Naismith formula). The speed values for each track grade were calibrated through hundreds of kilometres of real hikes in the Australian bush.

## Files

```
index.html          — Calculator (main page)
about.html          — Background on the formula and its development
privacy-policy.html — Privacy policy
sitemap.xml         — XML sitemap
robots.txt          — Robots directives
site.webmanifest    — PWA manifest
```

## Tech stack

Plain HTML, CSS, and vanilla JavaScript. No build step, no dependencies, no framework.

## iOS app

Also available on the [App Store](https://apps.apple.com/us/app/naismiths-rule-calculator/id6475137430).

## Author

James Robinson — Scout Leader, 1st Blackheath Scout Group, Blue Mountains NSW, Australia.

## License

Copyright © 2023–2025 James Robinson. All rights reserved.
