"""Gera os cards SVG dos projetos em assets/cards/.

Uso: python scripts/build_cards.py
Para trocar textos, cores ou miniaturas, edite a lista PROJECTS e rode de novo.
"""

import base64
import textwrap
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "cards"
THUMBS = ROOT / "assets" / "thumbs"

W, H = 600, 300
SANS = "'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', Consolas, 'DejaVu Sans Mono', Menlo, monospace"

PROJECTS = [
    {
        "slug": "metacheck",
        "kicker_en": "ANDROID · WEB",
        "desc_en": "Daily, monthly and yearly goals with exact-time local alarms. Published APK plus a web version on GitHub Pages.",
        "kicker": "ANDROID · WEB",
        "title": "MetaCheck",
        "desc": "Metas diárias, mensais e anuais com alarmes locais no horário exato. APK publicado e versão web no GitHub Pages.",
        "tags": ["React 19", "TypeScript", "Capacitor"],
        "accent": "#38bdf8",
        "visual": ("phone", "metacheck.jpg"),
    },
    {
        "slug": "radar-bot",
        "kicker_en": "PYTHON · AUTOMATION",
        "desc_en": "Scans intern and junior dev jobs across several sources, scores them against my skills and only notifies what is new.",
        "kicker": "PYTHON · AUTOMAÇÃO",
        "title": "Telegram Radar Bot",
        "desc": "Varre vagas de estágio e júnior em várias fontes, dá nota pela compatibilidade com o meu perfil e só avisa o que é novo.",
        "tags": ["asyncio", "httpx", "SQLite", "Docker"],
        "accent": "#22c55e",
        "visual": ("telegram", None),
    },
    {
        "slug": "saudecontrol",
        "kicker_en": "WEB · HEALTH",
        "desc_en": "Medication schedule, treatment adherence and vitals. Reads prescriptions from PDF or photos with OCR and imports them.",
        "kicker": "WEB · SAÚDE",
        "title": "SaúdeControl",
        "desc": "Agenda de remédios, adesão ao tratamento e sinais vitais. Lê receitas em PDF ou foto com OCR e importa os remédios.",
        "tags": ["JavaScript", "Express", "Tesseract"],
        "accent": "#0ea5e9",
        "visual": ("browser", "saudecontrol.jpg"),
    },
    {
        "slug": "monitoring",
        "kicker_en": "DEVOPS · OBSERVABILITY",
        "desc_en": "Ping, HTTP, latency and traffic monitoring with alerts. The whole stack starts with one command, dashboard included.",
        "title_en": "Network Monitor",
        "kicker": "DEVOPS · OBSERVABILIDADE",
        "title": "Monitor de Redes",
        "desc": "Ping, HTTP, latência e tráfego da rede com alertas. Stack inteira sobe com um comando e o dashboard já vem pronto.",
        "tags": ["Prometheus", "Grafana", "Docker"],
        "accent": "#f97316",
        "visual": ("browser", "grafana.jpg"),
    },
    {
        "slug": "loja-testes",
        "kicker_en": "PYTHON · QA",
        "desc_en": "Unit tests with mocks and integration tests on a small e-commerce core. CI across three Python versions.",
        "title_en": "Store — Test Suite",
        "kicker": "PYTHON · QA",
        "title": "Loja Virtual — Testes",
        "desc": "Testes unitários com mocks e testes de integração sobre o núcleo de um e-commerce. CI em três versões do Python.",
        "tags": ["pytest", "mocks", "GitHub Actions"],
        "accent": "#a855f7",
        "visual": ("pytest", None),
    },
    {
        "slug": "docker-env",
        "kicker_en": "DOCKER · DX",
        "desc_en": "Multi-language dev environment using Compose profiles. The ./dev CLI detects the project type and starts what it needs.",
        "kicker": "DOCKER · DX",
        "title": "docker-env",
        "desc": "Ambiente de desenvolvimento multi-linguagem com profiles do Compose. A CLI ./dev detecta o tipo do projeto e sobe o necessário.",
        "tags": ["Docker Compose", "Bash", "Nginx"],
        "accent": "#3b82f6",
        "visual": ("dev", None),
    },
]


def img_data(name: str) -> str:
    return "data:image/jpeg;base64," + base64.b64encode((THUMBS / name).read_bytes()).decode()


def visual_phone(img: str, accent: str) -> str:
    return f"""
  <g transform="translate(398 22)">
    <rect width="178" height="256" rx="24" fill="#020617" stroke="{accent}" stroke-opacity=".5"/>
    <clipPath id="scr"><rect x="8" y="8" width="162" height="240" rx="17"/></clipPath>
    <image href="{img_data(img)}" x="8" y="8" width="162" height="240" preserveAspectRatio="xMidYMin slice" clip-path="url(#scr)"/>
  </g>"""


def visual_browser(img: str, accent: str) -> str:
    return f"""
  <g transform="translate(336 58)">
    <rect width="244" height="184" rx="10" fill="#020617" stroke="{accent}" stroke-opacity=".45"/>
    <circle cx="14" cy="13" r="4" fill="#f87171"/><circle cx="27" cy="13" r="4" fill="#fbbf24"/><circle cx="40" cy="13" r="4" fill="#34d399"/>
    <rect x="56" y="7" width="176" height="12" rx="6" fill="#1e293b"/>
    <clipPath id="win"><rect x="1" y="26" width="242" height="157" rx="0"/></clipPath>
    <image href="{img_data(img)}" x="1" y="26" width="242" height="157" preserveAspectRatio="xMidYMin slice" clip-path="url(#win)"/>
  </g>"""


def terminal(lines: list[tuple[str, str]], accent: str, title: str) -> str:
    rows = "".join(
        f'<text x="14" y="{52 + i * 21}" fill="{color}">{escape(text).replace(" ", "\u00a0")}</text>' for i, (text, color) in enumerate(lines)
    )
    return f"""
  <g transform="translate(336 44)">
    <rect width="244" height="212" rx="10" fill="#020617" stroke="{accent}" stroke-opacity=".45"/>
    <circle cx="14" cy="13" r="4" fill="#f87171"/><circle cx="27" cy="13" r="4" fill="#fbbf24"/><circle cx="40" cy="13" r="4" fill="#34d399"/>
    <text x="122" y="17" text-anchor="middle" font-family="{MONO}" font-size="10" fill="#475569">{escape(title)}</text>
    <g font-family="{MONO}" font-size="11.5">{rows}</g>
    <rect class="cursor" x="14" y="{44 + len(lines) * 21}" width="7" height="12" fill="#e2e8f0"/>
  </g>"""


def visual_pytest(accent: str) -> str:
    return terminal(
        [
            ("$ pytest --cov=src", "#e2e8f0"),
            ("test_carrinho_unit ....... ok", "#94a3b8"),
            ("test_estoque_unit ........ ok", "#94a3b8"),
            ("test_pagamento_unit ...... ok", "#94a3b8"),
            ("test_integracao .......... ok", "#94a3b8"),
            ("TOTAL        123    0  100%", "#c084fc"),
            ("===== 28 passed in 0.2s =====", "#4ade80"),
        ],
        accent,
        "pytest",
    )


def visual_dev(accent: str) -> str:
    return terminal(
        [
            ("$ ./dev up", "#e2e8f0"),
            ("▶ projeto detectado: php", "#60a5fa"),
            ("✔ nginx     :80", "#4ade80"),
            ("✔ php83     fpm", "#4ade80"),
            ("✔ mysql     :3306", "#4ade80"),
            ("✔ redis     :6379", "#4ade80"),
            ("ambiente pronto em 4.1s", "#94a3b8"),
        ],
        accent,
        "docker-env",
    )


def visual_telegram(accent: str) -> str:
    return f"""
  <g transform="translate(336 44)" font-family="{SANS}">
    <rect width="244" height="212" rx="12" fill="#0e1621" stroke="{accent}" stroke-opacity=".45"/>
    <rect width="244" height="34" rx="12" fill="#17212b"/><rect y="22" width="244" height="12" fill="#17212b"/>
    <circle cx="20" cy="17" r="10" fill="{accent}"/>
    <text x="36" y="15" font-size="11" font-weight="700" fill="#e2e8f0">Radar Bot</text>
    <text x="36" y="27" font-size="9" fill="#64748b">bot</text>
    <rect x="12" y="46" width="206" height="102" rx="10" fill="#182533"/>
    <text x="22" y="66" font-size="10.5" font-weight="700" fill="#4ade80">● ALTA AFINIDADE · 92%</text>
    <text x="22" y="85" font-size="11" font-weight="600" fill="#e2e8f0">Estágio Backend Python</text>
    <text x="22" y="102" font-size="10" fill="#94a3b8">Acme · Remoto</text>
    <text x="22" y="120" font-size="10" fill="#60a5fa">Python · Docker · SQL</text>
    <text x="22" y="138" font-size="9" fill="#64748b">via backend-br/vagas</text>
    <rect x="12" y="156" width="162" height="46" rx="10" fill="#182533"/>
    <text x="22" y="176" font-size="10.5" font-weight="700" fill="#facc15">● BOA OPORTUNIDADE · 68%</text>
    <text x="22" y="193" font-size="11" fill="#e2e8f0">Dev Júnior React</text>
  </g>"""


def wrap(text: str, width: int = 36, max_lines: int = 4) -> list[str]:
    lines = textwrap.wrap(text, width)
    return lines[:max_lines]


def card(p: dict, lang: str = "pt") -> str:
    if lang == "en":
        p = {**p, "kicker": p["kicker_en"], "desc": p["desc_en"], "title": p.get("title_en", p["title"])}
    accent = p["accent"]
    kind, img = p["visual"]
    visual = {
        "phone": lambda: visual_phone(img, accent),
        "browser": lambda: visual_browser(img, accent),
        "telegram": lambda: visual_telegram(accent),
        "pytest": lambda: visual_pytest(accent),
        "dev": lambda: visual_dev(accent),
    }[kind]()

    desc = "".join(
        f'<text x="28" y="{124 + i * 21}" font-size="14" fill="#94a3b8">{escape(line)}</text>'
        for i, line in enumerate(wrap(p["desc"]))
    )

    tags, x = [], 28
    for t in p["tags"]:
        w = 16 + len(t) * 7
        if x + w > 320:
            break
        tags.append(
            f'<rect x="{x}" y="244" width="{w}" height="24" rx="12" fill="{accent}" fill-opacity=".12" stroke="{accent}" stroke-opacity=".35"/>'
            f'<text x="{x + w / 2}" y="260" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{accent}">{escape(t)}</text>'
        )
        x += w + 8

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(p['title'])}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0b1020"/><stop offset="1" stop-color="#131a2e"/>
    </linearGradient>
    <radialGradient id="glow" cx="1" cy="0" r="1">
      <stop offset="0" stop-color="{accent}" stop-opacity=".22"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="bar" x1="0" x2="1">
      <stop offset="0" stop-color="{accent}"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/>
    </linearGradient>
    <style>
      .cursor {{ animation: blink 1s steps(1) infinite; }}
      @keyframes blink {{ 50% {{ opacity: 0 }} }}
      .shine {{ animation: shine 5s ease-in-out infinite; }}
      @keyframes shine {{ 0%, 100% {{ opacity: .55 }} 50% {{ opacity: 1 }} }}
    </style>
  </defs>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="url(#bg)" stroke="#ffffff" stroke-opacity=".08"/>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="url(#glow)"/>
  <rect class="shine" x="28" y="0" width="180" height="3" rx="1.5" fill="url(#bar)"/>
  <g font-family="{SANS}">
    <text x="28" y="50" font-family="{MONO}" font-size="11" letter-spacing="1.5" fill="{accent}">{escape(p['kicker'])}</text>
    <text x="28" y="88" font-size="26" font-weight="800" fill="#f1f5f9">{escape(p['title'])}</text>
    {desc}
  </g>
  {''.join(tags)}
  {visual}
</svg>
"""


def main() -> None:
    for lang, folder in (("pt", OUT), ("en", OUT / "en")):
        folder.mkdir(parents=True, exist_ok=True)
        for p in PROJECTS:
            (folder / f"{p['slug']}.svg").write_text(card(p, lang), encoding="utf-8")
    print("ok", len(PROJECTS), "cards x 2 idiomas")


if __name__ == "__main__":
    main()
