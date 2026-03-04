import feedparser, google.generativeai as genai, os, base64

def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as img:
            return f"data:image/png;base64,{base64.get_image_base64(img.read()).decode('utf-8')}"
    except: return ""

user_image_base64 = get_image_base64("image_3.png")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

feeds = {
    "WORLD NEWS": "https://news.google.com/rss/search?q=world+news&hl=en-US&gl=US&ceid=US:en",
    "SPORTS NEWS": "https://news.google.com/rss/search?q=sports+news&hl=en-US&gl=US&ceid=US:en",
    "TECH TRENDING": "https://news.google.com/rss/search?q=trending+tech&hl=en-US&gl=US&ceid=US:en"
}

def create_super_portal():
    print("🚀 ZONE 94: Running Master Upgrade v6.0...")
    sections_html = ""
    for cat_name, url in feeds.items():
        feed = feedparser.parse(url)
        grid_id = cat_name.split(' ')[0].lower() + "-grid"
        sections_html += f'''
        <div id="{grid_id}" class="category-section animate-up">
            <h2 class="section-header">{cat_name}</h2>
            <div class="news-grid">'''
        for entry in feed.entries[:8]:
            sections_html += f"""
            <div class="bbc-card" onclick="window.open('{entry.link}', '_blank')">
                <span class="category-tag">{cat_name.split(' ')[0]}</span>
                <h3>{entry.title}</h3>
                <p>Global Intelligence Report.</p>
            </div>"""
        sections_html += '</div></div>'

    full_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZONE 94 | Global Intelligence</title>
    <script src="https://www.gstatic.com/firebasejs/9.6.10/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.6.10/firebase-database-compat.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Poppins:wght@300;400;700;900&display=swap');
        :root {{ --bbc-red: #bb1919; --bg: #000; --card: #111; --text: #fff; }}
        body {{ background: var(--bg); color: var(--text); font-family: 'Poppins', sans-serif; margin: 0; overflow-x: hidden; }}
        .hidden {{ display: none !important; }}
        
        /* ANIMATIONS */
        @keyframes fadeInUp {{ from {{ opacity: 0; transform: translateY(30px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        @keyframes slideIn {{ from {{ transform: translateX(-100%); }} to {{ transform: translateX(0); }} }}
        .animate-up {{ animation: fadeInUp 0.5s ease forwards; }}
        
        /* HEADER & UI */
        .ticker-wrap {{ background: #111; display: flex; justify-content: space-between; padding: 12px 20px; border-bottom: 1px solid #222; }}
        .site-header {{ display: flex; justify-content: space-between; align-items: center; padding: 30px 50px; }}
        .main-logo-bbc span {{ background: white; color: black; padding: 5px 15px; font-size: 2.2rem; font-family: 'Bebas Neue'; }}
        .main-logo-bbc .num {{ background: var(--bbc-red); color: white; }}
        .avatar-circle {{ width: 50px; height: 50px; background: #fff; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 900; border: 4px solid var(--bbc-red); cursor: pointer; color: #000; }}
        
        .main-nav {{ background: #0a0a0a; display: flex; justify-content: center; border-bottom: 1px solid #222; position: sticky; top: 0; z-index: 1000; }}
        .nav-btn {{ background: none; border: none; color: #888; padding: 18px 25px; cursor: pointer; font-weight: bold; text-transform: uppercase; transition: 0.3s; }}
        .nav-btn:hover, .nav-btn.active {{ color: #fff; border-bottom: 4px solid var(--bbc-red); background: #111; }}
        
        /* CARDS */
        .content {{ padding: 50px 30px; max-width: 1400px; margin: auto; }}
        .section-header {{ font-family: 'Bebas Neue'; font-size: 2.5rem; border-left: 8px solid var(--bbc-red); padding-left: 20px; margin-bottom: 35px; }}
        .news-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 30px; }}
        .bbc-card {{ background: var(--card); padding: 30px; border-radius: 15px; border: 1px solid #222; cursor: pointer; transition: 0.4s; }}
        .bbc-card:hover {{ transform: scale(1.03); border-color: var(--bbc-red); }}

        /* AUTH */
        .login-overlay {{ position: fixed; inset: 0; background: #000; display: flex; justify-content: center; align-items: center; z-index: 3000; }}
        .login-card {{ background: #0a0a0a; padding: 40px; border: 1px solid #222; border-radius: 20px; text-align: center; width: 380px; }}
        input, select {{ width: 100%; padding: 14px; margin: 15px 0; background: #151515; border: 1px solid #333; color: #fff; border-radius: 8px; box-sizing: border-box; }}
        .main-btn {{ width: 100%; background: var(--bbc-red); color: #fff; border: none; padding: 16px; cursor: pointer; font-weight: 900; font-family: 'Bebas Neue'; font-size: 1.5rem; border-radius: 8px; }}

        /* CHANNELS */
        .ch-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 15px; margin-bottom: 30px; }}
        .ch-card {{ background: #111; border: 1px solid #333; color: #fff; padding: 20px; border-radius: 10px; cursor: pointer; text-align: center; font-weight: bold; transition: 0.3s; }}
        .ch-card:hover {{ background: var(--bbc-red); transform: translateY(-5px); }}

        /* MODALS */
        .modal-bg {{ position: fixed; inset: 0; background: rgba(0,0,0,0.95); display: flex; justify-content: center; align-items: center; z-index: 4000; }}
        .modal-content {{ background: #0a0a0a; padding: 50px; text-align: center; border-radius: 25px; border: 1px solid #333; max-width: 500px; }}
        .modal-photo {{ width: 150px; height: 150px; border-radius: 50%; border: 4px solid var(--bbc-red); margin-bottom: 20px; }}
        .social-btn {{ padding: 10px 20px; border-radius: 5px; text-decoration: none; color: #fff; font-weight: bold; margin: 5px; display: inline-block; }}
        
        #user-tooltip {{ position: absolute; top: 90px; right: 50px; background: #0a0a0a; border: 1px solid #333; border-radius: 15px; padding: 25px; width: 280px; z-index: 2000; }}
    </style>
</head>
<body>

    <div id="login-overlay" class="login-overlay">
        <div class="login-card">
            <div class="main-logo-bbc"><span>Z</span><span>O</span><span>N</span><span>E</span><span class="num">94</span></div>
            <div style="display:flex; margin:20px 0;">
                <button onclick="toggleAuth('login')" id="tab-l" style="flex:1; background:none; color:#fff; border:none; cursor:pointer; font-weight:bold;">LOGIN</button>
                <button onclick="toggleAuth('signup')" id="tab-s" style="flex:1; background:none; color:#555; border:none; cursor:pointer; font-weight:bold;">SIGNUP</button>
            </div>
            <input type="text" id="reg-name" placeholder="Full Name" class="hidden">
            <input type="email" id="auth-email" placeholder="Email Address">
            <input type="password" id="auth-pass" placeholder="Password">
            <select id="auth-country"></select>
            <button class="main-btn" onclick="handleAuth()">ENTER THE ZONE</button>
        </div>
    </div>

    <div id="main-site" class="hidden">
        <div class="ticker-wrap">
            <div class="ticker">🚀 WORLD'S NUMBER 1 AI PORTAL — ZONE 94 — ALL SYSTEMS ACTIVE — </div>
            <button onclick="triggerAIUpdate()" style="background:var(--bbc-red); color:#fff; border:none; padding:5px 15px; border-radius:20px; font-size:10px; cursor:pointer; font-weight:bold;">AI UPDATE ⚡</button>
            <div id="live-clock" style="color:#666; font-weight:bold">00:00:00</div>
        </div>

        <header class="site-header">
            <div style="width:100px"></div>
            <div class="main-logo-bbc" onclick="window.location.reload()"><span>Z</span><span>O</span><span>N</span><span>E</span><span class="num">94</span></div>
            <div id="user-avatar" class="avatar-circle" onclick="toggleTooltip()">U</div>
        </header>

        <nav class="main-nav">
            <button class="nav-btn active" onclick="switchTab('news', this)">Global News</button>
            <button class="nav-btn" onclick="switchTab('channels', this)">Live Channels</button>
            <button class="nav-btn hidden" id="nav-admin" onclick="switchTab('admin', this)" style="color:var(--bbc-red)">ADMIN PANEL</button>
            <button class="nav-btn" onclick="showAbout()">About Founder</button>
        </nav>

        <main class="content">
            <div id="news-container">{sections_html}</div>

            <div id="channels-container" class="hidden">
                <h2 class="section-header">Live Global Broadcasts</h2>
                <div id="channel-list"></div>
            </div>

            <div id="admin-container" class="hidden">
                <h2 class="section-header">Admin Control Panel</h2>
                <div style="background:#111; padding:30px; border-radius:15px; border:1px solid var(--bbc-red);">
                    <h3>Manual Content Management</h3>
                    <input type="text" id="admin-news-title" placeholder="Headline">
                    <textarea style="width:100%; height:100px; background:#1a1a1a; border:1px solid #333; color:#fff; padding:10px; border-radius:8px;" placeholder="AI Summary Content..."></textarea>
                    <button class="main-btn" style="margin-top:10px; width:auto; padding:10px 40px;">Publish Manually</button>
                    
                    <h3 style="margin-top:40px;">Real-time User Monitoring</h3>
                    <table style="width:100%; color:#aaa; font-size:13px; text-align:left;">
                        <thead><tr style="color:var(--bbc-red);"><th>User Email</th><th>Country</th><th>Login Time</th></tr></thead>
                        <tbody id="log-tbody"></tbody>
                    </table>
                </div>
            </div>
        </main>
        
        <footer style="text-align:center; padding:40px; border-top:1px solid #222; font-size:12px; color:#444;">
            ZONE 94 | ALL RIGHTS RESERVED © 2026 | GLOBAL INTELLIGENCE ENGINE
        </footer>
    </div>

    <div id="user-tooltip" class="hidden">
        <h4 style="margin:0; color:var(--bbc-red); font-family:'Bebas Neue';">USER PROFILE</h4>
        <p id="tp-name" style="margin:10px 0; font-size:13px;">Name</p>
        <p id="tp-email" style="margin:5px 0; font-size:12px; color:#555;">Email</p>
        <button class="main-btn" style="font-size:12px; padding:8px; margin-top:10px;" onclick="toggleTooltip()">OK</button>
        <button class="main-btn" style="font-size:12px; padding:8px; margin-top:5px; background:#333;" onclick="window.location.reload()">LOGOUT</button>
    </div>

    <div id="about-modal" class="modal-bg hidden" onclick="this.classList.add('hidden')">
        <div class="modal-content" onclick="event.stopPropagation()">
            <img src="{user_image_base64}" class="modal-photo">
            <h2>P.D.T SATHSARA</h2>
            <p>Founder & Developer | ZONE 94</p>
            <div style="margin:20px 0;">
                <a href="https://wa.me/94765738122" target="_blank" class="social-btn" style="background:#25D366;">WhatsApp</a>
                <a href="https://www.linkedin.com/in/thanuka-sathsara-freelancer" target="_blank" class="social-btn" style="background:#0077b5;">LinkedIn</a>
            </div>
            <button class="main-btn" style="width:auto; padding:10px 40px;" onclick="document.getElementById('about-modal').classList.add('hidden')">OK</button>
        </div>
    </div>

    <script>
        // CONFIG
        const firebaseConfig = {{
            apiKey: "AIzaSyDsrbp-BPJRqJi8UPRx99KRNIALsQvKpxg",
            authDomain: "zone94-2553a.firebaseapp.com",
            databaseURL: "https://zone94-2553a-default-rtdb.asia-southeast1.firebasedatabase.app",
            projectId: "zone94-2553a",
            storageBucket: "zone94-2553a.firebasestorage.app",
            appId: "1:722640877424:web:5e145b4c767af86e60c1b5"
        }};
        firebase.initializeApp(firebaseConfig);
        const db = firebase.database();

        let mode = 'login'; let selectedCountry = "Sri Lanka";
        const countries = {{
            "Sri Lanka": ["Hiru News", "Sirasa TV", "TV Derana", "ITN", "Swarnavahini"],
            "USA": ["ABC News", "NBC News", "CBS News", "Fox News", "CNN"],
            "UK": ["BBC World", "Sky News", "GB News", "Channel 4", "Reuters"],
            "India": ["NDTV", "Aaj Tak", "India Today", "Republic World", "Zee News"]
        }};

        const countrySelect = document.getElementById('auth-country');
        Object.keys(countries).forEach(c => {{ let opt = document.createElement('option'); opt.value = c; opt.innerText = c; countrySelect.appendChild(opt); }});

        function toggleAuth(m) {{
            mode = m; document.getElementById('tab-l').style.color = (m==='login'?'#fff':'#555'); document.getElementById('tab-s').style.color = (m==='signup'?'#fff':'#555');
            document.getElementById('reg-name').classList.toggle('hidden', m==='login');
        }}

        function handleAuth() {{
            const email = document.getElementById('auth-email').value;
            const pass = document.getElementById('auth-pass').value;
            selectedCountry = countrySelect.value;
            if(email === "contact.sthanu2009@gmail.com" && pass === "200928001301") {{ loginSuccess({{name: "Admin", email, isAdmin: true}}); }}
            else if(mode === 'signup') {{
                const name = document.getElementById('reg-name').value;
                db.ref('users/' + btoa(email)).set({{name, email, pass, country: selectedCountry}}, () => {{ alert("Signup Success!"); toggleAuth('login'); }});
            }} else {{
                db.ref('users/' + btoa(email)).once('value', s => {{
                    const u = s.val(); if(u && u.pass === pass) loginSuccess(u); else alert("Login Failed! Try Signup.");
                }});
            }}
        }}

        function loginSuccess(user) {{
            document.getElementById('login-overlay').classList.add('hidden');
            document.getElementById('main-site').classList.remove('hidden');
            document.getElementById('user-avatar').innerText = user.name.charAt(0).toUpperCase();
            document.getElementById('tp-name').innerText = user.name;
            document.getElementById('tp-email').innerText = user.email;
            if(user.isAdmin) document.getElementById('nav-admin').classList.remove('hidden');
            db.ref('logs').push({{email: user.email, country: selectedCountry, time: new Date().toLocaleString()}});
            loadChannels();
        }}

        function loadChannels() {{
            const list = document.getElementById('channel-list'); list.innerHTML = "";
            const chs = countries[selectedCountry] || countries["USA"];
            list.innerHTML += `<div class="ch-grid">` + chs.map(c => `<div class="ch-card">${{c}} LIVE</div>`).join('') + `</div>`;
        }}

        function switchTab(type, btn) {{
            document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active')); btn.classList.add('active');
            document.getElementById('news-container').classList.toggle('hidden', type !== 'news');
            document.getElementById('channels-container').classList.toggle('hidden', type !== 'channels');
            document.getElementById('admin-container').classList.toggle('hidden', type !== 'admin');
            if(type === 'admin') {{
                db.ref('logs').on('value', s => {{
                    const tbody = document.getElementById('log-tbody'); tbody.innerHTML = "";
                    s.forEach(child => {{ const l = child.val(); tbody.innerHTML = `<tr><td style='padding:10px;'>${{l.email}}</td><td>${{l.country}}</td><td>${{l.time}}</td></tr>` + tbody.innerHTML; }});
                }});
            }}
        }}

        function triggerAIUpdate() {{ alert("🚀 AI Update Triggered! Generating fresh global intelligence..."); window.location.reload(); }}
        function toggleTooltip() {{ document.getElementById('user-tooltip').classList.toggle('hidden'); }}
        function showAbout() {{ document.getElementById('about-modal').classList.remove('hidden'); }}
        setInterval(() => {{ document.getElementById('live-clock').innerText = new Date().toLocaleTimeString(); }}, 1000);
    </script>
</body>
</html>
    """
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    print("\n✅ Success! ZONE 94 PRO v6.0 Is Live with Cloud Sync.")

if __name__ == "__main__": create_super_portal()
