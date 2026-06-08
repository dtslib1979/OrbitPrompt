# OrbitPrompt 갤러리 카테고리 재설계

> 설계자: Claude (인지과학 기반)
> 문제: DeepSeek가 지적한 "분석모델에 도메인 혼재" 해결
> 목적: 박씨가 DeepSeek한테 던질 수 있는 리마인더

---

## 현재 구조 문제 진단

```
현재 카테고리:
철학/헌법 / 분석모델 / 콘텐츠 / Generator / 인프라/도구

문제:
- "분석모델"에 축구·정치·금융이 무분별하게 묶임 → 도메인이 기준
- "Generator"와 "콘텐츠"가 중복됨 → Generator가 콘텐츠를 만드는 도구인데 분리
- Φ드라이버 철학이 "분석모델"에 섞여 메타레벨 죽음
```

---

## 인지과학 3원칙

**1. Miller's Law** — 카테고리는 5개 이하. 그 이상이면 인지 부하 증가.

**2. 동사 기반 분류** — "축구"(명사, 도메인)보다 "예측한다"(동사, 행동의도)가 처리 속도 빠름. 사용자가 오는 이유가 도메인이 아니라 "뭘 하러 왔냐"이기 때문.

**3. Progressive Disclosure** — 탑레벨은 단순하게 4개, 드릴다운에서 도메인 분기. 첫 화면에서 모든 걸 보여주면 인지 과부하.

---

## 새 구조: 4분류 동사 기반

```
┌─────────────────────────────────────────────────────┐
│                  OrbitPrompt Gallery                │
├──────────┬──────────┬──────────┬────────────────────┤
│ 🎯 THINK │ ✍️ MAKE  │ 🔬 DRAW  │ 📐 FRAME           │
│ 예측·분석 │ 생성·제작 │ 추출·파싱 │ 철학·방법론        │
└──────────┴──────────┴──────────┴────────────────────┘
```

### 🎯 THINK — 예측하고 분석한다
도메인별 2단계 드릴다운:
```
THINK
 ├── ⚽ 스포츠 → 축구 WC2026 MCP (Φ-I-C-K-P 시뮬레이터)
 ├── 🏛️ 정치  → 선거/정치인 분석 MCP
 ├── 📊 금융  → 재무비율 철학 모델
 └── ➕ (도메인 추가 가능)
```

**왜 여기가 Φ드라이버 홈이 아닌가**: Φ드라이버는 THINK의 도구가 아니라 FRAME이다. 철학이 먼저 있고, 그 철학으로 THINK를 한다.

### ✍️ MAKE — 만들고 생성한다
Generator + 완성 콘텐츠 통합:
```
MAKE
 ├── Chalkboard Generator (방송용 칠판)
 ├── PWA Generator (앱 제작)
 ├── Editorial Generator (럭셔리 에디토리얼)
 ├── 박찬대 되기 프로젝트 (비즈니스 소설)
 └── 오복집 사례 (FLD 에피소드 01)
```

### 🔬 DRAW — 뽑아내고 추출한다
데이터/패턴 추출 도구:
```
DRAW
 ├── Dataset Generator (대화→파인튜닝 JSONL)
 ├── Identity Engine (7축 자기모델 추출)
 └── Narrative Extract (레포 서사 추출)
```

### 📐 FRAME — 프레임을 세운다
철학·방법론·헌법:
```
FRAME
 ├── Φ드라이버 철학 (7축 Meta/Reverse/Modular/Lang/Zoom/Spiral/Quantum)
 ├── PHL 프로토콜
 ├── 백서 (OrbitPrompt 철학)
 ├── 삼각 실행 루프 방법론 (Triangular Staff Method)
 └── FAB 라우트 정의
```

---

## DeepSeek한테 던질 리마인더 (복붙용)

```
OrbitPrompt 갤러리 카테고리 재설계해줘.

현재 문제:
- 분석모델에 도메인이 혼재 (축구/정치/금융)
- Φ드라이버가 분석모델에 묻혀있음
- Generator와 콘텐츠 중복

새 구조 (4분류, 동사 기반):
- 🎯 THINK: 예측·분석 (도메인별 드릴다운: 스포츠/정치/금융)
- ✍️ MAKE: 콘텐츠·앱 생성 (Generator + 완성 결과물 통합)
- 🔬 DRAW: 추출·파싱 (Dataset, Identity Engine)
- 📐 FRAME: 철학·방법론 (Φ드라이버, PHL, 백서, 삼각실행루프)

인지과학 근거:
- 4개 탑레벨 (Miller's Law)
- 동사 기반 (사용자 의도 매핑)
- 도메인은 2단계로 (Progressive Disclosure)

index.html cat-btn 4개로 교체 + 각 전시물 data-cat 업데이트.
```

---

## 변경 대상 파일

- `index.html` — cat-btn 교체 (철학/헌법·분석모델·콘텐츠·Generator·인프라 → THINK·MAKE·DRAW·FRAME)
- 각 전시물 `data-cat` 속성 업데이트
- `data/templates.json` — category 필드 업데이트
