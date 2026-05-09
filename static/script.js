// Global Auth
document.addEventListener('DOMContentLoaded', () => {
    const authArea = document.getElementById('authArea');
    if (authArea) {
        const isAuth = localStorage.getItem('nexus_auth');
        if (isAuth === 'true') {
            authArea.innerHTML = `
                <div class="auth-nav">
                    <a href="dashboard.html" class="avatar">JD</a>
                    <div class="logout-btn" onclick="logout()">Logout</div>
                </div>
            `;
        } else {
            authArea.innerHTML = `
                <a href="login.html" class="nav-btn" style="text-decoration:none;">Sign In</a>
            `;
        }
    }

    // Chatbot Initialization
    const chatBtn = document.getElementById('chatToggleBtn');
    const chatWidget = document.getElementById('chatWidget');
    const chatClose = document.getElementById('chatClose');
    const chatInput = document.getElementById('chatInput');
    const chatSend = document.getElementById('chatSend');
    const chatBody = document.getElementById('chatBody');

    if (chatBtn && chatWidget) {
        chatBtn.addEventListener('click', () => chatWidget.classList.add('open'));
        chatClose.addEventListener('click', () => chatWidget.classList.remove('open'));

        async function sendChatMessage() {
            const text = chatInput.value.trim();
            if (!text) return;

            // Append User Msg
            const uMsg = document.createElement('div');
            uMsg.className = 'chat-msg msg-user';
            uMsg.innerText = text;
            chatBody.appendChild(uMsg);
            chatInput.value = '';
            chatBody.scrollTop = chatBody.scrollHeight;

            try {
                const response = await fetch('http://localhost:8000/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });
                const data = await response.json();
                
                const aiMsg = document.createElement('div');
                aiMsg.className = 'chat-msg msg-ai';
                aiMsg.innerText = data.reply || 'Connection error. Is backend running?';
                chatBody.appendChild(aiMsg);
            } catch (err) {
                const aiMsg = document.createElement('div');
                aiMsg.className = 'chat-msg msg-ai';
                aiMsg.innerText = 'System Offline. Ensure backend is running.';
                chatBody.appendChild(aiMsg);
            }
            chatBody.scrollTop = chatBody.scrollHeight;
        }

        chatSend.addEventListener('click', sendChatMessage);
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendChatMessage();
        });
    }
});

window.logout = function() {
    localStorage.removeItem('nexus_auth');
    window.location.reload();
}

// WebSocket Command Center Logic
const analyzeForm = document.getElementById('analyzeForm');
if(analyzeForm) {
    let globalProfiles = [];

    analyzeForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const postUrl = document.getElementById('postUrl').value;
        const cookie = document.getElementById('cookie').value;
        const userEmail = document.getElementById('userEmail').value;
        
        const submitBtn = document.getElementById('submitBtn');
        const loader = document.getElementById('loader');
        const statusTextEl = document.getElementById('statusText');
        const feedGrid = document.getElementById('feedGrid');
        const downloadBtn = document.getElementById('downloadBtn');
        
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<div class="loader"></div>';
        statusTextEl.classList.remove('hidden');
        downloadBtn.classList.add('hidden');
        
        feedGrid.innerHTML = '';
        globalProfiles = [];
        
        // Hardcoded to local backend so it works even if frontend is a static file://
        const wsUrl = `ws://localhost:8000/ws/analyze`;
        const ws = new WebSocket(wsUrl);
        
        ws.onopen = () => {
            ws.send(JSON.stringify({ post_url: postUrl, li_at_cookie: cookie, target_email: userEmail }));
        };
        
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            
            if (data.type === 'status') {
                statusTextEl.innerText = data.message;
            } else if (data.type === 'error') {
                statusTextEl.innerText = "Error: " + data.message;
                statusTextEl.style.color = "#ef4444";
                cleanup();
            } else if (data.type === 'profile') {
                const profile = data.data;
                globalProfiles.push(profile);
                const score = profile.score || 0;
                const isHigh = score > 80;
                
                const card = document.createElement('div');
                card.className = `lead-card ${isHigh ? 'high-score' : ''}`;
                card.innerHTML = `
                    <div class="lead-header">
                        <div class="lead-name"><a href="${profile.url}" target="_blank">${profile.name}</a></div>
                        <div class="lead-score">${score}</div>
                    </div>
                    <div class="lead-category">${profile.category || 'Unknown'}</div>
                    <div class="lead-headline">${profile.headline}</div>
                    <div class="lead-outreach">"${profile.outreach || 'No outreach generated.'}"</div>
                `;
                feedGrid.prepend(card);
            } else if (data.type === 'complete') {
                statusTextEl.innerText = data.message;
                statusTextEl.style.color = "#10b981";
                downloadBtn.classList.remove('hidden');
                cleanup();
            }
        };
        
        ws.onerror = () => {
            statusTextEl.innerText = "Connection lost. Please ensure 'python -m uvicorn main:app' is running.";
            statusTextEl.style.color = "#ef4444";
            cleanup();
        };

        ws.onclose = () => {
            cleanup();
        };
        
        function cleanup() {
            submitBtn.disabled = false;
            submitBtn.innerText = 'Execute Scan';
        }
    });

    const dBtn = document.getElementById('downloadBtn');
    if(dBtn) {
        dBtn.addEventListener('click', () => {
            if(globalProfiles.length === 0) return;
            const headers = ["Name", "Headline", "URL", "Score", "Category", "Outreach"];
            let csvContent = "data:text/csv;charset=utf-8," + headers.join(",") + "\n";
            
            globalProfiles.forEach(p => {
                const row = [
                    `"${(p.name || '').replace(/"/g, '""')}"`,
                    `"${(p.headline || '').replace(/"/g, '""')}"`,
                    `"${(p.url || '').replace(/"/g, '""')}"`,
                    `"${p.score || 0}"`,
                    `"${(p.category || '').replace(/"/g, '""')}"`,
                    `"${(p.outreach || '').replace(/"/g, '""')}"`
                ];
                csvContent += row.join(",") + "\n";
            });
            
            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", "10x_automations_leads.csv");
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        });
    }
}
