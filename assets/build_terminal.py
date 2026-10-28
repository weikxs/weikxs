"""Generate the neofetch-style terminal card (dark + light) as animated SVGs.

Run: python3 assets/build_terminal.py
"""
from html import escape
from pathlib import Path

from build_banner import THEMES

WIDTH, HEIGHT = 1200, 500
CHROME = 46
CELL, PIXEL = 24, 20
LOGO_X, LOGO_Y = 62, 190
TEXT_X = 380
FIRST_LINE_Y = 128
LINE_HEIGHT = 32
COMMAND = "fetch --me"
TYPE_SECONDS = 0.9
LINE_STEP_SECONDS = 0.16

# (key, value); a None key renders the value as a heading in the pixel colour.
LINES = [
    (None, "weikxs@github"),
    (None, "─────────────"),
    ("role", "toolsmith · 做小而好用的工具"),
    ("langs", "Go · Rust · TypeScript"),
    ("builds", "CLI · desktop · cross-platform apps"),
    ("believes", "local-first · no account · no telemetry"),
    ("motto", "make it useful, then make it fast"),
    ("now", "Supercy · a clipboard that stays on your devices"),
]
# 1 = fur, 2 = eyes (they blink)
CAT = ["10000000001", "11000000011", "11111111111", "11111111111", "11211111211",
       "11111111111", "11111111111", "01111111110", "00111111100"]
SWATCHES = ("pixel", "coffee", "steam", "text", "split_a", "split_b")


def logo(theme: dict) -> str:
    rects = []
    for row, bits in enumerate(CAT):
        for col, bit in enumerate(bits):
            if bit != "0":
                cls, fill = ("eye", theme["coffee"]) if bit == "2" else ("fur", theme["pixel"])
                rects.append(f'<rect class="{cls}" x="{LOGO_X + col * CELL}" y="{LOGO_Y + row * CELL}" '
                             f'width="{PIXEL}" height="{PIXEL}" rx="3" fill="{fill}"/>')
    return "\n    ".join(rects)


def info_lines() -> str:
    out = []
    for i, (key, value) in enumerate(LINES):
        y = FIRST_LINE_Y + (i + 1) * LINE_HEIGHT
        delay = TYPE_SECONDS + i * LINE_STEP_SECONDS
        body = (f'<tspan class="head">{escape(value)}</tspan>' if key is None else
                f'<tspan class="key">{key:<10}</tspan><tspan class="val">{escape(value)}</tspan>')
        out.append(f'<text class="line" x="{TEXT_X}" y="{y}" xml:space="preserve" '
                   f'style="animation-delay:{delay:.2f}s">{body}</text>')
    return "\n  ".join(out)


def swatches(theme: dict) -> str:
    y = FIRST_LINE_Y + (len(LINES) + 1) * LINE_HEIGHT
    delay = TYPE_SECONDS + len(LINES) * LINE_STEP_SECONDS
    blocks = [f'<rect x="{TEXT_X + i * 40}" y="{y}" width="34" height="20" rx="3" fill="{theme[name]}"/>'
              for i, name in enumerate(SWATCHES)]
    return f'<g class="line" style="animation-delay:{delay:.2f}s">{"".join(blocks)}</g>'


def styles(theme: dict) -> str:
    return f"""
      .chrome {{ fill: {theme["grid"]}; }}
      .title {{ fill: {theme["text"]}; font: 500 16px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; opacity: .8; }}
      .prompt, .line {{ font: 500 21px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
      .prompt {{ fill: {theme["pixel"]}; }}
      .cmd {{ fill: {theme["text"]}; }}
      .typed {{ clip-path: inset(0 100% 0 0); animation: type {TYPE_SECONDS}s steps({len(COMMAND)}) forwards; }}
      .line {{ opacity: 0; animation: in .3s ease-out forwards; }}
      .head {{ fill: {theme["pixel"]}; font-weight: 700; }}
      .key {{ fill: {theme["pixel"]}; }}
      .val {{ fill: {theme["text"]}; }}
      .eye {{ transform-box: fill-box; transform-origin: center; animation: wink 5s steps(1) infinite; }}
      .cursor {{ fill: {theme["pixel"]}; animation: blink 1.1s steps(1) infinite; }}
      @keyframes type {{ to {{ clip-path: inset(0 0 0 0); }} }}
      @keyframes in {{ from {{ opacity: 0; transform: translateX(-6px); }} to {{ opacity: 1; transform: none; }} }}
      @keyframes blink {{ 50% {{ opacity: 0; }} }}
      @keyframes wink {{ 0%, 92%, 100% {{ transform: none; }} 94% {{ transform: scaleY(.15); }} }}
      @media (prefers-reduced-motion: reduce) {{
        .typed {{ animation: none; clip-path: none; }}
        .line {{ animation: none; opacity: 1; }}
        .eye {{ animation: none; }}
        .cursor {{ animation: none; }}
      }}"""


def build(theme: dict) -> str:
    dots = "".join(f'<circle cx="{28 + i * 24}" cy="{CHROME // 2}" r="7" fill="{c}"/>'
                   for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840")))
    prompt_y = FIRST_LINE_Y - 10
    cursor_y = FIRST_LINE_Y + (len(LINES) + 2) * LINE_HEIGHT + 4
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-label="weikxs: toolsmith, Go, Rust and TypeScript, local-first tools">
  <defs><style>{styles(theme)}
  </style></defs>
  <rect width="{WIDTH}" height="{HEIGHT}" rx="18" fill="{theme["bg"]}"/>
  <path class="chrome" d="M18 0 H{WIDTH - 18} A18 18 0 0 1 {WIDTH} 18 V{CHROME} H0 V18 A18 18 0 0 1 18 0 Z"/>
  {dots}
  <text class="title" x="{WIDTH // 2}" y="{CHROME // 2 + 6}" text-anchor="middle">weikxs@github: ~</text>
  <text class="prompt" x="{LOGO_X - 20}" y="{prompt_y}">~ $ <tspan class="cmd typed">{COMMAND}</tspan></text>
  <g>
    {logo(theme)}
  </g>
  {info_lines()}
  {swatches(theme)}
  <rect class="cursor" x="{TEXT_X}" y="{cursor_y}" width="13" height="22" rx="2"/>
</svg>
'''


def main() -> None:
    out_dir = Path(__file__).parent
    for name, theme in THEMES.items():
        (out_dir / f"terminal-{name}.svg").write_text(build(theme))


if __name__ == "__main__":
    main()
