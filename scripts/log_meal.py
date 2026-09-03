#!/usr/bin/env python3
"""Registra um item de refeição em data/nutrition/<data>.json.

Uso:
  python3 scripts/log_meal.py --date 2026-09-03 --slot almoco \
      --name "Frango grelhado (150g)" --kcal 248 --protein 46 --carbs 0 --fat 6 \
      [--time 12:30]

Mantido simples e sem dependências externas de propósito: é chamado por sessões
do Claude Code em lote, uma vez por item, então precisa ser previsível e barato
de auditar no diff do commit.
"""
import argparse
import json
import re
import sys
from pathlib import Path

SLOTS = ["cafe", "lm", "almoco", "lt", "janta", "ceia"]
DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "nutrition"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TIME_RE = re.compile(r"^\d{2}:\d{2}$")


def load_json(path, default):
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    return default


def save_json(path, data):
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--date", required=True, help="YYYY-MM-DD")
    p.add_argument("--slot", required=True, choices=SLOTS)
    p.add_argument("--name", required=True)
    p.add_argument("--kcal", type=int, required=True)
    p.add_argument("--protein", type=int, required=True)
    p.add_argument("--carbs", type=int, required=True)
    p.add_argument("--fat", type=int, required=True)
    p.add_argument("--time", default=None, help="HH:MM opcional")
    args = p.parse_args()

    if not DATE_RE.match(args.date):
        sys.exit(f"--date inválido: {args.date!r} (esperado YYYY-MM-DD)")
    if args.time and not TIME_RE.match(args.time):
        sys.exit(f"--time inválido: {args.time!r} (esperado HH:MM)")
    name = args.name.strip()
    if not name:
        sys.exit("--name não pode ser vazio")
    for label, val in (("--kcal", args.kcal), ("--protein", args.protein), ("--carbs", args.carbs), ("--fat", args.fat)):
        if val < 0:
            sys.exit(f"{label} não pode ser negativo")

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    day_file = DATA_DIR / f"{args.date}.json"
    day = load_json(day_file, {s: [] for s in SLOTS})
    for s in SLOTS:
        day.setdefault(s, [])

    entry = {"n": name, "k": args.kcal, "p": args.protein, "c": args.carbs, "f": args.fat, "src": "chat"}
    if args.time:
        entry["t"] = args.time
    day[args.slot].append(entry)
    save_json(day_file, day)

    index_file = DATA_DIR / "index.json"
    index = load_json(index_file, {"dates": []})
    index.setdefault("dates", [])
    if args.date not in index["dates"]:
        index["dates"].append(args.date)
        index["dates"].sort()
        save_json(index_file, index)

    print(f"OK: '{name}' adicionado em {args.date} / {args.slot} "
          f"({args.kcal} kcal, {args.protein}P {args.carbs}C {args.fat}G)")


if __name__ == "__main__":
    main()
