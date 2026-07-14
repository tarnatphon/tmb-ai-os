from datetime import date

PILLARS = [
    ("Materials", "เลือกผ้ากระเป๋า OEM ให้เหมาะกับการใช้งานและงบประมาณ"),
    ("Quality Control", "จุดตรวจคุณภาพที่ควรกำหนดก่อนผลิตกระเป๋าจำนวนมาก"),
    ("OEM Manufacturing", "ข้อมูลที่ฝ่ายจัดซื้อควรเตรียมก่อนขอใบเสนอราคากระเป๋า OEM"),
    ("Printing Techniques", "เลือกงานสกรีน งานปัก หรือฮีตทรานสเฟอร์ให้เหมาะกับโลโก้"),
    ("ODM Development", "จากไอเดียสู่ตัวอย่างจริง: ขั้นตอนพัฒนากระเป๋า ODM"),
    ("Laptop Bags", "ออกแบบช่องใส่โน้ตบุ๊กอย่างไรให้ใช้งานจริงและผลิตได้"),
    ("Sustainability", "วางแผนกระเป๋าองค์กรที่ลดวัสดุสิ้นเปลืองโดยไม่ลดคุณภาพ"),
]


def daily_topic() -> tuple[str, str]:
    idx = date.today().toordinal() % len(PILLARS)
    return PILLARS[idx]
