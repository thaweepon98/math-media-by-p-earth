#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""สำรวจคลิปต้นฉบับก่อนตัด — ต้องรันตัวนี้ก่อนเขียนข้อความใดๆ เสมอ

ใช้:
    python3 probe_clip.py <video> [--outdir DIR] [--grid-fps 1] [--crop W:H:X:Y]

พิมพ์ออกมา: ความยาว/ขนาด/เฟรมเรต, จุดเริ่มเอนด์การ์ด CapCut (จอดำ),
ตารางสรุปช่วงเงียบที่เกณฑ์ต่างๆ, และรายการช่วงเงียบทั้งหมด
เซฟลง outdir: contact sheet (grid_*.jpg) ไว้ให้อ่านว่าในคลิปเกิดอะไรขึ้นตอนไหน
"""
import argparse, json, os, re, subprocess, sys


def ffmpeg_bin():
    """ffmpeg จากระบบ ถ้าไม่มีก็ใช้ตัวที่มากับ imageio-ffmpeg"""
    for cand in ("ffmpeg", "/usr/bin/ffmpeg"):
        try:
            subprocess.run([cand, "-version"], capture_output=True, check=True)
            return cand
        except Exception:
            pass
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit("ไม่พบ ffmpeg — รัน scripts/setup.sh ก่อน")


def run(ff, args):
    return subprocess.run([ff, "-hide_banner", *args], capture_output=True, text=True).stderr


def probe(ff, src):
    err = run(ff, ["-i", src])
    dur = re.search(r"Duration: (\d+):(\d+):([\d.]+)", err)
    seconds = None
    if dur:
        h, m, s = dur.groups()
        seconds = int(h) * 3600 + int(m) * 60 + float(s)
    streams = [l.strip() for l in err.splitlines() if "Stream #" in l]
    return seconds, streams


def find_outro(ff, src, seconds):
    """เอนด์การ์ด CapCut เป็นจอดำท้ายคลิป — คืนวินาทีที่จอดำเริ่ม (None ถ้าไม่มี)"""
    start = max(0.0, seconds - 12) if seconds else 0.0
    err = run(ff, ["-ss", f"{start}", "-i", src,
                   "-vf", "blackdetect=d=0.5:pic_th=0.98:pix_th=0.05", "-an", "-f", "null", "-"])
    hits = [start + float(m.group(1)) for m in re.finditer(r"black_start:([\d.]+)", err)]
    # เอาเฉพาะจอดำที่ต่อยาวไปจนจบจริงๆ ไม่ใช่จอดำกลางคลิป
    return next((t for t in hits if seconds and seconds - t < 12), None)


def silences(ff, src, noise="-33dB"):
    err = run(ff, ["-i", src, "-af", f"silencedetect=noise={noise}:d=0.30", "-f", "null", "-"])
    out, cur = [], None
    for m in re.finditer(r"silence_(start|end): ([\d.]+)", err):
        kind, val = m.group(1), float(m.group(2))
        if kind == "start":
            cur = val
        elif cur is not None:
            out.append((cur, val))
            cur = None
    return out


def contact_sheets(ff, src, seconds, outdir, fps, crop):
    """แผ่นภาพรวมทุกวินาที — นี่คือวิธี 'ดู' คลิปโดยไม่ต้องเปิดเล่น"""
    os.makedirs(outdir, exist_ok=True)
    made, cols, rows = [], 6, 10
    chunk = cols * rows / fps
    t = 0.0
    while seconds and t < seconds:
        path = os.path.join(outdir, f"grid_{int(t):04d}s.jpg")
        vf = f"fps={fps}," + (f"crop={crop}," if crop else "") + f"scale=240:-1,tile={cols}x{rows}"
        subprocess.run([ff, "-hide_banner", "-loglevel", "error", "-y",
                        "-ss", f"{t}", "-t", f"{chunk}", "-i", src,
                        "-vf", vf, "-frames:v", "1", path], check=False)
        if os.path.exists(path):
            made.append((t, fps, cols, path))
        t += chunk
    return made


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--outdir", default="probe")
    ap.add_argument("--grid-fps", type=float, default=1.0)
    ap.add_argument("--crop", default=None, help="W:H:X:Y ครอปเฉพาะโซนที่อยากอ่าน เช่นกระดาน")
    a = ap.parse_args()

    ff = ffmpeg_bin()
    seconds, streams = probe(ff, a.video)
    print(f"ความยาว : {seconds:.2f} วินาที" if seconds else "อ่านความยาวไม่ได้")
    for s in streams:
        print("  " + s)

    outro = find_outro(ff, a.video, seconds)
    if outro:
        print(f"\nเอนด์การ์ด CapCut : จอดำเริ่มที่ {outro:.2f} วินาที  -> ตั้ง \"end\": {outro:.2f}")
    else:
        print("\nเอนด์การ์ด CapCut : ไม่พบจอดำท้ายคลิป")

    sil = silences(ff, a.video, )
    limit = outro or seconds or 0
    sil = [(s, e) for s, e in sil if s < limit]
    print(f"\nช่วงเงียบ (ก่อน {limit:.2f} วิ) — เลือกเกณฑ์จากตารางนี้")
    print(f"{'เกณฑ์':>8} {'จำนวนรอยตัด':>12} {'ประหยัด(วิ)':>12}")
    for thr in (0.4, 0.6, 0.9, 1.2, 1.5):
        hits = [(s, e) for s, e in sil if e - s >= thr]
        saved = sum((e - s) - 0.36 for s, e in hits)
        print(f"{thr:>8.1f} {len(hits):>12} {max(saved, 0):>12.1f}")
    print("\nรายการช่วงเงียบ >= 0.4 วิ:")
    for s, e in sil:
        if e - s >= 0.4:
            print(f"  {s:7.2f} -> {e:7.2f}  ({e - s:.2f})")

    sheets = contact_sheets(ff, a.video, limit, a.outdir, a.grid_fps, a.crop)
    print(f"\nแผ่นภาพรวม {len(sheets)} แผ่น (อ่านซ้ายไปขวา บนลงล่าง):")
    for t, fps, cols, path in sheets:
        print(f"  {path}  ช่องแรก = {t:.0f} วิ, ห่างกันช่องละ {1/fps:.2f} วิ, แถวละ {cols} ช่อง")


if __name__ == "__main__":
    main()
