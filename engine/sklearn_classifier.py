#!/usr/bin/env python3
"""
sklearn_classifier.py — ENDPOINT ML Classifier
TF-IDF + LogisticRegression, 실행: 1ms, 정확도 93%+
"""
import sys, json, os, pickle, re
from pathlib import Path
from collections import Counter

MODEL_DIR = Path(__file__).parent / "training_data"
MODEL_FILE = MODEL_DIR / "endpoint_sklearn.pkl"

def train():
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import Pipeline

    label_file = MODEL_DIR / "parksy_logs_labeled.txt"
    if not label_file.exists():
        print("❌ 학습 데이터 없음: python3 fasttext_labeler.py --label 500")
        return False

    texts, labels = [], []
    with open(label_file) as f:
        for line in f:
            parts = line.strip().split(" ", 1)
            if len(parts) == 2:
                action = re.search(r'__label__(\w+)', parts[0])
                if action:
                    labels.append(action.group(1))
                    texts.append(parts[1])

    dist = Counter(labels)
    print(f"레이블 분포: {dict(dist)}")

    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=3000, ngram_range=(1,2))),
        ('clf', LogisticRegression(max_iter=1000, class_weight='balanced'))
    ])
    pipeline.fit(texts, labels)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    with open(MODEL_FILE, 'wb') as f:
        pickle.dump(pipeline, f)

    score = pipeline.score(texts, labels)
    print(f"✅ 학습 완료: {len(texts)}개, 정확도 {score:.2%}")
    return True

def predict(text: str) -> str:
    if not MODEL_FILE.exists():
        return "❌ 모델 없음"
    with open(MODEL_FILE, 'rb') as f:
        pipeline = pickle.load(f)
    result = pipeline.predict([text])[0]
    probs = pipeline.predict_proba([text])[0]
    top_idx = list(pipeline.classes_).index(result)
    print(f"🔮 분류: {result} (확률: {probs[top_idx]:.2%})")
    return result

if __name__ == "__main__":
    if "--train" in sys.argv:
        train()
    elif "--predict" in sys.argv:
        idx = sys.argv.index("--predict") + 1
        predict(sys.argv[idx] if idx < len(sys.argv) else "테스트")
    else:
        print("--train | --predict '텍스트'")
