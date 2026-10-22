"""Generate the pixel-art profile banner (dark + light) as animated SVGs.

Run: python3 assets/build_banner.py
"""
from pathlib import Path

GLYPHS = {
    "W": ["10001", "10001", "10001", "10101", "10101", "10101", "01010"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
}
# 1 = mug outline, 2 = coffee
MUG = ["1111100", "1222110", "1222101", "1222101", "1222110", "1222100", "0111000"]
WORD = "WEIKXS"
TAGLINES = [
    "do the right thing · build the fun thing",
    "make it work → make it right",
    "rm -rf ./complexity",
    "still compiling ideas_",
]

WIDTH, HEIGHT = 1200, 320
CELL, PIXEL = 20, 17
LETTER_GAP = 30
CURSOR_GAP = 34
MUG_GAP = 70
TOP = 74
INTRO_SECONDS = 0.9
TAGLINE_SECONDS = 3.2
GLITCH_CYCLE_SECONDS = 7
STEAM_COLUMNS = (1, 2, 3)

THEMES = {
    "dark": {"bg": "#0b1416", "grid": "#12302a", "pixel": "#43ff88", "coffee": "#c98a4b",
             "steam": "#b9f6ff", "text": "#7fe9ff", "split_a": "#ff2e88", "split_b": "#2ee6ff"},
    "light": {"bg": "#f4fbf6", "grid": "#dcefe2", "pixel": "#0a8a4a", "coffee": "#9a5b25",
              "steam": "#6aa7b8", "text": "#1f6f8b", "split_a": "#e0216f", "split_b": "#1aa3c4"},
}


def word_width() -> int:
    return len(WORD) * 5 * CELL + (len(WORD) - 1) * LETTER_GAP


def layout() -> dict:
    """Horizontal positions so word + cursor + mug are centred as one group."""
    group = word_width() + CURSOR_GAP + CELL + MUG_GAP + len(MUG[0]) * CELL
    left = (WIDTH - group) // 2
    cursor_x = left + word_width() + CURSOR_GAP
    return {"left": left, "cursor_x": cursor_x, "mug_x": cursor_x + CELL + MUG_GAP}


def rect(x: int, y: int, cls: str, delay: float | None = None, size: int = PIXEL) -> str:
    style = f' style="animation-delay:{delay:.2f}s"' if delay is not None else ""
    return f'<rect class="{cls}" x="{x}" y="{y}" width="{size}" height="{size}" rx="2"{style}/>'


def word_rects(left: int) -> list[str]:
    total_cols = len(WORD) * 5
    rects = []
    for li, ch in enumerate(WORD):
        x0 = left + li * (5 * CELL + LETTER_GAP)
        for row, bits in enumerate(GLYPHS[ch]):
            for col, bit in enumerate(bits):
                if bit == "1":
                    delay = INTRO_SECONDS * (li * 5 + col) / total_cols
                    rects.append(rect(x0 + col * CELL, TOP + row * CELL, "p", delay))
    return rects


def mug_rects(x0: int) -> list[str]:
    rects = []
    for row, bits in enumerate(MUG):
        for col, bit in enumerate(bits):
            if bit != "0":
                cls = "p" if bit == "1" else "p coffee"
                rects.append(rect(x0 + col * CELL, TOP + row * CELL, cls, INTRO_SECONDS))
    return rects


def steam_rects(x0: int) -> list[str]:
    size = CELL // 2
    return [
        rect(x0 + col * CELL + (CELL - size) // 2, TOP - size - 6, "steam", INTRO_SECONDS + i * 0.7, size)
        for i, col in enumerate(STEAM_COLUMNS)
    ]


def tagline_texts() -> list[str]:
    cycle = TAGLINE_SECONDS * len(TAGLINES)
    return [
        f'<text class="tag" x="{WIDTH // 2}" y="{HEIGHT - 50}" text-anchor="middle" '
        f'style="animation-duration:{cycle:.1f}s;animation-delay:{INTRO_SECONDS + i * TAGLINE_SECONDS:.1f}s">'
        f'<tspan class="prompt">› </tspan>{line}</text>'
        for i, line in enumerate(TAGLINES)
    ]


def styles(theme: dict) -> str:
    share = 100 / len(TAGLINES)
    return f"""
      .p {{ fill: var(--px, {theme["pixel"]}); opacity: 0; animation: in .35s ease-out forwards; }}
      .p.coffee {{ fill: {theme["coffee"]}; }}
      .cursor {{ fill: {theme["pixel"]}; animation: blink 1.1s steps(1) infinite; }}
      .steam {{ fill: {theme["steam"]}; opacity: 0; animation: steam 2.1s ease-in infinite; }}
      .tag {{ fill: {theme["text"]}; font: 500 22px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
              letter-spacing: 4px; opacity: 0; animation-name: rotate; animation-iteration-count: infinite;
              animation-timing-function: ease-out; }}
      .prompt {{ fill: {theme["pixel"]}; }}
      .split-a, .split-b {{ opacity: 0; animation: glitch {GLITCH_CYCLE_SECONDS}s steps(1) infinite; }}
      .split-a {{ --dx: -5px; --px: {theme["split_a"]}; }}
      .split-b {{ --dx: 5px; --px: {theme["split_b"]}; animation-delay: .05s; }}
      .word {{ animation: jitter {GLITCH_CYCLE_SECONDS}s steps(1) infinite; }}
      @keyframes in {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: none; }} }}
      @keyframes blink {{ 50% {{ opacity: 0; }} }}
      @keyframes steam {{ 0% {{ opacity: 0; transform: translateY(0); }} 30% {{ opacity: .8; }}
                          100% {{ opacity: 0; transform: translateY(-34px); }} }}
      @keyframes rotate {{ 0% {{ opacity: 0; transform: translateY(8px); }} {share * 0.12:.1f}% {{ opacity: 1; transform: none; }}
                           {share * 0.85:.1f}% {{ opacity: 1; transform: none; }} {share:.1f}% {{ opacity: 0; transform: translateY(-8px); }}
                           100% {{ opacity: 0; }} }}
      @keyframes glitch {{ 0%, 90% {{ opacity: 0; transform: none; }} 91% {{ opacity: .75; transform: translateX(var(--dx)); }}
                           93% {{ opacity: .6; transform: translate(calc(var(--dx) * -0.6), 2px); }} 95%, 100% {{ opacity: 0; transform: none; }} }}
      @keyframes jitter {{ 0%, 90% {{ transform: none; }} 91% {{ transform: translateX(2px); }} 93% {{ transform: translateX(-3px); }} 95%, 100% {{ transform: none; }} }}
      @media (prefers-reduced-motion: reduce) {{
        .p {{ animation: none; opacity: 1; }}
        .cursor, .word {{ animation: none; }}
        .steam, .split-a, .split-b {{ display: none; }}
        .tag {{ animation: none; }}
        .tag:first-of-type {{ opacity: 1; }}
      }}"""


def build(theme: dict) -> str:
    pos = layout()
    word = "\n      ".join(word_rects(pos["left"]))
    mug = "\n    ".join(mug_rects(pos["mug_x"]))
    steam = "\n    ".join(steam_rects(pos["mug_x"]))
    tags = "\n  ".join(tagline_texts())
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-label="Weikxs">
  <defs>
    <pattern id="grid" width="{CELL}" height="{CELL}" patternUnits="userSpaceOnUse">
      <path d="M {CELL} 0 L 0 0 0 {CELL}" fill="none" stroke="{theme["grid"]}" stroke-width="1"/>
    </pattern>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="b"/>
      <feFlood flood-color="{theme["pixel"]}" flood-opacity="0.45"/>
      <feComposite in2="b" operator="in"/>
      <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <style>{styles(theme)}
    </style>
    <g id="word">
      {word}
    </g>
  </defs>
  <rect width="{WIDTH}" height="{HEIGHT}" rx="18" fill="{theme["bg"]}"/>
  <rect width="{WIDTH}" height="{HEIGHT}" rx="18" fill="url(#grid)" opacity="0.6"/>
  <use class="split-a" href="#word" xlink:href="#word"/>
  <use class="split-b" href="#word" xlink:href="#word"/>
  <g filter="url(#glow)">
    <use class="word" href="#word" xlink:href="#word"/>
    <rect class="cursor" x="{pos["cursor_x"]}" y="{TOP + 6 * CELL}" width="{CELL}" height="{PIXEL}" rx="2"/>
    {mug}
    {steam}
  </g>
  {tags}
</svg>
'''


def main() -> None:
    out_dir = Path(__file__).parent
    for name, theme in THEMES.items():
        (out_dir / f"banner-{name}.svg").write_text(build(theme))


if __name__ == "__main__":
    main()
