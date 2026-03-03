import feedparser, google.generativeai as genai, os, base64

# ==========================================
# 0. IMAGE ENCODING (Founder Photo)
# ==========================================
def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return f"data:image/png;base64,{base64.b64encode(image_file.read()).decode('utf-8')}"
    except: return ""

# මතක ඇතුව ඔයාගේ ෆොටෝ එකේ නම GitHub එකේදී "image_3.png" කියලා වෙනස් කරන්න
user_image_base64 = get_image_base64("image_3.png")

# ==========================================
# 1. SETUP & NEWS SOURCES
# ==========================================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

feeds = {
    "WORLD NEWS": "https://news.google.com/rss/search?q=world+news&hl=en-US&gl=US&ceid=US:en",
    "SPORTS NEWS": "https://news.google.com/rss/search?q=sports+news&hl=en-US&gl=US&ceid=US:en",
    "TECH TRENDING": "https://news.google.com/rss/search?q=trending+tech&hl=en-US&gl=US&ceid=US:en"
}

def create_final_portal():
    print("🚀 ZONE 94: Deploying World's #1 Cloud Integrated Portal...")
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
                <p>Click to read full coverage.</p>
            </div>"""
        sections_html += '</div></div>'

    full_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZONE 94 | World's #1 AI News Portal</title>
    <script src="https://www.gstatic.com/firebasejs/9.6.10/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.6.10/firebase-database-compat.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Poppins:wght@300;400;700;900&display=swap');
        :root {{ --bbc-red: #bb1919; --bg: #000; --card: #111; --text: #fff; }}
        body {{ background: var(--bg); color: var(--text); font-family: 'Poppins', sans-serif; margin: 0; overflow-x: hidden; }}
        .hidden {{ display: none !important; }}
        @keyframes fadeInUp {{ from {{ opacity: 0; transform: translateY(30px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        .animate-up {{ animation: fadeInUp 0.6s ease forwards; }}
        
        .ticker-wrap {{ background: #111; display: flex; justify-content: space-between; padding: 12px 20px; border-bottom: 1px solid #222; }}
        .site-header {{ display: flex; justify-content: space-between; align-items: center; padding: 30px 50px; }}
        .main-logo-bbc span {{ background: white; color: black; padding: 5px 15px; font-size: 2.2rem; font-family: 'Bebas Neue'; }}
        .main-logo-bbc .num {{ background: var(--bbc-red); color: white; }}
        .avatar-circle {{ width: 50px; height: 50px; background: #fff; color: #000; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 900; border: 4px solid var(--bbc-red); cursor: pointer; }}
        
        .main-nav {{ background: #0a0a0a; display: flex; justify-content: center; border-bottom: 1px solid #222; position: sticky; top: 0; z-index: 1000; }}
        .main-nav button {{ background: none; border: none; color: #888; padding: 18px 25px; cursor: pointer; font-weight: bold; text-transform: uppercase; }}
        .main-nav button:hover, .main-nav button.active {{ color: #fff; border-bottom: 4px solid var(--bbc-red); }}
        
        .content {{ padding: 50px 30px; max-width: 1400px; margin: auto; }}
        .section-header {{ font-family: 'Bebas Neue'; font-size: 2.5rem; border-left: 8px solid var(--bbc-red); padding-left: 20px; margin-bottom: 35px; }}
        .news-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 30px; }}
        .bbc-card {{ background: var(--card); padding: 30px; border-radius: 15px; border: 1px solid #222; cursor: pointer; transition: 0.3s; }}
        .bbc-card:hover {{ border-color: var(--bbc-red); transform: translateY(-5px); }}
        
        .login-overlay {{ position: fixed; inset: 0; background: #000; display: flex; justify-content: center; align-items: center; z-index: 3000; }}
        .login-card {{ background: #0a0a0a; padding: 40px; border: 1px solid #222; border-radius: 20px; text-align: center; width: 380px; }}
        input, select {{ width: 100%; padding: 14px; margin: 15px 0; background: #151515; border: 1px solid #333; color: #fff; border-radius: 8px; box-sizing: border-box; }}
        .main-btn {{ width: 100%; background: var(--bbc-red); color: #fff; border: none; padding: 16px; cursor: pointer; font-weight: 900; font-family: 'Bebas Neue'; font-size: 1.5rem; border-radius: 8px; }}

        #user-tooltip {{ position: absolute; top: 90px; right: 50px; background: #0a0a0a; border: 1px solid #333; border-radius: 15px; padding: 25px; width: 260px; z-index: 2000; box-shadow: 0 20px 50px rgba(0,0,0,0.9); }}
        .modal-bg {{ position: fixed; inset: 0; background: rgba(0,0,0,0.95); display: flex; justify-content: center; align-items: center; z-index: 4000; }}
        .modal-photo {{ width: 160px; height: 160px; border-radius: 50%; border: 4px solid var(--bbc-red); margin-bottom: 25px; object-fit: cover; }}
    </style>
</head>
<body>

    <div id="login-overlay" class="login-overlay">
        <div class="login-card">
            <div class="main-logo-bbc"><span>Z</span><span>O</span><span>N</span><span>E</span><span class="num">94</span></div>
            <div style="display:flex; margin:20px 0;"><button onclick="toggleAuth('login', this)" style="flex:1; background:none; color:#fff; border:none; cursor:pointer;" id="tab-login">LOGIN</button><button onclick="toggleAuth('signup', this)" style="flex:1; background:none; color:#555; border:none; cursor:pointer;" id="tab-signup">SIGNUP</button></div>
            <input type="text" id="reg-name" placeholder="Full Name" class="hidden">
            <input type="email" id="auth-email" placeholder="Email Address">
            <input type="password" id="auth-pass" placeholder="Password">
            <select id="auth-country"></select>
            <button class="main-btn" onclick="handleAuth()">ENTER THE ZONE</button>
        </div>
    </div>

    <div id="main-site" class="hidden">
        <div class="ticker-wrap"><div class="ticker">🚀 ZONE 94 — WORLD'S NUMBER 1 AI NEWS PORTAL — CLOUD DATABASE CONNECTED — </div><div id="live-clock" style="color:#666; font-weight:bold">00:00:00</div></div>
        <header class="site-header">
            <div style="width:100px"></div>
            <div class="main-logo-bbc" onclick="window.location.reload()"><span>Z</span><span>O</span><span>N</span><span>E</span><span class="num">94</span></div>
            <div id="user-avatar" class="avatar-circle" onclick="toggleTooltip()">U</div>
        </header>
        <nav class="main-nav">
            <button class="nav-btn active" onclick="showSection('news', this)">Global News</button>
            <button class="nav-btn hidden" id="nav-admin" onclick="showSection('admin', this)" style="color:var(--bbc-red)">ADMIN PANEL</button>
            <button class="nav-btn" onclick="showAbout()">About Founder</button>
        </nav>
        <main class="content">
            <div id="news-container" class="animate-up">{sections_html}</div>
            <div id="admin-container" class="hidden animate-up">
                <h2 class="section-header">Live User Logs</h2>
                <table style="width:100%; border-collapse:collapse; color:#aaa; font-size:13px;" id="admin-table">
                    <thead><tr style="color:var(--bbc-red); text-align:left; border-bottom:1px solid #222;"><th style="padding:10px;">Email</th><th>Country</th><th>Login Time</th></tr></thead>
                    <tbody id="log-tbody"></tbody>
                </table>
            </div>
        </main>
        <footer style="text-align:center; padding:40px; color:#444; font-size:11px; border-top:1px solid #222;">ZONE 94 | ALL RIGHTS RESERVED © 2026 | POWERED BY AI</footer>
    </div>

    <div id="about-modal" class="modal-bg hidden" onclick="this.classList.add('hidden')">
        <div class="modal-content" style="background:#0a0a0a; padding:50px; text-align:center; border-radius:25px; border:1px solid #333;" onclick="event.stopPropagation()">
            <img src="{user_image_base64}" class="modal-photo">
            <h3>P.D.T SATHSARA</h3>
            <p style="color:#666;">Founder & Lead Developer</p>
            <div style="margin-top:20px; text-align:left; font-size:14px;">
                <p>Email: contact.sthanu2009@gmail.com</p>
                <p>Age: 17 | Sri Lanka</p>
            </div>
            <button class="main-btn" style="width:auto; padding:10px 40px; margin-top:20px; font-size:1rem;" onclick="document.getElementById('about-modal').classList.add('hidden')">CLOSE</button>
        </div>
    </div>

    <div id="user-tooltip" class="hidden">
        <h4 style="margin:0; color:var(--bbc-red); font-family:'Bebas Neue';">USER PROFILE</h4>
        <p id="tp-name" style="margin:10px 0; font-size:13px;">Name</p>
        <p id="tp-email" style="margin:5px 0; font-size:12px; color:#555;">Email</p>
        <button class="main-btn" style="font-size:12px; padding:5px; margin-top:15px;" onclick="window.location.reload()">LOGOUT</button>
    </div>

    <script>
        // OYAGE FIREBASE CONFIG EKAI OYAGE SPECIFIC DATABASE URL EKAI
        const firebaseConfig = {{
            apiKey: "AIzaSyDsrbp-BPJRqJi8UPRx99KRNIALsQvKpxg",
            authDomain: "zone94-2553a.firebaseapp.com",
            databaseURL: "https://zone94-2553a-default-rtdb.asia-southeast1.firebasedatabase.app",
            projectId: "zone94-2553a",
            storageBucket: "zone94-2553a.firebasestorage.app",
            messagingSenderId: "722640877424",
            appId: "1:722640877424:web:5e145b4c767af86e60c1b5"
        }};
        firebase.initializeApp(firebaseConfig);
        const db = firebase.database();

        let mode = 'login'; let selectedCountry = "Sri Lanka";
        const countryTz = {{ "Sri Lanka": "Asia/Colombo", "USA": "America/New_York", "UK": "Europe/London", "India": "Asia/Kolkata", "Australia": "Australia/Sydney" }};
        const countrySelect = document.getElementById('auth-country');
        Object.keys(countryTz).forEach(c => {{ let opt = document.createElement('option'); opt.value = c; opt.innerText = c; countrySelect.appendChild(opt); }});

        function toggleAuth(m, btn) {{
            mode = m; document.getElementById('tab-login').style.color = (m==='login'?'#fff':'#555'); document.getElementById('tab-signup').style.color = (m==='signup'?'#fff':'#555');
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
                    const u = s.val(); if(u && u.pass === pass) loginSuccess(u); else alert("Invalid Login!");
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
        }}

        function showSection(type, btn) {{
            document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active')); btn.classList.add('active');
            document.getElementById('news-container').classList.toggle('hidden', type !== 'news');
            document.getElementById('admin-container').classList.toggle('hidden', type !== 'admin');
            if(type === 'admin') {{
                db.ref('logs').on('value', s => {{
                    const tbody = document.getElementById('log-tbody'); tbody.innerHTML = "";
                    s.forEach(child => {{ const l = child.val(); tbody.innerHTML = `<tr><td style='padding:10px;'>${{l.email}}</td><td>${{l.country}}</td><td>${{l.time}}</td></tr>` + tbody.innerHTML; }});
                }});
            }}
        }}

        function toggleTooltip() {{ document.getElementById('user-tooltip').classList.toggle('hidden'); }}
        function showAbout() {{ document.getElementById('about-modal').classList.remove('hidden'); }}
        setInterval(() => {{ document.getElementById('live-clock').innerText = new Date().toLocaleTimeString('en-US', {{ timeZone: countryTz[selectedCountry] }}); }}, 1000);
    </script>
</body>
</html>
    """
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    print("\n✅ Final index.html generated with Firebase Integration.")

if __name__ == "__main__": create_final_portal()
