# Web-Deploy@v1

> GitHub Pages/도메인/CNAME/리다이렉트 전용 프롬프트 템플릿

## Variables

| 변수 | 타입 | 설명 |
|------|------|------|
| `{{repo}}` | string | 레포지토리 이름 |
| `{{domain}}` | string | 커스텀 도메인 (선택) |
| `{{redirect_from}}` | array | 리다이렉트 소스 |
| `{{ssl}}` | boolean | HTTPS 강제 여부 |

## Template

```
웹 배포 설정해줘:

레포: {{repo}}
도메인: {{domain}}
리다이렉트: {{redirect_from}}
HTTPS: {{ssl}}

처리할 것:
1. GitHub Pages 활성화 확인
2. CNAME 파일 생성/수정
3. DNS 설정 안내 (필요시)
4. robots.txt 생성
5. sitemap.xml 생성
6. 배포 확인 및 URL 제공
```

## Example Usage

```json
{
  "type": "web-deploy",
  "version": "v1",
  "variables": {
    "repo": "namoneygoal",
    "domain": "namoneygoal.kr",
    "redirect_from": ["www.namoneygoal.kr"],
    "ssl": true
  }
}
```
