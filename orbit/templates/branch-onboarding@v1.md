# Branch-Onboarding@v1

> 길드/브랜치 온보딩 전용 프롬프트 템플릿

## Variables

| 변수 | 타입 | 설명 |
|------|------|------|
| `{{branch_name}}` | string | 브랜치/길드 이름 |
| `{{member_name}}` | string | 새 멤버 이름 |
| `{{slot_id}}` | string | 슬롯 ID (slot01~slot12) |
| `{{industry}}` | string | 업종 |
| `{{features}}` | array | 활성화할 기능 |

## Template

```
새 멤버 온보딩 처리해줘:

브랜치/길드: {{branch_name}}
새 멤버: {{member_name}}
슬롯: {{slot_id}}
업종: {{industry}}

활성화할 기능:
{{#features}}
- {{.}}
{{/features}}

처리할 것:
1. slots/{{slot_id}}/index.html 생성
2. registry.json에 멤버 추가
3. 디지털 명함 생성
4. 환영 메시지 템플릿
5. console/billing.html 업데이트
```

## Example Usage

```json
{
  "type": "branch-onboarding",
  "version": "v1",
  "variables": {
    "branch_name": "namoneygoal",
    "member_name": "김철수",
    "slot_id": "slot02",
    "industry": "부동산",
    "features": ["card", "blog", "walkie"]
  }
}
```
