import { useState } from 'react'

export default function App() {
  const [creds, setCreds] = useState({
    token: '',
    refresh_token: '',
    client_id: '',
    client_secret: '',
  })
  const [messages, setMessages] = useState([])

  const listSubs = async () => {
    const res = await fetch('http://localhost:5000/subscriptions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(creds),
    })
    const data = await res.json()
    setMessages(data.messages || [])
  }

  const unsubscribe = async (id) => {
    await fetch('http://localhost:5000/unsubscribe', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...creds, message_id: id }),
    })
    setMessages(messages.filter((m) => m.id !== id))
  }

  return (
    <div>
      <h1>LeaveMeAlone</h1>
      {['token', 'refresh_token', 'client_id', 'client_secret'].map((k) => (
        <input
          key={k}
          placeholder={k}
          value={creds[k]}
          onChange={(e) => setCreds({ ...creds, [k]: e.target.value })}
        />
      ))}
      <button onClick={listSubs}>List Subscriptions</button>
      <ul>
        {messages.map((m) => (
          <li key={m.id}>
            {m.subject} - {m.from}
            <button onClick={() => unsubscribe(m.id)}>Unsub & Delete</button>
          </li>
        ))}
      </ul>
    </div>
  )
}
