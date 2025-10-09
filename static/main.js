document.addEventListener('DOMContentLoaded', () => {
  const askBtn = document.getElementById('ask')
  const questionEl = document.getElementById('question')
  const authEl = document.getElementById('auth')
  const sessionEl = document.getElementById('session_id')
  const newSessionBtn = document.getElementById('new_session')
  const resetSessionBtn = document.getElementById('reset_session')
  const messagesEl = document.getElementById('messages')

  // initialize session input from localStorage
  if (sessionEl) {
    const saved = localStorage.getItem('session_id')
    if (saved) sessionEl.value = saved
  }

  if (newSessionBtn) {
    newSessionBtn.addEventListener('click', (e) => {
      e.preventDefault()
      let id = ''
      if (window.crypto && crypto.randomUUID) {
        id = crypto.randomUUID()
      } else {
        id = Math.random().toString(36).slice(2) + Date.now().toString(36)
      }
      if (sessionEl) {
        sessionEl.value = id
        localStorage.setItem('session_id', id)
      }

      appendMessage('==== New Session Started ====', 'user');
    })
  }

  if (resetSessionBtn) {
    resetSessionBtn.addEventListener('click', async (e) => {
      e.preventDefault()
      const auth = authEl.value.trim()
      if (!auth) {
        alert('Please provide auth token to reset sessions')
        return
      }

      try {
        const res = await fetch('/reset', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ auth_token: auth })
        })

        if (!res.ok) {
          const err = await res.json().catch(() => ({ error: res.statusText }))
          alert('Reset failed: ' + (err.error || res.statusText))
          return
        }

        const data = await res.json()
        // clear local session and UI
        localStorage.removeItem('session_id')
        if (sessionEl) sessionEl.value = ''
        messagesEl.innerHTML = ''

        alert('Sessions reset on server: ' + (data.status || 'ok'))
      } catch (err) {
        alert('Network error: ' + err.message)
      }
    })
  }

  function appendMessage(text, side = 'bot', meta = null) {
    const wrapper = document.createElement('div')
    wrapper.className = `message ${side}`

    const bubble = document.createElement('div')
    bubble.className = 'bubble'
    bubble.textContent = text

    wrapper.appendChild(bubble)

    if (meta) {
      const metaEl = document.createElement('div')
      metaEl.className = 'meta'
      if (meta.files && meta.files.length) {
        const filesTitle = document.createElement('div')
        filesTitle.className = 'meta-title'
        filesTitle.textContent = 'Files used:'
        metaEl.appendChild(filesTitle)

        const ul = document.createElement('ul')
        meta.files.forEach(f => {
          const li = document.createElement('li')
          li.textContent = f
          ul.appendChild(li)
        })
        metaEl.appendChild(ul)
      }

      if (meta.file_search_text) {
        const fsTitle = document.createElement('div')
        fsTitle.className = 'meta-title'
        fsTitle.textContent = 'File search text:'
        metaEl.appendChild(fsTitle)

        const pre = document.createElement('pre')
        pre.textContent = meta.file_search_text
        metaEl.appendChild(pre)
      }

      if (meta.sources && meta.sources.length) {
        const srcTitle = document.createElement('div')
        srcTitle.className = 'meta-title'
        srcTitle.textContent = 'Sources:'
        metaEl.appendChild(srcTitle)

        const ul = document.createElement('ul')
        meta.sources.forEach(s => {
          const li = document.createElement('li')
          li.textContent = s
          ul.appendChild(li)
        })
        metaEl.appendChild(ul)
      }

      if (meta.tools_used && meta.tools_used.length) {
        const tTitle = document.createElement('div')
        tTitle.className = 'meta-title'
        tTitle.textContent = 'Tools used:'
        metaEl.appendChild(tTitle)

        const ul = document.createElement('ul')
        meta.tools_used.forEach(t => {
          const li = document.createElement('li')
          li.textContent = t
          ul.appendChild(li)
        })
        metaEl.appendChild(ul)
      }

      wrapper.appendChild(metaEl)
    }

    messagesEl.appendChild(wrapper)
    messagesEl.scrollTop = messagesEl.scrollHeight
  }

  async function sendQuestion() {
    const q = questionEl.value
    const auth = authEl.value.trim()
    let session_id = sessionEl.value.trim()
    if (!session_id) {
      // try localStorage
      session_id = localStorage.getItem('session_id') || ''
    } else {
      localStorage.setItem('session_id', session_id)
    }
    if (!q.trim()) return

    // append user message
    appendMessage(q.trim(), 'user')
    questionEl.value = ''

    // append bot placeholder
    appendMessage('Thinking...', 'bot')

    try {
      const res = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: q, auth_token: auth, session_id })
      })

      // remove the last bot placeholder
      const bots = messagesEl.querySelectorAll('.message.bot')
      const lastBot = bots[bots.length - 1]
      if (!res.ok) {
        const err = await res.json().catch(() => ({ error: res.statusText }))
        if (lastBot) lastBot.querySelector('.bubble').textContent = `Error: ${err.error || res.statusText}`
        return
      }

      const data = await res.json()
      // persist session_id returned by server (if server generated one)
      if (data && data.session_id) {
        if (sessionEl) {
          sessionEl.value = data.session_id
        }
        localStorage.setItem('session_id', data.session_id)
      }
      if (lastBot) lastBot.querySelector('.bubble').textContent = data.answer || 'No answer returned.'

      // attach meta under the bot message (files, file search text, sources, tools)
      if (lastBot) {
        const meta = {
          files: data.files_used || [],
          file_search_text: data.file_search_text || '',
          sources: data.sources || [],
          tools_used: data.tools_used || []
        }

        if (meta.files.length || meta.file_search_text || meta.sources.length || meta.tools_used.length) {
          const metaEl = document.createElement('div')
          metaEl.className = 'meta'

          if (meta.files.length) {
            const filesTitle = document.createElement('div')
            filesTitle.className = 'meta-title'
            filesTitle.textContent = 'Files used:'
            metaEl.appendChild(filesTitle)

            const ul = document.createElement('ul')
            meta.files.forEach(f => {
              const li = document.createElement('li')
              li.textContent = f
              ul.appendChild(li)
            })
            metaEl.appendChild(ul)
          }

          if (meta.file_search_text) {
            const fsTitle = document.createElement('div')
            fsTitle.className = 'meta-title'
            fsTitle.textContent = 'File search text:'
            metaEl.appendChild(fsTitle)

            const pre = document.createElement('pre')
            pre.textContent = meta.file_search_text
            metaEl.appendChild(pre)
          }

          if (meta.sources.length) {
            const srcTitle = document.createElement('div')
            srcTitle.className = 'meta-title'
            srcTitle.textContent = 'Sources:'
            metaEl.appendChild(srcTitle)

            const ul = document.createElement('ul')
            meta.sources.forEach(s => {
              const li = document.createElement('li')
              li.textContent = s
              ul.appendChild(li)
            })
            metaEl.appendChild(ul)
          }

          if (meta.tools_used.length) {
            const tTitle = document.createElement('div')
            tTitle.className = 'meta-title'
            tTitle.textContent = 'Tools used:'
            metaEl.appendChild(tTitle)

            const ul = document.createElement('ul')
            meta.tools_used.forEach(t => {
              const li = document.createElement('li')
              li.textContent = t
              ul.appendChild(li)
            })
            metaEl.appendChild(ul)
          }

          lastBot.appendChild(metaEl)
        }
      }
    } catch (e) {
      const bots = messagesEl.querySelectorAll('.message.bot')
      const lastBot = bots[bots.length - 1]
      if (lastBot) lastBot.querySelector('.bubble').textContent = 'Network error: ' + e.message
    }
  }

  askBtn.addEventListener('click', sendQuestion)

  // Send on Enter, allow Shift+Enter for newline
  questionEl.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendQuestion()
    }
  })
})
