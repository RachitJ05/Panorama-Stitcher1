# 🌄 Panorama Stitcher  
A full-stack React + Flask application that stitches multiple images into a panoramic output using OpenCV.  
The system performs automatic geometric cropping to extract the largest valid rectangular region.

## 🚀 Features
- 📸 Upload multiple overlapping images  
- 🧠 Auto-stitching with OpenCV  
- ✂️ Smart geometric cropping  
- 🎨 Attractive UI (glassmorphism + gradients)  
- ⚡ React + Vite frontend  
- 🔌 Flask backend  
- 📥 Download final stitched image  
- 🚫 Cache-busting ensures fresh images every time  

## 🛠️ Tech Stack
### Frontend
- React (Vite)
- TailwindCSS
- Axios  

### Backend
- Python (Flask)
- OpenCV
- NumPy

## 🗂️ Project Structure
panorama-stitcher/
├── backend/
│   ├── app.py
│   ├── stitcher.py
│   ├── requirements.txt
│   └── uploads/ (generated at runtime)
├── frontend/
│   ├── index.html
│   ├── vite.config.js
│   ├── tailwind.config.cjs
│   ├── postcss.config.cjs
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── index.css
│       └── components/
│           ├── UploadDropzone.jsx
│           └── ResultPreview.jsx
└── README.md

## 🧩 Setup Instructions
### Backend
```
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Frontend
```
cd frontend
npm install
npm run dev
```

<img width="2559" height="1186" alt="image" src="https://github.com/user-attachments/assets/34b6e87f-f462-4c1e-8b4d-0d72bfa0a398" />


## 📦 Deployment
Frontend → Vercel / Netlify  
Backend → Render / Railway / Heroku
