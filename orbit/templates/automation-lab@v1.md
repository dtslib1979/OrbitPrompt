# Automation-Lab@v1

> 파이썬/스크립트/워크플로우 자동화 전용 프롬프트 템플릿

## Variables

| 변수 | 타입 | 설명 |
|------|------|------|
| `{{task}}` | string | 자동화할 작업 |
| `{{trigger}}` | string | 트리거 조건 |
| `{{input_source}}` | string | 입력 소스 |
| `{{output_dest}}` | string | 출력 목적지 |
| `{{language}}` | string | 언어 (bash/python/js) |
| `{{constraints}}` | array | 제약 조건 |

## Template

```
자동화 스크립트 만들어줘:

작업: {{task}}
트리거: {{trigger}}
입력: {{input_source}}
출력: {{output_dest}}
언어: {{language}}

제약:
{{#constraints}}
- {{.}}
{{/constraints}}

요구사항:
1. 에러 핸들링 포함
2. 로그 출력
3. dry-run 옵션
4. 주석 포함
```

## Example Usage

```json
{
  "type": "automation-lab",
  "version": "v1",
  "variables": {
    "task": "모든 브랜치 레포 git pull",
    "trigger": "매일 아침 6시",
    "input_source": "~/bin/계열사 목록",
    "output_dest": "로그 파일",
    "language": "bash",
    "constraints": ["Termux 환경", "백그라운드 실행"]
  }
}
```
