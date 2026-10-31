#!/usr/bin/env python3
"""sentences.json이 앱과 알림 스크립트에서 읽을 수 있는 형태인지 검사합니다."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = ["id", "text", "translation", "summary"]
QUIZ_TYPES = {"cloze", "ko2en", "meaning", "linking"}


def main():
    errors = []
    try:
        data = json.loads((ROOT / "sentences.json").read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit("JSON 문법 오류: %s (줄 %d, 열 %d)" % (e.msg, e.lineno, e.colno))

    seen = set()
    for i, s in enumerate(data.get("sentences", [])):
        label = s.get("id", "#%d" % i)
        for key in REQUIRED:
            if not s.get(key):
                errors.append("%s: '%s' 항목이 비어 있습니다." % (label, key))
        if s.get("id") in seen:
            errors.append("%s: id가 중복됩니다." % label)
        seen.add(s.get("id"))
        for j, q in enumerate(s.get("quiz", [])):
            where = "%s 퀴즈 %d" % (label, j + 1)
            if q.get("type") not in QUIZ_TYPES:
                errors.append("%s: type은 %s 중 하나여야 합니다." % (where, sorted(QUIZ_TYPES)))
            if not q.get("q") or not q.get("answer"):
                errors.append("%s: q와 answer가 필요합니다." % where)
            if q.get("type") == "meaning" and q.get("choices") and q.get("answer") not in q["choices"]:
                errors.append("%s: answer가 choices 안에 없습니다." % where)

    if errors:
        print("검사 실패:")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print("OK: 문장 %d개" % len(seen))


if __name__ == "__main__":
    main()
