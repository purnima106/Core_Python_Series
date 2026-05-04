import { useState } from 'react'
import './App.css'

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
      const response = await fetch('/api/review', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pr_url: prUrl })
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Something went wrong')
      }

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
              {typeof review === 'string'
                ? review
                : JSON.stringify(review, null, 2)}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default App
