import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts'

const COLORS = ['#3b82f6','#f59e0b','#10b981','#ef4444','#8b5cf6','#ec4899']

export default function ResultPanel({ result }) {
  const { detections, annotated_image, gradcam_image, inference_time_ms } = result

  const chartData = detections.map((d, i) => ({
    name:       d.defect,
    confidence: Math.round(d.confidence * 100),
    fill:       COLORS[i % COLORS.length],
  }))

  return (
    <div className="space-y-6">

      {/* Images */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-gray-900 rounded-2xl p-4">
          <h3 className="text-sm text-gray-400 mb-2">Detection Result</h3>
          <img
            src={`data:image/jpeg;base64,${annotated_image}`}
            className="w-full rounded-lg object-contain"
          />
        </div>
        <div className="bg-gray-900 rounded-2xl p-4">
          <h3 className="text-sm text-gray-400 mb-2">EigenCAM Explainability</h3>
          <img
            src={`data:image/jpeg;base64,${gradcam_image}`}
            className="w-full rounded-lg object-contain"
          />
        </div>
      </div>

      {/* Stats */}
      <div className="bg-gray-900 rounded-2xl p-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="font-semibold">Detections</h3>
          <span className="text-sm text-gray-400">⏱ {inference_time_ms}ms</span>
        </div>

        {detections.length === 0 ? (
          <p className="text-gray-400">No defects detected.</p>
        ) : (
          <>
            {/* Table */}
            <div className="overflow-x-auto mb-6">
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-gray-400 border-b border-gray-800">
                    <th className="text-left py-2">Defect</th>
                    <th className="text-left py-2">Confidence</th>
                    <th className="text-left py-2">Area</th>
                    <th className="text-left py-2">Location</th>
                  </tr>
                </thead>
                <tbody>
                  {detections.map((d, i) => (
                    <tr key={i} className="border-b border-gray-800">
                      <td className="py-2 font-medium">{d.defect}</td>
                      <td className="py-2">
                        <span className="bg-blue-900 text-blue-300 px-2 py-0.5 rounded text-xs">
                          {Math.round(d.confidence * 100)}%
                        </span>
                      </td>
                      <td className="py-2">{d.area_percent}%</td>
                      <td className="py-2 text-gray-400">{d.location}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Chart */}
            <h4 className="text-sm text-gray-400 mb-2">Confidence Chart</h4>
            <ResponsiveContainer width="100%" height={180}>
              <BarChart data={chartData}>
                <XAxis dataKey="name" tick={{ fill: '#9ca3af', fontSize: 11 }} />
                <YAxis domain={[0, 100]} tick={{ fill: '#9ca3af', fontSize: 11 }} unit="%" />
                <Tooltip
                  formatter={(v) => [`${v}%`, 'Confidence']}
                  contentStyle={{ backgroundColor: '#1f2937', border: 'none', borderRadius: '8px' }}
                />
                <Bar dataKey="confidence" radius={[4, 4, 0, 0]}>
                  {chartData.map((entry, i) => (
                    <Cell key={i} fill={entry.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </>
        )}
      </div>
    </div>
  )
}