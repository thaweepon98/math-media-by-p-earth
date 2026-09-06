#!/usr/bin/env bash
# ติดตั้ง ffmpeg + ฟอนต์ Kanit — รันครั้งเดียวต่อ session (คอนเทนเนอร์ถูกล้างทุกครั้งที่เริ่มใหม่)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
FONTS="$HERE/../assets/fonts"

if ! command -v ffmpeg >/dev/null 2>&1; then
  python3 -c "import imageio_ffmpeg" 2>/dev/null || pip install -q imageio-ffmpeg
  echo "ffmpeg: $(python3 -c 'import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())')"
else
  echo "ffmpeg: $(command -v ffmpeg)"
fi

mkdir -p "$FONTS"
for w in Regular Medium SemiBold Bold ExtraBold Black; do
  f="$FONTS/Kanit-$w.ttf"
  [ -s "$f" ] || curl -sSLf -o "$f" \
    "https://raw.githubusercontent.com/google/fonts/main/ofl/kanit/Kanit-$w.ttf" || {
      rm -f "$f"; echo "ข้าม Kanit-$w (โหลดไม่ได้)" >&2; }
done
echo "ฟอนต์ Kanit: $(ls "$FONTS" | wc -l) น้ำหนัก ที่ $FONTS"

# libass อ่านฟอนต์จาก fontsdir ได้อยู่แล้ว แต่ลงในระบบด้วยจะชัวร์กว่าถ้ามีสิทธิ์
if [ -w /usr/share/fonts ] 2>/dev/null; then
  mkdir -p /usr/share/fonts/truetype/kanit
  cp "$FONTS"/Kanit-*.ttf /usr/share/fonts/truetype/kanit/ && fc-cache -f >/dev/null 2>&1 || true
fi
