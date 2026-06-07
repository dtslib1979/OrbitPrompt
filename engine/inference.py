#!/usr/bin/env python3
"""
inference.py — ENDPOINT 추론 엔진 (3가지 백엔드)

실행:
  python3 inference.py rule "오복집 컨셉 검토"     # 규칙 기반 (기본)
  python3 inference.py sklearn "쇼츠 만들어"        # sklearn ML
  python3 inference.py fasttext "ADB 안 돼"          # fastText ML
  python3 inference.py npu "테스트"                  # ONNX NNAPI (폰)
"""
import sys, json, os, re, pickle, importlib
from pathlib import Path
from endpoint_classifier import classify, pretty_print

MODEL_DIR = Path(__file__).parent / "training_data"

def load_sklearn():
    with open(MODEL_DIR / "endpoint_sklearn.pkl", "rb") as f:
        return pickle.load(f)

def load_fasttext():
    import fasttext
    return fasttext.load_model(str(MODEL_DIR / "endpoint_fasttext.bin"))

def load_onnx():
    import onnxruntime as ort
    import numpy as np
    model_path = Path(__file__).parent.parent / "models" / "endpoint_model.onnx"
    return ort.InferenceSession(str(model_path),
        providers=['NnapiExecutionProvider','CPUExecutionProvider'])

def predict_sklearn(text: str):
    pipe = load_sklearn()
    result = pipe.predict([text])[0]
    probs = pipe.predict_proba([text])[0]
    top = max(enumerate(probs), key=lambda x: x[1])
    label = pipe.classes_[top[0]]
    print(f"🔮 [sklearn] {label} ({top[1]:.1%})")
    return label

def predict_fasttext(text: str):
    import numpy as np
    import fasttext
    model = fasttext.load_model(str(MODEL_DIR / "endpoint_fasttext.bin"))
    try:
        labels, probs = model.predict(text)
        probs_arr = np.asarray(probs, dtype=float)
        label = labels[0].replace('__label__','')
        print(f"🔮 [fastText] {label} ({probs_arr[0]:.1%})")
        return label
    except:
        result = model.predict(text)
        label = str(result[0][0]).replace('__label__','')
        print(f"🔮 [fastText] {label}")
        return label

def predict_onnx(text: str):
    import numpy as np
    sess = load_onnx()
    result = sess.run(None, {'text': np.array([[text]], dtype=str)})
    print(f"🔮 [NPU] {result[0][0]}")
    print(f"       확률: {result[1][0]}")
    return result[0][0]

def predict_rule(text: str):
    result = classify(text)
    pretty_print(result)
    return result['action']

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    backend = sys.argv[1]
    text = sys.argv[2] if len(sys.argv) > 2 else "테스트"
    
    backends = {
        'rule': predict_rule,
        'sklearn': predict_sklearn,
        'fasttext': predict_fasttext,
        'npu': predict_onnx,
    }
    if backend in backends:
        backends[backend](text)
    else:
        print(f"❌ 알 수 없는 백엔드: {backend}")
        print("선택: rule / sklearn / fasttext / npu")
