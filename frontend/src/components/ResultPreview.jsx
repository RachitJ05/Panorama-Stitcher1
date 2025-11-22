import React from 'react'

export default function ResultPreview({ result }) {
  const createUrl = p => `/download?path=${encodeURIComponent(p)}&t=${Date.now()}`

  return (
    <div className="mt-10 flex flex-col items-center">
      <h2 className="text-4xl font-bold text-white drop-shadow mb-6">
        Stitched Image
      </h2>

      <div className="w-full max-w-3xl bg-white/20 backdrop-blur-xl rounded-3xl p-6 shadow-2xl border border-white/30">
        <img
          src={createUrl(result.cropped)}
          className="w-full rounded-xl shadow-lg hover:scale-[1.02] transition-transform duration-300"
        />

        <div className="text-center mt-6">
          <a
            href={createUrl(result.cropped)}
            className="px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-xl shadow-lg transition font-semibold"
          >
            Download Image
          </a>
        </div>
      </div>
    </div>
  )
}
