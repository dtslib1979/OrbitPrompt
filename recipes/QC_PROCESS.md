# PARKSY QC 프로세스 — 미디아 출력 검증

## MP4 검수 항목 (자동)

| 항목 | 검사 | 불합격 기준 |
|------|------|-----------|
| `pix_fmt` | ffprobe | yuv420p가 아니면 ❌ |
| `codec` | ffprobe | h264 + aac가 아니면 ❌ |
| audio `RMS` | sox --stat | RMS = 0이면 무음 ❌ |
| audio `Maximum` | sox --stat | > 0.999면 클리핑 ❌ |
| `duration` | ffprobe | 5초 미만 ❌ |
| `size` | ffprobe | 100KB 미만 ❌ |

## QC 명령어

```bash
# 1. 코덱/픽셀포맷 확인
ffprobe -v error -show_entries stream=codec_name,pix_fmt -of default=noprint_wrappers=1 input.mp4

# 2. 오디오 무음/클리핑 체크
sox input.wav -n stat 2>&1 | grep -E "RMS|Maximum"

# 3. 최종 검증
ffprobe -v error -show_entries format=size,duration -of default=noprint_wrappers=1 input.mp4
```
