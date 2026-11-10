# LUMIÈRE SKIN LAB & RETAIL
เว็บแอปพลิเคชันร้านขายสกินแคร์มัลติแบรนด์ สไตล์คลีนมินิมอล พร้อมระบบวิเคราะห์สภาพผิวเฉพาะบุคคล และระบบสั่งออนไลน์รับสินค้าที่หน้าร้าน (Click & Collect)

---

## 🌟 จุดเด่นและฟีเจอร์หลัก (Key Features)

1. **สกินแคร์หลากแบรนด์ชั้นนำ (Multi-Brand Skincare)**
   - รวมสินค้าแบรนด์ยอดนิยมระดับโลก เช่น CeraVe, La Roche-Posay, Anua, Beauty of Joseon, The Ordinary, Kiehl's, Paula's Choice, Torriden, Round Lab, Cosrx
   - แยกตามหมวดหมู่รูทีนครบวงจร: คลีนเซอร์ (Cleanser), โทนเนอร์ (Toner), เซรั่ม (Serum), มอยส์เจอไรเซอร์ (Moisturizer), ครีมกันแดด (Sunscreen)
   - ข้อมูลเจาะลึก: รายละเอียดส่วนผสมเด่น (Active Ingredients), วิธีและลำดับการใช้, สภาพผิวที่เหมาะ

2. **ระบบระบุสภาพผิว & แนะนำสกินแคร์ (Personalized Skin Match Finder)**
   - เลือกระบุ **สภาพผิว** (ผิวมัน, ผิวแห้ง, ผิวผสม, บอบบางแพ้ง่าย, ผิวธรรมดา)
   - เลือกระบุ **ปัญหาผิวที่กังวล** (สิวอุดตัน/อักเสบ, รูขุมขนกว้าง, รอยสิว/ฝ้ากระ, ผิวขาดน้ำ, ริ้วรอย, รอยแดง)
   - ระบบประมวลผลจัดเซตรูทีน 5 ขั้นตอน (เช้า - เย็น) ที่เข้ากับผิวผู้ใช้โดยเฉพาะ พร้อมคำแนะนำจากผู้เชี่ยวชาญ
   - ปุ่มเลือกซื้อแยกชิ้น หรือ **"สั่งซื้อทั้งเซต 5 ชิ้น" รับส่วนลดพิเศษ 10%**

3. **สั่งออนไลน์และรับสินค้าที่หน้าร้านได้ทันที (Store Pickup / Click & Collect)**
   - เลือกระหว่าง:
     - **รับที่หน้าร้าน (Store Pickup - ไม่มีค่าส่ง)**: เลือกสาขา (สยามสแควร์วัน, เซ็นทรัล ลาดพร้าว, เมกาบางนา), เลือกวันและช่วงเวลาที่สะดวกรับ
     - **จัดส่งถึงบ้าน (Standard Delivery)**
   - ออก **บัตรรับสินค้าดิจิทัล (Digital Store Pickup Pass)** พร้อม Order Code และ QR Code สำหรับนำไปยื่นรับของที่หน้าร้าน

4. **ระบบสำหรับพนักงานหน้าร้าน & สต็อกสินค้า (`/admin`)**
   - ค้นหาออเดอร์ด้วยรหัสคำสั่งซื้อ หรือเบอร์โทรลูกค้า
   - อัปเดตสถานะการส่งมอบสินค้า (รอเตรียมของ $\rightarrow$ พร้อมรับ $\rightarrow$ ส่งมอบของแล้ว)
   - ดูรายงานสต็อกสินค้าคงเหลือแบบ Real-time ของแต่ละสาขา

---

## 🚀 วิธีเปิดใช้งาน (Getting Started)

เซิร์ฟเวอร์เปิดทำงานอยู่ที่:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

หน้าระบบพนักงานหน้าร้าน:
👉 **[http://127.0.0.1:5000/admin](http://127.0.0.1:5000/admin)**

### คำสั่งเปิดรันโปรเจกต์เองในครั้งถัดไป:
```bash
cd c:\075
python app.py
```

---

## 📁 โครงสร้างโปรเจกต์ (Project Structure)
```
c:\075\
├── app.py                   # Flask Application, Routing & API Endpoints
├── database.py              # SQLite Database, Schemas & Initial Seed Data
├── skincare.db              # SQLite Database File
├── requirements.txt         # Dependencies
├── static/
│   ├── css/
│   │   └── custom.css       # Clean Minimalist Styling & Print Layout
│   └── js/
│       └── app.js           # Cart, Skin Match Engine, Filters, Checkout logic
└── templates/
    ├── base.html            # Layout, Header, Cart Drawer & Navigation
    ├── index.html           # Hero, Skin Match Finder, Product Catalog, Store Locations
    ├── order_success.html   # Digital Pickup Pass with QR Code
    └── admin.html           # Staff Order Management & Store Inventory
```
