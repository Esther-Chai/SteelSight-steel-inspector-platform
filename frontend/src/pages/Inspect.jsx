import { useState, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { predictAPI, reportAPI } from '../services/api'
import ResultPanel from '../components/ResultPanel'
import ReportCard from '../components/ReportCard'

const SAMPLE_IMAGES = [
  { name: 'Crazing 1',         file: 'crazing_1.jpg' },
  { name: 'Crazing 2',         file: 'crazing_2.jpg' },
  { name: 'Inclusion 1',       file: 'inclusion_1.jpg' },
  { name: 'Inclusion 2',       file: 'inclusion_2.jpg' },
  { name: 'Patches 1',         file: 'patches_1.jpg' },
  { name: 'Patches 2',         file: 'patches_2.jpg' },
  { name: 'Pitted Surface 1',  file: 'pitted_surface_1.jpg' },
  { name: 'Pitted Surface 2',  file: 'pitted_surface_2.jpg' },
  { name: 'Rolled-in Scale 1', file: 'rolled-in_scale_1.jpg' },
  { name: 'Rolled-in Scale 2', file: 'rolled-in_scale_2.jpg' },
  { name: 'Scratches 1',       file: 'scratches_1.jpg' },
  { name: 'Scratches 2',       file: 'scratches_2.jpg' },
]

export default function Inspect() {
  const navigate  = useNavigate()
  const fileRef   = useRef()
  const [preview,    setPreview]    = useState(null)
  const [result,     setResult]     = useState(null)
  const [report,     setReport]     = useState(null)
  const [loading,    setLoading]    = useState(false)
  const [reportLoad, setReportLoad] = useState(false)
  const [error,      setError]      = useState('')
  const [threshold,  setThreshold]  = useState(0.15)   // ← moved inside

  const handleFile = (file) => {
    if (!file) return
    setPreview(URL.createObjectURL(file))
    setResult(null)
    setReport(null)
    setError('')
  }

  const handleUpload = (e) => handleFile(e.target.files[0])

  const handleDrop = (e) => {
    e.preventDefault()
    handleFile(e.dataTransfer.files[0])
  }

  const handleSample = async (filename) => {
    const res  = await fetch(`/samples/${filename}`)
    const blob = await res.blob()
    const file = new File([blob], filename, { type: 'image/jpeg' })
    handleFile(file)
    fileRef.current._file = file
  }

  const handleInspect = async () => {
    const file = fileRef.current?.files?.[0] || fileRef.current?._file
    if (!file) return
    setLoading(true)
    setError('')
    try {
      const fd = new FormData()
      fd.append('file', file)
      fd.append('conf_threshold', threshold)
      const res = await predictAPI.predict(fd)
      setResult(res.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Inspection failed')
    } finally {
      setLoading(false)
    }
  }

  const handleReport = async () => {
    if (!result) return
    setReportLoad(true)
    try {
      const res = await reportAPI.generate(result.detections)
      setReport(res.data)
    } catch {
      setError('Report generation failed')
    } finally {
      setReportLoad(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    navigate('/login')
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white">

      {/* Navbar */}
      <nav className="bg-gray-900 border-b border-gray-800 px-6 py-4 flex justify-between items-center">
        <h1 className="text-xl font-bold">🔩 SteelSight</h1>
        <button onClick={handleLogout} className="text-gray-400 hover:text-white text-sm transition">
          Logout
        </button>
      </nav>

      <div className="max-w-6xl mx-auto px-4 py-8 space-y-8">

        {/* Upload Section */}
        <div className="bg-gray-900 rounded-2xl p-6">
          <h2 className="text-lg font-semibold mb-4">Upload Image</h2>

          {/* Drop zone */}
          <div
            onDrop={handleDrop}
            onDragOver={e => e.preventDefault()}
            onClick={() => fileRef.current.click()}
            className="border-2 border-dashed border-gray-700 hover:border-blue-500 rounded-xl p-10 text-center cursor-pointer transition"
          >
            {preview
              ? <img src={preview} className="max-h-48 mx-auto rounded-lg object-contain" />
              : <p className="text-gray-400">Drag & drop an image here, or click to browse</p>
            }
          </div>
          <input
            ref={fileRef}
            type="file"
            accept="image/jpeg,image/png"
            onChange={handleUpload}
            className="hidden"
          />

          {/* Sample images */}
          <div className="mt-4">
            <p className="text-sm text-gray-400 mb-2">Or try a sample:</p>
            <div className="flex flex-wrap gap-2">
              {SAMPLE_IMAGES.map(s => (
                <button
                  key={s.file}
                  onClick={() => handleSample(s.file)}
                  className="bg-gray-800 hover:bg-gray-700 text-sm px-3 py-1.5 rounded-lg transition"
                >
                  {s.name}
                </button>
              ))}
            </div>
          </div>

          {/* Confidence Threshold Slider */}
          <div className="mt-4">
            <div className="flex justify-between items-center mb-1">
              <label className="text-sm text-gray-400">Confidence Threshold</label>
              <span className="text-sm font-semibold text-blue-400">{Math.round(threshold * 100)}%</span>
            </div>
            <input
              type="range"
              min="0.10"
              max="0.90"
              step="0.05"
              value={threshold}
              onChange={e => setThreshold(parseFloat(e.target.value))}
              className="w-full accent-blue-500"
            />
            <div className="flex justify-between text-xs text-gray-600 mt-1">
              <span>10% — more detections</span>
              <span>90% — fewer, high confidence only</span>
            </div>
          </div>

          {/* Inspect button */}
          <button
            onClick={handleInspect}
            disabled={!preview || loading}
            className="mt-4 w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-50 font-semibold py-2.5 rounded-lg transition"
          >
            {loading ? 'Inspecting...' : 'Run Inspection'}
          </button>

          {error && <p className="text-red-400 text-sm mt-2">{error}</p>}
        </div>

        {/* Results */}
        {result && (
          <>
            <ResultPanel result={result} />
            <div className="text-center">
              <button
                onClick={handleReport}
                disabled={reportLoad}
                className="bg-green-600 hover:bg-green-700 disabled:opacity-50 font-semibold px-8 py-2.5 rounded-lg transition"
              >
                {reportLoad ? 'Generating Report...' : '📋 Generate AI Inspection Report'}
              </button>
            </div>
          </>
        )}

        {/* Report */}
        {report && <ReportCard report={report} />}
      </div>
    </div>
  )
}