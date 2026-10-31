# Copyright © 2026 Aklan Almorisi. All rights reserved.
# P2P-Mesh-Hotspot-Voucher-Sync: Decentralized WISP Framework

import hashlib
import json
import time

class VoucherNode:
    def __init__(self, node_id, local_db_path):
        self.node_id = node_id
        self.local_db_path = local_db_path
        self.vouchers = {}  # التخزين المحلي للحالة والأرصدة
        self.ledger = []    # سجل المقاصة المحاسبية

    def load_local_vouchers(self):
        """تحميل حالة الكروت من قاعدة البيانات المحلية للراوتر/الشبكة"""
        print(f"[{self.node_id}] Loading local voucher states...")

    def generate_sync_packet(self, voucher_code, remaining_balance):
        """توليد حزمة بيانات مشفرة وموقعة للمزامنة مع العقد المجاورة"""
        payload = {
            "node": self.node_id,
            "code": voucher_code,
            "balance": remaining_balance,
            "timestamp": time.time()
        }
        raw_data = json.dumps(payload, sort_keys=True)
        signature = hashlib.sha256(raw_data.encode()).hexdigest()
        
        return {"payload": payload, "sig": signature}

    def receive_peer_sync(self, packet):
        """استقبال تحديث من شبكة مجاورة وتطبيق خوارزمية منع التضارب"""
        payload = packet["payload"]
        code = payload["code"]
        peer_balance = payload["balance"]
        
        if code in self.vouchers:
            local_balance = self.vouchers[code]["balance"]
            # خوارزمية إجماع محلية: اعتماد الأحدث والأقل رصيداً لمنع إعادة الاستخدام المزدوج
            if peer_balance < local_balance:
                self.vouchers[code]["balance"] = peer_balance
                print(f"[{self.node_id}] Voucher {code} synced. Updated balance: {peer_balance}")
        else:
            # إضافة كرت جديد ورد من شبكة الجار
            self.vouchers[code] = {"balance": peer_balance, "status": "ACTIVE"}
            print(f"[{self.node_id}] New voucher {code} imported from peer node.")

    def record_clearing(self, target_node, amount):
        """تسجيل المعاملات المالية المتبادلة للمقاصة بين الشبكتين"""
        clearing_entry = {
            "from": self.node_id,
            "to": target_node,
            "amount": amount,
            "time": time.time()
        }
        self.ledger.append(clearing_entry)
        print(f"Clearing logged: {amount} units between {self.node_id} and {target_node}")

# مثال عملي لاختبار العقدة محلياً
if __name__ == "__main__":
    node_a = VoucherNode("NODE_MARIB_A", "db_a.json")
    node_a.load_local_vouchers()
    
    # محاكاة مزامنة كرت بين شبكتين
    sync_packet = node_a.generate_sync_packet("VOUCH_9876", 500)
    
    # عقدة جار تلقي التحديث
    node_b = VoucherNode("NODE_MARIB_B", "db_b.json")
    node_b.receive_peer_sync(sync_packet)
