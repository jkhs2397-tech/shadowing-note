#!/usr/bin/env python3
"""sentences.json에서 문장 하나를 골라 퀴즈 알림을 ntfy로 보냅니다.

환경 변수
  NTFY_TOPIC   (필수) 추측하기 어려운 알림 주소 이름
  NTFY_SERVER  (선택) 기본값 https://ntfy.sh
  PAGES_URL    (선택) 앱 주소. 있으면 알림을 눌렀을 때 해당 문제가 열립니다.

사용법
  python3 scripts/quiz_push.py --dry-run   # 보내지 않고 내용만 출력
  python3 scripts/quiz_push.py             # 실제 전송
"""
import argparse
import json
import os
import random
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TYPE_LABEL = {
    "cloze": "빈칸 채우기",
    "ko2en": "한국어 → 영어",
    "meaning": "뜻 맞히기",
    "linking": "연음",
}


def auto_cloze(sentence):
    """quiz 항목이 없는 문장을 위한 자동 빈칸 문제."""
    words = re.findall(r"[A-Za-z']+", sentence["text"])
    long_words = [w for w in words if len(w) >= 4]
    if not long_words:
        return None
    target = random.choice(long_words)
    blanked = re.sub(r"\b%s\b" % re.escape(target), "___", sentence["text"], count=1)
    return {"type": "cloze", "q": blanked, "answer": target, "explanation": ""}


def pick(data):
    sentences = data.get("sentences", [])
    if not sentences:
        sys.exit("sentences.json에 문장이 없습니다.")
    s = random.choice(sentences)
    quizzes = s.get("quiz") or []
    q = random.choice(quizzes) if quizzes else auto_cloze(s)
    if q is None:
        sys.exit("출제할 수 있는 퀴즈가 없습니다: " + s["id"])
    return s, q


def build_message(q):
    lines = [q["q"]]
    if q["type"] == "meaning" and q.get("choices"):
        choices = q["choices"][:]
        random.shuffle(choices)
        lines.append("")
        lines += ["%d) %s" % (i + 1, c) for i, c in enumerate(choices)]
    lines.append("")
    lines.append("눌러서 정답 확인")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    data = json.loads((ROOT / "sentences.json").read_text(encoding="utf-8"))
    s, q = pick(data)

    title = "쉐도잉 퀴즈 · " + TYPE_LABEL.get(q["type"], "퀴즈")
    message = build_message(q)
    pages = os.environ.get("PAGES_URL", "").rstrip("/")
    payload = {
        "topic": os.environ.get("NTFY_TOPIC", "(dry-run)"),
        "title": title,
        "message": message,
        "tags": ["speech_balloon"],
    }
    if pages:
        payload["click"] = "%s/#q=%s" % (pages, s["id"])

    if args.dry_run:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    topic = os.environ.get("NTFY_TOPIC")
    if not topic:
        sys.exit("NTFY_TOPIC 환경 변수가 필요합니다.")
    server = os.environ.get("NTFY_SERVER", "https://ntfy.sh").rstrip("/")
    req = urllib.request.Request(
        server + "/",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as res:
        print("전송 완료:", res.status, s["id"], q["type"])


if __name__ == "__main__":
    main()
