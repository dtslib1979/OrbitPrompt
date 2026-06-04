# PARKSY 표준 레시피 — 철학 에세이 v3

> **버전:** 3.0 (표준)
> **MCP 원소:** mcp_slide_builder + GPT-SoVITS v2ProPlus + Chrome + FFmpeg + Telegram
> **출력:** 정적 웹페이지 이미지 + 박씨 AI 목소리 → MP4 → @philosopher-parksy

---

## 레시피 시퀀스 (6단계, 총 90초)

| 단계 | 도구 | 소요 | 설명 |
|------|------|------|------|
| ① | `mcp_slide_builder.parksy_build_page()` | 3초 | 텍스트 → HTML 웹페이지 |
| ② | `Chrome Headless --screenshot` | 2초 | HTML → PNG 1080×1080 |
| ③ | `GPT-SoVITS v2ProPlus (sovits_worker)` | 5초 | 텍스트 → 박씨 AI 목소리 WAV |
| ④ | `FFmpeg -loop 1 -i img -i audio` | 3초 | PNG+WAV → MP4 (H.264+AAC) |
| ⑤ | `Telegram Bot API sendVideo` | 2초 | 결과 전송 |
| ⑥ | `distributor → @philosopher-parksy` | 60초 | YouTube 업로드 (OAuth 후) |

## 명령어 모음

```bash
# ① 웹페이지 빌드
python3 -c "from page_service import build_page as b; open('/tmp/p.html','w').write(b(text, page_type='article', lang='ko'))"

# ② 스크린샷
google-chrome --headless --screenshot=/tmp/p.png --window-size=1080,1350 file:///tmp/p.html

# ③ 박씨 목소리 TTS (v2ProPlus)
curl -X POST http://localhost:7766/synth \
  -H "Content-Type: application/json" \
  -d '{"text":"...","lang":"ko","output_path":"/tmp/v.wav"}'

# ④ FFmpeg 합성
ffmpeg -y -loop 1 -i /tmp/p.png -i /tmp/v.wav \
  -c:v libx264 -tune stillimage -preset ultrafast \
  -c:a aac -shortest /tmp/final.mp4

# ⑤ Telegram 전송
curl -F video=@/tmp/final.mp4 \
  https://api.telegram.org/bot${TOKEN}/sendVideo \
  -F chat_id="${CHAT_ID}"

# ⑥ YouTube 업로드 (OAuth 필요)
node ~/dtslib-papyrus/tools/youtube/upload.cjs a /tmp/final.mp4
```

## MCP 버전 관리

| 도구 | 버전 | 위치 |
|------|------|------|
| mcp_slide_builder | v2 (25 tools) | parksy-image/tools/mcp_slide_builder/_v2/ |
| GPT-SoVITS | v2ProPlus | parksy-audio/voice_models/matched_v2/ |
| sovits_worker | 1.0 | parksy-audio/scripts/sovits_worker.py |
| tts_engine | 1.0 | parksy-audio/scripts/tts_engine.py |
| web2video | 1.0 | parksy-image/tools/web2video/ |
