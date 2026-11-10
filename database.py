import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'skincare.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        brand TEXT NOT NULL,
        name TEXT NOT NULL,
        thai_name TEXT,
        category TEXT NOT NULL,
        step_order INTEGER NOT NULL,
        price REAL NOT NULL,
        original_price REAL,
        size TEXT,
        description TEXT,
        image_url TEXT,
        skin_types TEXT, -- JSON array: ["oily", "dry", "combination", "sensitive", "normal"]
        skin_concerns TEXT, -- JSON array: ["acne", "dark_spots", "aging", "pores", "dehydration"]
        key_ingredients TEXT, -- JSON array: [{"name": "...", "desc": "..."}]
        how_to_use TEXT,
        routine_time TEXT, -- "AM", "PM", "BOTH"
        rating REAL DEFAULT 4.8,
        reviews_count INTEGER DEFAULT 120,
        stock_siam INTEGER DEFAULT 15,
        stock_ladprao INTEGER DEFAULT 10,
        stock_mega INTEGER DEFAULT 8,
        is_bestseller INTEGER DEFAULT 0
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stores (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        location TEXT NOT NULL,
        hours TEXT NOT NULL,
        phone TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_code TEXT UNIQUE NOT NULL,
        order_type TEXT NOT NULL, -- "pickup" or "delivery"
        store_id TEXT,
        pickup_date TEXT,
        pickup_time TEXT,
        customer_name TEXT NOT NULL,
        customer_phone TEXT NOT NULL,
        customer_email TEXT,
        shipping_address TEXT,
        items TEXT NOT NULL, -- JSON array of items
        subtotal REAL NOT NULL,
        discount REAL DEFAULT 0,
        total REAL NOT NULL,
        payment_method TEXT DEFAULT "promptpay",
        payment_status TEXT DEFAULT "paid",
        order_status TEXT DEFAULT "ready_for_pickup", -- "pending", "preparing", "ready_for_pickup", "completed", "cancelled"
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()

    # Seed Stores if empty
    cursor.execute('SELECT COUNT(*) FROM stores')
    if cursor.fetchone()[0] == 0:
        stores = [
            (
                'siam',
                'สาขา สยามสแควร์วัน (Siam Square One)',
                'ชั้น 2 โซน Fashion Walk (ใกล้ทางเชื่อม BTS สยาม)',
                'เปิดทุกวัน 10:00 - 21:00 น.',
                '02-115-9981'
            ),
            (
                'ladprao',
                'สาขา เซ็นทรัล ลาดพร้าว (Central Ladprao)',
                'ชั้น G โซน Beauty Avenue ฝั่งทางออก MRT',
                'เปิดทุกวัน 10:00 - 21:30 น.',
                '02-541-1822'
            ),
            (
                'mega',
                'สาขา เมกาบางนา (Mega Bangna)',
                'ชั้น 1 Mega Wellness Zone (ใกล้ Big C Extra)',
                'เปิดทุกวัน 10:00 - 22:00 น.',
                '02-105-1934'
            )
        ]
        cursor.executemany('INSERT INTO stores VALUES (?, ?, ?, ?, ?)', stores)
        conn.commit()

    # Seed Products if empty
    cursor.execute('SELECT COUNT(*) FROM products')
    if cursor.fetchone()[0] == 0:
        products = [
            # Cleansers (Step 1)
            (
                'CeraVe',
                'Foaming Cleanser for Normal to Oily Skin',
                'เจลล้างหน้าสูตรฟอง สำหรับผิวมัน-ผิวผสม เป็นสิวง่าย',
                'Cleanser',
                1,
                490.0,
                550.0,
                '236 ml',
                'เจลทำความสะอาดผิวหน้าและผิวกายสำหรับผิวธรรมดาถึงผิวมัน อ่อนโยนด้วยเซราไมด์จำเป็น 3 ชนิดและไนอะซินาไมด์ ไม่ทำให้ผิวแห้งตึง',
                'https://images.unsplash.com/photo-1556228720-195a672e8a03?auto=format&fit=crop&w=700&q=80',
                json.dumps(['oily', 'combination', 'sensitive']),
                json.dumps(['acne', 'pores']),
                json.dumps([
                    {'name': 'Ceramides 1, 3, 6-II', 'desc': 'ฟื้นบำรุงและเสริมปราการผิวให้แข็งแรง'},
                    {'name': 'Niacinamide (Vitamin B3)', 'desc': 'ช่วยปลอบประโลมผิว ลดรอยแดง และความมันส่วนเกิน'},
                    {'name': 'Hyaluronic Acid', 'desc': 'ช่วยกักเก็บความชุ่มชื้นตามธรรมชาติของผิว'}
                ]),
                'ลูบไล้โฟมลงบนผิวที่เปียก นวดวนเบา ๆ แล้วล้างออกด้วยน้ำสะอาด ใช้ได้ทั้งเช้าและเย็น',
                'BOTH',
                4.9,
                380,
                25, 18, 12,
                1
            ),
            (
                'La Roche-Posay',
                'Effaclar Purifying Foaming Gel',
                'เจลล้างหน้าสูตรอ่อนโยน ดูแลปัญหาสิวและผิวมันระคายเคืองง่าย',
                'Cleanser',
                1,
                820.0,
                890.0,
                '200 ml',
                'ทำความสะอาดผิวอย่างล้ำลึก ขจัดสิ่งสกปรกและความมันส่วนเกินอย่างอ่อนโยน ด้วยสูตร pH 5.5 ผสานน้ำแร่ธรรมชาติ ลา โรช-โพเซย์',
                'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?auto=format&fit=crop&w=700&q=80',
                json.dumps(['oily', 'combination', 'sensitive']),
                json.dumps(['acne', 'pores']),
                json.dumps([
                    {'name': 'Zinc PCA', 'desc': 'ควบคุมความมันส่วนเกิน ลดสาเหตุการเกิดสิว'},
                    {'name': 'Thermal Spring Water', 'desc': 'น้ำแร่ธรรมชาติปลอบประโลมผิว ลดการระคายเคือง'}
                ]),
                'บีบเจลลงบนฝ่ามือผสมน้ำเล็กน้อยให้เกิดฟอง นวดเบาๆ ทั่วใบหน้า แล้วล้างออก',
                'BOTH',
                4.8,
                245,
                18, 14, 10,
                1
            ),
            (
                'Round Lab',
                '1025 Dokdo Cleanser',
                'โฟมล้างหน้าน้ำแร่เกาะด็อกโด ฟองละเอียด ค่า pH อ่อนโยนต่อผิว',
                'Cleanser',
                1,
                420.0,
                480.0,
                '150 ml',
                'โฟมล้างหน้าคลีนซิ่งครีมนุ่มละมุน อุดมด้วยแร่ธาตุ 72 ชนิดจากน้ำทะเลลึกเกาะด็อกโด ช่วยกักเก็บความชุ่มชื้น ขจัดฝุ่นละอองขนาดเล็ก',
                'https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?auto=format&fit=crop&w=700&q=80',
                json.dumps(['dry', 'normal', 'sensitive']),
                json.dumps(['dehydration', 'redness']),
                json.dumps([
                    {'name': 'Deep Sea Water', 'desc': 'แร่ธาตุเข้มข้นช่วยคงสมดุลความชุ่มชื้น'},
                    {'name': 'Panthenol & Allantoin', 'desc': 'ปลอบประโลมผิวอย่างอ่อนโยน สมานผิว'}
                ]),
                'ตีฟองให้ฟูนุ่ม นวดวนเบา ๆ ทั่วใบหน้าแล้วล้างออกด้วยน้ำอุ่น',
                'BOTH',
                4.8,
                190,
                20, 15, 14,
                0
            ),

            # Toners / Essences (Step 2)
            (
                'Anua',
                'Heartleaf 77% Soothing Toner',
                'โทนเนอร์ใบฮาร์ทลีฟเข้มข้น 77% ปลอบประโลมผิวเป็นสิวและลดรอยแดง',
                'Toner',
                2,
                590.0,
                690.0,
                '250 ml',
                'โทนเนอร์ยอดนิยมอันดับ 1 ในเกาหลี อุดมด้วยสารสกัด Heartleaf 77% ช่วยลดการอักเสบ ปลอบประโลมผิวระคายเคือง และเตรียมผิวรับการบำรุง',
                'https://images.unsplash.com/photo-1608248597359-009581781297?auto=format&fit=crop&w=700&q=80',
                json.dumps(['oily', 'combination', 'sensitive', 'normal']),
                json.dumps(['acne', 'redness', 'pores']),
                json.dumps([
                    {'name': 'Heartleaf Extract 77%', 'desc': 'ลดอาการอักเสบ ปลอบประโลมผิวแพ้ง่าย'},
                    {'name': 'Centella Asiatica', 'desc': 'ฟื้นฟูผิว ลดรอยสิว สมานแผลสิว'}
                ]),
                'เทลงบนสำลีแล้วเช็ดเบา ๆ ทั่วใบหน้า หรือเทลงบนฝ่ามือแล้วตบเบา ๆ หรือทำเป็น Toner Mask 5-10 นาที',
                'BOTH',
                4.9,
                520,
                30, 22, 16,
                1
            ),
            (
                'Paula\'s Choice',
                'Skin Perfecting 2% BHA Liquid Exfoliant',
                'น้ำตบผลัดเซลล์ผิว BHA 2% ลดสิวเสี้ยน สิวอุดตัน กระชับรูขุมขน',
                'Toner',
                2,
                1250.0,
                1350.0,
                '118 ml',
                'ไอคอนิก BHA ขจัดเซลล์ผิวที่ตายแล้วอย่างล้ำลึกถึงภายในรูขุมขน ช่วยให้รูขุมขนกระชับ ผิวเรียบเนียน สิวเสี้ยนและสิวอุดตันลดลงชัดเจน',
                'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?auto=format&fit=crop&w=700&q=80',
                json.dumps(['oily', 'combination']),
                json.dumps(['acne', 'pores']),
                json.dumps([
                    {'name': 'Salicylic Acid 2% (BHA)', 'desc': 'ละลายน้ำมันส่วนเกินในรูขุมขน สลายสิวอุดตัน'},
                    {'name': 'Green Tea Extract', 'desc': 'สารต้านอนุมูลอิสระ ปกป้องผิวจากการระคายเคือง'}
                ]),
                'เทใส่สำลีหรือมือ ลูบไล้ทั่วใบหน้าช่วงเย็นหลังล้างหน้า เริ่มใช้สัปดาห์ละ 2-3 ครั้ง (ไม่ต้องล้างออก)',
                'PM',
                4.9,
                410,
                12, 8, 5,
                1
            ),
            (
                'Torriden',
                'DIVE-IN Low Molecular Hyaluronic Acid Toner',
                'โทนเนอร์ไฮยาลูรอน 5 โมเลกุล เติมน้ำให้ผิวอิ่มฟู ฉ่ำน้ำขั้นสุด',
                'Toner',
                2,
                550.0,
                620.0,
                '300 ml',
                'โทนเนอร์เติมความชุ่มชื้นลึกถึงผิวชั้นใน ด้วยกรดไฮยาลูรอนโมเลกุลต่ำ 5 ชนิด เนื้อสัมผัสบางเบา ไม่เหนียวเหนอะหนะ เผยผิวโกลว์สุขภาพดี',
                'https://images.unsplash.com/photo-1617897903246-719242758050?auto=format&fit=crop&w=700&q=80',
                json.dumps(['dry', 'combination', 'normal', 'sensitive']),
                json.dumps(['dehydration', 'redness']),
                json.dumps([
                    {'name': '5D Complex Hyaluronic Acid', 'desc': 'ซึมลึกเติมความชุ่มชื้นทุกระดับชั้นผิว'},
                    {'name': 'Malachite Extract', 'desc': 'แร่มาลาไคต์ให้สีฟ้าธรรมชาติและต้านอนุมูลอิสระ'}
                ]),
                'หยดลงบนฝ่ามือแล้วกดเบา ๆ ทั่วใบหน้า สามารถทาซ้ำได้ 2-3 เลเยอร์เพื่อความชุ่มชื้นขั้นสุด',
                'BOTH',
                4.8,
                230,
                18, 14, 11,
                0
            ),

            # Serums (Step 3)
            (
                'The Ordinary',
                'Niacinamide 10% + Zinc 1%',
                'เซรั่มลดรอยสิว คุมมัน และกระชับรูขุมขนยอดนิยมระดับโลก',
                'Serum',
                3,
                380.0,
                450.0,
                '30 ml',
                'สูตรวิตามินและแร่ธาตุเข้มข้นสูง ช่วยลดรอยแดง รอยดำจากสิว ควบคุมความมันบนใบหน้า และปรับสภาพผิวให้สม่ำเสมอเรียบเนียน',
                'https://images.unsplash.com/photo-1601049541289-9b1b7bbbfe19?auto=format&fit=crop&w=700&q=80',
                json.dumps(['oily', 'combination', 'normal']),
                json.dumps(['acne', 'dark_spots', 'pores']),
                json.dumps([
                    {'name': 'Niacinamide 10%', 'desc': 'ลดเลือนรอยสิว ปรับสีผิวให้กระจ่างใส'},
                    {'name': 'Zinc PCA 1%', 'desc': 'ลดความมันส่วนเกิน ยับยั้งแบคทีเรีย'}
                ]),
                'ทาทั่วใบหน้า เช้าและเย็น ก่อนลงมอยส์เจอไรเซอร์',
                'BOTH',
                4.7,
                680,
                35, 25, 20,
                1
            ),
            (
                'Beauty of Joseon',
                'Glow Deep Serum : Rice + Arbutin',
                'เซรั่มข้าวเกาหลีและอาร์บูติน จัดการฝ้า กระ จุดด่างดำ ผิวโกลว์ใส',
                'Serum',
                3,
                480.0,
                550.0,
                '30 ml',
                'เซรั่มสูตรดั้งเดิมฮันบัง ผสานน้ำรำข้าว 68% และอัลฟาอาร์บูติน 2% ช่วยลดการสร้างเม็ดสีเมลานิน ปรับผิวให้สว่างกระจ่างใสอย่างเป็นธรรมชาติ',
                'https://images.unsplash.com/photo-1616683693504-3ea7e9ad6fec?auto=format&fit=crop&w=700&q=80',
                json.dumps(['dry', 'normal', 'combination', 'sensitive']),
                json.dumps(['dark_spots', 'dehydration']),
                json.dumps([
                    {'name': 'Rice Bran Water 68%', 'desc': 'อุดมด้วยสารอาหารบำรุงผิว เติมความเนียนนุ่ม'},
                    {'name': 'Alpha-Arbutin 2%', 'desc': 'ยับยั้งเม็ดสีเมลานิน ลดจุดด่างดำ รอยฝ้ากระจางลง'}
                ]),
                'หยดเซรั่ม 2-3 หยด ลูบไล้ทั่วใบหน้าและลำคอ ใช้ได้ทั้งเช้าและก่อนนอน',
                'BOTH',
                4.9,
                340,
                20, 16, 12,
                1
            ),
            (
                'Kiehl\'s',
                'Retinol Skin-Renewing Daily Micro-Dose Serum',
                'เรตินอลสูตรอ่อนโยน ลดเลือนริ้วรอย ผิวกระชับ ไม่ระคายเคือง',
                'Serum',
                3,
                2950.0,
                3300.0,
                '50 ml',
                'นวัตกรรมเรตินอลในปริมาณที่แม่นยำ ผสานเซราไมด์และเปปไทด์ ช่วยเร่งการผลัดเซลล์ผิวใหม่ ลดเลือนริ้วรอย ร่องลึก ให้ผิวดูกระชับและอ่อนเยาว์',
                'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?auto=format&fit=crop&w=700&q=80',
                json.dumps(['dry', 'normal', 'combination', 'oily']),
                json.dumps(['aging', 'pores']),
                json.dumps([
                    {'name': 'Pure Retinol', 'desc': 'ผลัดเซลล์ผิว ลดเลือนริ้วรอย ปรับผิวเรียบเนียน'},
                    {'name': 'Peptides', 'desc': 'เสริมโครงสร้างอีลาสติน ให้ผิวเฟิร์มกระชับ'},
                    {'name': 'Ceramides', 'desc': 'เสริมเกราะป้องกันผิว ป้องกันผิวแห้งลอก'}
                ]),
                'กด 1 ปั๊มทาทั่วใบหน้าช่วงค่ำ หลีกเลี่ยงรอบดวงตาและริมฝีปาก (ตอนเช้าต้องทากันแดดทุกครั้ง)',
                'PM',
                4.9,
                290,
                10, 6, 4,
                1
            ),
            (
                'Cosrx',
                'Advanced Snail 96 Mucin Power Essence',
                'เอสเซนส์เมือกหอยทากเข้มข้น 96% ซ่อมแซมผิว ชุ่มชื้นล้ำลึก',
                'Serum',
                3,
                490.0,
                590.0,
                '100 ml',
                'เอสเซนส์เมือกหอยทากธรรมชาติเข้มข้น 96% ซึมซาบไว ซ่อมแซมผิวเสีย ปลอบประโลมผิวแห้งกร้าน และเติมความยืดหยุ่นให้ผิวดูฉ่ำวาว',
                'https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?auto=format&fit=crop&w=700&q=80',
                json.dumps(['dry', 'sensitive', 'combination', 'normal']),
                json.dumps(['dehydration', 'redness', 'aging']),
                json.dumps([
                    {'name': 'Snail Secretion Filtrate 96%', 'desc': 'สมานผิว ฟื้นฟูเกราะป้องกันผิว ชุ่มชื้นยาวนาน'},
                    {'name': 'Sodium Hyaluronate', 'desc': 'อุ้มน้ำไว้ใต้ผิว ผิวเปล่งปลั่งสุขภาพดี'}
                ]),
                'กด 1-2 ปั๊ม ตบเบา ๆ ให้ทั่วผิวหน้าจนซึมเข้าสู่ผิว',
                'BOTH',
                4.8,
                460,
                25, 20, 15,
                0
            ),

            # Moisturizers (Step 4)
            (
                'CeraVe',
                'Moisturising Cream for Dry to Very Dry Skin',
                'ครีมบำรุงผิวหน้าและผิวกาย ล็อคความชุ่มชื้นยาวนาน 24 ชั่วโมง',
                'Moisturizer',
                4,
                695.0,
                795.0,
                '340 g',
                'เทคโนโลยี MVE ปลดปล่อยความชุ่มชื้นต่อเนื่องยาวนาน พร้อมเซราไมด์จำเป็น 3 ชนิด ฟื้นฟูปราการปกป้องผิวแห้งลอกให้กลับมานุ่มชุ่มชื้น',
                'https://images.unsplash.com/photo-1556228720-195a672e8a03?auto=format&fit=crop&w=700&q=80',
                json.dumps(['dry', 'sensitive', 'normal']),
                json.dumps(['dehydration', 'redness']),
                json.dumps([
                    {'name': 'Essential Ceramides (1, 3, 6-II)', 'desc': 'กักเก็บความชุ่มชื้น ฟื้นฟูปราการผิว'},
                    {'name': 'MVE Technology', 'desc': 'ค่อยๆ ปล่อยสารบำรุงเข้าสู่ผิวตลอดวัน'}
                ]),
                'ทาบำรุงผิวหน้าและผิวกายได้บ่อยตามต้องการ ทั้งเช้าและก่อนนอน',
                'BOTH',
                4.9,
                550,
                28, 20, 18,
                1
            ),
            (
                'La Roche-Posay',
                'Cicaplast Baume B5+ Ultra-Repairing Soothing Balm',
                'บาล์มฟื้นบำรุงผิวเข้มข้น ปลอบประโลมผิวระคายเคืองและรอยแดงทันที',
                'Moisturizer',
                4,
                650.0,
                720.0,
                '40 ml',
                'บาล์มบำรุงสูตรปรับปรุงใหม่ เสริมด้วยสาร Tribioma พรีไบโอติก ฟื้นบำรุงผิวที่มีปัญหาแห้ง แตก ลอก แดง และอาการระคายเคืองได้อย่างรวดเร็ว',
                'https://images.unsplash.com/photo-1617897903246-719242758050?auto=format&fit=crop&w=700&q=80',
                json.dumps(['dry', 'sensitive', 'combination', 'oily']),
                json.dumps(['redness', 'acne', 'dehydration']),
                json.dumps([
                    {'name': 'Madecassoside & Tribioma', 'desc': 'สารสกัดจากใบบัวบกบริสุทธิ์ ฟื้นฟูปราการผิว'},
                    {'name': 'Panthenol 5% (Vitamin B5)', 'desc': 'ลดอาการคัน ระคายเคือง แสบแดง'}
                ]),
                'ทาให้ทั่วใบหน้าหรือแต้มเฉพาะบริเวณที่ระคายเคือง สามารถใช้ได้ทั้งเช้าและก่อนนอน',
                'BOTH',
                4.9,
                480,
                22, 18, 14,
                1
            ),
            (
                'Torriden',
                'DIVE-IN Soothing Cream',
                'ซูทติ้งครีมเจลฟ้า ล็อคผิวฉ่ำน้ำ เย็นสดชื่น ไม่หนักหน้า สำหรับผิวมัน',
                'Moisturizer',
                4,
                590.0,
                650.0,
                '100 ml',
                'มอยส์เจอไรเซอร์เนื้อเจลบางเบา ซึมไวทันที ไม่ทิ้งความมันหรือความเหนียวเหนอะหนะ เติมความชุ่มชื้นและปลอบประโลมผิวที่เหนื่อยล้า',
                'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?auto=format&fit=crop&w=700&q=80',
                json.dumps(['oily', 'combination', 'sensitive']),
                json.dumps(['dehydration', 'pores', 'acne']),
                json.dumps([
                    {'name': '5D Complex Hyaluronic Acid', 'desc': 'กักเก็บความชุ่มชื้นล้ำลึก'},
                    {'name': 'Trehalose', 'desc': 'ป้องกันการสูญเสียน้ำออกจากผิว'}
                ]),
                'ทาในขั้นตอนสุดท้ายของการบำรุงผิวหน้า ทาได้ทั้งเช้าและเย็น',
                'BOTH',
                4.8,
                210,
                16, 12, 10,
                0
            ),

            # Sunscreens (Step 5)
            (
                'Beauty of Joseon',
                'Relief Sun : Rice + Probiotics SPF50+ PA++++',
                'ครีมกันแดดออร์แกนิกข้าวเกาหลี เนื้อนุ่มเกลี่ยง่าย ไม่วอก ไม่เป็นคราบ',
                'Sunscreen',
                5,
                490.0,
                550.0,
                '50 ml',
                'กันแดดยอดฮิตทั่วโลก เนื้อครีมชุ่มชื้นคล้ายมอยส์เจอไรเซอร์ สารสกัดจากข้าว 30% และสารสกัดจากธัญพืชหมัก ป้องกันรังสียูวีได้อย่างมีประสิทธิภาพสูง',
                'https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?auto=format&fit=crop&w=700&q=80',
                json.dumps(['dry', 'normal', 'combination', 'sensitive']),
                json.dumps(['dark_spots', 'aging', 'dehydration']),
                json.dumps([
                    {'name': 'Rice Extract 30%', 'desc': 'อุดมด้วยวิตามิน B, C, E ช่วยให้ผิวนุ่มชุ่มชื้น'},
                    {'name': 'Grain Fermented Extracts', 'desc': 'โพรไบโอติกส์เสริมความแข็งแรงให้ผิว'}
                ]),
                'ทาทั่วใบหน้าและลำคอเป็นขั้นตอนสุดท้ายก่อนแต่งหน้า ในตอนเช้าอย่างน้อย 15 นาทีก่อนออกแดด',
                'AM',
                4.9,
                750,
                40, 30, 25,
                1
            ),
            (
                'La Roche-Posay',
                'Anthelios UVMune 400 Oil Control Fluid SPF50+',
                'กันแดดคุมมันเนื้อฟลูอิด ปกป้องรังสี Ultra Long UVA สูงสุด',
                'Sunscreen',
                5,
                1350.0,
                1490.0,
                '50 ml',
                'สุดยอดนวัตกรรมกันแดด ปกป้องผิวลึกถึงระดับดีเอ็นเอด้วยฟิลเตอร์ Mexoryl 400 คุมมันยาวนาน 12 ชั่วโมง ไม่เยิ้ม ไม่เหนียวเหนอะหนะ สบายผิวสุดๆ',
                'https://images.unsplash.com/photo-1556228720-195a672e8a03?auto=format&fit=crop&w=700&q=80',
                json.dumps(['oily', 'combination', 'sensitive']),
                json.dumps(['acne', 'pores', 'aging', 'dark_spots']),
                json.dumps([
                    {'name': 'Mexoryl 400', 'desc': 'ปกป้องรังสี Long UVA ถึง 400nm ป้องกันฝ้าและริ้วรอยลึก'},
                    {'name': 'Airlicium', 'desc': 'อนุภาคดักจับความมันส่วนเกิน ให้ผิวแมตต์ไม่เหนอะหนะ'}
                ]),
                'เขย่าขวดก่อนใช้ ทาทั่วใบหน้าและลำคอทุกเช้าก่อนออกแดด',
                'AM',
                4.9,
                620,
                24, 18, 15,
                1
            )
        ]

        query = '''
        INSERT INTO products (
            brand, name, thai_name, category, step_order, price, original_price, size,
            description, image_url, skin_types, skin_concerns, key_ingredients,
            how_to_use, routine_time, rating, reviews_count,
            stock_siam, stock_ladprao, stock_mega, is_bestseller
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        cursor.executemany(query, products)
        conn.commit()

    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized and seeded successfully!")
