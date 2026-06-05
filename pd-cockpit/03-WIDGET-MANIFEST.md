# Termux 위젯 목록 — S25 Ultra

> **갱신**: 2026-06-05
> **위치**: 폰 `~/.shortcuts/`
> **총 9개** (0~8)

---

## 위젯 맵

| 번호 | 파일명 | 용도 | 중요도 |
|------|--------|------|--------|
| 0 | `0.setup.sh` | WSL/PC 초기 설정 | ⭐ |
| 1 | `1.wsl_claude.sh` | WSL Claude Code 접속 | ⭐⭐⭐ |
| 2 | `2.wsl_aider.sh` | WSL Aider 접속 | ⭐⭐⭐ |
| 3 | `3.win_claude.sh` | Windows Claude Code 접속 | ⭐⭐ |
| 4 | `4.win_aider.sh` | Windows Aider 접속 | ⭐⭐ |
| 5 | `5.rustdesk.sh` | RustDesk 원격 접속 | ⭐⭐ |
| 6 | `6.proot.sh` | Proot 실행 | ⭐ |
| 7 | `7.android.sh` | 안드로이드 도구 모음 | ⭐⭐ |
| 8 | `8.adb.sh` | **ADB 무선 디버깅** (상태/설정/저장) | ⭐⭐⭐ |

---

## 삭제 내역 (2026-06-05)

### 오디오북 위젯 3개 제거

| 파일명 | 생성일 | 사유 |
|--------|--------|------|
| `audiobook` | 2026-05-22 | 클립보드→TTS→Telegram (PD 시스템으로 대체) |
| `audiobook-rvc` | 2026-05-22 | audiobook + RVC 음색 (parksy-voice MCP로 대체) |
| `audiolog` | 2026-05-22 | 오디오 로그 (PD 시스템으로 대체) |

**대체된 이유**: 과거에는 폰에서 직접 위젯 탭으로 파이프라인 실행했으나,
현재는 Claude PD + DeepSeek PD가 모든 미디어 처리를 담당.
GPT-SoVITS + RVC 음질이 edge-tts보다 월등.
