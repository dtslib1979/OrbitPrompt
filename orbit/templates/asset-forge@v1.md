# Asset-Forge@v1

> 로고/카피/톤/브랜딩 자산 생성 전용 프롬프트 템플릿

## Variables

| 변수 | 타입 | 설명 |
|------|------|------|
| `{{brand_name}}` | string | 브랜드 이름 |
| `{{identity}}` | string | 정체성 한 줄 |
| `{{colors}}` | object | 컬러 팔레트 |
| `{{tone}}` | string | 브랜드 톤 |
| `{{assets_needed}}` | array | 필요한 자산 목록 |

## Template

```
브랜딩 자산 만들어줘:

브랜드: {{brand_name}}
정체성: {{identity}}
컬러: {{colors.primary}}, {{colors.accent}}
톤: {{tone}}

생성할 자산:
{{#assets_needed}}
- {{.}}
{{/assets_needed}}

출력:
1. 태그라인 (3개 후보)
2. 한 줄 소개
3. SNS 바이오
4. 이메일 서명
5. OG 이미지 텍스트
```

## Example Usage

```json
{
  "type": "asset-forge",
  "version": "v1",
  "variables": {
    "brand_name": "NAMONEYGOAL",
    "identity": "AI 쓰는 부동산 중개인 길드",
    "colors": {
      "primary": "#A855F7",
      "accent": "#F59E0B"
    },
    "tone": "전문적이지만 친근한",
    "assets_needed": ["tagline", "bio", "email_signature"]
  }
}
```
