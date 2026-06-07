#!/usr/bin/env python3
"""
fasttext_labeler.py — parksy-logs 11,695개 자동 레이블링 + fastText 학습

v0.1: 규칙 기반 레이블링 (judge_rules.json 재사용)
v0.2: LLM 보조 레이블링 (모호한 케이스만)
v0.3: fastText 학습 완료

실행: python3 fasttext_labeler.py --label     # 레이블링
      python3 fasttext_labeler.py --train     # 학습
      python3 fasttext_labeler.py --predict   # 분류 테스트
"""
import sys, json, os, glob
from pathlib import Path

# endpoint_classifier 재사용
sys.path.insert(0, str(Path(__file__).parent))
from endpoint_classifier import classify, DECISION_TABLE

HOME = os.environ.get("HOME", "/data/data/com.termux/files/home")
LOGS_DIR = Path(HOME) / "parksy-logs" / "logs"
SESSION_DIR = Path(HOME) / "parksy-logs" / "session-logs"
OUTPUT_DIR = Path(__file__).parent / "training_data"
LABELED_FILE = OUTPUT_DIR / "parksy_logs_labeled.txt"
TRAINED_MODEL = OUTPUT_DIR / "endpoint_model.bin"

def collect_recent_logs(max_files: int = 500) -> list:
    """최신 로그 파일 수집 (11,695개 중 최근 500개)"""
    files = []
    for d in [LOGS_DIR, SESSION_DIR]:
        if d.exists():
            files.extend(sorted(d.glob("**/*.md"), key=os.path.getmtime, reverse=True))
    # 중복 제거 후 최신 N개
    seen = set()
    unique = []
    for f in files:
        if f.name not in seen:
            seen.add(f.name)
            unique.append(f)
    return unique[:max_files]

def auto_label(text: str) -> str:
    """ENDPOINT classify 결과를 fastText 레이블로 변환"""
    result = classify(text)
    # __label__{action}_{route} 형식
    return f"__label__{result['action']} __label__{result['route']} __label__{result['input_type']}"

def generate_training_data(max_files: int = 500):
    """로그 → fastText 학습 데이터 생성 (의존성 0)"""
    logs = collect_recent_logs(max_files)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    count = 0
    with open(LABELED_FILE, "w") as f:
        for log_path in logs:
            try:
                text = log_path.read_text(encoding="utf-8", errors="ignore")[:200]
                if len(text) < 20:
                    continue
                # 한 줄로: 레이블 + 텍스트
                label = auto_label(text)
                line = f"{label} {text.replace(chr(10),' ').strip()[:180]}\n"
                f.write(line)
                count += 1
            except:
                continue
    
    print(f"✅ 학습 데이터 생성 완료: {count}개 샘플")
    print(f"   파일: {LABELED_FILE}")
    return count

def train_fasttext():
    """fastText 학습 실행 (pip install fasttext 필요)"""
    try:
        import fasttext
    except ImportError:
        print("❌ fasttext 미설치: pip install fasttext")
        return False
    
    if not LABELED_FILE.exists() or os.path.getsize(LABELED_FILE) < 1000:
        print("❌ 학습 데이터 없음. 먼저 --label 실행")
        return False
    
    model = fasttext.train_supervised(
        str(LABELED_FILE),
        lr=0.5, epoch=25, wordNgrams=2,
        dim=100, loss='softmax'
    )
    model.save_model(str(TRAINED_MODEL))
    print(f"✅ fastText 학습 완료: {TRAINED_MODEL}")
    print(f"   샘플: {sum(1 for _ in open(LABELED_FILE))}개")
    
    # 테스트
    test_results = model.test(str(LABELED_FILE))
    print(f"   정확도: @1={test_results[1]:.2%} @P={test_results[0]}")
    return True

def predict(text: str):
    """학습된 fastText 모델로 분류"""
    try:
        import fasttext
        model = fasttext.load_model(str(TRAINED_MODEL))
        labels, probs = model.predict(text)
        print(f"🔮 fastText 분류: {labels[0]} (확률: {probs[0]:.2%})")
    except:
        print("❌ 모델 없음. --train 먼저 실행")

if __name__ == "__main__":
    if "--label" in sys.argv:
        max_f = int(sys.argv[sys.argv.index("--label") + 1]) if "--label" in sys.argv and sys.argv.index("--label") + 1 < len(sys.argv) and sys.argv[sys.argv.index("--label") + 1].isdigit() else 500
        generate_training_data(max_f)
    elif "--train" in sys.argv:
        train_fasttext()
    elif "--predict" in sys.argv:
        idx = sys.argv.index("--predict") + 1
        text = sys.argv[idx] if idx < len(sys.argv) else "테스트"
        predict(text)
    else:
        print("사용법:")
        print("  --label [N]   parksy-logs에서 N개 레이블링 (기본 500)")
        print("  --train       fastText 학습")
        print("  --predict '텍스트'  분류 테스트")
        print(f"\n현재 로그 가용: {len(collect_recent_logs(10))}개 파일")
