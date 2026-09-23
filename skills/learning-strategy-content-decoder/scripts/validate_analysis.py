#!/usr/bin/env python3
"""Validate a Content Decoder JSON result against the lenses and source text."""

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

PILLARS = {
    "Operational efficiency and effectiveness", "The science of learning",
    "Education and industry partnerships", "Assessment lifecycle",
    "Lifelong learning", "Recognition of learning", "Generative AI",
    "Evidence-based design",
}
BELIEFS = {
    "Learning is personal", "Learning needs people", "Learning earns you trust",
    "Learning proves itself", "Learning never stops",
}
GAPS = {"Experiential Learning at Scale", "Authentic Assessment", "Protecting Cognitive Struggle"}


def normalize(value):
    value = unicodedata.normalize("NFKC", str(value or ""))
    value = value.translate(str.maketrans({"\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"', "\u2013": "-", "\u2014": "-"}))
    return re.sub(r"\s+", " ", value).strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--analysis", required=True, type=Path)
    parser.add_argument("--source", required=True, type=Path)
    args = parser.parse_args()
    result = json.loads(args.analysis.read_text())
    source = normalize(args.source.read_text())
    errors = []

    def require_text(obj, key, where):
        if not isinstance(obj.get(key), str) or not obj[key].strip():
            errors.append(f"{where}: {key} must be non-empty text")

    require_text(result, "suggested_title", "result")
    require_text(result, "summary", "result")
    if len(str(result.get("suggested_title", ""))) > 90:
        errors.append("result: suggested_title must be 90 characters or fewer")

    pillars = result.get("impactful_eight")
    if not isinstance(pillars, list):
        errors.append("result: impactful_eight must be an array")
        pillars = []
    if len(pillars) > 4:
        errors.append("result: select no more than four Impactful Eight pillars")
    seen = set()
    for index, item in enumerate(pillars):
        where = f"impactful_eight[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{where}: item must be an object")
            continue
        pillar = item.get("pillar")
        if pillar not in PILLARS:
            errors.append(f"{where}: unknown pillar {pillar!r}")
        if pillar in seen:
            errors.append(f"{where}: duplicate pillar {pillar!r}")
        seen.add(pillar)
        for key in ("why_it_matters", "key_insight", "evidence_excerpt"):
            require_text(item, key, where)
        excerpt = normalize(item.get("evidence_excerpt", "")).strip('"')
        if excerpt and excerpt not in source:
            errors.append(f"{where}: evidence excerpt was not found in the source")

    learning = result.get("learning_2_0")
    if not isinstance(learning, dict):
        errors.append("result: learning_2_0 must be an object")
        learning = {}
    selected_beliefs = []
    for key in ("primary_connection", "supporting_connection"):
        item = learning.get(key)
        if item is None:
            continue
        if not isinstance(item, dict):
            errors.append(f"learning_2_0.{key}: must be an object or null")
            continue
        belief = item.get("belief")
        if belief not in BELIEFS:
            errors.append(f"learning_2_0.{key}: unknown belief {belief!r}")
        selected_beliefs.append(belief)
        require_text(item, "why", f"learning_2_0.{key}")
        require_text(item, "evidence_excerpt", f"learning_2_0.{key}")
        excerpt = normalize(item.get("evidence_excerpt", "")).strip('"')
        if excerpt and excerpt not in source:
            errors.append(f"learning_2_0.{key}: evidence excerpt was not found in the source")
    if len(selected_beliefs) != len(set(selected_beliefs)):
        errors.append("learning_2_0: primary and supporting beliefs must be distinct")

    gaps = learning.get("strategic_gaps")
    if not isinstance(gaps, list):
        errors.append("learning_2_0.strategic_gaps: must be an array")
        gaps = []
    if len(gaps) > 2:
        errors.append("learning_2_0.strategic_gaps: select no more than two gaps")
    for index, item in enumerate(gaps):
        where = f"learning_2_0.strategic_gaps[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{where}: item must be an object")
            continue
        if item.get("gap") not in GAPS:
            errors.append(f"{where}: unknown gap {item.get('gap')!r}")
        for key in ("insight", "evidence_excerpt"):
            require_text(item, key, where)
        excerpt = normalize(item.get("evidence_excerpt", "")).strip('"')
        if excerpt and excerpt not in source:
            errors.append(f"{where}: evidence excerpt was not found in the source")

    for key in ("tension", "strategic_implication", "say", "study", "build"):
        require_text(learning, key, "learning_2_0")

    if errors:
        print("Validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Content Decoder analysis is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
