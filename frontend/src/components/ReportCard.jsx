const SEVERITY_COLORS = {
  None:     'bg-gray-700 text-gray-300',
  Low:      'bg-green-900 text-green-300',
  Moderate: 'bg-yellow-900 text-yellow-300',
  High:     'bg-red-900 text-red-300',
}

export default function ReportCard({ report }) {
  const { summary, severity, recommendations } = report

  return (
    <div className="bg-gray-900 rounded-2xl p-6 space-y-4">
      <div className="flex justify-between items-center">
        <h3 className="font-semibold text-lg">📋 AI Inspection Report</h3>
        <span className={`text-xs font-semibold px-3 py-1 rounded-full ${SEVERITY_COLORS[severity] || SEVERITY_COLORS.Moderate}`}>
          {severity} Severity
        </span>
      </div>

      <p className="text-gray-300 leading-relaxed">{summary}</p>

      <div>
        <h4 className="text-sm text-gray-400 mb-2 font-medium">Recommended Actions</h4>
        <ul className="space-y-2">
          {recommendations.map((rec, i) => (
            <li key={i} className="flex items-start gap-2 text-sm text-gray-300">
              <span className="text-blue-400 mt-0.5">✓</span>
              {rec}
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}