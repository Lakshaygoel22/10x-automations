import os

chatbot_and_footer = """
    <!-- Scrollable Expansion Sections -->
    <div class="enterprise-footer">
        <div class="footer-grid">
            <div class="footer-col">
                <h4>Platform</h4>
                <a href="#">Fulfillment</a>
                <a href="#">Inventory</a>
                <a href="#">Integrations</a>
                <a href="#">Analytics</a>
            </div>
            <div class="footer-col">
                <h4>Solutions</h4>
                <a href="#">DTC Brands</a>
                <a href="#">B2B Wholesale</a>
                <a href="#">Global Expansion</a>
                <a href="#">Custom Packaging</a>
            </div>
            <div class="footer-col">
                <h4>Company</h4>
                <a href="#">About Us</a>
                <a href="#">Careers</a>
                <a href="#">Partners</a>
                <a href="#">Contact</a>
            </div>
            <div class="footer-col">
                <h4>Resources</h4>
                <a href="#">Help Center</a>
                <a href="#">API Documentation</a>
                <a href="#">Blog</a>
                <a href="#">Case Studies</a>
            </div>
        </div>
        <div class="footer-bottom">
            <span>&copy; 2026 10x Automations (Ecomflow Theme). All rights reserved.</span>
            <span>Privacy Policy | Terms of Service</span>
        </div>
    </div>

    <!-- Background 3D Cubes -->
    <div class="bg-cube-wrapper cube-1">
        <div class="supply-box">
            <div class="box-face box-front"></div>
            <div class="box-face box-back"></div>
            <div class="box-face box-right"></div>
            <div class="box-face box-left"></div>
            <div class="box-face box-top"></div>
            <div class="box-face box-bottom"></div>
        </div>
    </div>
    <div class="bg-cube-wrapper cube-2">
        <div class="supply-box">
            <div class="box-face box-front"></div>
            <div class="box-face box-back"></div>
            <div class="box-face box-right"></div>
            <div class="box-face box-left"></div>
            <div class="box-face box-top"></div>
            <div class="box-face box-bottom"></div>
        </div>
    </div>
    <div class="bg-cube-wrapper cube-3">
        <div class="supply-box">
            <div class="box-face box-front"></div>
            <div class="box-face box-back"></div>
            <div class="box-face box-right"></div>
            <div class="box-face box-left"></div>
            <div class="box-face box-top"></div>
            <div class="box-face box-bottom"></div>
        </div>
    </div>
    <div class="bg-cube-wrapper cube-4">
        <div class="supply-box">
            <div class="box-face box-front"></div>
            <div class="box-face box-back"></div>
            <div class="box-face box-right"></div>
            <div class="box-face box-left"></div>
            <div class="box-face box-top"></div>
            <div class="box-face box-bottom"></div>
        </div>
    </div>

    <!-- Chat Widget -->
    <div class="chat-toggle-btn" id="chatToggleBtn">
        <svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/></svg>
    </div>
    <div class="chat-widget" id="chatWidget">
        <div class="chat-header">
            <span>Sales Representative</span>
            <span class="chat-close" id="chatClose">✖</span>
        </div>
        <div class="chat-body" id="chatBody">
            <div class="chat-msg msg-ai">Welcome to 10x Automations. How can we streamline your supply chain and LinkedIn growth today?</div>
        </div>
        <div class="chat-input-area">
            <input type="text" id="chatInput" placeholder="Type a message..." style="flex:1;">
            <button id="chatSend" class="action-btn" style="padding: 10px 15px; min-width:auto;">Send</button>
        </div>
    </div>
    <script src="script.js"></script>
</body>
"""

files = [f for f in os.listdir('static') if f.endswith('.html')]
for f in files:
    with open(f"static/{f}", 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Try to replace the old chatbot/script injection with the massive new injection
    if '<!-- Scrollable Expansion Sections -->' in content:
        continue # Already injected
        
    if '<!-- Chat Widget -->' in content:
        # Split at the old chat widget and replace everything below it
        parts = content.split('<!-- Chat Widget -->')
        content = parts[0] + chatbot_and_footer
    elif '    <script src="script.js"></script>\n</body>' in content:
        content = content.replace('    <script src="script.js"></script>\n</body>', chatbot_and_footer)
    elif '<script src="script.js"></script>\n</body>' in content:
        content = content.replace('<script src="script.js"></script>\n</body>', chatbot_and_footer)
    elif '</body>' in content:
        content = content.replace('</body>', chatbot_and_footer)
        
    with open(f"static/{f}", 'w', encoding='utf-8') as file:
        file.write(content)
