#!/usr/bin/env python3
"""Generate the front page for Sunday 22 November 2026.

The page is drawn for one viewing size that matters: a 1024 square seen at
about 300 pixels across. So the sheet carries one lead and eight briefs, each
headline big enough to read as a thumbnail.

BRIEFS is the only place stories live. The generator counts them for the
masthead, refuses to write a page whose parts disagree, and refuses a headline
or gloss too long for the column it has to fit - so a build that would spill
fails loudly instead of shipping a broken page.
"""

import html
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
DAY = "SUNDAY 22 NOVEMBER 2026"

LEAD = {
    "kicker": "CLIMATE \u00b7 ANTALYA",
    "headline": "COP31 ends with no deal",
    "dek": "Two days into overtime, the longest UN climate summit on record closed "
           "without a pact, after the EU and island states refused a text that never "
           "named fossil fuels.",
    "body": "COP31 President Murat Kurum, Turkey's environment minister, told the "
            "plenary there was no agreement and the decisions were not adopted. "
            "Ireland's Darragh O'Brien, speaking for the EU, called the omission "
            "\u201cunconscionable\u201d. Panama, Vanuatu, Belize and the Marshall Islands "
            "also withheld support. Ant\u00f3nio Guterres said there may be no consensus "
            "in the room, but \u201cno ambiguity in the science\u201d. The file passes to "
            "COP32 in Addis Ababa.",
}

# beat -> (headline, one short line of gloss)
BRIEFS = [
    ("EUROPE", "Drone-hit ship towed away",
     "Sparta II, ablaze off Loviisa, handed to Russian rescuers"),
    ("MIDDLE EAST", "Three tankers hit off Hormuz",
     "Projectiles strike ships leaving the gulf; no casualties"),
    ("NORTH AMERICA", "Democrats seal 258 seats",
     "Largest House majority for either party since 1992"),
    ("AFRICA", "Kenya, DRC to restore envoys",
     "Ruto and Tshisekedi meet in Oyo after a three-year rift"),
    ("SOUTH ASIA", "Pakistan minister in Delhi",
     "First such visit since 2023, at an SCO cultural forum"),
    ("EAST ASIA", "Two probes reach Mercury",
     "Japan-Europe BepiColombo arrives after eight years"),
    ("MARKETS", "Meme coin under $1 at gala",
     "Trump hosts 185 holders as the token keeps sliding"),
    ("SPORT", "Verstappen wins Las Vegas",
     "35 lead changes; Ferrari team-mates collide again"),
]

CREDIT = "Reporting: Reuters, AP, BBC, AFP, Xinhua, Kyodo"

UNIQUE_BEATS = {"EUROPE", "MIDDLE EAST", "NORTH AMERICA", "AFRICA",
                "SOUTH ASIA", "EAST ASIA", "MARKETS", "SPORT"}


def check():
    """Refuse to build a page whose parts contradict each other."""
    beats = [b[0] for b in BRIEFS]
    if len(set(beats)) != len(beats):
        sys.exit("a beat appears twice")
    if set(beats) != UNIQUE_BEATS:
        sys.exit("beats drifted: %s" % sorted(set(beats) ^ UNIQUE_BEATS))
    for beat, headline, gloss in BRIEFS:
        if not headline.strip() or not gloss.strip():
            sys.exit("empty brief in %s" % beat)
        if len(headline) > 28:
            sys.exit("headline too long for the column in %s: %r" % (beat, headline))
        if len(gloss) > 62:
            sys.exit("gloss too long for one line in %s: %d chars" % (beat, len(gloss)))
    if len(BRIEFS) % 2:
        sys.exit("briefs must fill whole rows of the two-column grid")


def glyph(beat):
    """One flat mark per beat, drawn in a single 24x24 box, one stroke weight."""
    paths = {
        "EUROPE": '<path d="M3.5 16c4-6 8 2 12-4"/><path d="M5 20h11"/><circle cx="17.5" cy="7" r="2.5"/>',
        "MIDDLE EAST": '<path d="M12 3.5c4 4 6 7 6 10a6 6 0 0 1-12 0c0-3 2-6 6-10z"/>',
        "NORTH AMERICA": '<rect x="3.5" y="6" width="17" height="12" rx="2"/><path d="M7.5 12h9"/>',
        "AFRICA": '<path d="M8 3.5h8l-1.5 7 3 9.5h-11l3-9.5z"/>',
        "SOUTH ASIA": '<path d="M12 3.5l8.5 15.5h-17z"/><path d="M8 14h8"/>',
        "EAST ASIA": '<circle cx="12" cy="12" r="4"/><ellipse cx="12" cy="12" rx="9" ry="4"/>',
        "MARKETS": '<path d="M3.5 19l6-8 4 4 6.5-9.5"/><path d="M15 5.5h5V11"/>',
        "SPORT": '<circle cx="12" cy="12" r="8.5"/><path d="M12 3.5v17M6 7.5l12 9"/>',
    }
    return ('<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="#e9b95c" '
            'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">%s</svg>'
            % paths[beat])


def build():
    check()
    cards = "\n".join(
        """      <article class="brief">
        <div class="tag">{glyph}<span>{beat}</span></div>
        <h3>{headline}</h3>
        <p>{gloss}</p>
      </article>""".format(
            glyph=glyph(beat),
            beat=html.escape(beat),
            headline=html.escape(headline),
            gloss=html.escape(gloss),
        )
        for beat, headline, gloss in BRIEFS
    )
    tick = '<span class="credit">%s</span>' % html.escape(CREDIT)

    page = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>The World in One Page \u2014 22 November 2026</title>
<style>{css}</style></head>
<body>
<div class="page">
  <header class="masthead">
    <div class="top-rule"></div>
    <h1>THE WORLD IN ONE PAGE</h1>
    <div class="dateline">{day}</div>
    <div class="strap">{n} stories \u00b7 {b} beats \u00b7 one Sunday, everywhere</div>
    <div class="bot-rule"></div>
  </header>

  <section class="lead">
    <div class="lead-text">
      <div class="kicker">{kicker}</div>
      <h2>{headline}</h2>
      <p class="dek">{dek}</p>
      <p class="body">{body}</p>
    </div>
    <figure class="lead-art">
      <svg viewBox="0 0 160 160" fill="none" stroke="#f3efe2" stroke-width="3.4">
        <circle cx="80" cy="80" r="66"/>
        <path d="M14 80h132M80 14c22 21 22 111 0 132M80 14c-22 21-22 111 0 132"/>
        <path d="M28 46c26 16 78 16 104 0M28 114c26-16 78-16 104 0"/>
      </svg>
      <figcaption>Antalya, Türkiye</figcaption>
    </figure>
  </section>

  <section class="grid">
{cards}
  </section>

  <footer class="ticker"><span class="label">22 NOVEMBER 2026</span> {tick}</footer>
</div>
</body></html>
""".format(
        css=(HERE / "poster.css").read_text(),
        day=DAY,
        n=len(BRIEFS) + 1,
        b=len(BRIEFS) + 1,
        kicker=html.escape(LEAD["kicker"]),
        headline=html.escape(LEAD["headline"]),
        dek=html.escape(LEAD["dek"]),
        body=html.escape(LEAD["body"]),
        cards=cards,
        tick=tick,
    )

    out = HERE / "poster.html"
    out.write_text(page)
    print("wrote %s (%d bytes, %d stories, %d beats)"
          % (out, len(page), len(BRIEFS) + 1, len(BRIEFS) + 1))


if __name__ == "__main__":
    build()
