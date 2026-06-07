"""
log_parser.py — 폰 로그 → 학습 데이터 변환
"""
import re, sys, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from endpoint_classifier import classify

def parse_log(md_text: str) -> list:
    lines = md_text.split('\n')
    out = []
    for line in lines:
        line = line.strip()
        if not line: continue
        if line.startswith('date:') or line.startswith('source:'): continue
        if line == '---': continue
        if re.match(r'\d+ 단계 완료', line): continue
        if line.startswith('#'): continue
        if len(line) < 15: continue  # 너무 짧은 건 제외
        out.append(line)
    return out

# ADB로 폰 로그 가져오기
print("=== 폰 로그 가져오기 ===")
adb_result = os.system("adb pull /sdcard/Download/parksy-logs/ /tmp/phone_logs/ 2>/dev/null")
logs_dir = Path("/tmp/phone_logs")
if not logs_dir.exists() or not list(logs_dir.glob("*.md")):
    print("ADB 실패, WSL 로그로 대체")
    logs_dir = Path.home() / "uploads/log-samples"

# 파싱
all_samples = []
for f in sorted(logs_dir.glob("*.md")):
    text = f.read_text(encoding="utf-8", errors="ignore")
    samples = parse_log(text)
    all_samples.extend(samples)
    print(f"  {f.name}: {len(samples)}개 샘플 추출")

print(f"\n✅ 전체 샘플: {len(all_samples)}개")

# ENDPOINT로 레이블링
labeled = []
from collections import Counter
dist = Counter()
for s in all_samples:
    result = classify(s)
    action = result['action']
    dist[action] += 1
    labeled.append(f"__label__{action} {s[:180]}")

# 분포 출력
print(f"\n레이블 분포: {dict(dist)}")

# 저장
out_path = Path(__file__).parent / "training_data" / "phone_logs_labeled.txt"
out_path.parent.mkdir(parents=True, exist_ok=True)
with open(out_path, "w") as f:
    for l in labeled:
        f.write(l + "\n")
print(f"\n✅ 저장 완료: {out_path} ({len(labeled)}개)")
