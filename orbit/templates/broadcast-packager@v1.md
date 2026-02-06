# Broadcast-Packager@v1

> YouTube/방송 콘텐츠 패키징 전용 프롬프트 템플릿

## Variables

| 변수 | 타입 | 설명 |
|------|------|------|
| `{{topic}}` | string | 방송 주제 |
| `{{footage_notes}}` | string | 영상 소재 메모 |
| `{{tone}}` | string | 톤 (parksy/formal/casual) |
| `{{length}}` | string | 길이 (shorts/5min/15min) |
| `{{cta}}` | string | Call to Action |
| `{{links}}` | array | 관련 링크 |

## Template

```
방송 콘텐츠 패키지를 만들어줘:

주제: {{topic}}
영상 메모: {{footage_notes}}
톤: {{tone}}
길이: {{length}}

생성할 것:
1. 제목 (3개 후보)
2. 설명란 (링크 포함)
3. 태그 (10개)
4. 썸네일 텍스트
5. 쇼츠용 훅 문장

CTA: {{cta}}
링크: {{links}}
```

## Example Usage

```json
{
  "type": "broadcast-packager",
  "version": "v1",
  "variables": {
    "topic": "2개월만에 28개 레포 만든 방법",
    "footage_notes": "Termux 화면 녹화, 계열사 CLI 시연",
    "tone": "parksy",
    "length": "15min",
    "cta": "구독하고 다음 영상 기다려",
    "links": ["https://github.com/dtslib1979"]
  }
}
```
