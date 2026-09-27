"""Gera dist/stats.svg e dist/languages.svg a partir da API GraphQL do GitHub.

Roda no workflow (GITHUB_TOKEN no ambiente). Localmente: GITHUB_TOKEN=$(gh auth token) python scripts/build_stats.py
"""

import json
import os
import sys
import urllib.request
from html import escape
from pathlib import Path

USER = os.getenv("STATS_USER", "MvitorLS")
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "dist")

# Relatórios em LaTeX e código gerado pelo Capacitor (projetos Android/iOS) distorcem a barra
IGNORED_LANGS = {"TeX", "Batchfile", "Swift", "Java", "Ruby", "Dockerfile", "Makefile"}

SANS = "'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', Consolas, 'DejaVu Sans Mono', Menlo, monospace"

QUERY = """
query($login: String!) {
  user(login: $login) {
    createdAt
    followers { totalCount }
    contributionsCollection {
      contributionCalendar { totalContributions }
      totalCommitContributions
      totalPullRequestContributions
    }
    repositories(ownerAffiliations: OWNER, isFork: false, first: 100, privacy: PUBLIC) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 10) { edges { size node { name color } } }
      }
    }
  }
}
"""


def fetch() -> dict:
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = json.load(resp)
    if "errors" in body:
        raise SystemExit(body["errors"])
    return body["data"]["user"]


def frame(width: int, height: int, title: str, body: str, accent: str = "#38bdf8") -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1020"/><stop offset="1" stop-color="#131a2e"/></linearGradient>
    <radialGradient id="glow" cx="1" cy="0" r="1"><stop offset="0" stop-color="{accent}" stop-opacity=".18"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>
    <style>
      .grow {{ transform-box: fill-box; transform-origin: left; animation: grow 1.2s ease-out both; }}
      @keyframes grow {{ from {{ transform: scaleX(0) }} }}
      .up {{ animation: up .8s ease-out both; }}
      @keyframes up {{ from {{ opacity: 0; transform: translateY(6px) }} }}
    </style>
  </defs>
  <rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" rx="16" fill="url(#bg)" stroke="#ffffff" stroke-opacity=".08"/>
  <rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" rx="16" fill="url(#glow)"/>
  <text x="28" y="44" font-family="{MONO}" font-size="12" letter-spacing="1.5" fill="{accent}">{escape(title)}</text>
  {body}
</svg>
"""


LABELS = {
    "pt": ("Contribuições (12 meses)", "Commits", "Repositórios públicos", "Estrelas recebidas", "LINGUAGENS MAIS USADAS"),
    "en": ("Contributions (12 months)", "Commits", "Public repositories", "Stars earned", "MOST USED LANGUAGES"),
}


def stats_svg(u: dict, lang: str = "pt") -> str:
    labels = LABELS[lang]
    cc = u["contributionsCollection"]
    items = [
        (labels[0], cc["contributionCalendar"]["totalContributions"], "#38bdf8"),
        (labels[1], cc["totalCommitContributions"], "#a78bfa"),
        (labels[2], u["repositories"]["totalCount"], "#34d399"),
        (labels[3], sum(r["stargazerCount"] for r in u["repositories"]["nodes"]), "#fbbf24"),
    ]
    cells = []
    for i, (label, value, color) in enumerate(items):
        x, y = 28 + (i % 2) * 272, 78 + (i // 2) * 78
        cells.append(
            f'<g class="up" style="animation-delay:{i * 0.12:.2f}s">'
            f'<rect x="{x}" y="{y}" width="256" height="64" rx="12" fill="#ffffff" fill-opacity=".03" stroke="#ffffff" stroke-opacity=".06"/>'
            f'<rect x="{x}" y="{y + 16}" width="3" height="32" rx="1.5" fill="{color}"/>'
            f'<text x="{x + 18}" y="{y + 34}" font-family="{SANS}" font-size="26" font-weight="800" fill="#f1f5f9">{value}</text>'
            f'<text x="{x + 18}" y="{y + 52}" font-family="{SANS}" font-size="12" fill="#94a3b8">{escape(label)}</text>'
            "</g>"
        )
    return frame(584, 244, "GITHUB STATS", "".join(cells))


def languages_svg(u: dict, lang: str = "pt", top: int = 6) -> str:
    totals: dict[str, list] = {}
    for repo in u["repositories"]["nodes"]:
        for edge in repo["languages"]["edges"]:
            name = edge["node"]["name"]
            if name in IGNORED_LANGS:
                continue
            entry = totals.setdefault(name, [0, edge["node"]["color"] or "#94a3b8"])
            entry[0] += edge["size"]
    ranked = sorted(totals.items(), key=lambda kv: -kv[1][0])[:top]
    total = sum(size for _, (size, _) in ranked) or 1

    bar, x = [], 28.0
    for name, (size, color) in ranked:
        w = 528 * size / total
        bar.append(f'<rect class="grow" x="{x:.1f}" y="70" width="{max(w - 2, 1):.1f}" height="12" rx="3" fill="{color}"/>')
        x += w

    legend = []
    for i, (name, (size, color)) in enumerate(ranked):
        lx, ly = 28 + (i % 2) * 272, 118 + (i // 2) * 38
        legend.append(
            f'<g class="up" style="animation-delay:{0.3 + i * 0.1:.2f}s">'
            f'<circle cx="{lx + 6}" cy="{ly - 4}" r="6" fill="{color}"/>'
            f'<text x="{lx + 20}" y="{ly}" font-family="{SANS}" font-size="14" font-weight="600" fill="#e2e8f0">{escape(name)}</text>'
            f'<text x="{lx + 244}" y="{ly}" text-anchor="end" font-family="{MONO}" font-size="12" fill="#94a3b8">{100 * size / total:.1f}%</text>'
            "</g>"
        )
    return frame(584, 244, LABELS[lang][4], "".join(bar) + "".join(legend), accent="#a78bfa")


def main() -> None:
    user = fetch()
    OUT.mkdir(parents=True, exist_ok=True)
    for lang, suffix in (("pt", ""), ("en", "-en")):
        (OUT / f"stats{suffix}.svg").write_text(stats_svg(user, lang), encoding="utf-8")
        (OUT / f"languages{suffix}.svg").write_text(languages_svg(user, lang), encoding="utf-8")
    print("stats ok")


if __name__ == "__main__":
    main()
