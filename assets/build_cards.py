"""Generate one pixel card per tool (dark + light) as animated SVGs.

Run: python3 assets/build_cards.py
"""
from html import escape
from pathlib import Path

from build_banner import THEMES

WIDTH, HEIGHT = 400, 210
CELL, PIXEL = 10, 8
ICON_X, ICON_Y = 30, 34

# 8x8 pixel icons; 1 = pixel colour, 2 = accent colour.
ICONS = {
    "git": ["01100000", "01100110", "01000110", "01000010", "01000100", "01011000", "01100000", "01100000"],
    "key": ["01110000", "10001000", "10201000", "10001000", "01111111", "00010101", "00010101", "00000000"],
    "note": ["00011111", "00010001", "00010001", "00010001", "01110001", "11110111", "11110111", "01100000"],
}
TOOLS = [
    {"slug": "gitpersona", "name": "GitPersona", "icon": "git",
     "en": "Git identity that follows your folder", "zh": "按目录自动切换 Git 身份"},
    {"slug": "otpkeep", "name": "OTPKeep", "icon": "key",
     "en": "2FA codes, synced only on your LAN", "zh": "只在局域网同步的两步验证器"},
    {"slug": "timbrebox", "name": "TimbreBox", "icon": "note",
     "en": "Music from public sources, no login", "zh": "无需登录的跨平台音乐播放器"},
]


def icon(theme: dict, rows: list[str]) -> str:
    rects = []
    for row, bits in enumerate(rows):
        for col, bit in enumerate(bits):
            if bit != "0":
                fill = theme["pixel"] if bit == "1" else theme["coffee"]
                delay = (row + col) * 0.06
                rects.append(f'<rect class="px" x="{ICON_X + col * CELL}" y="{ICON_Y + row * CELL}" '
                             f'width="{PIXEL}" height="{PIXEL}" rx="1.5" fill="{fill}" '
                             f'style="animation-delay:{delay:.2f}s"/>')
    return "\n    ".join(rects)


def styles(theme: dict) -> str:
    return f"""
      .name {{ fill: {theme["pixel"]}; font: 700 30px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
      .en {{ fill: {theme["text"]}; font: 500 15px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
      .zh {{ fill: {theme["text"]}; font: 500 17px system-ui, -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif; opacity: .8; }}
      .go {{ fill: {theme["pixel"]}; font: 700 18px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
             animation: nudge 1.6s ease-in-out infinite; }}
      .px {{ animation: twinkle 4s ease-in-out infinite; }}
      .edge {{ fill: none; stroke: {theme["pixel"]}; stroke-width: 2; stroke-dasharray: 10 6; opacity: .55;
               animation: march 12s linear infinite; }}
      @keyframes twinkle {{ 0%, 80%, 100% {{ opacity: 1; }} 88% {{ opacity: .35; }} }}
      @keyframes nudge {{ 50% {{ transform: translateX(5px); }} }}
      @keyframes march {{ to {{ stroke-dashoffset: -160; }} }}
      @media (prefers-reduced-motion: reduce) {{ .px, .go, .edge {{ animation: none; }} }}"""


def build(theme: dict, tool: dict) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-label="{tool["name"]}: {escape(tool["en"])}">
  <defs><style>{styles(theme)}
  </style></defs>
  <rect width="{WIDTH}" height="{HEIGHT}" rx="16" fill="{theme["bg"]}"/>
  <rect class="edge" x="6" y="6" width="{WIDTH - 12}" height="{HEIGHT - 12}" rx="12"/>
  <g>
    {icon(theme, ICONS[tool["icon"]])}
  </g>
  <text class="name" x="130" y="80">{tool["name"]}</text>
  <text class="en" x="30" y="140">{escape(tool["en"])}</text>
  <text class="zh" x="30" y="172">{escape(tool["zh"])}</text>
  <text class="go" x="{WIDTH - 44}" y="80">→</text>
</svg>
'''


def main() -> None:
    out_dir = Path(__file__).parent
    for tool in TOOLS:
        for name, theme in THEMES.items():
            (out_dir / f"card-{tool['slug']}-{name}.svg").write_text(build(theme, tool))


if __name__ == "__main__":
    main()
