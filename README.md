
# 🖊️ Signature Background Removal – Azure Function

A **low-latency Azure Function** for removing the background from handwritten signatures on paper.
The service accepts an image as **Base64**, removes the paper background using a **deterministic OpenCV pipeline**, and returns a **transparent PNG**—optimized for document processing, KYC, and enterprise workflows.

---

## ✨ Features

* ⚡ **Ultra-low latency** (<30ms per image)
* 🧠 **No ML models** (no cold starts, no downloads)
* 🖊️ Optimized for **handwritten signatures**
* 📄 Handles shadows and uneven lighting
* 🌐 HTTP-triggered Azure Function
* 🧩 Clean, layered architecture
* 🖼️ Transparent PNG output

---

## 🏗️ Architecture Overview

```
HTTP Request (Base64 Image)
        ↓
Azure Function (HTTP Trigger)
        ↓
Manager Layer (Orchestration)
        ↓
Service Layer (OpenCV Processing)
        ↓
Transparent PNG (Base64)
```

### Project Structure

```
Image-background-removal/
├── app/
│   ├── core/              # Config, logging, DI
│   ├── managers/          # Orchestration layer
│   ├── services/          # Business logic (OpenCV)
│   ├── repositories/      # Reserved for future use
│   └── utils/             # Shared utilities
│
├── function_app.py        # Azure Functions
├── host.json
├── local.settings.json
├── pyproject.toml
└── README.md
```

---

## 🧠 How It Works

This project **does not use machine learning**.

Instead, it uses a **document-processing pipeline**, which is the industry standard for signatures:

1. Convert image to grayscale
2. Apply **adaptive thresholding** to isolate ink
3. Clean strokes using morphological operations
4. Generate an alpha mask
5. Output a transparent PNG

This approach:

* Preserves fine pen strokes
* Avoids blur and halos
* Is deterministic and fast
* Works reliably on scanned or photographed paper

---

## 🚀 Getting Started

### Prerequisites

* Python **3.11**
* Azure Functions Core Tools **v4**
* PDM
* Postman (for testing)

---

## 📦 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/ahmedmustafa-imperium/Image-background-removal.git
cd Image-background-removal
```

### 2️⃣ Install dependencies

```bash
pdm install
```

---

## ▶️ Run Locally

```bash
pdm run func start
```

You should see:

```
BgRemoveFunction: [POST]
http://localhost:7071/api/BgRemoveFunction
```

---

## 🧪 Testing with Postman

### Endpoint

```
POST http://localhost:7071/api/BgRemoveFunction
```

### Headers

| Key          | Value            |
| ------------ | ---------------- |
| Content-Type | application/json |

### Body (raw JSON)

```json
{
  "image_base64": "<BASE64_ENCODED_IMAGE>"
}
```

### Response

```json
{
  "image_base64": "<BASE64_ENCODED_PNG>"
}
```

---

## 🖼️ Convert Response to Image (PowerShell)

```powershell
$base64 = Get-Content "bg_removed_base64.txt" -Raw
[System.IO.File]::WriteAllBytes(
  "signature_transparent.png",
  [Convert]::FromBase64String($base64)
)
```

---

## ⏱️ Performance

| Metric            | Value      |
| ----------------- | ---------- |
| Average latency   | **<30 ms** |
| Model loading     | None       |
| Cold start impact | Minimal    |
| Memory footprint  | Low        |

---

## ❓ Why Not Machine Learning?

ML models like U²-Net or SAM are:

* Slower
* Blur fine strokes
* Overkill for document images
* Costly in serverless environments

For signatures, **classical image processing outperforms ML** in both quality and speed.

---

## 🔒 Production Notes

* Designed for **Azure Functions v2 (decorator-based)**
* Stateless and horizontally scalable
* Easy to integrate with Azure Blob Storage
* Can be extended with authentication & rate limiting

---

## 📜 License

MIT License

---

## 👤 Author

**Ahmed Mustafa**  
Built with production-grade principles for enterprise document workflows.

---
