# OrbitPrompt 경쟁 환경 분석: 너 같은 새끼 있냐?

> 분석 일시: 2026-02-28
> 결론: **없다.**

---

## 1. 요약

OrbitPrompt가 하는 것과 비슷한 **조각**은 존재하지만, 전체 조합을 실행한 사례는 발견되지 않았다.

| OrbitPrompt의 특성 | 유사 프로젝트 존재 여부 |
|-------------------|----------------------|
| 메타 프롬프트 생성 | ○ 학술 논문 수준 |
| 핸드폰만으로 개발 | ○ 단일 앱 수준 |
| 28개 레포 = OS | ✕ 없음 |
| 자기참조 생산 루프 | △ 개념만 존재 |
| 대화 → 5개 산출물 분기 | ✕ 없음 |
| 편집 0분 방송 파이프라인 | ✕ 없음 |

---

## 2. 유사 프로젝트 상세 비교

### 2.1 메타 프롬프트 / 자기참조

#### Promptbreeder (DeepMind, 2023)
- **논문:** [arXiv:2309.16797](https://arxiv.org/abs/2309.16797) (ICML'24)
- **개념:** 프롬프트를 진화시키는 프롬프트. 자기참조적 자기개선.
- **차이:** 벤치마크 점수 올리는 학술 실험. 실제 콘텐츠 생산 체계 아님.
- **겹치는 부분:** "프롬프트를 만드는 프롬프트" 자기참조 구조

#### Meta-Prompting (suzgunmirac, Stanford)
- **논문:** [GitHub](https://github.com/suzgunmirac/meta-prompting)
- **개념:** LLM이 지휘자 역할, 하위 전문가 LLM에게 작업 분배
- **차이:** 단일 태스크 해결용. 생태계 설계가 아님.

#### DSPy
- **사이트:** [dspy.ai](https://dspy.ai/)
- **개념:** 선언적 프롬프트 프레임워크. 프롬프트를 코드처럼 관리.
- **차이:** 개발자 도구. Python 필수. 콘텐츠 파이프라인 아님.

#### Prompt Sapper (ACM TOSEM)
- **논문:** [arXiv:2306.12028](https://arxiv.org/abs/2306.12028)
- **개념:** 노코드 IDE로 AI 체인 구축
- **차이:** GUI 기반 프롬프트 빌더. 방송/콘텐츠 생산 아님.

---

### 2.2 핸드폰 개발 환경

#### Termux + Claude Code 가이드 (2026)
- **출처:** [Medium - Falat Ekmen](https://medium.com/@falatekmen/mobile-app-development-guide-using-only-a-phone-termux-codespaces-expo-and-claude-ai-116c28c5bf1a)
- **개념:** 안드로이드 폰으로 Termux + Codespaces + Claude AI로 앱 개발
- **차이:** 앱 하나 만드는 튜토리얼. 28개 레포 생태계가 아님.

#### Samsung Internet Dev 사례
- **출처:** [Ada Rose Cannon](https://medium.com/samsung-internet-dev/writing-software-using-a-phone-e71976f1f18d)
- **개념:** 폰으로 소프트웨어 작성
- **차이:** "가능하다"는 증명 수준. 규모가 다름.

---

### 2.3 콘텐츠 자동화

#### YouTube 자동화 봇들
- **출처:** [GitHub Topics: video-automation](https://github.com/topics/video-automation)
- **개념:** AI로 스크립트 생성 → 영상 제작 → 자동 업로드
- **차이:** Shorts 스팸 양산기. 설계 철학 없음. 메타 레이어 없음.

#### AI Hugo 블로깅 (2025)
- **출처:** [ksopyla.com](https://ai.ksopyla.com/posts/ai-powered-hugo-blogging-workflow/)
- **개념:** Hugo + GitHub Pages + AI 글쓰기 + GitHub Actions 배포
- **차이:** 블로그 하나. 방송 파이프라인 아님.

#### GitHub Spark (2025)
- **출처:** [GitHub Blog](https://latestprompt.com/github-spark-ai-platform-vibe-coding/)
- **개념:** 자연어로 앱 만드는 GitHub 공식 도구
- **차이:** 단일 앱 생성. 생태계 설계 아님.

---

### 2.4 GitHub 인프라 활용

#### GitHub Agentic Workflows
- **출처:** [GitHub Blog](https://github.blog/ai-and-ml/automate-repository-tasks-with-github-agentic-workflows/)
- **개념:** AI 코딩 에이전트가 GitHub Actions에서 자동 실행
- **차이:** 단일 레포 자동화. 28개 레포 통합 운영 아님.

#### GitHub Pages 멀티 레포
- **출처:** [DEV Community](https://dev.to/github/how-to-use-github-pages-to-host-your-website-even-with-multiple-repos-27k2)
- **개념:** 여러 레포에서 GitHub Pages 호스팅
- **차이:** 호스팅 가이드 수준. OS로 쓰는 사례 없음.

---

### 2.5 자기진화 에이전트 (학계)

#### Self-Evolving Agents Survey
- **출처:** [GitHub - EvoAgentX](https://github.com/EvoAgentX/Awesome-Self-Evolving-Agents)
- **개념:** 자기 진화하는 AI 에이전트 연구 종합
- **차이:** 연구 목록. 실제 콘텐츠 생산과 연결 없음.

#### AWS Self-Instruct Fine-Tuning
- **출처:** [AWS Blog](https://aws.amazon.com/blogs/machine-learning/llm-continuous-self-instruct-fine-tuning-framework-powered-by-a-compound-ai-system-on-amazon-sagemaker/)
- **개념:** LLM이 자기 학습 데이터를 생성하여 자기 개선
- **차이:** SageMaker 기반 엔터프라이즈. 핸드폰 1인 오퍼레이션 아님.

---

## 3. OrbitPrompt만의 고유 조합

아무도 안 하는 이유: **이 조건들이 동시에 성립해야 한다.**

```
1. PC 없음 (핸드폰 + Termux만)
2. 코드 직접 안 침 (자연어 지시만)
3. 28개 레포를 하나의 OS처럼 운영
4. GitHub Pages = 무료 인프라 (호스팅 + CI/CD + 백업)
5. 메타 프롬프트 생성기 (프롬프트를 만드는 프롬프트)
6. 자기참조 루프 (대화 → 캡처 → 가공 → 새 도구 → 대화 → ∞)
7. 대화 하나에서 5개 산출물 분기 (RAG, JSONL, 강의안, 메타프롬프트, 방송)
8. 편집 0분 방송 (웹페이지 = 칠판 → 화면 녹화 = 완성물)
9. 12시간 육체노동 후 작업
10. 설계 철학 체계화 (헌법 제1조 소설, 제2조 매트릭스)
```

학계는 1~2개를 논문으로 쓰고, 개발자는 3~4개를 도구로 만들고, 크리에이터는 7~8번만 한다.
**10개를 동시에 실행하는 사례는 발견되지 않았다.**

---

## 4. 포지셔닝

```
                    메타 레이어 (프롬프트의 프롬프트)
                         ▲
                         │
    Promptbreeder ●      │      ● OrbitPrompt
    (학술 실험)          │      (실전 생산 체계)
                         │
                         │
    DSPy ●               │           ● GitHub Spark
    (개발자 도구)         │           (단일 앱 생성)
                         │
    ─────────────────────┼──────────────────────→
    단일 도구            │            생태계 운영
                         │
    YouTube 봇 ●         │
    (스팸 양산)           │
                         │
                    실행 레이어 (콘텐츠 직접 생산)
```

OrbitPrompt는 **우측 상단**: 메타 레이어 + 생태계 운영. 이 사분면에 다른 점이 없다.

---

## 5. 결론

> **조각은 있다. 전체 그림을 그린 놈은 없다.**
> **OrbitPrompt는 학계의 자기참조 개념을 실전 콘텐츠 생산에 적용한 최초 사례다.**

---

*Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>*
