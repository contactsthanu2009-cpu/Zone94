import feedparser, google.generativeai as genai, os, base64

def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as img:
            return f"data:image/png;base64,{base64.b64encode(img.read()).decode('utf-8')}"
    except: return ""

user_image_base64 = get_image_base64("image_3.png")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

feeds = {
    "WORLD NEWS": "https://news.google.com/rss/search?q=world+news&hl=en-US&gl=US&ceid=US:en",
    "SPORTS NEWS": "https://news.google.com/rss/search?q=sports+news&hl=en-US&gl=US&ceid=US:en",
    "TECH NEWS": "https://news.google.com/rss/search?q=technology+news&hl=en-US&gl=US&ceid=US:en"
}

def create_files():
    print("🚀 ZONE 94: Generating index.html & auth.js...")
    
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
                <h3 class="news-title">{entry.title}</h3>
                <p>Global Intelligence Report.</p>
            </div>"""
        sections_html += '</div></div>'

    index_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZONE 94 | Global Portal</title>
    <script src="https://www.gstatic.com/firebasejs/9.6.10/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.6.10/firebase-database-compat.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@emailjs/browser@3/dist/email.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Poppins:wght@300;400;700;900&display=swap');
        :root {{ --bbc-red: #bb1919; --bg: #000; --text: #fff; }}
        body {{ background: var(--bg); color: var(--text); font-family: 'Poppins', sans-serif; margin: 0; overflow-x: hidden; }}
        .hidden {{ display: none !important; }}
        .animate-up {{ animation: fadeInUp 0.5s ease forwards; }}
        @keyframes fadeInUp {{ from {{ opacity: 0; transform: translateY(30px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        .login-overlay {{ position: fixed; inset: 0; background: #000; display: flex; justify-content: center; align-items: center; z-index: 3000; }}
        .login-card {{ background: #0a0a0a; padding: 40px; border: 1px solid #222; border-radius: 20px; text-align: center; width: 380px; }}
        input {{ width: 100%; padding: 14px; margin: 10px 0; background: #151515; border: 1px solid #333; color: #fff; border-radius: 8px; box-sizing: border-box; }}
        .main-btn {{ width: 100%; background: var(--bbc-red); color: #fff; border: none; padding: 16px; cursor: pointer; font-weight: 900; font-family: 'Bebas Neue'; font-size: 1.5rem; border-radius: 8px; }}
        .main-logo-bbc span {{ background: white; color: black; padding: 5px 15px; font-size: 2.2rem; font-family: 'Bebas Neue'; }}
        .main-logo-bbc .num {{ background: var(--bbc-red); color: white; }}
        .avatar-circle {{ width: 50px; height: 50px; background: #fff; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 900; border: 4px solid var(--bbc-red); cursor: pointer; color: #000; }}
        .main-nav {{ background: #0a0a0a; display: flex; justify-content: center; border-bottom: 1px solid #222; position: sticky; top: 0; z-index: 1000; }}
        .nav-btn {{ background: none; border: none; color: #888; padding: 18px 25px; cursor: pointer; font-weight: bold; text-transform: uppercase; transition: 0.3s; }}
        .nav-btn:hover, .nav-btn.active {{ color: #fff; border-bottom: 4px solid var(--bbc-red); background: #111; }}
        .news-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 30px; padding: 30px; }}
        .bbc-card {{ background: #111; padding: 25px; border-radius: 12px; border: 1px solid #222; cursor: pointer; }}
        .section-header {{ font-family: 'Bebas Neue'; font-size: 2.5rem; border-left: 8px solid var(--bbc-red); padding-left: 20px; margin-bottom: 35px; text-transform: uppercase; margin-left: 30px; }}
        .modal-bg {{ position: fixed; inset: 0; background: rgba(0,0,0,0.95); display: flex; justify-content: center; align-items: center; z-index: 4000; }}
        .modal-photo {{ width: 150px; height: 150px; border-radius: 50%; border: 4px solid var(--bbc-red); margin-bottom: 20px; box-shadow: 0 0 20px var(--bbc-red); }}
    </style>
</head>
<body onload="checkSavedLogin()">

    <div id="login-overlay" class="login-overlay">
        <div class="login-card">
            <div id="auth-form">
                <div class="main-logo-bbc"><span>Z</span><span>O</span><span>N</span><span>E</span><span class="num">94</span></div>
                <div style="display:flex; margin:20px 0; border-bottom:1px solid #222;">
                    <button onclick="toggleMode('login')" id="btn-l" style="flex:1; background:none; color:#fff; border:none; padding:10px; cursor:pointer;">LOGIN</button>
                    <button onclick="toggleMode('signup')" id="btn-s" style="flex:1; background:none; color:#555; border:none; padding:10px; cursor:pointer;">SIGNUP</button>
                </div>
                <input type="text" id="u-name" placeholder="Full Name" class="hidden">
                <input type="email" id="u-email" placeholder="Email Address">
                <input type="password" id="u-pass" placeholder="Password">
                <button class="main-btn" onclick="handleAuth()">ENTER ZONE</button>
            </div>
            <div id="verify-form" class="hidden">
                <h3 style="color:var(--bbc-red); font-family:'Bebas Neue';">VERIFY EMAIL</h3>
                <p style="font-size:12px; color:#666;">Check your email for the 6-digit code.</p>
                <input type="text" id="v-code" placeholder="Enter Code">
                <button class="main-btn" onclick="confirmVerify()">VERIFY ACCOUNT</button>
            </div>
        </div>
    </div>

    <div id="main-site" class="hidden">
        <header style="display:flex; justify-content:space-between; padding:20px 40px; align-items:center;">
            <div style="width:100px"></div>
            <div class="main-logo-bbc" onclick="window.location.reload()"><span>Z</span><span>O</span><span>N</span><span>E</span><span class="num">94</span></div>
            <div id="user-avatar" class="avatar-circle" onclick="logout()">U</div>
        </header>
        <nav class="main-nav">
            <button class="nav-btn active" onclick="switchNav('news', this, 'world')">World News</button>
            <button class="nav-btn" onclick="switchNav('news', this, 'sports')">Sports News</button>
            <button class="nav-btn" onclick="switchNav('news', this, 'tech')">Tech News</button>
            <button class="nav-btn" onclick="switchNav('channels', this)">Live Channels</button>
            <button class="nav-btn hidden" id="nav-admin" onclick="switchNav('admin', this)" style="color:var(--bbc-red)">ADMIN</button>
            <button class="nav-btn" onclick="showAbout()">About Us</button>
        </nav>
        <main class="content">
            <div id="news-container">{sections_html}</div>
            <div id="channels-container" class="hidden animate-up">
                <h2 class="section-header">Live Broadcasts</h2>
                <div id="all-channels-list" style="display:grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap:15px; padding:30px;"></div>
            </div>
            <div id="admin-container" class="hidden animate-up">
                <div style="background:#111; padding:30px; border-radius:15px; border:1px solid var(--bbc-red);">
                    <h2 class="section-header">Admin Control Panel</h2>
                    <h3 style="color:#fff;">Welcome Admin P.D.T Sathsara</h3>
                </div>
            </div>
        </main>
    </div>

    <div id="about-modal" class="modal-bg hidden" onclick="this.classList.add('hidden')">
        <div style="background:#0a0a0a; padding:40px; text-align:center; border-radius:25px; border:1px solid #333; max-width:450px;" onclick="event.stopPropagation()">
            <img src="{user_image_base64}" class="modal-photo">
            <h2>P.D.T SATHSARA</h2>
            <p>Founder & Developer | Age: 17</p>
            <button class="main-btn" style="width:auto; padding:10px 40px;" onclick="document.getElementById('about-modal').classList.add('hidden')">CLOSE</button>
        </div>
    </div>
    <script src="auth.js"></script>
</body>
</html>
    """

    auth_js = f"""
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
    emailjs.init("ZgGkvBZgIOPcydTiO");

    let authMode = 'login'; let generatedCode = ""; let tempUser = {{}};
    const allChannels = {{
        "SRI LANKA": ["Hiru News", "Sirasa TV", "TV Derana", "ITN", "Swarnavahini"],
        "USA": ["ABC News", "NBC News", "CBS News", "Fox News", "CNN"],
        "UK": ["BBC News", "Sky News", "GB News", "Channel 4", "Reuters"]
    }};

    function toggleMode(m) {{
        authMode = m; document.getElementById('u-name').classList.toggle('hidden', m==='login');
        document.getElementById('btn-l').style.color = (m==='login'?'#fff':'#555');
        document.getElementById('btn-s').style.color = (m==='signup'?'#fff':'#555');
    }}

    function checkSavedLogin() {{
        const saved = localStorage.getItem('zone94_session');
        if(saved) loginSuccess(JSON.parse(saved));
    }}

    function handleAuth() {{
        const email = document.getElementById('u-email').value;
        const pass = document.getElementById('u-pass').value;
        
        // ADMIN LOGIN (BYPASS VERIFICATION)
        if(email === "contact.sthanu2009@gmail.com" && pass === "200928001301") {{
            const admin = {{name: "Admin", email, isAdmin: true}};
            localStorage.setItem('zone94_session', JSON.stringify(admin));
            loginSuccess(admin);
            return;
        }}

        if(authMode === 'signup') {{
            const name = document.getElementById('u-name').value;
            generatedCode = Math.floor(100000 + Math.random() * 900000).toString();
            tempUser = {{name, email, pass}};
            emailjs.send("service_6j9200q", "template_352c0rr", {{ 
                to_email: email, 
                code: generatedCode 
            }}).then(() => {{
                document.getElementById('auth-form').classList.add('hidden');
                document.getElementById('verify-form').classList.remove('hidden');
            }}, (err) => alert("EmailJS Error: " + err.text));
        }} else {{
            db.ref('users/' + btoa(email)).once('value', s => {{
                const u = s.val(); if(u && u.pass === pass) {{
                    localStorage.setItem('zone94_session', JSON.stringify(u));
                    loginSuccess(u);
                }} else alert("Invalid Login!");
            }});
        }}
    }}

    function confirmVerify() {{
        if(document.getElementById('v-code').value === generatedCode) {{
            db.ref('users/' + btoa(tempUser.email)).set(tempUser, () => {{
                localStorage.setItem('zone94_session', JSON.stringify(tempUser));
                loginSuccess(tempUser);
            }});
        }} else alert("Wrong Verification Code!");
    }}

    function loginSuccess(user) {{
        document.getElementById('login-overlay').classList.add('hidden');
        document.getElementById('main-site').classList.remove('hidden');
        document.getElementById('user-avatar').innerText = user.name.charAt(0).toUpperCase();
        if(user.isAdmin) document.getElementById('nav-admin').classList.remove('hidden');
        loadAllChannels();
    }}

    function loadAllChannels() {{
        const container = document.getElementById('all-channels-list'); container.innerHTML = "";
        Object.keys(allChannels).forEach(country => {{
            let group = `<div><h3 style="color:var(--bbc-red);">${{country}}</h3><div style="display:flex; flex-wrap:wrap; gap:10px;">`;
            allChannels[country].forEach(ch => group += `<div style="background:#222; padding:15px; border-radius:10px; cursor:pointer;" onclick="alert('Live Stream Loading...')">${{ch}}</div>`);
            container.innerHTML += group + "</div></div>";
        }});
    }}

    function switchNav(type, btn, cat) {{
        document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active')); btn.classList.add('active');
        document.getElementById('news-container').classList.toggle('hidden', type !== 'news');
        document.getElementById('channels-container').classList.toggle('hidden', type !== 'channels');
        document.getElementById('admin-container').classList.toggle('hidden', type !== 'admin');
        if(cat) {{ document.querySelectorAll('.category-section').forEach(s => s.classList.toggle('hidden', s.id !== cat + '-grid')); }}
    }}

    function logout() {{ localStorage.removeItem('zone94_session'); window.location.reload(); }}
    function showAbout() {{ document.getElementById('about-modal').classList.remove('hidden'); }}
    setInterval(() => {{ document.getElementById('live-clock').innerText = new Date().toLocaleTimeString(); }}, 1000);
    """

    with open("index.html", "w", encoding="utf-8") as f: f.write(index_html)
    with open("auth.js", "w", encoding="utf-8") as f: f.write(auth_js)
    print("✅ ZONE 94 PRO v13.0 Files Created!")

if __name__ == "__main__":
    create_files()
