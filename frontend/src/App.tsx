import { useEffect, useState } from 'react'

type Health =
  | { state: 'loading' }
  | { state: 'ok'; status: string }
  | { state: 'error'; message: string }

function App() {
  const [health, setHealth] = useState<Health>({ state: 'loading' })

  useEffect(() => {
    const controller = new AbortController()

    fetch('/api/health', { signal: controller.signal })
      .then(async (res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        const body: { status: string } = await res.json()
        setHealth({ state: 'ok', status: body.status })
      })
      .catch((err: unknown) => {
        if (controller.signal.aborted) return
        setHealth({
          state: 'error',
          message: err instanceof Error ? err.message : String(err),
        })
      })

    return () => controller.abort()
  }, [])

  return (
    <main>
      <h1>Backend health</h1>
      {health.state === 'loading' && <p>Checking…</p>}
      {health.state === 'ok' && <p>Status: {health.status}</p>}
      {health.state === 'error' && <p role="alert">Error: {health.message}</p>}
    </main>
  )
}

export default App
