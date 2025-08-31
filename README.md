# 🐍 Snake Game on WS2812 LEDs

This project runs the classic **Snake game** on an **8×8 WS2812 LED matrix** using a **Raspberry Pi 5**.  
It uses **FastAPI** as the backend server to control the game logic and LED display.  

⚠️ **Important:** This project only works on a Raspberry Pi 5 with WS2812 LEDs.

---

## 🚀 Features
- Snake game logic implemented in Python.
- WS2812 LED control via Raspberry Pi 5 SPI interface.
- REST API endpoints to move the snake:
  - `/up`
  - `/down`
  - `/left`
  - `/right`
- Lightweight server using [FastAPI](https://fastapi.tiangolo.com/).

---

## 🛠 Hardware Requirements
- Raspberry Pi 5  
- WS2812 LED strip/matrix (8×8 = 64 pixels)  
- Power supply sufficient for WS2812 strip

### 🔌 Wiring
Connect the WS2812 **DIN (Data In)** pin to the Raspberry Pi 5:

- **DIN → MOSI (GPIO10 / Pin 19)**  
- **5V → 5V (Pin 2 or Pin 4)**  
- **GND → GND (Pin 6, 9, 14, …)**  

---

## 📦 Installation & Setup

Clone the repository:

```bash
git clone https://github.com/MaksioPiksio/Snake.git
cd Snake
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows (PowerShell)
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Server

Start the server with **uvicorn**:

```bash
uvicorn server:app --host 10.0.0.22 --port 8459
```

- Replace `10.0.0.22` with your Raspberry Pi’s IP address.  
- The app will be available at:  
  👉 `http://10.0.0.22:8459`

---

## 🎮 Controlling the Game

You can control the snake using HTTP requests. Example with **JavaScript fetch**:

```javascript
fetch("http://10.0.0.22:8459/up", { method: "GET" });
fetch("http://10.0.0.22:8459/down", { method: "GET" });
fetch("http://10.0.0.22:8459/left", { method: "GET" });
fetch("http://10.0.0.22:8459/right", { method: "GET" });
```

---

## ⚡ Notes
- Ensure your Raspberry Pi 5 SPI interface is enabled (`raspi-config`).  
- Use an adequate power supply to avoid LED flickering.  
- Only tested with WS2812 LEDs; other LED types may require different drivers.

---

## 📚 References
- [FastAPI Documentation](https://fastapi.tiangolo.com/)  
- [WS2812 LED Control on Raspberry Pi](https://github.com/niklasr22/rpi5-ws2812)  

---

Enjoy your Snake game on LEDs! 🐍✨
