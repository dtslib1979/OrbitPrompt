# 28개 레포지토리 — 의학 분과 매핑

> 각 레포의 기능적 역할을 의학 분과·과목에 대응시킨 매핑 테이블
> 2026-07-02

---

## P0: TELEGRAM — 통신의학

| 레포 | 역할 | 의학 분과 | 이유 |
|------|------|-----------|------|
| parksy-logs | 대화 로그 저장소 | **신경과 (Neurology)** | 기억을 저장하고 패턴을 분석한다. 임상 기록의 신경망 |
| telegram-bridges | 텔레그램 브릿지 | **신경외과 (Neurosurgery)** | 신호를 연결하고 단절된 회로를 우회한다. 브릿지=신경접합 |

## P1: INFRA — 인프라의학

| 레포 | 역할 | 의학 분과 | 이유 |
|------|------|-----------|------|
| dtslib-papyrus | 본사 중앙 문서 | **내과 (Internal Medicine)** | 전체 시스템을 총괄하고 진단한다. 가장 먼저 보는 창 |
| dtslib-localpc | 로컬PC 실행 노드 | **가정의학과 (Family Medicine)** | 일차 진료, 지역 기반, 가까운 곳에서 해결 |
| termux-bridge | PC↔폰 간극 해결 | **응급의학과 (Emergency Medicine)** | 위기 상황에서 연결, 골든타임 확보 |

## P2: YOUTUBE — 감각기관

| 레포 | 역할 | 의학 분과 | 이유 |
|------|------|-----------|------|
| parksy-audio | 오디오 엔진 | **이비인후과 (Otorhinolaryngology)** | 소리와 음성을 담당. 귀·성대 |
| parksy-image | 이미지 에셋 | **영상의학과 (Radiology)** | 시각 정보 저장과 가공. CT·MRI의 디지털 버전 |
| parksy.kr | 지식 아카이브 | **의학도서관 (Medical Library)** | 축적된 지식의 카탈로그. 참조점 |

## P3: BROADCAST — 방송의학

| 레포 | 역할 | 의학 분과 | 이유 |
|------|------|-----------|------|
| eae.kr | 교육 PWA | **의학교육학 (Medical Education)** | 가르치고 전수하는 학문 |
| gohsy-production | 방송 스튜디오 | **정형외과 (Orthopedics)** | 구조를 세우고 움직임을 만든다. 스튜디오=근골격계 |
| hoyadang.com | 레스토랑 프로토콜 | **소화기내과/영양학 (Gastroenterology)** | 들어오는 걸 처리하고 영양분을 만든다. 레스토랑=위장관 |

## P4: KNOWLEDGE — 기초의학

| 레포 | 역할 | 의학 분과 | 이유 |
|------|------|-----------|------|
| eae-univ | 온라인 학습 플랫폼 | **기초의학 (Basic Medicine)** | 의학의 기초를 쌓는 과정. 생리·생화·미생물 |
| OrbitPrompt | 프롬프트 엔진 | **진단검사의학·의료정보학 (Lab Medicine/Informatics)** | 입력을 분석하고 결과를 생성한다. 진단 키트 |
| dtslib-branch | 브랜치·모델 개발 | **해부학 (Anatomy)** | 구조를 나누고 연결 방식을 연구한다. 브랜치=혈관·신경가지 |

## P5: PHYSICAL — 외피와 운동

| 레포 | 역할 | 의학 분과 | 이유 |
|------|------|-----------|------|
| gohsy-fashion | 패션 스튜디오 | **피부과 (Dermatology)** | 가장 바깥층, 외관과 보호. 패션=피부의 연장 |
| espiritu-tango | 탱고 | **스포츠의학·재활의학 (Sports Medicine)** | 움직임과 리듬. 몸의 표현과 회복 |
| gohsy | 꿈과 현실 | **정신건강의학과 (Psychiatry)** | 존재의 의미를 묻는다. 정신과는 가장 철학적인 분과 |
| alexandria-sanctuary | 도서관·성지 | **의사학·의료인류학 (Medical History)** | 시간을 축적하고 지혜를 보존한다. 역사가 미래를 말한다 |

## P6: DIRECT — 중개의학

| 레포 | 역할 | 의학 분과 | 이유 |
|------|------|-----------|------|
| phoneparis | 폰 판매·유통 | **소아청소년과 (Pediatrics)** | 가볍고 빠르게 성장한다. 폰=아이의 손에 가장 먼저 |
| dtslib-apk-lab | APK 실험실 | **병리과·실험실의학 (Pathology/Lab Medicine)** | 실험하고 검증한다. APK=조직切片 |
| buckleychang.com | 회계사 사이트 | **법의학 (Forensic Medicine)** | 숫자와 증거를 다룬다. 회계=재무 부검 |
| obokzip | 물리 스튜디오 | **재활의학과 (Rehabilitation Medicine)** | 회복하고 재창조한다. 물리=재활치료 |

## P7: BRANCH — 특수 분과

| 레포 | 역할 | 의학 분과 | 이유 |
|------|------|-----------|------|
| buddies.kr | 소매·유통 운영 | **산업의학·직업환경의학 (Occupational Medicine)** | 현장에서 일어나는 일, 작업 환경 관리 |
| namoneygoal | 부동산·사업 운영 | **예방의학·공중보건 (Preventive Medicine)** | 장기적 안정성, 위험 요소 사전 차단 |
| papafly | 인큐베이션 | **산부인과·발생학 (OBGYN/Embryology)** | 새로운 것을 탄생시키는 과정. 인큐베이터=태내 |
| koosy | 연예 편집 방송 | **성형외과 (Plastic Surgery)** | 이미지를 재구성한다. 편집=성형 |
| artrew | 아트·예술 | **예술치료학 (Art Therapy)** | 표현을 통한 치유. 아트는 가장 오래된 의학 |
| dtslib.kr | 경제방송 플랫폼 | **통합의학 (Integrative Medicine)** | 경제와 삶을 통합적으로 본다. 가장 큰 단위의 진료 |
| dtslib-cloud-appstore | 클라우드 앱 배포 | **약리학·처방학 (Pharmacology)** | 약(앱)을 개발하고 유통한다. 앱스토어=약국 |

---

## 종합 — 의학적 해석

```
P0 TELEGRAM    = 신경계    (소통과 기록)
P1 INFRA       = 순환계    (인프라가 흐른다)
P2 YOUTUBE     = 특수감각  (보고 듣는다)
P3 BROADCAST   = 소화계    (받아서 가공한다)
P4 KNOWLEDGE   = 중추신경  (배우고 판단한다)
P5 PHYSICAL    = 외피+운동 (표현하고 움직인다)
P6 DIRECT      = 내분비계  (직접 전달한다)
P7 BRANCH      = 면역계    (다양하게 대응한다)
```

> 28개 레포는 하나의 병원이다. 각 분과가 협진하여 하나의 콘텐츠를 완성한다.
