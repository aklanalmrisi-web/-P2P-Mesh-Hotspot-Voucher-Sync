/*
 * Copyright © 2026 Aklan Almorisi. All rights reserved.
 * P2P-Mesh-Hotspot-Voucher-Sync: ESP32 Hardware Mesh Bridge Node
 */

#include <WiFi.h>
#include <esp_now.h>

// هيكل البيانات لحزم المزامنة المرسلة بين العقد عبر ESP-NOW
typedef struct struct_message {
    char voucher_code[32];
    int remaining_balance;
    unsigned long timestamp;
} struct_message;

struct_message incomingData;

// دالة الاستقبال عند تلقي حزمة بيانات من عقدة مجاورة (Peer Node)
void OnDataRecv(const uint8_t *mac, const uint8_t *incomingDataBytes, int len) {
    memcpy(&incomingData, incomingDataBytes, sizeof(incomingData));
    
    Serial.println("--- [MESH SYNC PACKET RECEIVED] ---");
    Serial.print("Voucher Code: ");
    Serial.println(incomingData.voucher_code);
    Serial.print("Remaining Balance: ");
    Serial.println(incomingData.remaining_balance);
    Serial.print("Timestamp: ");
    Serial.println(incomingData.timestamp);
    Serial.println("-----------------------------------");
    
    // هنا يتم تمرير البيانات عبر منفذ Serial إلى راوتر MikroTik لتحديث الحالة محلياً
}

void setup() {
  // تهيئة الاتصال التسلسلي
  Serial.begin(115200);
  
  // ضبط وحدة الواي فاي في وضع Station
  WiFi.mode(WIFI_STA);

  // إرسال العنوان الخاص بهذه العقدة
  Serial.print("ESP32 Bridge Node Initialized. MAC Address: ");
  Serial.println(WiFi.macAddress());

  // تهيئة بروتوكول ESP-NOW للاتصال المباشر السريع بدون راوتر مركزي
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  // تسجيل دالة استقبال البيانات
  esp_now_register_recv_cb(esp_now_recv_cb_t(OnDataRecv));
}

void loop() {
  // حلقة التشغيل الرئيسية للمراقبة وإدارة الإشارات الميدانية
  delay(1000);
}
