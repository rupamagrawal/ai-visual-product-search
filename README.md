# 👚 AI Visual Product Search Web App

A full-stack artificial intelligence web application that allows users to seamlessly upload a picture of a clothing item (like a hoodie, shoes, or jeans), detects its object and dominant color locally using Machine Learning, and immediately returns real-world shopping links so they can buy it!

## 🚀 Features
- **Local AI Object Detection**: Uses a lightweight TensorFlow model (MobileNetV2) with a custom, highly-accurate mapping logic capable of zeroing in on 30+ fashion specific items completely offline.
- **K-Means Color & Pattern Detection**: Utilizes OpenCV image processing and mathematical K-Means clustering to extract the exact dominant color profile.
- **Live Shopping Data**: Pings the SerpAPI (Google Shopping) engine with the AI-generated query (e.g., "yellow hoodie") to bring back live product titles, images, and buy links.
- **Modern User Interface**: A gorgeous Single Page Application (SPA) built entirely with React and styled flawlessly with Tailwind CSS.

## 🛠️ Tech Stack
**Frontend:**
- React (Vite)
- Tailwind CSS

**Backend:**
- Python & Flask (REST API)
- TensorFlow / Keras (MobileNetV2)
- OpenCV (Computer Vision logic)
- SerpAPI (Google Shopping integration)

## 🌊 Application Flow (Architecture)
1. **Frontend Request**: The React UI allows the user to upload a local image file and sends it to the Flask backend via an async POST request.
2. **Object Labelling**: The image is pre-processed (scaled and resampled) up to `224x224` and parsed by TensorFlow MobileNetV2. It scans for the top 5 image guesses and maps them to a dictionary of 30 exact wardrobe terms.
3. **Color Extraction**: OpenCV crops out the background, converts RGB to HSV, and mathematically clusters the remaining pixels to deduce the exact dominant color (e.g. mapping dark-grey/black to purely "black").
4. **Google Shopping Search**: The backend strings the color and the object together (e.g. `"black dress"`) and calls SerpAPI, fetching live products.
5. **Render Results**: The shopping JSON payload is returned to the Frontend and beautifully rendered on `ResultCards`.

## ⚙️ How to install & run locally

### 1. Set up your secret keys
You will need a SerpAPI key which is free to get at `serpapi.com`. 
Navigate into the `backend/` folder and create a `.env` file containing:
```env
SERPAPI_KEY=your_key_here
```

### 2. Start the Python Backend
Open a terminal inside the `/backend` folder:
```bash
# Create a virtual environment
python -m venv .venv

# Activate it (on Windows Git Bash)
source .venv/Scripts/activate

# Install the Python requirements
pip install -r requirements.txt

# Start the Flask API
python app.py
```

### 3. Start the React Frontend
Open a *second* terminal tab inside the `/frontend` folder:
```bash
# Install node modules
npm install

# Start the Vite development server
npm run dev
```

Finally, open your browser and go to `http://localhost:5173/`
