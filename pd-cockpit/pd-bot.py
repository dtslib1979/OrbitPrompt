#!/usr/bin/env python3
"""
pd-bot.py — PD 작전채널 봇

용도: 박씨 + Claude PD + DeepSeek PD 3자 소통
      제작보고서 제출 / 작업 시작-완료 알림 / git push 자동 보고

연결: 기존 텔레그램 봇 토큰 재사용
      chat_id만 새 그룹으로 변경하면 즉시 전환

사용법:
  python3 pd-bot.py send "메시지" [--chat_id CHAT_ID]
  python3 pd-bot.py report start [project] --strategy "전략"
  python3 pd-bot.py report done  [project] --commit HASH
  python3 pd-bot.py report plan  [project] --desc "제작보고서"
"""

import json, os, sys, argparse, subprocess, urllib.request
from pathlib import Path
from datetime import datetime

# ─── 설정 ─────────────────────────────────────────────────────────────────────

CONFIG_PATHS = [
    Path.home() / "dtslib-localpc" / "telegram-bots" / "config.json",
    Path.home() / "dtslib-localpc" / ".env",
]

DEFAULT_CHAT_ID = "6858098283"  # 박씨 개인 chat (PD채널 생성 시 교체)
REPO_NAME = "OrbitPrompt"
PD_NAME = "DeepSeek PD"

# ─── 토큰 로드 ────────────────────────────────────────────────────────────────

def load_token() -> str:
    """config.json 또는 .env에서 봇 토큰 로드"""
    for cfg_path in CONFIG_PATHS:
        if cfg_path.suffix == ".json" and cfg_path.exists():
            with open(cfg_path) as f:
                cfg = json.load(f)
            if cfg.get("bot_token"):
                return cfg["bot_token"]
        elif cfg_path.suffix == ".env" and cfg_path.exists():
            with open(cfg_path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("TG_BOT_TOKEN="):
                        return line.split("=", 1)[1].strip()
    # Fallback: 환경변수
    token = os.environ.get("TG_BOT_TOKEN", "")
    if token:
        return token
    print("❌ 봇 토큰을 찾을 수 없음", file=sys.stderr)
    print("  확인 경로:", [str(p) for p in CONFIG_PATHS], file=sys.stderr)
    sys.exit(1)

# ─── 메시지 전송 ──────────────────────────────────────────────────────────────

def send_message(text: str, chat_id: str = "", parse_mode: str = "Markdown") -> bool:
    """텔레그램 메시지 전송"""
    token = load_token()
    cid = chat_id or DEFAULT_CHAT_ID
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = json.dumps({
        "chat_id": cid,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True,
    }).encode()
    
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        result = json.loads(resp.read())
        if result.get("ok"):
            msg_id = result["result"].get("message_id", "?")
            print(f"✅ 전송 완료 (message_id={msg_id})")
            return True
        else:
            print(f"❌ 전송 실패: {result.get('description', '?')}")
            return False
    except Exception as e:
        print(f"❌ 전송 오류: {e}")
        return False

# ─── 명령어 핸들러 ─────────────────────────────────────────────────────────────

def cmd_send(args):
    """메시지 직접 전송"""
    return send_message(args.text, args.chat_id)

def cmd_report_start(args):
    """작업 시작 보고"""
    text = (
        f"🟡 **{PD_NAME}** · 작업 시작\n"
        f"└ 프로젝트: `{args.project}`\n"
    )
    if args.strategy:
        text += f"└ 전략: {args.strategy}\n"
    text += f"└ 시간: {datetime.now().strftime('%H:%M')}"
    return send_message(text, args.chat_id)

def cmd_report_done(args):
    """작업 완료 보고"""
    text = (
        f"✅ **{PD_NAME}** · 작업 완료\n"
        f"└ 프로젝트: `{args.project}`\n"
    )
    if args.commit:
        text += f"└ 커밋: `{args.commit}`\n"
    text += f"└ 시간: {datetime.now().strftime('%H:%M')}"
    return send_message(text, args.chat_id)

def cmd_report_plan(args):
    """제작보고서 제출"""
    text = (
        f"📋 **{PD_NAME}** · 제작보고서\n"
        f"└ 프로젝트: `{args.project}`\n"
        f"└ 내용:\n{args.desc}\n"
        f"└ 시간: {datetime.now().strftime('%H:%M')}"
    )
    return send_message(text, args.chat_id)

# ─── CLI ──────────────────────────────────────────────────────────────────────

def _add_chat_id(parser):
    parser.add_argument("--chat_id", help="텔레그램 chat_id (기본: 개인채널)")

def main():
    parser = argparse.ArgumentParser(description="PD 작전채널 봇")

    sub = parser.add_subparsers(dest="command")

    # send
    p_send = sub.add_parser("send", help="메시지 전송")
    p_send.add_argument("text", help="전송할 메시지")
    _add_chat_id(p_send)
    p_send.set_defaults(func=cmd_send)

    # report subcommands
    p_report = sub.add_parser("report", help="작업 보고")
    p_report_sub = p_report.add_subparsers(dest="report_type")

    p_start = p_report_sub.add_parser("start", help="작업 시작")
    p_start.add_argument("project", help="프로젝트명")
    p_start.add_argument("--strategy", "-s", help="전략 설명")
    _add_chat_id(p_start)
    p_start.set_defaults(func=cmd_report_start)

    p_done = p_report_sub.add_parser("done", help="작업 완료")
    p_done.add_argument("project", help="프로젝트명")
    p_done.add_argument("--commit", "-c", help="커밋 해시")
    _add_chat_id(p_done)
    p_done.set_defaults(func=cmd_report_done)

    p_plan = p_report_sub.add_parser("plan", help="제작보고서")
    p_plan.add_argument("project", help="프로젝트명")
    p_plan.add_argument("--desc", "-d", required=True, help="보고서 내용")
    _add_chat_id(p_plan)
    p_plan.set_defaults(func=cmd_report_plan)

    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        sys.exit(1)

    args.func(args)

if __name__ == "__main__":
    main()
