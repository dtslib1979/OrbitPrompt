# ENDPOINT 엔진

ENDPOINT는 Capture → Classify → Judge → Archive → Publish 5단계 선형 판단 모델.

## 설치

```bash
pip install scikit-learn fasttext onnxruntime imbalanced-learn
```

## 사용법

### CLI

```bash
# 규칙 기반 분류 (기본, 의존성 0)
python3 inference.py rule "오복집 컨셉 검토"

# sklearn ML 분류 (68K 학습)
python3 inference.py sklearn "쇼츠 만들어"

# fastText 분류
python3 inference.py fasttext "ADB 연결이 안 돼"

# ONNX NPU 분류 (폰 NNAPI)
python3 inference.py npu "테스트"
```

### Python API

```python
from endpoint_classifier import classify
result = classify("오복집 컨셉 검토")
print(result['action'])  # hold / execute / discard
```

## 데이터 학습

```bash
# parksy-logs 레이블링
python3 fasttext_labeler.py --label 500

# fastText 학습
python3 fasttext_labeler.py --train

# sklearn 학습
python3 sklearn_classifier.py --train

# 폰 로그 파싱
python3 log_parser.py
```

## 파일 구조

```
engine/
├── endpoint_classifier.py  # 분류 엔진 (120줄)
├── inference.py            # 추론 CLI (rule/sklearn/fasttext/npu)
├── judge_rules.json        # 결정 테이블 (11개 규칙)
├── fasttext_labeler.py     # 자동 레이블링
├── sklearn_classifier.py   # ML 분류기
├── log_parser.py           # 폰 로그 파싱
├── training_data/          # 학습 데이터 + 모델
└── README.md               # 이 파일

models/
└── endpoint_model.onnx     # ONNX 모델 (237KB)
```

## 스펙

| 항목 | 값 |
|------|-----|
| 학습 샘플 | 68,816개 (ChatGPT 48K + 폰 로그 19K) |
| Weighted F1 | 0.901 |
| NPU 백엔드 | NNAPI (Snapdragon 8 Elite) |
| 결정 규칙 | 11개 if-elif + 충돌 해결 |
| 저장소 | brain_delta/ + events/ + HQ queue/ |
