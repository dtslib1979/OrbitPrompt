# Repo-Janitor@v1

> 레포지토리 정리/통합/디프리케이트 전용 프롬프트 템플릿

## Variables

| 변수 | 타입 | 설명 |
|------|------|------|
| `{{repo_list}}` | array | 대상 레포 목록 |
| `{{rules}}` | object | 정리 규칙 |
| `{{delete_policy}}` | string | 삭제 정책 (archive/delete/merge) |
| `{{naming_policy}}` | string | 네이밍 규칙 |

## Template

```
다음 레포지토리들을 정리해줘:

대상: {{repo_list}}

규칙:
- {{rules.description_format}}
- {{rules.folder_structure}}
- {{rules.commit_convention}}

삭제 정책: {{delete_policy}}
네이밍 규칙: {{naming_policy}}

완료 기준:
- [ ] 모든 레포 디스크립션 통일
- [ ] 불필요 레포 archive/삭제 처리
- [ ] CLAUDE.md 업데이트
- [ ] 계열사 스크립트 동기화
```

## Example Usage

```json
{
  "type": "repo-janitor",
  "version": "v1",
  "variables": {
    "repo_list": ["namone", "namoneygoal"],
    "rules": {
      "description_format": "영문 1줄 + 한글 설명",
      "folder_structure": "CLAUDE.md 필수"
    },
    "delete_policy": "archive",
    "naming_policy": "dtslib- prefix"
  }
}
```
