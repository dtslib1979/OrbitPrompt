# Termux 위젯 목록 — S25 Ultra

> **갱신**: 2026-06-05
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
| 8 | `8.adb.sh` | **ADB 무선 디버깅** | `status/settings/pair` | ⭐⭐⭐ |

---

## 삭제 내역 (2026-06-05)

### 오디오북 위젯 3개 제거

| 파일명 | 생성일 | 사유 |
|--------|--------|------|
| `audiobook` | 2026-05-22 | PD 시스템으로 대체 (구 TTS 파이프라인) |
| `audiobook-rvc` | 2026-05-22 | parksy-voice MCP로 대체 |
| `audiolog` | 2026-05-22 | PD 시스템으로 대체 |

---

## ADB 설정 현황 (2026-06-05)

| 항목 | 상태 |
|------|------|
| 폰 adbd 데몬 | ✅ 실행중 |
| USB ADB | ✅ 활성 (`sec_charging,adb`) |
| WiFi ADB | ❌ 꺼짐 (TCP 포트 없음) |
| Magisk 루팅 | ❌ 불가 (S25 부트로더 잠김) |

**해법**: USB 케이블 1회 연결 후 `~/.local/bin/adb-usb-setup.sh` 실행
→ WiFi ADB 영구 사용 가능 (재부팅 시 Termux:Boot 자동 복구)
