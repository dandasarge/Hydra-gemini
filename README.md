<div align="center">
  <img src="hydra/api/static/logo_complete.png" alt="Hydra Logo" height="120"/>
  <br/><br/>

  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
  [![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
  [![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
  [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

  <h3>Unlimited Free-Tier Gemini API Gateway</h3>
  <p><strong>Route requests to 20+ free keys with automatic failover, rate-limit rotation, and full OpenAI compatibility.</strong></p>
</div>

---

## 📖 Table of Contents
- [✨ Features](#-features)
- [🔑 The Strategy (Unlimited Free Tier)](#-the-strategy-unlimited-free-tier)
- [📦 Installation](#-installation)
- [⚙️ Configuration (keys.json)](#️-configuration-keysjson)
- [🚀 Quick Start](#-quick-start)
- [🔐 Authentication](#-authentication)
- [🔌 API Reference](#-api-reference)
- [🤖 Advanced Features](#-advanced-features)
- [🛡️ Admin & Tunneling](#️-admin--tunneling)
- [⚠️ Troubleshooting](#️-troubleshooting)

---

## ✨ Features
- **Unlimited Usage**: Aggregate multiple free-tier keys into a single high-throughput endpoint (RPM/RPD vary by model; lite tiers up to 15 RPM / 500 RPD each).
- **Failover & Rotation**: Automatically detects `429` (Rate Limit) and switches to the next healthy key instantly.
- **OpenAI Compatible**: Drop-in replacement for `openai` SDKs, Cursor, VS Code, and LangChain.
- **Smart Routing**: Routes across free-tier Gemini 3.x / 2.5 models — `gemini-3.6-flash`, `gemini-3.5-flash`, `gemini-3-flash-preview`, `gemini-3.7-flash`, `gemini-3.5-flash-lite`, `gemini-3.1-flash-lite`, `gemini-2.5-flash-lite`, plus `gemini-2.5-flash-image` and `gemini-embedding-001`.
- **Visual Dashboard**: Monitor key health, RPM, and errors in real-time.
- **Secure Tunneling**: Expose your localhost API to the internet via Cloudflare Tunnel.

---

## 🔑 The Strategy (Unlimited Free Tier)

### The "Secret" to Unlimited Usage
Google's Gemini API free tier has a limit of **15 Requests Per Minute (RPM)** and **1,500 Requests Per Day** per **Google Cloud Project**.

**Crucial Insight:** The limit applies to the *Project*, NOT your Google Account.
You can create multiple projects under one Google Account.

**✅ The Golden Rule:**
> **ONE API KEY per PROJECT.**

Do not create multiple keys in the same project; they share the same quota! Instead:
1.  Create **Project A** -> Get Key A.
2.  Create **Project B** -> Get Key B.
3.  Hydra pools them together. 10 Projects = 150 RPM (Enterprise Grade).

### Step-by-Step Guide
1.  Go to [Google AI Studio](https://aistudio.google.com/).
2.  Click **Get API key**.
3.  Click **Create API key in new project**.
4.  Copy the key.
5.  **Repeat steps 2-4** as many times as you want (e.g., 10-20 times).
6.  Save all keys into your `keys.json` file.

**Quota Notes:**
-   **Unverified Accounts**: Can create ~10-12 projects.
-   **Billing Enabled/Verified**: Can create ~25+ projects.
-   **Multiple Accounts**: You can use tokens from different Gmail accounts in the same `keys.json`.

---

## 📦 Installation

### ⚡ Auto-Setup (Recommended)
Hydra now has a built-in wizard that handles everything (Redis, Keys, etc).

1.  **Install Hydra**:
    ```bash
    pip install -e .
    ```
2.  **Run Onboard**:
    ```bash
    hydra onboard
    ```
    This command will:
    -   ✅ Check/Install Redis (if missing).
    -   ✅ Start Redis in the background.
    -   ✅ Create/Validate your `keys.json`.
    -   ✅ Launch the Gateway.

### 🐧 Manual Setup
If you prefer to do it yourself:
1.  **Install Redis**: Use `brew`, `apt`, or download manually.
2.  **Start Redis**: `redis-server`
3.  **Run Hydra**: `hydra setup --file keys.json` then `hydra gateway`.

---

## 🔌 Integrations

### VS Code (Roo Code / Cline)
You can use Hydra as the backend for AI coding assistants like **Roo Code** or **Cline**.

1.  **API Provider**: `OpenAI Compatible`
2.  **Base URL**: `http://localhost:8000/v1` (or your Tunnel URL)
3.  **API Key**: `sk-hydra-local` (or generate one with `hydra tokens create`)
4.  **Model ID**: `gemini-3.5-flash-lite` (or `gemini-3.6-flash`)

### Cursor / other OpenAI-compatible tools
Hydra works with any tool that supports the OpenAI API format. Just point the `baseUrl` to Hydra and use any model name.

---

## ⚙️ Configuration (keys.json)

Create a file named `keys.json` in the root directory. This is where you store your pool of keys.

### Structure
```json
[
  {
    "email": "primary@gmail.com", 
    "api_key": "AIzaSy_KEY_1...", 
    "project_id": "my-project-001"
  },
  {
    "email": "primary@gmail.com",
    "api_key": "AIzaSy_KEY_2...",
    "project_id": "my-project-002"
  },
  {
    "email": "secondary@gmail.com",
    "api_key": "AIzaSy_KEY_3...",
    "project_id": "other-project-x"
  }
]
```

### Fields
| Field | Description | Importance |
|---|---|---|
| `email` | Just a label for you to identify the account owner. | Optional (but recommended) |
| `api_key` | The actual API key starting with `AIzaSy`. | **REQUIRED** |
| `project_id` | Should be unique per key for maximum quota. | Optional (Label) |

---

## 🚀 Quick Start

1.  **Validate Keys**:
    Use the setup wizard to test your keys before running.
    ```bash
    hydra setup --file keys.json
    # OR if 'hydra' command fails:
    python -m hydra setup --file keys.json
    ```

2.  **Start Gateway**:
    ```bash
    hydra gateway
    # OR
    python -m hydra gateway
    ```
    Your API is now live at: `http://localhost:8000/v1`

---

## 🔐 Authentication

By default (fresh install), the API is **Open**. Anyone can use it.
To secure it, you generate **Access Tokens**.

**Note:** Hydra tokens are NOT `sk-` keys. They can be any string, but we recommend letting Hydra generate secure UUIDs.

```bash
# Create a token description 'cursor-ide'
hydra tokens create --name cursor-ide
# Output: hydra-8f3a2b1c-.... (Your Secure Token)

# List active tokens
hydra tokens list
```

Add the header to your requests:
`Authorization: Bearer hydra-8f3a2b1c-...`

---

## 🔌 API Reference

Hydra is 100% OpenAI-compatible.

### Python (OpenAI SDK)
```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="hydra-8f3a..."  # Your Hydra Token
)

response = client.chat.completions.create(
    model="gemini-3.5-flash-lite",
    messages=[{"role": "user", "content": "Hello!"}],
    stream=True
)
for chunk in response:
    print(chunk.choices[0].delta.content or "", end="")
```

### Node.js
```javascript
import OpenAI from 'openai';

const client = new OpenAI({
    baseURL: 'http://localhost:8000/v1',
    apiKey: 'hydra-8f3a...'
});
```

### Supported Models
-   `gemini-3.6-flash` / `gemini-3.5-flash` / `gemini-3.7-flash` (newest free-tier flash)
-   `gemini-3-flash-preview` (Gemini 3 flash preview)
-   `gemini-3.5-flash-lite` / `gemini-3.1-flash-lite` (highest free-tier RPD)
-   `gemini-2.5-flash-lite` (reliable fallback)
-   `gemini-2.5-flash-image` (image generation)
-   `gemini-embedding-001` (embeddings)

---

## 🤖 Advanced Features

### 👁️ Vision (Multimodal)
Send images using standard OpenAI format (URL or Base64).

```python
response = client.chat.completions.create(
    model="gemini-3.5-flash-lite",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}}
            ]
        }
    ]
)
```

### ⚙️ Function Calling (Tool Use)
Define tools in Python/JS, and Hydra converts them for Gemini.

```python
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "parameters": {
            "type": "object",
            "properties": {"location": {"type": "string"}}
        }
    }
}]

# Hydra handles the translation automatically
client.chat.completions.create(..., tools=tools)
```

### 🌍 Web Search (Grounding)
Enable Google's real-time search grounding by passing a special tool.
```json
// In your raw request or tool definition
"tools": [{"google_search": {}}]
```

---

## 🛡️ Admin & Tunneling

### Admin Dashboard (`/dashboard`)
Access `http://localhost:8000/dashboard` to view:
-   **RPM Graph**: Live traffic monitoring.
-   **Key Status**: Which keys are healthy (green), limited (yellow), or dead (red).
-   **Token Manager**: Revoke access instantly.

> **Security**: The Dashboard is accessible **ONLY via Localhost**. It is blocked on public URLs.

### Public Access (Tunneling)
Want to use Hydra from a mobile app or a friend's computer?
```bash
hydra gateway --expose
```
Hydra downloads `cloudflared` and creates a minimal secure tunnel.
You will get a URL like: `https://cool-name.trycloudflare.com`
Use this URL as your `base_url`.

---

## ⚠️ Troubleshooting

| Error Code | Meaning | Solution |
|---|---|---|
| `429` | Rate Limit | All your keys are exhausted. Add more projects/keys! |
| `401` | Unauthorized | Your `Authorization` header is missing or invalid. Check `hydra tokens list`. |
| `503` | Gateway Error | Hydra can't reach Google. Check your internet connection. |
| `WinError 1225` | `ConnectionRefused` | **Redis is NOT running!**<br>**Fix**: Run `install_windows.bat`. It will auto-install and start Redis for you. |
| `Command Not Found` | `'hydra' is not recognized` | **Fix**: run `install_windows.bat` again, or check your PATH.

---
<div align="center">
Built with ❤️ by the Open Source Community
</div>
