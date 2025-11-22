import React from 'react'

export default function UploadDropzone({ files, setFiles }) {
  const handleFiles = e => {
    const arr = Array.from(e.target.files)
    setFiles(prev => [...prev, ...arr])
  }

  return (
    <div className="w-full bg-white/30 backdrop-blur-xl p-6 rounded-2xl shadow-xl border border-white/40">
      <h2 className="text-xl font-semibold text-white mb-3 drop-shadow">
        Upload Your Images
      </h2>

      <label className="block w-full cursor-pointer">
        <div className="w-full p-6 bg-white/20 border-2 border-dashed border-white/50 rounded-2xl text-center text-white hover:bg-white/30 transition">
          Click to select images
        </div>
        <input
          type="file"
          multiple
          accept="image/*"
          onChange={handleFiles}
          className="hidden"
        />
      </label>

      <div className="grid grid-cols-3 gap-3 mt-4">
        {files.map((f, i) => (
          <div
            key={i}
            className="relative rounded-xl overflow-hidden shadow-lg border border-white/40"
          >
            <img
              src={URL.createObjectURL(f)}
              className="w-full h-24 object-cover"
            />
          </div>
        ))}
      </div>
    </div>
  )
}
