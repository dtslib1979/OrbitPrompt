#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────────
# FX Engine v3.3 — 일일 시장 모니터링 cron 스크립트
# 등록: crontab -e → 0 9 * * 1-5 /home/dtsli/OrbitPrompt/dollar-system-mcp/mcp/cron_daily_monitor.sh
# 매일 09:00 KST (평일) 실행
# ──────────────────────────────────────────────────────────────────────────────
set -e

BASE="/home/dtsli/OrbitPrompt/dollar-system-mcp"
LOG_DIR="$BASE/logs"
mkdir -p "$LOG_DIR"

LOG_FILE="$LOG_DIR/monitor_$(date +%Y%m%d).log"

echo "=============================================" >> "$LOG_FILE"
echo "FX Monitor — $(date '+%Y-%m-%d %H:%M KST')" >> "$LOG_FILE"
echo "=============================================" >> "$LOG_FILE"

cd "$BASE"

# 1. 시그널 모니터 실행
python3 mcp/auto_signal_monitor.py --json >> "$LOG_FILE" 2>&1
EXIT_CODE=$?

echo "" >> "$LOG_FILE"
echo "Exit code: $EXIT_CODE" >> "$LOG_FILE"
echo "---------------------------------------------" >> "$LOG_FILE"

# 2. signal_log.json git commit (신호가 기록된 경우에만)
if grep -q "Signals recorded" "$LOG_FILE" 2>/dev/null; then
    git add mcp/data/signal_log.json
    git commit -m "feat: auto signal monitor $(date +%Y-%m-%d)" \
        --author="FX Bot <fx-bot@dtslib>" > /dev/null 2>&1 || true
fi

# 3. 텔레그램 알림 (신호가 기록된 경우)
if grep -q '"signals_recorded"' "$LOG_FILE" 2>/dev/null; then
    RECORDED=$(python3 -c "
import json
with open('$LOG_FILE') as f:
    content = f.read()
try:
    data = json.loads(content.split('{\"timestamp\":')[-1].rsplit('}', 1)[0] + '}')
    n = len(data.get('signals_recorded', []))
    print(n)
except: print(0)
" 2>/dev/null)
    if [ "$RECORDED" -gt 0 ]; then
        MSG="📊 FX Engine Monitor: $RECORDED new signal(s) recorded"
        # 텔레그램 발송 (bot token은 환경변수에서)
        TG_TOKEN="${PARKSY_AUDIO_TG_TOKEN:-}"
        TG_CHAT="${FX_TG_CHAT:-6858098283}"
        if [ -n "$TG_TOKEN" ]; then
            curl -s -X POST "https://api.telegram.org/bot${TG_TOKEN}/sendMessage" \
                -d chat_id="$TG_CHAT" \
                -d text="$MSG" > /dev/null 2>&1 || true
        fi
    fi
fi

echo "Done: $(date '+%Y-%m-%d %H:%M KST')" >> "$LOG_FILE"
exit 0
