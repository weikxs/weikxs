"""Generate one pixel card per tool (dark + light) as animated SVGs.

Run: python3 assets/build_cards.py
"""
from html import escape
from pathlib import Path

from build_banner import THEMES

WIDTH, HEIGHT = 300, 220
CELL, PIXEL = 8, 6.5
ICON_X, ICON_Y = 26, 26

# 8x8 pixel icons; 1 = pixel colour, 2 = accent colour.
ICONS = {
    "git": ["01100000", "01100110", "01000110", "01000010", "01000100", "01011000", "01100000", "01100000"],
    "key": ["01110000", "10001000", "10201000", "10001000", "01111111", "00010101", "00010101", "00000000"],
    "note": ["00011111", "00010001", "00010001", "00010001", "01110001", "11110111", "11110111", "01100000"],
    "clip": ["00222200", "11222211", "10000001", "10111101", "10000001", "10111001", "10000001", "11111111"],
}
TOOLS = [
    {"slug": "gitpersona", "name": "GitPersona", "icon": "git",
     "en": "Git identity per folder", "zh": "按目录切换 Git 身份"},
    {"slug": "otpkeep", "name": "OTPKeep", "icon": "key",
     "en": "2FA synced on your LAN", "zh": "局域网同步的验证器"},
    {"slug": "timbrebox", "name": "TimbreBox", "icon": "note",
     "en": "Music, no login", "zh": "免登录的音乐播放器"},
    {"slug": "supercy", "name": "Supercy", "icon": "clip",
     "en": "A private clipboard", "zh": "只属于你的剪贴板"},
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
      .name {{ fill: {theme["pixel"]}; font: 700 26px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
      .en {{ fill: {theme["text"]}; font: 500 16px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
      .zh {{ fill: {theme["text"]}; font: 500 16px system-ui, -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif; opacity: .8; }}
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
  <text class="name" x="26" y="132">{tool["name"]}</text>
  <text class="en" x="26" y="166">{escape(tool["en"])}</text>
  <text class="zh" x="26" y="194">{escape(tool["zh"])}</text>
  <text class="go" x="{WIDTH - 44}" y="56">→</text>
</svg>
'''


def main() -> None:
    out_dir = Path(__file__).parent
    for tool in TOOLS:
        for name, theme in THEMES.items():
            (out_dir / f"card-{tool['slug']}-{name}.svg").write_text(build(theme, tool))


if __name__ == "__main__":
    main()
