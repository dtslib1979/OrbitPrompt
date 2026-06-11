# OrbitPrompt 디자인 리팩터링 플랜 — v2.0 (칠판 그린)

> **목표:** 다크그린(#0A1A0F) 칠판 + 흰색 분필 컨셉으로 73페이지 통일
> **도구:** parksy-webpage MCP (gold-dark 테마 기반)
> **상태:** 플랜 수립 완료. 샘플 1페이지 적용 후 일괄 적용 결정 대기.

---

## 디자인 시스템 — 칠판 그린

```css
:root {
  /* 칠판 */
  --bg:      #0A1A0F;  /* 칠판 전체 */
  --bg2:     #0D2214;  /* 표면 */
  --bg3:     #112A18;  /* 카드 hover */
  
  /* 분필 */
  --text:    #FFFFFF;  /* 흰색 분필 */
  --muted:   rgba(255,255,255,0.62);
  --muted2:  rgba(255,255,255,0.40);
  
  /* 금분필 (강조) */
  --gold:    #EEC864;
  
  /* 테두리 (분필 먼지) */
  --border:  rgba(212,175,55,0.15);
  
  /* 폰트 */
  --font-sans:  'Pretendard', 'Noto Sans KR', system-ui, sans-serif;
  --font-mono:  'JetBrains Mono', monospace;
  --font-serif: 'Playfair Display', Georgia, serif;
}
```

## 분필 효과 2가지 (프로 마감용)

1. **노이즈 텍스처** — `body::before`에 SVG noise (칠판 질감)
2. **스크롤 시 먼지 애니메이션** — subtle particle

## 적용 순서

1. 샘플 1페이지 → 박씨 승인 → 일괄 적용
2. orbit-theme.css 교체
3. 73페이지 순차 적용 (루트→boards→football→prompts)
