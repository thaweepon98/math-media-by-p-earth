# รวมสื่อการสอน by P'Earth

เว็บไซต์รวมสื่อการสอน HTML แยกตามรายวิชา สำหรับฉายในห้องเรียนและให้นักเรียนเปิดเอง

- **Live URL**: https://thaweepon98.github.io/math-media-by-p-earth/ (หลัง deploy ครั้งแรก)
- **GitHub repo**: https://github.com/thaweepon98/math-media-by-p-earth
- **ต้นฉบับสื่อ (ที่ทำใหม่/แก้ไข)**: `สื่อการสอนคณิตศาสตร์\รวมสื่อhtml\` — โฟลเดอร์นี้ (`math-media-by-p-earth\`) คือสำเนาที่เผยแพร่

## โครงสร้าง

```
math-media-by-p-earth\
├── index.html          ← หน้าแรก การ์ดรายวิชา (แก้ array SUBJECTS ในสคริปต์)
└── <slug>\              ← 1 โฟลเดอร์ต่อ 1 วิชา (slug เป็นอังกฤษ)
    ├── index.html       ← การ์ดหัวข้อในวิชานั้น (แก้ array TOPICS ในสคริปต์)
    └── <ไฟล์สื่อ>.html   ← ไฟล์สื่อการสอนจริง เปิดตรงๆ ไม่ครอบ iframe
```

ไม่ใช้ manifest.json/fetch() เพราะต้องเปิดไฟล์ตรงๆ ผ่าน double-click ได้ (file://) โดยไม่ต้องรันเซิร์ฟเวอร์ — ข้อมูลการ์ดฝังเป็น JS array ในแต่ละหน้า index.html แทน

**CSS ฝังในตัวไฟล์ (inline `<style>`) ทุกหน้า ไม่ใช้ไฟล์ CSS แยก** — เจอบั๊กจริงว่าบางตัวแสดงผล HTML (เช่น preview pane บางประเภท) โหลด `<link rel="stylesheet" href="ไฟล์แยก">` ไม่สำเร็จ ทำให้หน้าเว็บไม่มีสไตล์เลย แต่ยังรัน `<script>` inline ได้ปกติ — เพื่อความชัวร์ ทุกหน้า index.html จึงคัดลอก CSS เดียวกันฝังไว้ในตัวเอง (เหมือนไฟล์สื่อการสอนอื่นๆ ทั้งหมดในโปรเจกต์นี้ที่ไม่เคยใช้ CSS แยกไฟล์เลย) — **ถ้าจะแก้สี/ธีมทีหลัง ต้องแก้ทุกหน้า index.html ที่มี (ไม่ใช่ไฟล์เดียว)**

## วิธีเพิ่มหัวข้อใหม่ในวิชาเดิม

1. Copy ไฟล์ HTML สื่อใหม่เข้าโฟลเดอร์วิชานั้น (เช่น `math\`)
2. เปิด `math\index.html` เพิ่ม object ใหม่ใน `TOPICS` array (file, title, desc, icon, tags)
3. Commit + push (ดูขั้นตอน deploy ด้านล่าง)

## วิธีจัดกลุ่มหัวข้อย่อยหลายสื่อ (nested topic group)

เมื่อหัวข้อเดียว (เช่น "เซต") มีสื่อมากกว่า 1 ชิ้น ให้ทำเป็นโฟลเดอร์ย่อยที่มี `index.html`
ของตัวเอง (แพทเทิร์นเดียวกับ `math\index.html`) แทนที่จะโชว์การ์ดแยกทุกสื่อในหน้าวิชา —
ตัวอย่างจริง: `math\sets\` (จำนวนสมาชิกของเซต + การดำเนินการของเซต)

1. สร้างโฟลเดอร์ย่อยใต้โฟลเดอร์วิชา (เช่น `math\sets\`) ย้ายไฟล์สื่อที่เกี่ยวข้องเข้าไป
   — **ไม่ต้องแก้ back-link ในไฟล์สื่อ** เพราะ `href="./index.html"` จะยังชี้ไปที่
   `index.html` ในโฟลเดอร์เดียวกับตัวเองเสมอ ซึ่งตอนนี้คือ index.html ของกลุ่มย่อยพอดี
2. สร้าง `<โฟลเดอร์ย่อย>\index.html` โดย copy โครงจาก `math\index.html` แล้วแก้:
   - header title/desc ให้ตรงหัวข้อกลุ่ม
   - crumb กลับ ให้เป็น `href="../index.html"` (กลับไปหน้าวิชา) พร้อมข้อความ "← กลับหน้า<วิชา>"
   - `TOPICS` array ใส่เฉพาะสื่อในกลุ่มนี้ (path เป็น `./<ไฟล์>.html` เหมือนเดิม)
3. ใน `math\index.html` แก้ `TOPICS` array ให้เหลือ **entry เดียว** สำหรับกลุ่มนี้ โดยตั้ง
   `file: "<โฟลเดอร์ย่อย>/index.html"` (การ์ดจะลิงก์เข้าไปที่ index.html ของกลุ่มย่อยแทนไฟล์สื่อโดยตรง)
4. Commit + push

## วิธีเพิ่มวิชาใหม่

1. สร้างโฟลเดอร์ใหม่ระดับ root ด้วย slug ภาษาอังกฤษ (เช่น `thai\`)
2. Copy `math\index.html` ไปเป็น `thai\index.html` แล้วแก้ header/title + array `TOPICS` ให้ตรงวิชาใหม่ (โค้ดไม่ผูกกับวิชา ใช้ซ้ำได้ทันที)
3. เปิด `index.html` (root) เพิ่ม object ใหม่ใน `SUBJECTS` array (slug ต้องตรงชื่อโฟลเดอร์)
4. Commit + push

## Deploy workflow

Repo root ของ git คือโฟลเดอร์นี้เอง (`math-media-by-p-earth\`) — ไม่ต้อง clone/copy เหมือนโปรเจกต์ `แอปสอบบรรจุ` เพราะเป็น repo ใหม่ ไม่มี history เดิมต้อง merge

```
git add .
git commit -m "..."
git push origin main
```

Git credential ใช้ Windows Credential Manager (auth account thaweepon98 อยู่แล้วจากการ push repo thaweepon98.github.io)

GitHub Pages ตั้งค่าที่ Settings → Pages → Source: Deploy from branch `main` / root

**หมายเหตุ**: การสร้าง repo ใหม่/push ครั้งแรกทำให้ repo เป็นสาธารณะและเว็บมองเห็นได้จริง ต้อง confirm กับเจ้าของก่อนทุกครั้งที่จะสร้าง repo ใหม่
