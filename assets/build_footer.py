"""Generate the pixel-snake footer (dark + light) as animated SVGs.

The snake crawls across the strip and eats each dot as its head passes it.
Run: python3 assets/build_footer.py
"""
from pathlib import Path

from build_banner import THEMES

WIDTH, HEIGHT = 1200, 120
CELL, PIXEL = 20, 16
ROW_Y = 40
SNAKE_LENGTH = 7
DOT_EVERY = 3
CYCLE_SECONDS = 10
MESSAGE = "thanks for stopping by · 感谢来访"


def snake(theme: dict) -> str:
    body = [f'<rect x="{-i * CELL - CELL}" y="{ROW_Y}" width="{PIXEL}" height="{PIXEL}" rx="3" '
            f'fill="{theme["pixel"]}" opacity="{1 - i * 0.11:.2f}"/>' for i in range(SNAKE_LENGTH)]
    return "\n    ".join(body)


def dot_positions() -> list[int]:
    return list(range(CELL * 2, WIDTH - CELL, CELL * DOT_EVERY))


def eaten_percent(x: int) -> float:
    """Share of the cycle at which the snake's head reaches the dot at x."""
    return 100 * (x + CELL) / (WIDTH + SNAKE_LENGTH * CELL)


def dots(theme: dict) -> str:
    return "\n  ".join(
        f'<rect class="dot" x="{x + 4}" y="{ROW_Y + 4}" width="8" height="8" rx="2" fill="{theme["coffee"]}" '
        f'style="animation-name:eat{i}"/>'
        for i, x in enumerate(dot_positions())
    )


def eat_keyframes() -> str:
    return "\n      ".join(
        f"@keyframes eat{i} {{ 0%, {eaten_percent(x):.1f}% {{ opacity: 1; }} {eaten_percent(x) + 0.1:.1f}%, 100% {{ opacity: 0; }} }}"
        for i, x in enumerate(dot_positions())
    )


def styles(theme: dict) -> str:
    travel = WIDTH + SNAKE_LENGTH * CELL
    return f"""
      .snake {{ animation: crawl {CYCLE_SECONDS}s steps({travel // CELL}) infinite; }}
      .dot {{ animation-duration: {CYCLE_SECONDS}s; animation-timing-function: steps(1); animation-iteration-count: infinite; }}
      .msg {{ fill: {theme["text"]}; font: 500 18px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; letter-spacing: 3px; }}
      .prompt {{ fill: {theme["pixel"]}; }}
      .cursor {{ fill: {theme["pixel"]}; animation: blink 1.1s steps(1) infinite; }}
      @keyframes crawl {{ from {{ transform: translateX(0); }} to {{ transform: translateX({travel}px); }} }}
      {eat_keyframes()}
      @keyframes blink {{ 50% {{ opacity: 0; }} }}
      @media (prefers-reduced-motion: reduce) {{
        .snake, .cursor {{ animation: none; }}
        .dot {{ animation: none; opacity: 1; }}
      }}"""


def build(theme: dict) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-label="A pixel snake eating dots; thanks for stopping by">
  <defs><style>{styles(theme)}
  </style></defs>
  {dots(theme)}
  <g class="snake">
    {snake(theme)}
  </g>
  <text class="msg" x="{WIDTH // 2}" y="{HEIGHT - 18}" text-anchor="middle"><tspan class="prompt">› </tspan>{MESSAGE}</text>
</svg>
'''


def main() -> None:
    out_dir = Path(__file__).parent
    for name, theme in THEMES.items():
        (out_dir / f"footer-{name}.svg").write_text(build(theme))


if __name__ == "__main__":
    main()
