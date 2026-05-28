# 공통 계약: 보안

> 모든 PHL 토큰 실행 시 이 규칙을 따른다.

## OWASP Top 10 체크리스트

| 항목 | 점검 |
|------|------|
| Injection | SQL/NoSQL/OS 명령 파라미터 바인딩 |
| Broken Auth | 인증 우회 경로 없음 |
| Sensitive Data | 평문 저장/전송 금지 |
| XXE | XML 파서 외부 엔티티 비활성화 |
| Broken Access Control | 모든 보호 경로에 권한 체크 |
| Misconfiguration | 디버그 모드 비활성화, 기본 비밀번호 없음 |
| XSS | 모든 출력 이스케이프 |
| Insecure Deserialization | 신뢰되지 않은 데이터 역직렬화 금지 |
| Known Vulnerabilities | 의존성 취약점 점검 |
| Insufficient Logging | 보안 이벤트 로깅 |

## 비밀키 관리

```
절대 금지:
- 소스 코드에 하드코딩
- 커밋 메시지에 포함
- 로그에 출력
- URL 파라미터로 전달

허용:
- 환경변수
- .env 파일 (.gitignore에 포함)
- 시크릿 매니저
```

## 기본 원칙

1. **Deny by default.** 명시적으로 허용하지 않은 것은 거부.
2. **Fail closed.** 에러 시 안전한 상태로 전환 (접근 허용 X).
3. **최소 권한.** 필요한 최소한의 권한만 부여.
4. **심층 방어.** 한 계층이 뚫려도 다음 계층이 방어.
