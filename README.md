# Local Key-Value Log Database Engine (V1.0.0)

A high-performance log-structured key-value storage engine engineered in Python featuring append-only disk serialization persistence and sub-millisecond in-memory O(1) index map lookups.

## 🧮 Core Architecture & Features
* **Log-Structured Storage:** Engineered an append-only transaction pipeline that writes incoming key-value record matrices directly onto physical disk storage, eliminating random disk I/O performance bottlenecks.
* **In-Memory Hash Indexing:** Built a volatile dictionary map tracking system that records exact absolute file byte offsets upon transaction commits to ensure sub-millisecond lookup latency.
* **Crash-Recovery Routine:** Programmed a baseline disk scanning routine that parses raw transaction log blocks line-by-line during engine bootup sequences to fully reconstruct memory lookup states after forced reboots.
* **Interactive Shell Interface:** Integrated a clean terminal parser command loop processing physical interactive `SET [key] [value]`, `GET [key]`, and `EXIT` commands natively.
