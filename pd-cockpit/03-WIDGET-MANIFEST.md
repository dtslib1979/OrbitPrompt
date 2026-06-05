# Termux 위젯 목록 — S25 Ultra

> **갱신**: 2026-06-06 01:20
> **위치**: 폰 `~/.shortcuts/`
> **총 9개** (0~8)

---

## 위젯 맵

| 번호 | 파일명 | 용도 | 명령어 | 중요도 |
|------|--------|------|--------|--------|
| 0 | `0.setup.sh` | WSL/PC 초기 설정 | - | ⭐ |
| 1 | `1.wsl_claude.sh` | WSL Claude Code 접속 | - | ⭐⭐⭐ |
| 2 | `2.wsl_aider.sh` | WSL Aider 접속 | - | ⭐⭐⭐ |
| 3 | `3.win_claude.sh` | Windows Claude Code 접속 | - | ⭐⭐ |
| 4 | `4.win_aider.sh` | Windows Aider 접속 | - | ⭐⭐ |
| 5 | `5.rustdesk.sh` | RustDesk 원격 접속 | - | ⭐⭐ |
| 6 | `6.proot.sh` | Proot 실행 | - | ⭐ |
| 7 | `7.android.sh` | 안드로이드 도구 모음 | - | ⭐⭐ |
| 8 | `8.adb.sh` | **ADB 무선 디버깅** | `status/settings` | ⭐⭐⭐ |

---

## 삭제 내역 (2026-06-05)

| 파일명 | 생성일 | 사유 |
|--------|--------|------|
| `audiobook` | 2026-05-22 | PD 시스템으로 대체 |
| `audiobook-rvc` | 2026-05-22 | parksy-voice MCP로 대체 |
| `audiolog` | 2026-05-22 | PD 시스템으로 대체 |

---

## ADB 설정 내역 (2026-06-06 01:20)

| 항목 | 상태 |
|------|------|
| WiFi ADB | ✅ **연결됨** (`100.103.250.45:5555`) |
| 터치 자동화 | ✅ `input tap` 정상 작동 |
| 화면 캡처 | ✅ `screencap` 정상 작동 |
| 부트 자동복구 | ✅ Termux:Boot 등록 완료 |
| USB 케이블 | ✅ 분리 가능 (WiFi 유지) |
| 폰 위젯 8번 | ✅ ADB 상태 표시 |

**방법**: USB 1회 연결 후 `powershell.exe -Command "adb tcpip 5555"` → WiFi 영구 사용
