import React, { useState } from 'react'
import axios from 'axios'
import UploadDropzone from './components/UploadDropzone'
import ResultPreview from './components/ResultPreview'
import './index.css'

export default function App() {
  const [files, setFiles] = useState([])
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const API = import.meta.env.VITE_API_BASE || '';  // <-- IMPORTANT

  const handleUpload = async () => {
    if (files.length < 2) {
      setError('Upload at least 2 images')
      return
    }

    setLoading(true)
    setError(null)

    const form = new FormData()
    files.forEach(f => form.append('images', f))

    try {
      const res = await axios.post(`${API}/stitch`, form, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      setResult(res.data)
    } catch (err) {
      console.error(err)
      setError('Images could not be stitched! Likely not enough keypoints being detected!')
    }

    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-500 via-pink-500 to-blue-500 p-8 flex justify-center items-start">
      <div className="w-full max-w-4xl bg-white/20 backdrop-blur-xl shadow-2xl rounded-3xl p-10 border border-white/30">

        <h1 className="text-5xl font-extrabold text-white drop-shadow-lg text-center mb-8">
          Panorama Stitcher
        </h1>

        <UploadDropzone files={files} setFiles={setFiles} />

        <div className="mt-6 flex justify-center gap-4">
          <button
            onClick={handleUpload}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-xl shadow-lg transition transform hover:scale-105"
          >
            Generate Panorama
          </button>

          <button
            onClick={() => { setFiles([]); setResult(null); setError(null) }}
            className="px-6 py-3 bg-white/30 backdrop-blur-lg border border-white/40 text-white rounded-xl hover:bg-white/40 transition"
          >
            Reset
          </button>
        </div>

        {loading && (
          <div className="mt-6 text-center text-white text-lg animate-pulse">
            Processing images…
          </div>
        )}

        {error && (
          <div className="mt-6 text-center text-red-200 text-lg">
            {error}
          </div>
        )}

        {result && <ResultPreview result={result} />}
      </div>
    </div>
  )
}
