#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ตัด + อัปสเกล + เบิร์นข้อความสไตล์ฟอนต์ไวรัล จากไฟล์ config เดียว

ใช้:
    python3 build_clip.py config.json [--ass-only]

config.json (คีย์ที่ไม่ใส่จะใช้ค่า default):
{
  "source": "raw.mov",
  "output": "out.mp4",
  "end": 110.80,            # ตัดทุกอย่างหลังวินาทีนี้ (จุดเริ่มเอนด์การ์ด CapCut)
  "start": 0.0,
  "width": 1080, "height": 1920,
  "min_silence": 0.90,      # ตัดช่วงเงียบที่ยาวกว่านี้ (ดู references/style.md ก่อนลดเลข)
  "silence_pad": 0.18,      # เว้นหายใจไว้ข้างละเท่านี้ ช่วงเงียบจึงเหลือ 0.36 วิ
  "loudnorm": true,
  "hook":  {"start":0.2,"end":4.8,"line1":"บรรทัดขาวเล็ก","line2":"บรรทัดเหลืองใหญ่"},
  "band":  "ข้อความแถบบนที่ค้างทั้งคลิป",     # ใส่ null ถ้าไม่ต้องการ
  "pops":  [{"start":5.5,"end":12.5,"big":"เหลืองใหญ่","small":"ขาวเล็ก","layout":"YW"}],
  "srt":   "captions.srt"   # ถ้ามี จะเบิร์นซับคำพูดด้วย (ดู README ในสคริปต์)
}

layout: "YW" = เหลืองใหญ่บน/ขาวเล็กล่าง (ค่าปกติ)
        "WY" = ขาวเล็กบน/เหลืองใหญ่ล่าง (ใช้เมื่ออยากให้อ่านต่อกันเป็นประโยค)
"""
import argparse, json, os, re, subprocess, sys

# --- ค่าสไตล์ ดูที่มาของตัวเลขได้ใน references/style.md ---
YELLOW = r"\c&H0025D9FF&"          # RGB 255,217,37 ดูดจากคลิปอ้างอิงจริง
WHITE = r"\c&H00FFFFFF&"
FS_BIG, FS_SMALL = 96, 60
POP_ANIM = (r"\fad(90,90)\fscx55\fscy55"
            r"\t(0,130,\fscx106\fscy106)\t(130,230,\fscx100\fscy100)")

DEFAULTS = {"start": 0.0, "width": 1080, "height": 1920, "min_silence": 0.90,
            "silence_pad": 0.18, "loudnorm": True, "band": None, "hook": None,
            "pops": [], "srt": None, "crf": 19, "fps": 30}


def ffmpeg_bin():
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


def detect_silences(ff, src, start, end, min_sil, pad):
    """คืน (รายการช่วงที่เก็บไว้, จำนวนรอยตัด) — ตัดเฉพาะแกนกลางของช่วงเงียบ"""
    err = subprocess.run([ff, "-hide_banner", "-i", src,
                          "-af", "silencedetect=noise=-33dB:d=0.30", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    sil, cur = [], None
    for m in re.finditer(r"silence_(start|end): ([\d.]+)", err):
        kind, val = m.group(1), float(m.group(2))
        if kind == "start":
            cur = val
        elif cur is not None:
            sil.append((cur, val))
            cur = None

    cuts = []
    for s, e in sil:
        s, e = max(s, start), min(e, end)
        if e - s >= min_sil and (e - pad) - (s + pad) > 0.05:
            cuts.append((s + pad, e - pad))
    cuts.sort()

    keeps, t = [], start
    for a, b in cuts:
        if a > t:
            keeps.append((t, a))
        t = b
    if t < end:
        keeps.append((t, end))
    return [(a, b) for a, b in keeps if b - a > 0.08], len(cuts)


def timemap(keeps):
    """เวลาบนคลิปต้นฉบับ -> เวลาบนคลิปที่ตัดแล้ว (ข้อความต้องแปลงผ่านตัวนี้เสมอ)"""
    def to_out(ts):
        acc = 0.0
        for a, b in keeps:
            if ts < a:
                return acc
            if ts <= b:
                return acc + (ts - a)
            acc += b - a
        return acc
    return to_out


def tc(s):
    return f"{int(s // 3600)}:{int(s % 3600 // 60):02d}:{s % 60:05.2f}"


def build_ass(cfg, to_out, path):
    w, h = cfg["width"], cfg["height"]
    # ข้อความล่างวางให้ก้นตัวอักษรอยู่เหนือแถบ UI ของ TikTok (ประมาณ 17% ล่างสุด)
    pop_y = int(h * 0.828)
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {w}
PlayResY: {h}
ScaledBorderAndShadow: yes
WrapStyle: 2
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Hook,Kanit SemiBold,64,&H00FFFFFF,&H00FFFFFF,&H00000000,&HC8000000,0,0,0,0,100,100,0,0,1,5,3,8,30,30,20,1
Style: Band,Kanit Medium,52,&H00FFFFFF,&H00FFFFFF,&H00000000,&HC8000000,0,0,0,0,100,100,0,0,1,4,2,8,30,30,20,1
Style: Key,Kanit SemiBold,{FS_BIG},&H0025D9FF,&H0025D9FF,&H00000000,&HC8000000,0,0,0,0,100,100,0,0,1,7,5,2,30,30,20,1
Style: Sub,Kanit SemiBold,{FS_SMALL},&H00FFFFFF,&H00FFFFFF,&H00000000,&HC8000000,0,0,0,0,100,100,0,0,1,5,3,2,60,60,20,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    hook = cfg.get("hook")
    if hook:
        lines.append(
            f"Dialogue: 1,{tc(to_out(hook['start']))},{tc(to_out(hook['end']))},Hook,,0,0,0,,"
            + r"{\an8\pos(" + f"{w//2},30" + r")\fad(150,150)}"
            + "{" + WHITE + "}" + hook["line1"] + r"\N"
            + "{" + YELLOW + r"\fs" + str(FS_BIG) + "}" + hook["line2"])
    if cfg.get("band"):
        band_from = hook["end"] if hook else cfg["start"]
        lines.append(
            f"Dialogue: 0,{tc(to_out(band_from))},{tc(to_out(cfg['end']))},Band,,0,0,0,,"
            + r"{\an8\pos(" + f"{w//2},64" + r")\fad(200,200)\alpha&H3C&}"
            + "{" + WHITE + "}" + cfg["band"])
    for p in cfg.get("pops", []):
        big = "{" + YELLOW + r"\fs" + str(FS_BIG) + "}" + p["big"]
        small = "{" + WHITE + r"\fs" + str(FS_SMALL) + "}" + p["small"]
        top, bot = (big, small) if p.get("layout", "YW") == "YW" else (small, big)
        lines.append(
            f"Dialogue: 2,{tc(to_out(p['start']))},{tc(to_out(p['end']))},Key,,0,0,0,,"
            + r"{\an2\pos(" + f"{w//2},{pop_y}" + r")" + POP_ANIM + "}" + top + r"\N" + bot)
    open(path, "w", encoding="utf-8").write(head + "\n".join(lines) + "\n")
    return len(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--ass-only", action="store_true", help="สร้างไฟล์ .ass อย่างเดียว ไม่เรนเดอร์")
    a = ap.parse_args()

    cfg = {**DEFAULTS, **json.load(open(a.config, encoding="utf-8"))}
    base = os.path.dirname(os.path.abspath(a.config)) or "."
    resolve = lambda p: p if os.path.isabs(p) else os.path.join(base, p)
    src, out = resolve(cfg["source"]), resolve(cfg["output"])
    ass = os.path.splitext(out)[0] + ".ass"
    fontsdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "fonts")

    ff = ffmpeg_bin()
    keeps, n_cuts = detect_silences(ff, src, cfg["start"], cfg["end"],
                                    cfg["min_silence"], cfg["silence_pad"])
    span = cfg["end"] - cfg["start"]
    kept = sum(b - a_ for a_, b in keeps)
    print(f"ตัดช่วงเงียบ {n_cuts} จุด  ประหยัด {span - kept:.2f} วิ  "
          f"({span:.2f} -> {kept:.2f} วิ)")

    n = build_ass(cfg, timemap(keeps), ass)
    print(f"เขียนข้อความ {n} รายการลง {ass}")
    if a.ass_only:
        return

    fc = []
    for i, (s, e) in enumerate(keeps):
        fc.append(f"[0:v]trim={s:.3f}:{e:.3f},setpts=PTS-STARTPTS[v{i}]")
        fc.append(f"[0:a]atrim={s:.3f}:{e:.3f},asetpts=PTS-STARTPTS[a{i}]")
    pairs = "".join(f"[v{i}][a{i}]" for i in range(len(keeps)))
    fc.append(f"{pairs}concat=n={len(keeps)}:v=1:a=1[vc][ac]")

    esc = lambda p: p.replace("\\", "/").replace(":", r"\:")
    vchain = (f"[vc]scale={cfg['width']}:{cfg['height']}:flags=lanczos")
    if cfg.get("srt"):
        vchain += (f",subtitles={esc(resolve(cfg['srt']))}:fontsdir={esc(fontsdir)}"
                   f":force_style='FontName=Kanit SemiBold,Fontsize={FS_SMALL},"
                   f"PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=5,Shadow=3,"
                   f"Alignment=2,MarginV={int(cfg['height']*0.10)}'")
    vchain += f",ass={esc(ass)}:fontsdir={esc(fontsdir)},format=yuv420p[vout]"
    fc.append(vchain)
    fc.append("[ac]" + ("loudnorm=I=-14:TP=-1.5:LRA=11," if cfg["loudnorm"] else "")
              + "aresample=48000[aout]")

    filt = os.path.splitext(out)[0] + ".filter.txt"
    open(filt, "w", encoding="utf-8").write(";\n".join(fc))

    cmd = [ff, "-hide_banner", "-y", "-i", src, "-filter_complex_script", filt,
           "-map", "[vout]", "-map", "[aout]",
           "-c:v", "libx264", "-preset", "medium", "-crf", str(cfg["crf"]),
           "-profile:v", "high", "-level", "4.1", "-pix_fmt", "yuv420p",
           "-r", str(cfg["fps"]), "-g", str(cfg["fps"] * 2), "-movflags", "+faststart",
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:], file=sys.stderr)
        sys.exit("เรนเดอร์ไม่สำเร็จ")
    print(f"เรนเดอร์เสร็จ: {out}  ({os.path.getsize(out)/1e6:.1f} MB)")
    print("อย่าลืมตรวจงานตามหัวข้อ 'ตรวจก่อนส่ง' ใน SKILL.md")


if __name__ == "__main__":
    main()
