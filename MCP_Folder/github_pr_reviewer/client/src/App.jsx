import { useState } from 'react'
import './App.css'
import { API, apiCall } from './api'

function App() {
  const [prUrl, setPrUrl] = useState('')
  const [review, setReview] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!prUrl.trim()) return

    setLoading(true)
    setReview(null)
    setError(null)

    try {
      // Use centralized API call with environment-based URL
      // API.reviewPR uses VITE_API_URL from .env
      const data = await apiCall(API.reviewPR, {
        method: 'POST',
        body: JSON.stringify({ pr_url: prUrl })
      })

      setReview(data.review)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <div className="header__icon">🔍</div>
        <h1 className="header__title">PR Reviewer</h1>
        <p className="header__subtitle">
          AI-powered GitHub Pull Request analysis
        </p>
      </header>

      <div className="card">
        <form className="form" onSubmit={handleSubmit}>
          <label className="form__label" htmlFor="pr-url">
            Pull Request URL
          </label>
          <input
            id="pr-url"
            className="form__input"
            type="url"
            placeholder="https://github.com/owner/repo/pull/123"
            value={prUrl}
            onChange={(e) => setPrUrl(e.target.value)}
            required
          />
          <button
            className="form__button"
            type="submit"
            disabled={loading || !prUrl.trim()}
          >
            {loading ? 'Analyzing…' : 'Review PR'}
          </button>
        </form>

        {loading && (
          <div className="loading">
            <div className="loading__spinner" />
            <span>AI is reviewing the pull request…</span>
          </div>
        )}
      </div>

      {error && (
        <div className="error">
          <div className="error__card">
            <span>⚠️</span>
            <span>{error}</span>
          </div>
        </div>
      )}

      {review && (
        <div className="result">
          <div className="result__card">
            <div className="result__title">
              <span>✅</span> Review Complete
            </div>
            <div className="result__content">
              {typeof review === 'string' ? (
                review
              ) : (
                <div className="review-sections">
                  {/* Summary Section */}
                  <div className="review-section">
                    <h2 className="section-title">📋 Summary</h2>
                    <p className="section-text">{review.summary || 'No summary available'}</p>
                  </div>

                  {/* Risk Section */}
                  <div className="review-section">
                    <h2 className="section-title">⚠️ Risk Level</h2>
                    <p className={`risk-level risk-${review.risk?.toLowerCase() || 'unknown'}`}>
                      {review.risk?.charAt(0).toUpperCase() + review.risk?.slice(1).toLowerCase() || 'Unknown'}
                    </p>
                  </div>

                  {/* Issues Section */}
                  <div className="review-section">
                    <h2 className="section-title">🐛 Issues</h2>
                    {review.issues && review.issues.length > 0 ? (
                      <ul className="issues-list">
                        {review.issues.map((issue, idx) => (
                          <li key={idx} className="issue-item">{issue}</li>
                        ))}
                      </ul>
                    ) : (
                      <p className="no-items">No issues found</p>
                    )}
                  </div>

                  {/* Suggestions Section */}
                  <div className="review-section">
                    <h2 className="section-title">💡 Suggestions</h2>
                    {review.suggestions && review.suggestions.length > 0 ? (
                      <ul className="suggestions-list">
                        {review.suggestions.map((suggestion, idx) => (
                          <li key={idx} className="suggestion-item">{suggestion}</li>
                        ))}
                      </ul>
                    ) : (
                      <p className="no-items">No suggestions</p>
                    )}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default App
