# parksy-finance MCP

재무비율 시계 × 60갑자 × MCP 분석 엔진

> 재무비율을 외우는 강의가 아니라,
> 재무비율을 읽는 법을 알려주는 강의

## 아키텍처

| 레이어 | 구성 | 역할 |
|--------|------|------|
| L1 좌표계 | 12개 재무비율 시계 | 분석의 실무 좌표 |
| L2 관점계 | 5개 관점 (Form/Flow/Frag/Field/Fit) | 60개 분석 슬롯 |
| L3 서사계 | 60갑자 마스터 테이블 (LLM 생성) | 국면 스토리텔링 |

## 12개 재무비율 시계

| 시 | 비율 | 분석 질문 |
|----|------|----------|
| 1시 | 매출 성장률 | 외형이 확장되는가 |
| 2시 | 매출 규모 | 시장에서 어느 정도 크기인가 |
| 3시 | 매출총이익률 | 원가 구조에서 얼마를 남기는가 |
| 4시 | 영업이익률 | 운영 후 실제 영업 수익성이 있는가 |
| 5시 | 순이익률 | 이자·세금 반영 후 최종 수익이 남는가 |
| 6시 | ROE | 자기자본 효율이 높은가 |
| 7시 | ROIC | 전체 투하자본 효율이 높은가 |
| 8시 | 자산회전율 | 자산을 매출로 얼마나 효율적으로 바꾸는가 |
| 9시 | 재고회전율 | 재고가 얼마나 빠르게 소진되는가 |
| 10시 | 부채비율 | 재무구조가 레버리지에 얼마나 의존하는가 |
| 11시 | 이자보상배율 | 이익으로 금융비용을 감당할 수 있는가 |
| 12시 | PSR/PER | 시장은 이 구조를 얼마에 가격 매기는가 |

## 5개 하위 관점

| 분 | 코드 | 해석 초점 |
|----|------|----------|
| 1분 | Form | 구조와 형태 — 현재 상태의 구조적 윤곽 |
| 2분 | Flow | 돈의 흐름과 수익 모델 |
| 3분 | Frag | 취약성과 리스크 — 어디서 붕괴가 시작되는가 |
| 4분 | Field | 현장 운영과 공급망 |
| 5분 | Fit | 삶과 장기 정렬성 |

## 설치 및 실행

```bash
pip install -r requirements.txt

# 환경변수 설정 (택 1)
export PARKSY_FINANCE_LLM=anthropic
export ANTHROPIC_API_KEY=sk-...

# 또는 DeepSeek
export PARKSY_FINANCE_LLM=deepseek
export DEEPSEEK_API_KEY=sk-...

# MCP 등록
claude mcp add parksy-finance -- python /path/to/server.py
```

## 사용 예

```
유저: 4시 3분, 삼성전자 영업이익률 하락 국면 분석해줘

→ MCP: analyze_position(hour=4, minute=3, context='삼성전자')

→ 출력:
  slot_id: '04h3m'
  raw_ratio_block: '영업이익률이 취약성 관점에서...'
  story_blocks: ['경오(庚午): 강한 금속이 불 위에...', '임자(壬子): 유동성은 있으나...']
  prompt_suggestions: ['이 하락이 1회성인가 추세인가?', ...]
```

## 개발자

EduArt Engineer × dtslib.com · v2.0
