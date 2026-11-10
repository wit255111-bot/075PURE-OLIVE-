from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import json
import random
import string
from datetime import datetime
from database import get_db, init_db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lumier-skincare-secret-key-2026'

def row_to_dict(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        val = row[idx]
        if col[0] in ['skin_types', 'skin_concerns', 'key_ingredients', 'items'] and val:
            try:
                d[col[0]] = json.loads(val)
            except:
                d[col[0]] = val
        else:
            d[col[0]] = val
    return d

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    
    # Get all brands
    cursor.execute('SELECT DISTINCT brand FROM products ORDER BY brand')
    brands = [r[0] for r in cursor.fetchall()]

    # Get stores
    cursor.execute('SELECT * FROM stores')
    stores = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('index.html', brands=brands, stores=stores)

@app.route('/api/products')
def api_products():
    skin_type = request.args.get('skin_type')
    concern = request.args.get('concern')
    brand = request.args.get('brand')
    category = request.args.get('category')
    search = request.args.get('search', '').strip()

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products ORDER BY is_bestseller DESC, step_order ASC, price ASC')
    raw_products = cursor.fetchall()
    
    products = []
    for row in raw_products:
        item = row_to_dict(cursor, row)
        
        # Filter by skin_type
        if skin_type and skin_type != 'all':
            if skin_type not in item.get('skin_types', []):
                continue
                
        # Filter by concern
        if concern and concern != 'all':
            if concern not in item.get('skin_concerns', []):
                continue

        # Filter by brand
        if brand and brand != 'all':
            if item.get('brand') != brand:
                continue

        # Filter by category
        if category and category != 'all':
            if item.get('category') != category:
                continue

        # Filter by search
        if search:
            s = search.lower()
            name = item.get('name', '').lower()
            thai_name = (item.get('thai_name') or '').lower()
            b = item.get('brand', '').lower()
            if s not in name and s not in thai_name and s not in b:
                continue

        products.append(item)

    conn.close()
    return jsonify(products)

@app.route('/api/product/<int:product_id>')
def api_product_detail(product_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return jsonify({'error': 'Product not found'}), 404
        
    product = row_to_dict(cursor, row)
    conn.close()
    return jsonify(product)

@app.route('/api/recommend')
def api_recommend():
    """Smart Skin Match recommendation engine based on skin type and concerns"""
    skin_type = request.args.get('skin_type', 'oily')
    concerns_raw = request.args.get('concerns', '')
    concerns = [c.strip() for c in concerns_raw.split(',') if c.strip()] if concerns_raw else ['acne']

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    raw_products = cursor.fetchall()
    all_products = [row_to_dict(cursor, row) for row in raw_products]
    conn.close()

    # Routine categories in order
    steps = ['Cleanser', 'Toner', 'Serum', 'Moisturizer', 'Sunscreen']
    recommended_routine = []
    total_routine_price = 0

    for step in steps:
        matching_products = []
        for p in all_products:
            if p['category'] == step:
                # Scoring: +2 if matches skin_type, +1 for each matching concern, +0.5 for bestseller
                score = 0
                if skin_type in p.get('skin_types', []):
                    score += 3
                for c in concerns:
                    if c in p.get('skin_concerns', []):
                        score += 2
                if p.get('is_bestseller'):
                    score += 0.5
                matching_products.append((score, p))
        
        matching_products.sort(key=lambda x: x[0], reverse=True)
        if matching_products:
            best_match = matching_products[0][1]
            recommended_routine.append(best_match)
            total_routine_price += best_match['price']

    # Thai labels
    skin_type_labels = {
        'oily': 'ผิวมัน (Oily Skin)',
        'combination': 'ผิวผสม (Combination Skin)',
        'dry': 'ผิวแห้ง (Dry Skin)',
        'sensitive': 'ผิวบอบบางแพ้ง่าย (Sensitive Skin)',
        'normal': 'ผิวธรรมดา (Normal Skin)'
    }

    concern_labels = {
        'acne': 'ปัญหาสิวและสิวอุดตัน',
        'pores': 'รูขุมขนกว้าง หน้ามันส่วนเกิน',
        'dark_spots': 'รอยสิว ฝ้า กระ และความหมองคล้ำ',
        'aging': 'ริ้วรอยและความหย่อนคล้อย',
        'dehydration': 'ผิวขาดน้ำ ลอกเป็นขุย ขาดสมดุล',
        'redness': 'รอยแดง ระคายเคืองง่าย'
    }

    summary_concerns = [concern_labels.get(c, c) for c in concerns]

    # Skin doctor tips based on combination
    tips = []
    if 'oily' in skin_type or 'combination' in skin_type:
        tips.append("เน้นการทำความสะอาดรูขุมขนอย่างล้ำลึกโดยไม่ทำลายเกราะป้องกันผิว และเลือกรองพื้น/มอยส์เจอไรเซอร์เนื้อเจลบางเบา")
    if 'dry' in skin_type or 'dehydration' in concerns:
        tips.append("เสริมเซราไมด์และไฮยาลูรอนเพื่อกักเก็บน้ำในผิว หลีกเลี่ยงการล้างหน้าด้วยน้ำอุ่นจัด")
    if 'acne' in concerns:
        tips.append("ใช้ BHA (Salicylic Acid) ช่วยละลายสิ่งอุดตัน และ Niacinamide ลดการอักเสบโดยไม่ทำให้ผิวระคายเคือง")
    if 'sensitive' in skin_type or 'redness' in concerns:
        tips.append("งดสครับผิว และเน้นสารปลอบประโลมอย่างใบบัวบก (Centella), Panthenol หรือ Heartleaf เพื่อคืนความแข็งแรง")

    return jsonify({
        'skin_type': skin_type,
        'skin_type_label': skin_type_labels.get(skin_type, skin_type),
        'concerns': concerns,
        'concerns_labels': summary_concerns,
        'routine': recommended_routine,
        'total_price': total_routine_price,
        'bundle_discount': round(total_routine_price * 0.1, 0), # 10% bundle discount
        'final_bundle_price': round(total_routine_price * 0.9, 0),
        'tips': tips
    })

@app.route('/api/stores')
def api_stores():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM stores')
    stores = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(stores)

@app.route('/api/orders', methods=['POST'])
def api_create_order():
    data = request.get_json()
    if not data or 'items' not in data or not data['items']:
        return jsonify({'error': 'ข้อมูลคำสั่งซื้อไม่ถูกต้อง'}), 400

    order_type = data.get('order_type', 'pickup') # 'pickup' or 'delivery'
    store_id = data.get('store_id', 'siam')
    pickup_date = data.get('pickup_date', '')
    pickup_time = data.get('pickup_time', '')
    customer_name = data.get('customer_name', '').strip()
    customer_phone = data.get('customer_phone', '').strip()
    customer_email = data.get('customer_email', '').strip()
    shipping_address = data.get('shipping_address', '').strip()
    items = data.get('items', [])
    subtotal = float(data.get('subtotal', 0))
    discount = float(data.get('discount', 0))
    total = float(data.get('total', subtotal - discount))
    payment_method = data.get('payment_method', 'promptpay')

    if not customer_name or not customer_phone:
        return jsonify({'error': 'กรุณากรอกชื่อและเบอร์โทรศัพท์สำหรับติดต่อ'}), 400

    if order_type == 'pickup' and not store_id:
        return jsonify({'error': 'กรุณาเลือกสาขาที่ต้องการรับสินค้า'}), 400

    # Generate unique Order Code: LUM-YYMMDD-XXXX
    date_prefix = datetime.now().strftime('%y%m%d')
    random_suffix = ''.join(random.choices(string.digits + string.ascii_uppercase, k=4))
    order_code = f"LUM-{date_prefix}-{random_suffix}"

    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO orders (
        order_code, order_type, store_id, pickup_date, pickup_time,
        customer_name, customer_phone, customer_email, shipping_address,
        items, subtotal, discount, total, payment_method, payment_status, order_status
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        order_code, order_type, store_id, pickup_date, pickup_time,
        customer_name, customer_phone, customer_email, shipping_address,
        json.dumps(items), subtotal, discount, total, payment_method,
        'paid', 'ready_for_pickup' if order_type == 'pickup' else 'preparing'
    ))
    
    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'order_code': order_code,
        'redirect_url': f'/order/{order_code}'
    })

@app.route('/order/<order_code>')
def order_confirmation(order_code):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders WHERE order_code = ?', (order_code,))
    order_row = cursor.fetchone()
    
    if not order_row:
        conn.close()
        return "ไม่พบคำสั่งซื้อนี้", 404
        
    order = row_to_dict(cursor, order_row)
    
    store = None
    if order.get('store_id'):
        cursor.execute('SELECT * FROM stores WHERE id = ?', (order['store_id'],))
        s_row = cursor.fetchone()
        if s_row:
            store = dict(s_row)
            
    conn.close()
    return render_template('order_success.html', order=order, store=store)

@app.route('/admin')
def admin_page():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM orders ORDER BY created_at DESC')
    orders = [row_to_dict(cursor, r) for r in cursor.fetchall()]

    cursor.execute('SELECT * FROM stores')
    stores_list = [dict(r) for r in cursor.fetchall()]
    stores_map = {s['id']: s for s in stores_list}

    cursor.execute('SELECT * FROM products ORDER BY brand, name')
    products = [row_to_dict(cursor, r) for r in cursor.fetchall()]

    # Stats
    total_orders = len(orders)
    pickup_orders = sum(1 for o in orders if o.get('order_type') == 'pickup')
    pending_pickups = sum(1 for o in orders if o.get('order_type') == 'pickup' and o.get('order_status') in ['preparing', 'ready_for_pickup'])
    total_revenue = sum(o.get('total', 0) for o in orders)

    conn.close()
    return render_template('admin.html', 
                           orders=orders, 
                           stores_map=stores_map,
                           products=products,
                           total_orders=total_orders,
                           pickup_orders=pickup_orders,
                           pending_pickups=pending_pickups,
                           total_revenue=total_revenue)

@app.route('/api/admin/order/<order_code>/status', methods=['POST'])
def admin_update_status(order_code):
    data = request.get_json()
    new_status = data.get('status')
    if not new_status:
        return jsonify({'error': 'Missing status'}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE orders SET order_status = ? WHERE order_code = ?', (new_status, order_code))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'order_code': order_code, 'new_status': new_status})

if __name__ == '__main__':
    init_db()
    print("Starting Lumière Skin Lab on http://127.0.0.1:5000 ...")
    app.run(host='127.0.0.1', port=5000, debug=True)
