import os
import json
import re

receipts_root = '/<PATH_TO_YOUR_RECEIPTS>/Receipts/json'
sql_file = 'receipts.sql'

def extract_quantity(quantity_cost):
    if not quantity_cost:
        return 1
    match = re.search(r'(\d+)\s*st\s*\*', quantity_cost)
    if match:
        return int(match.group(1))
    return 1

def extract_price_per_item(quantity_cost):
    if not quantity_cost:
        return "0"
    match = re.search(r'\*\s*([\d,]+)\s*kr', quantity_cost)
    if match:
        return match.group(1).replace(',', '.')
    return "0"

def extract_price_per_kilo(quantity_cost):
    if not quantity_cost:
        return "0"
    # Example: "0,618 kg * 135,00 kr/kg"
    match = re.search(r'\*\s*([\d,.]+)\s*kr/kg', quantity_cost)
    if match:
        return match.group(1).replace(',', '.')
    return "0"

def parse_receipt(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    content = data.get('content', {})
    header = content.get('header', {})
    store_info = content.get('storeInformation', {}).get('storeInformation', [{}])
    items = content.get('items', {}).get('allItems', {}).get('items', [])
    date = header.get('isoDate', '')
    store = store_info[0].get('property', '')
    total = header.get('totalPurchaseAmount', '')
    sqls = []
    for item in items:
        name = item.get('name', '')
        price = item.get('money', {}).get('formatted', '')
        quantity_cost = item.get('quantityCost', {}).get('formatted') if item.get('quantityCost') else None
        quantity = extract_quantity(quantity_cost)
        price_per_item = extract_price_per_item(quantity_cost) if quantity > 1 else "0"
        price_per_kilo = extract_price_per_kilo(quantity_cost)
        sql = (
            f"INSERT INTO receipts (date, store, total, product, price, quantity, price_per_item, price_per_kilo) "
            f"VALUES ('{date}', '{store}', '{total}', '{name}', '{price}', '{quantity}', '{price_per_item}', '{price_per_kilo}');"
        )
        sqls.append(sql)
    return sqls

with open(sql_file, 'w', encoding='utf-8') as out:
    for root, dirs, files in os.walk(receipts_root):
        for filename in files:
            if filename.endswith('.json'):
                filepath = os.path.join(root, filename)
                sqls = parse_receipt(filepath)
                for sql in sqls:
                    out.write(sql + '\n')

print(f"SQL statements written to {sql_file}")


