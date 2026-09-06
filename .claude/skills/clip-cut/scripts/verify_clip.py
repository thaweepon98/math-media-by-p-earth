#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ตรวจไฟล์ที่เรนเดอร์เสร็จ ก่อนส่งให้เจ้าของงาน

ใช้:
    python3 verify_clip.py out.mp4 [--at 2 9 20 39] [--outdir check]

ทำสองอย่าง:
  1. เช็คเสียง — มีแทร็กเสียงไหม, ดังพอไหมทุกช่วง, ซ้าย/ขวาหักล้างกันไหม
     (สองข้อหลังคือบั๊กที่เงียบที่สุด ไฟล์เปิดได้ปกติแต่ไม่ได้ยินเสียง)
  2. ดึงเฟรมตรงวินาทีที่ระบุออกมาเป็นภาพ ให้เปิดดูว่าข้อความขึ้นถูกที่ถูกเวลา
     ตัวอักษรไม่ล้นขอบ และไม่ไปทับสิ่งที่ผู้ชมต้องอ่าน
"""
import argparse, os, re, subprocess, sys


def ffmpeg_bin():
    for cand in ("ffmpeg", "/usr/bin/ffmpeg"):
        try:
            subprocess.run([cand, "-version"], capture_output=True, check=True)
            return cand
        except Exception:
            pass
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def err_of(ff, args):
    return subprocess.run([ff, "-hide_banner", *args], capture_output=True, text=True).stderr


def mean_of(text):
    m = re.search(r"mean_volume: (-?[\d.]+) dB", text)
    return float(m.group(1)) if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--at", nargs="*", type=float, default=[])
    ap.add_argument("--outdir", default="check")
    ap.add_argument("--crop", default=None, help="W:H:X:Y ครอปเฉพาะโซนข้อความ")
    a = ap.parse_args()
    ff = ffmpeg_bin()

    info = err_of(ff, ["-i", a.video])
    dur = re.search(r"Duration: (\d+):(\d+):([\d.]+)", info)
    seconds = (int(dur.group(1)) * 3600 + int(dur.group(2)) * 60 + float(dur.group(3))) if dur else 0
    astream = [l.strip() for l in info.splitlines() if "Stream #" in l and "Audio:" in l]
    print(f"ความยาว {seconds:.2f} วิ")
    print("เสียง   :", astream[0] if astream else "*** ไม่มีแทร็กเสียงเลย ***")
    problems = []
    if not astream:
        problems.append("ไฟล์ไม่มีแทร็กเสียง")

    if astream:
        print("\nความดังต่อช่วง 10 วินาที")
        quiet = []
        for t in range(0, int(seconds), 10):
            mv = mean_of(err_of(ff, ["-ss", str(t), "-t", "10", "-i", a.video,
                                     "-af", "volumedetect", "-f", "null", "-"]))
            flag = ""
            if mv is None or mv < -45:
                flag = "  <-- เงียบผิดปกติ"
                quiet.append(t)
            print(f"  {t:4d}s : {mv if mv is not None else float('nan'):6.1f} dB{flag}")
        if quiet:
            problems.append(f"มีช่วงเงียบผิดปกติที่วินาที {quiet}")

        st = min(5.0, seconds / 4)
        mono = mean_of(err_of(ff, ["-ss", str(st), "-t", "15", "-i", a.video,
                                   "-af", "pan=mono|c0=0.5*c0+0.5*c1,volumedetect", "-f", "null", "-"]))
        left = mean_of(err_of(ff, ["-ss", str(st), "-t", "15", "-i", a.video,
                                   "-af", "pan=mono|c0=c0,volumedetect", "-f", "null", "-"]))
        print(f"\nดาวน์มิกซ์โมโน {mono:.1f} dB เทียบกับช่องซ้าย {left:.1f} dB")
        if mono is not None and left is not None and mono < left - 6:
            problems.append("ซ้าย/ขวากลับเฟสกัน พอเล่นบนลำโพงโมโนจะเงียบ")
        else:
            print("  ไม่มีการหักล้างเฟส")

    if a.at:
        os.makedirs(a.outdir, exist_ok=True)
        print(f"\nเฟรมที่ดึงออกมา (เปิดดูทีละไฟล์):")
        for t in a.at:
            path = os.path.join(a.outdir, f"t{t:07.2f}.png")
            vf = f"crop={a.crop}" if a.crop else None
            cmd = [ff, "-hide_banner", "-loglevel", "error", "-y", "-ss", str(t),
                   "-i", a.video, "-frames:v", "1"]
            if vf:
                cmd += ["-vf", vf]
            subprocess.run(cmd + [path], check=False)
            print(f"  {path}")

    print()
    if problems:
        print("*** เจอปัญหา ***")
        for p in problems:
            print("  - " + p)
        sys.exit(1)
    print("เสียงผ่านทุกข้อ — เหลือแค่เปิดดูเฟรมด้วยตาว่าข้อความถูกต้อง")


if __name__ == "__main__":
    main()
