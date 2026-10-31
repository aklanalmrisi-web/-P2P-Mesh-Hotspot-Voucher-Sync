# P2P Mesh Hotspot Voucher Sync

A groundbreaking decentralized architecture designed for localized Wireless Internet Service Providers (WISPs) operating in off-grid or infrastructure-challenged environments. It enables seamless cross-network voucher usage and automated financial clearing between independent local networks without requiring a central cloud server.

---

## 🚀 The Core Problem & Solution
Traditional WISP management relies heavily on central cloud RADIUS servers or continuous internet connectivity to sync user vouchers and balances. When internet links fail or backhauls drop, local networks become completely isolated.

**P2P Mesh Hotspot Voucher Sync** solves this by establishing a decentralized local mesh layer (using ESP32 and P2P RF/network protocols) that allows:
1. **Cross-Network Voucher Redemption:** A subscriber who buys a voucher in Network A can use it in Network B seamlessly during internet outages.
2. **Local Consensus & Double-Spend Prevention:** Prevents voucher abuse across disconnected nodes using state-synchronization algorithms.
3. **Autonomous Financial Clearing:** Logs inter-network data consumption to generate local clearing ledgers and settlement reports.

---

## 🛠️ Architectural Components

* **Hardware Tier:** ESP32 microcontrollers acting as bridge nodes over local wireless/mesh links.
* **Network Tier:** MikroTik RouterOS integration via API and local scripts for captive portal session control.
* **Logic Tier:** Lightweight synchronization daemon (`voucher_sync_core.py`) handling state consistency, cryptographic signatures, and clearing calculations.

---

## 📂 Project Structure

```text
P2P-Mesh-Hotspot-Voucher-Sync/
│
├── voucher_sync_core.py     # Core synchronization daemon & consensus logic
├── LICENSE                  # MIT Open-Source License
└── README.md                # Project documentation
