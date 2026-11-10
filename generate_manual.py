import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_shading(cell, color_hex):
    """Set background color of a table cell"""
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading)

def set_cell_margins(cell, top=120, bottom=120, left=160, right=160):
    """Set inner padding of a table cell (in dxa: 20 dxa = 1 pt)"""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_callout_border(cell, color_hex="4A5844"):
    """Set thick left accent border and clear other borders"""
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="none"/><w:left w:val="single" w:sz="24" w:space="0" w:color="{color_hex}"/><w:bottom w:val="none"/><w:right w:val="none"/></w:tcBorders>')
    tcPr.append(borders)

def set_table_borders(table, border_color="E7E2D8"):
    """Set clean subtle borders for table"""
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'<w:tblBorders {nsdecls("w")}><w:top w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/><w:bottom w:val="single" w:sz="6" w:space="0" w:color="4A5844"/><w:left w:val="none"/><w:right w:val="none"/><w:insideH w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/><w:insideV w:val="none"/></w:tblBorders>')
    tblPr.append(borders)

def add_callout(doc, title, text, icon="💡"):
    """Add an aesthetic callout box"""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_shading(cell, "F7F4EE") # Soft Sand
    set_callout_border(cell, "4A5844") # Olive accent
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    run_icon = p.add_run(f"{icon} {title}\n")
    run_icon.font.name = "Tahoma"
    run_icon.font.size = Pt(10)
    run_icon.font.bold = True
    run_icon.font.color.rgb = RGBColor(0x4A, 0x58, 0x44)

    run_text = p.add_run(text)
    run_text.font.name = "Tahoma"
    run_text.font.size = Pt(9.5)
    run_text.font.color.rgb = RGBColor(0x3B, 0x38, 0x36)

    # Empty paragraph after table for spacing
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(4)

def create_manual():
    doc = Document()

    # Page Margins (1 inch all around)
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Set Default Font
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Tahoma'
    normal_style.font.size = Pt(10)
    normal_style.font.color.rgb = RGBColor(0x26, 0x24, 0x22)

    # ----------------------------------------------------
    # COVER / HEADER
    # ----------------------------------------------------
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("LUMIÈRE SKIN LAB & RETAIL")
    r_sub.font.size = Pt(11)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(0x4A, 0x58, 0x44) # Olive

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(4)
    p_title.paragraph_format.space_after = Pt(8)
    r_title = p_title.add_run("คู่มือการใช้งานระบบเว็บไซต์จำหน่ายสกินแคร์\nและการให้บริการสั่งออนไลน์รับสินค้าหน้าร้าน (Click & Collect)")
    r_title.font.size = Pt(18)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0x1A, 0x18, 0x16)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_after = Pt(24)
    r_meta = p_meta.add_run("ระบบสกินแคร์มัลติแบรนด์ • ระบบวิเคราะห์สภาพผิวเฉพาะบุคคล (Personalized Skin Match) • ระบบจัดการพนักงานหน้าร้าน\nเวอร์ชัน 1.0 (อัปเดต: พฤศจิกายน 2026)")
    r_meta.font.size = Pt(9.5)
    r_meta.font.color.rgb = RGBColor(0x78, 0x71, 0x6C)

    # Horizontal Divider
    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_after = Pt(16)
    p_div_border = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="12" w:space="1" w:color="4A5844"/></w:pBdr>')
    p_div._p.get_or_add_pPr().append(p_div_border)

    # Helper function for Section Headings
    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x1A, 0x18, 0x16)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.size = Pt(11.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x4A, 0x58, 0x44)
        return p

    def add_body(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(0x2B, 0x28, 0x26)
        return p

    def add_bullet(bold_prefix, text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        r_bold = p.add_run(bold_prefix + " ")
        r_bold.font.bold = True
        r_bold.font.color.rgb = RGBColor(0x1A, 0x18, 0x16)
        r_text = p.add_run(text)
        r_text.font.color.rgb = RGBColor(0x3B, 0x38, 0x36)
        return p

    # ----------------------------------------------------
    # หมวดที่ 1: บทนำและภาพรวมระบบ
    # ----------------------------------------------------
    add_h1("หมวดที่ 1: บทนำและภาพรวมระบบ (System Overview)")
    add_body("เว็บไซต์ LUMIÈRE SKIN LAB & RETAIL เป็นแพลตฟอร์มพาณิชย์อิเล็กทรอนิกส์ (E-Commerce) ที่พัฒนาขึ้นภายใต้แนวคิด Clean & Minimalist Skincare Studio มุ่งเน้นการคัดสรรสกินแคร์แบรนด์ชั้นนำระดับโลก โดยมีจุดเด่นสำคัญ 3 ประการ คือ การวิเคราะห์สภาพผิวเฉพาะบุคคลเพื่อแนะนำสกินแคร์ที่ตรงจุด, การสั่งซื้อออนไลน์แล้วสามารถแวะรับสินค้าที่หน้าร้านได้ทันที (Click & Collect) ภายใน 1 ชั่วโมง, และระบบการบริหารจัดการสต็อกออเดอร์สำหรับพนักงานหน้าร้าน")

    add_h2("1.1 ช่องทางการเข้าใช้งานระบบ (System URLs)")
    add_bullet("หน้าร้านหลักสำหรับลูกค้า (Main Storefront):", "http://127.0.0.1:5000 (รองรับคอมพิวเตอร์ แท็บเล็ต และสมาร์ทโฟน)")
    add_bullet("ระบบหลังบ้านสำหรับพนักงานหน้าร้าน (Staff & Admin Portal):", "http://127.0.0.1:5000/admin (สำหรับตรวจเช็คออเดอร์ สแกนรหัส และปรับสถานะสินค้า)")

    add_h2("1.2 จุดเด่นของแพลตฟอร์ม")
    add_bullet("Multi-Brand Selection:", "รวมแบรนด์แท้ 100% เช่น CeraVe, La Roche-Posay, Anua, Beauty of Joseon, The Ordinary, Kiehl's, Paula's Choice, Torriden, Round Lab, Cosrx")
    add_bullet("Personalized Skin Match Finder:", "ระบบอัลกอริทึมคัดกรองส่วนผสมและประเภทสกินแคร์ จัดรูทีน 5 ขั้นตอน (Cleanser, Toner, Serum, Moisturizer, Sunscreen) พร้อมส่วนลดเซต 10%")
    add_bullet("Click & Collect (Store Pickup):", "สั่งออนไลน์ล่วงหน้า เลือกเวลานัดรับ และเข้ามารับที่ 3 สาขาหลัก (สยามสแควร์วัน, เซ็นทรัล ลาดพร้าว, เมกาบางนา) โดยไม่มีค่าจัดส่ง")
    add_bullet("Digital Pickup Pass:", "ออกบัตรรับของดิจิทัลพร้อม Order Code และ QR Code อัตโนมัติ เพื่อให้ลูกค้ายื่นให้พนักงานได้อย่างรวดเร็ว")

    # ----------------------------------------------------
    # หมวดที่ 2: คู่มือการใช้งานสำหรับลูกค้า
    # ----------------------------------------------------
    add_h1("หมวดที่ 2: คู่มือการใช้งานสำหรับลูกค้า (Customer User Guide)")
    
    add_h2("2.1 การใช้งานระบบวิเคราะห์สภาพผิว (Skin Match Finder)")
    add_body("ฟังก์ชันนี้ช่วยให้ลูกค้าที่ไม่แน่ใจว่าตนเองควรใช้ครีมตัวไหน สามารถค้นพบสกินแคร์ที่เหมาะกับปัญหาผิวของตนเองได้อย่างแม่นยำ โดยมีขั้นตอนดังนี้:")
    add_bullet("ขั้นตอนที่ 1 (ระบุสภาพผิว):", "คลิกเลือกสภาพผิวหน้าของคุณจาก 5 ตัวเลือก ได้แก่ ผิวมัน (มันเงาทั่วหน้า), ผิวผสม (มัน T-Zone แก้มแห้ง), ผิวแห้ง (ผิวตึง ลอกขุย), ผิวบอบบางแพ้ง่าย (แสบ แดง ระคายเคืองง่าย), หรือ ผิวธรรมดา (สมดุลดี)")
    add_bullet("ขั้นตอนที่ 2 (ระบุปัญหาผิวที่กังวล):", "ติ๊กเลือกปัญหาผิวที่ต้องการฟื้นฟูเป็นพิเศษ (สามารถเลือกได้มากกว่า 1 ข้อ) เช่น ปัญหาสิวและสิวอุดตัน, รูขุมขนกว้างและความมัน, รอยสิว/ฝ้ากระ/หมองคล้ำ, ผิวขาดน้ำแห้งกร้าน, รอยแดง/ผิวแสบแพ้, หรือ ริ้วรอยและความหย่อนคล้อย")
    add_bullet("ขั้นตอนที่ 3 (กดประมวลผล):", "กดปุ่ม 'ประมวลผลและแสดงครีมที่แนะนำ' ระบบจะทำการวิเคราะห์สารสกัดสำคัญและจับคู่สินค้าที่เหมาะกับผิวของคุณทันที")

    add_callout(doc, "ผลลัพธ์จากการวิเคราะห์ผิวที่จะได้รับ", 
                "1. บทสรุปสภาพผิวพร้อมคำแนะนำเฉพาะทางจากผู้เชี่ยวชาญ (Skincare Expert Tips)\n"
                "2. แผนการบำรุง 5 ขั้นตอน: Step 1 คลีนเซอร์ -> Step 2 โทนเนอร์ -> Step 3 เซรั่ม -> Step 4 มอยส์เจอไรเซอร์ -> Step 5 กันแดด\n"
                "3. รายละเอียดสารสกัดเด่น เช่น Niacinamide, BHA, Ceramide, Hyaluronic Acid, Centella พร้อมราคาแต่ละชิ้น\n"
                "4. ปุ่ม 'เพิ่มทั้งเซต 5 ชิ้นลงตะกร้า' พร้อมรับส่วนลดพิเศษ 10% ทันที")

    add_h2("2.2 การเลือกดูและกรองสินค้าทั้งหมด (Product Catalog & Filtering)")
    add_body("ในกรณีที่ลูกค้าต้องการค้นหาหรือเลือกดูสินค้าเพิ่มเติม:")
    add_bullet("ช่องค้นหาด่วน (Search Bar):", "พิมพ์ชื่อสินค้า, ชื่อแบรนด์ หรือสารสกัด เช่น 'CeraVe', 'BHA', 'เซรั่ม' เพื่อค้นหาแบบเรียลไทม์")
    add_bullet("แท็บหมวดหมู่ (Category Tabs):", "เลือกดูตามขั้นตอนการใช้งาน เช่น คลีนเซอร์, โทนเนอร์, เซรั่ม, มอยส์เจอไรเซอร์ หรือ ครีมกันแดด")
    add_bullet("ชิปกรองแบรนด์ (Brand Chips):", "กดเลือกแบรนด์ที่ต้องการ เช่น The Ordinary, Anua, La Roche-Posay เพื่อดูเฉพาะสินค้าของแบรนด์นั้น")
    add_bullet("ชิปกรองสภาพผิว (Skin Type Chips):", "คัดกรองเฉพาะสินค้าที่มีสูตรสำหรับผิวมัน, ผิวแห้ง หรือผิวแพ้ง่าย")

    add_h2("2.3 การดูข้อมูลรายละเอียดสินค้าเจาะลึก (Product Detail Modal)")
    add_body("เมื่อคลิกที่การ์ดสินค้าหรือปุ่ม 'ดูรายละเอียด' ระบบจะเปิดหน้าต่างข้อมูลครบถ้วน ประกอบด้วย:")
    add_bullet("สารสกัดสำคัญ (Key Active Ingredients):", "ระบุชื่อสารและสรรพคุณ เช่น ชะลอริ้วรอย, ลดรอยแดง, เสริมเกราะป้องกันผิว")
    add_bullet("วิธีใช้และช่วงเวลา (How to use):", "ระบุว่าควรใช้เวลาเช้า (AM), ก่อนนอน (PM) หรือทั้งสองเวลา พร้อมวิธีทาอย่างถูกต้อง")
    add_bullet("สต็อกสินค้าแยกตามสาขา (Real-time Branch Stock):", "แสดงจำนวนชิ้นคงเหลือพร้อมส่งมอบของสาขาสยามสแควร์วัน, เซ็นทรัล ลาดพร้าว และเมกาบางนา")

    add_h2("2.4 การจัดการตะกร้าสินค้าและการสั่งซื้อ (Checkout Flow)")
    add_body("เมื่อเลือกสินค้าลงในตะกร้าแล้ว สามารถคลิกปุ่ม 'ตะกร้า' ที่มุมขวาบนเพื่อดูรายการสินค้า จากนั้นกดปุ่ม 'ดำเนินการสั่งซื้อ' โดยจะมี 2 รูปแบบให้เลือก:")
    
    # Table of fulfillment options
    table = doc.add_table(rows=3, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table)

    headers = ["รูปแบบการสั่งซื้อ", "รายละเอียดและขั้นตอน"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        set_cell_shading(cell, "4A5844")
        set_cell_margins(cell, top=140, bottom=140, left=160, right=160)
        p = cell.paragraphs[0]
        run = p.add_run(h)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    data = [
        ("1. รับสินค้าที่หน้าร้าน\n(Store Pickup / Click & Collect)\n⭐ แนะนำ ไม่มีค่าจัดส่ง", 
         "• เลือกระบุสาขาที่สะดวกรับ: สยามสแควร์วัน, เซ็นทรัล ลาดพร้าว หรือ เมกาบางนา\n• เลือกวันที่และช่วงเวลาที่จะมารับ (เช่น 11:00-13:00 หรือ 16:00-19:00)\n• กรอกชื่อและเบอร์โทรศัพท์สำหรับรับ SMS ยืนยัน\n• รับสินค้าได้ภายใน 1 ชั่วโมงหลังสั่งซื้อ"),
        ("2. จัดส่งพัสดุถึงบ้าน\n(Standard Delivery)", 
         "• กรอกที่อยู่จัดส่งพัสดุอย่างละเอียด\n• กรอกชื่อ-นามสกุล และเบอร์โทรศัพท์ผู้รับ\n• สินค้าจะถูกจัดส่งผ่านขนส่งเอกชนภายใน 1-2 วันทำการ")
    ]

    for row_idx, (col1, col2) in enumerate(data, start=1):
        cell1 = table.cell(row_idx, 0)
        cell2 = table.cell(row_idx, 1)
        cell1.width = Inches(2.3)
        cell2.width = Inches(4.2)
        set_cell_shading(cell1, "F7F4EE" if row_idx % 2 == 1 else "FFFFFF")
        set_cell_shading(cell2, "FDFBF7" if row_idx % 2 == 1 else "FFFFFF")
        set_cell_margins(cell1, top=120, bottom=120, left=140, right=140)
        set_cell_margins(cell2, top=120, bottom=120, left=140, right=140)
        
        p1 = cell1.paragraphs[0]
        p1.paragraph_format.line_spacing = 1.15
        r1 = p1.add_run(col1)
        r1.font.bold = True
        r1.font.size = Pt(9.5)

        p2 = cell2.paragraphs[0]
        p2.paragraph_format.line_spacing = 1.15
        r2 = p2.add_run(col2)
        r2.font.size = Pt(9.5)

    doc.add_paragraph().paragraph_format.space_before = Pt(6)

    add_h2("2.5 บัตรรับสินค้าดิจิทัล (Digital Store Pickup Pass)")
    add_body("หลังจากกดยืนยันคำสั่งซื้อสำเร็จ ระบบจะนำไปยังหน้าออกบัตรรับสินค้าดิจิทัลทันที ซึ่งประกอบด้วย:")
    add_bullet("รหัสคำสั่งซื้อ (Order Code):", "รหัสประจำออเดอร์ เช่น 'LUM-261110-XXXX' สำหรับใช้แจ้งพนักงาน")
    add_bullet("ภาพ QR Code ประจำออเดอร์:", "ลูกค้าสามารถเปิดหน้าจอนี้ หรือกดปุ่ม 'พิมพ์หรือบันทึกบัตรนี้' เพื่อเซฟไว้ในสมาร์ทโฟน แล้วนำมายื่นให้พนักงานหน้าร้านสแกนรับสินค้าได้ทันที")
    add_bullet("รายละเอียดสาขาและแผนที่เบื้องต้น:", "แสดงตำแหน่งที่ตั้งของสาขา เวลาเปิด-ปิด และเบอร์โทรติดต่อประจำสาขา")

    # ----------------------------------------------------
    # หมวดที่ 3: คู่มือสำหรับพนักงานและผู้ดูแลระบบ
    # ----------------------------------------------------
    add_h1("หมวดที่ 3: คู่มือสำหรับพนักงานและผู้ดูแลระบบ (Staff & Admin Guide)")
    add_body("หน้าระบบพนักงานหน้าร้านออกแบบมาเพื่อช่วยให้เจ้าหน้าที่ประจำสาขาสามารถจัดเตรียมสินค้า ค้นหาข้อมูลลูกค้า และส่งมอบสินค้าได้อย่างมีประสิทธิภาพ ผ่าน URL: http://127.0.0.1:5000/admin")

    add_h2("3.1 ภาพรวมสถิติหน้าร้าน (Dashboard Metrics)")
    add_body("ส่วนบนของหน้าแดชบอร์ดแสดงตัวเลขสำคัญแบบเรียลไทม์ 4 รายการ:")
    add_bullet("ออเดอร์ทั้งหมด (Total Orders):", "จำนวนคำสั่งซื้อสะสมทั้งหมดในระบบ")
    add_bullet("รับที่หน้าร้าน (Store Pickups):", "จำนวนออเดอร์รูปแบบ Click & Collect")
    add_bullet("รอลูกค้ามารับ (Pending Pickups):", "จำนวนออเดอร์ที่เตรียมสินค้าพร้อมแล้ว และกำลังรอลูกค้าเดินทางมารับที่สาขา")
    add_bullet("ยอดขายรวม (Total Revenue):", "ยอดเงินที่ชำระเรียบร้อยแล้วทั้งหมด")

    add_h2("3.2 ขั้นตอนการตรวจสอบและส่งมอบสินค้าให้ลูกค้า (Pickup Verification)")
    add_body("เมื่อลูกค้าเดินทางมาถึงหน้าร้านเพื่อรับสินค้า พนักงานควรปฏิบัติตามขั้นตอนดังนี้:")
    add_bullet("ขั้นตอนที่ 1 (ค้นหาออเดอร์):", "พิมพ์รหัสคำสั่งซื้อ (Order Code เช่น LUM-261110-XXXX) หรือเบอร์โทรศัพท์ของลูกค้าลงในช่องค้นหาด่วน ระบบจะกรองรายการออเดอร์ที่ตรงกันขึ้นมาทันที")
    add_bullet("ขั้นตอนที่ 2 (ตรวจสอบรายการสินค้า):", "ตรวจเช็ครายการสินค้าและจำนวนชิ้นในออเดอร์ว่าตรงกับสินค้าในถุงเตรียมของหรือไม่")
    add_bullet("ขั้นตอนที่ 3 (บันทึกการส่งมอบ):", "เมื่อส่งมอบสินค้าให้ลูกค้าเรียบร้อยแล้ว ให้กดปุ่มสีเขียว 'ส่งมอบของแล้ว ✓' เพื่อเปลี่ยนสถานะเป็น 'รับสินค้าแล้ว (Completed)' ป้องกันการมารับซ้ำซ้อน")

    add_h2("3.3 การตรวจสอบสต็อกสินค้าตามสาขา (Real-time Inventory)")
    add_body("ส่วนล่างของหน้าแดชบอร์ดมีตารางรายงานจำนวนสินค้าคงเหลือแยกตามรายสาขา (สยามสแควร์วัน, เซ็นทรัล ลาดพร้าว, เมกาบางนา) ช่วยให้พนักงานตรวจสอบความพร้อมในการให้บริการ และวางแผนเติมสินค้าได้อย่างแม่นยำ")

    # ----------------------------------------------------
    # หมวดที่ 4: ข้อมูลสาขาและการติดต่อ
    # ----------------------------------------------------
    add_h1("หมวดที่ 4: ข้อมูลสาขาหน้าร้านและช่องทางติดต่อ (Branch Information)")
    
    # Store table
    t_stores = doc.add_table(rows=4, cols=4)
    t_stores.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_stores)

    s_headers = ["ชื่อสาขา", "ตำแหน่งที่ตั้ง", "เวลาทำการ", "เบอร์โทรศัพท์"]
    for i, h in enumerate(s_headers):
        cell = t_stores.cell(0, i)
        set_cell_shading(cell, "4A5844")
        set_cell_margins(cell, top=140, bottom=140, left=140, right=140)
        p = cell.paragraphs[0]
        run = p.add_run(h)
        run.font.bold = True
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    stores_data = [
        ("สยามสแควร์วัน (Siam Square One)", "ชั้น 2 โซน Fashion Walk (ใกล้ทางเชื่อม BTS สยาม)", "เปิดทุกวัน 10:00 - 21:00 น.", "02-115-9981"),
        ("เซ็นทรัล ลาดพร้าว (Central Ladprao)", "ชั้น G โซน Beauty Avenue ฝั่งทางออก MRT", "เปิดทุกวัน 10:00 - 21:30 น.", "02-541-1822"),
        ("เมกาบางนา (Mega Bangna)", "ชั้น 1 Mega Wellness Zone (ใกล้ Big C Extra)", "เปิดทุกวัน 10:00 - 22:00 น.", "02-105-1934")
    ]

    for row_idx, row_vals in enumerate(stores_data, start=1):
        for col_idx, val in enumerate(row_vals):
            cell = t_stores.cell(row_idx, col_idx)
            set_cell_shading(cell, "F7F4EE" if row_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            run = p.add_run(val)
            run.font.size = Pt(9)
            if col_idx == 0:
                run.font.bold = True

    doc.add_paragraph().paragraph_format.space_before = Pt(8)

    # ----------------------------------------------------
    # หมวดที่ 5: คำถามที่พบบ่อยและการแก้ปัญหา
    # ----------------------------------------------------
    add_h1("หมวดที่ 5: คำถามที่พบบ่อยและการแก้ปัญหา (FAQ & Troubleshooting)")

    add_bullet("Q1: ลูกค้าเดินทางมาถึงหน้าร้าน แต่จำรหัสคำสั่งซื้อไม่ได้?", 
               "พนักงานสามารถขอเบอร์โทรศัพท์หรือชื่อ-นามสกุลของลูกค้า แล้วนำไปพิมพ์ในช่องค้นหาบนหน้า /admin เพื่อค้นหาประวัติออเดอร์และส่งมอบของได้ตามปกติ")
    
    add_bullet("Q2: หากต้องการสั่งซื้อสินค้าหลายชิ้นพร้อมกันในตะกร้า?", 
               "ลูกค้าสามารถกดปุ่มเครื่องหมายบวก (+) เพิ่มสินค้าลงในตะกร้าได้ไม่จำกัด หรือจะเลือกเพิ่มทั้งเซตจากการวิเคราะห์ผิว แล้วไปเพิ่มสินค้าตัวอื่นในแคตตาล็อกต่อได้ตามต้องการ")

    add_bullet("Q3: วิธีการเริ่มต้นรันระบบใหม่หลังจากปิดเครื่องคอมพิวเตอร์?", 
               "เปิด PowerShell หรือ Terminal ไปที่โฟลเดอร์โปรเจกต์ จากนั้นรันคำสั่ง: 'python app.py' แล้วเปิดเบราว์เซอร์ไปที่ http://127.0.0.1:5000")

    # Document Footer / Closing
    p_end = doc.add_paragraph()
    p_end.paragraph_format.space_before = Pt(20)
    p_end.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_end = p_end.add_run("— สิ้นสุดเอกสารคู่มือการใช้งาน LUMIÈRE SKIN LAB & RETAIL —")
    r_end.font.size = Pt(9.5)
    r_end.font.color.rgb = RGBColor(0x78, 0x71, 0x6C)

    output_path = os.path.join(r"c:\075", "คู่มือการใช้งาน_LUMIERE_SKIN_LAB.docx")
    doc.save(output_path)
    print(f"Manual successfully saved to: {output_path}")

if __name__ == "__main__":
    create_manual()
