import feedparser, google.generativeai as genai, os, base64

# ==========================================
# 0. IMAGE ENCODING (Founder Photo)
# ==========================================
def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return f"data:image/png;base64,{base64.b64encode(image_file.read()).decode('utf-8')}"
    except: return ""

user_image_base64 = get_image_base64("image_3.png")

# ==========================================
# 1. SETUP & SOURCES
# ==========================================
GEMINI_API_KEY = "AIzaSyCfVVN-XGkxubueIMrPlEKXtX-uwZouwtY"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

feeds = {
    "WORLD NEWS": "https://news.google.com/rss/search?q=world+news&hl=en-US&gl=US&ceid=US:en",
    "SPORTS NEWS": "https://news.google.com/rss/search?q=sports+news&hl=en-US&gl=US&ceid=US:en",
    "TECH TRENDING": "https://news.google.com/rss/search?q=trending+tech&hl=en-US&gl=US&ceid=US:en"
}

def create_pro_portal():
    print("🚀 ZONE 94: Designing World's #1 AI Portal...")
    sections_html = ""
    for cat_name, url in feeds.items():
        feed = feedparser.parse(url)
        grid_id = cat_name.split(' ')[0].lower() + "-grid"
        tag = cat_name.split(' ')[0]
        sections_html += f'''
        <div id="{grid_id}" class="category-section animate-up">
            <h2 class="section-header">{cat_name}</h2>
            <div class="news-grid">'''
        for entry in feed.entries[:8]:
            sections_html += f"""
            <div class="bbc-card" onclick="window.open('{entry.link}', '_blank')">
                <span class="category-tag">{tag}</span>
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
    <title>ZONE 94 | World's #1 AI Portal</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Poppins:wght@300;400;700;900&display=swap');
        
        :root {{ --bbc-red: #bb1919; --bg: #000; --card: #111; --text: #fff; --accent: #ff0000; }}
        
        body {{ background: var(--bg); color: var(--text); font-family: 'Poppins', sans-serif; margin: 0; overflow-x: hidden; scroll-behavior: smooth; }}
        .hidden {{ display: none !important; }}

        /* ANIMATIONS */
        @keyframes fadeInUp {{ from {{ opacity: 0; transform: translateY(30px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        .animate-up {{ animation: fadeInUp 0.6s ease forwards; }}

        /* LOGIN / SIGNUP */
        .login-overlay {{ position: fixed; inset: 0; background: #000; display: flex; justify-content: center; align-items: center; z-index: 3000; }}
        .login-card {{ background: #0a0a0a; padding: 40px; border: 1px solid #222; text-align: center; border-radius: 20px; width: 380px; box-shadow: 0 0 40px rgba(187,25,25,0.3); }}
        .login-tabs {{ display: flex; margin-bottom: 25px; border-bottom: 1px solid #333; }}
        .tab-btn {{ flex: 1; padding: 12px; background: none; border: none; color: #555; cursor: pointer; font-weight: bold; font-family: 'Poppins'; transition: 0.3s; }}
        .tab-btn.active {{ color: var(--bbc-red); border-bottom: 3px solid var(--bbc-red); }}
        input, select {{ display: block; width: 100%; padding: 14px; margin: 15px 0; background: #151515; border: 1px solid #333; color: #fff; border-radius: 8px; box-sizing: border-box; }}
        .main-btn {{ width: 100%; background: var(--bbc-red); color: #fff; border: none; padding: 16px; cursor: pointer; font-weight: 900; font-family: 'Bebas Neue'; font-size: 1.5rem; letter-spacing: 2px; border-radius: 8px; transition: 0.3s; }}
        .main-btn:hover {{ background: #ff0000; box-shadow: 0 0 20px rgba(255,0,0,0.5); }}

        /* HEADER & TICKER */
        .ticker-wrap {{ background: #111; display: flex; justify-content: space-between; padding: 12px 20px; border-bottom: 1px solid #222; }}
        .ticker {{ color: var(--accent); font-weight: 900; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; }}
        .site-header {{ display: flex; justify-content: space-between; align-items: center; padding: 30px 50px; background: linear-gradient(to bottom, #111, transparent); }}
        .main-logo-bbc {{ font-family: 'Bebas Neue'; cursor: pointer; }}
        .main-logo-bbc span {{ background: white; color: black; padding: 5px 15px; font-size: 2.2rem; }}
        .main-logo-bbc .num {{ background: var(--bbc-red); color: white; }}
        .avatar-circle {{ width: 50px; height: 50px; background: #fff; color: #000; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 900; border: 4px solid var(--bbc-red); cursor: pointer; }}

        /* NAVIGATION */
        .main-nav {{ background: #0a0a0a; display: flex; justify-content: center; border-bottom: 1px solid #222; position: sticky; top: 0; z-index: 1000; }}
        .main-nav button {{ background: none; border: none; color: #888; padding: 18px 25px; cursor: pointer; font-weight: 700; text-transform: uppercase; font-size: 13px; transition: 0.3s; }}
        .main-nav button:hover, .main-nav button.active {{ color: #fff; border-bottom: 4px solid var(--bbc-red); background: #111; }}

        /* CONTENT */
        .content {{ padding: 50px 30px; max-width: 1400px; margin: auto; min-height: 80vh; }}
        .section-header {{ font-family: 'Bebas Neue'; font-size: 2.5rem; color: #fff; border-left: 8px solid var(--bbc-red); padding-left: 20px; margin-bottom: 35px; letter-spacing: 2px; }}
        .news-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 30px; }}
        .bbc-card {{ background: var(--card); padding: 30px; border-radius: 15px; border: 1px solid #222; cursor: pointer; transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); }}
        .bbc-card:hover {{ transform: scale(1.03) translateY(-10px); border-color: var(--bbc-red); box-shadow: 0 15px 30px rgba(0,0,0,0.5); }}
        .category-tag {{ color: var(--bbc-red); font-weight: 900; font-size: 11px; letter-spacing: 2px; }}
        h3 {{ font-size: 1.4rem; margin: 15px 0; line-height: 1.3; font-weight: 700; color: #fff; }}

        /* FOOTER */
        footer {{ text-align: center; padding: 40px; border-top: 1px solid #222; margin-top: 50px; font-size: 12px; color: #444; letter-spacing: 1px; }}

        /* MODALS */
        .modal-bg {{ position: fixed; inset: 0; background: rgba(0,0,0,0.95); display: flex; justify-content: center; align-items: center; z-index: 4000; }}
        .modal-content {{ background: #0a0a0a; padding: 50px; text-align: center; border: 1px solid #333; border-radius: 25px; max-width: 500px; position: relative; }}
        .modal-photo {{ width: 160px; height: 160px; border-radius: 50%; border: 4px solid var(--bbc-red); margin-bottom: 25px; object-fit: cover; box-shadow: 0 0 30px rgba(187,25,25,0.5); }}
        
        .social-links {{ display: flex; justify-content: center; gap: 20px; margin-top: 30px; }}
        .social-btn {{ padding: 12px 25px; border-radius: 10px; font-weight: 900; text-decoration: none; font-size: 14px; transition: 0.3s; color: #fff; }}
        .wa {{ background: #25d366; }}
        .ln {{ background: #0077b5; }}
        
        .channel-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 20px; }}
        .ch-btn {{ background: #111; border: 1px solid #333; color: #fff; padding: 25px; cursor: pointer; font-weight: 900; font-family: 'Bebas Neue'; font-size: 1.2rem; border-radius: 10px; transition: 0.3s; }}
        .ch-btn:hover {{ background: var(--bbc-red); transform: scale(1.05); }}

        #user-tooltip {{ position: absolute; top: 90px; right: 50px; background: #0a0a0a; border: 1px solid #333; border-radius: 15px; padding: 25px; width: 280px; z-index: 2000; box-shadow: 0 20px 50px rgba(0,0,0,0.9); }}
    </style>
</head>
<body>

    <div id="login-overlay" class="login-overlay">
        <div class="login-card animate-up">
            <div class="main-logo-bbc"><span>Z</span><span>O</span><span>N</span><span>E</span><span class="num">94</span></div>
            <div class="login-tabs">
                <button class="tab-btn active" id="tab-login" onclick="toggleAuth('login')">LOGIN</button>
                <button class="tab-btn" id="tab-signup" onclick="toggleAuth('signup')">SIGN UP</button>
            </div>
            <div id="signup-fields" class="hidden">
                <input type="text" id="reg-name" placeholder="User Name">
            </div>
            <input type="email" id="auth-email" placeholder="Email Address">
            <input type="password" id="auth-pass" placeholder="Password">
            <select id="auth-country" onchange="updateTimezoneHint()"></select>
            <button class="main-btn" id="auth-submit" onclick="handleAuth()">ENTER THE ZONE</button>
        </div>
    </div>

    <div id="main-site" class="hidden">
        <div class="ticker-wrap">
            <div class="ticker">🚀 ZONE 94 — WORLD'S NUMBER 1 AI NEWS PORTAL — 24/7 GLOBAL INTELLIGENCE — REAL-TIME UPDATES — </div>
            <div id="live-clock" style="color:#666; font-weight:bold">00:00:00</div>
        </div>

        <header class="site-header">
            <div style="width:100px"></div>
            <div class="main-logo-bbc" onclick="window.location.reload()"><span>Z</span><span>O</span><span>N</span><span>E</span><span class="num">94</span></div>
            <div id="user-avatar" class="avatar-circle" onclick="toggleUserTooltip()">U</div>
        </header>

        <nav class="main-nav">
            <button class="nav-btn active" onclick="showMain('news', this)">Global Intelligence</button>
            <button class="nav-btn" onclick="showMain('channels', this)">Live Channels</button>
            <button class="nav-btn hidden" id="nav-admin" onclick="showMain('admin', this)" style="color:var(--bbc-red)">ADMIN PANEL</button>
            <button class="nav-btn" onclick="showAboutModal()">About Founder</button>
        </nav>

        <main class="content">
            <div id="news-container" class="animate-up">{sections_html}</div>

            <div id="channels-container" class="hidden animate-up">
                <h2 class="section-header">Global Live Broadcasts</h2>
                <div style="margin-bottom:40px;">
                    <h3 style="color:var(--bbc-red)">UNITED STATES</h3>
                    <div class="channel-grid">
                        <button class="ch-btn" onclick="window.open('https://www.youtube.com/@ABCNews/live')">ABC News</button>
                        <button class="ch-btn" onclick="window.open('https://www.youtube.com/@NBCNews/live')">NBC News</button>
                        <button class="ch-btn" onclick="window.open('https://www.youtube.com/@CBSNews/live')">CBS News</button>
                        <button class="ch-btn" onclick="window.open('https://www.youtube.com/@FoxNews/live')">Fox News</button>
                    </div>
                </div>
                <div style="margin-bottom:40px;">
                    <h3 style="color:var(--bbc-red)">UNITED KINGDOM</h3>
                    <div class="channel-grid">
                        <button class="ch-btn" onclick="window.open('https://www.youtube.com/@bbcnews/live')">BBC World News</button>
                        <button class="ch-btn" onclick="window.open('https://www.youtube.com/@SkyNews/live')">Sky News</button>
                        <button class="ch-btn" onclick="window.open('https://www.youtube.com/@GBNewsOnline/live')">GB News</button>
                        <button class="ch-btn" onclick="window.open('https://www.youtube.com/@Channel4News/live')">Channel 4</button>
                    </div>
                </div>
            </div>

            <div id="admin-container" class="hidden animate-up">
                <div class="admin-panel" style="background:#111; padding:40px; border-radius:20px; border:1px solid var(--bbc-red);">
                    <h2 class="section-header">Master Control Panel</h2>
                    <table class="log-table" style="width:100%; border-collapse:collapse;">
                        <thead><tr style="color:var(--bbc-red); text-align:left;"><th>Email</th><th>Country</th><th>Timestamp</th></tr></thead>
                        <tbody id="log-tbody"></tbody>
                    </table>
                </div>
            </div>

            <footer>
                ZONE 94 | ALL RIGHTS RESERVED © 2026<br>
                SOURCES: AI-GEMINI ENGINE | POWERED BY GLOBAL INTELLIGENCE
            </footer>
        </main>
    </div>

    <div id="about-modal" class="modal-bg hidden" onclick="closeAboutModal()">
        <div class="modal-content animate-up" onclick="event.stopPropagation()">
            <h2 class="section-header" style="border:none; text-align:center;">THE FOUNDER</h2>
            <img src="{user_image_base64}" alt="Founder" class="modal-photo">
            <div style="text-align: left; display: inline-block; font-size: 14px;">
                <p><strong>NAME:</strong> P.D.T SATHSARA</p>
                <p><strong>AGE:</strong> 17</p>
                <p><strong>ADDRESS:</strong> 57, MIRISWATHTHA, PELPOLA, PARAGASTHOTA</p>
                <p><strong>EMAIL:</strong> contact.sthanu2009@gmail.com</p>
            </div>
            <div class="social-links">
                <a href="https://wa.me/94765738122" target="_blank" class="social-btn wa">WHATSAPP</a>
                <a href="https://www.linkedin.com/in/thanuka-sathsara-freelancer" target="_blank" class="social-btn ln">LINKEDIN</a>
            </div>
            <button class="main-btn" style="margin-top:30px; width:auto; padding:10px 40px; font-size:1.2rem;" onclick="closeAboutModal()">CLOSE</button>
            <div style="font-size: 10px; color: #333; margin-top: 20px;">ZONE 94 ALL RIGHTS RESERVED.</div>
        </div>
    </div>

    <div id="user-tooltip" class="hidden">
        <h4 style="margin:0; color:var(--bbc-red); font-family:'Bebas Neue'; font-size:1.5rem;">USER PROFILE</h4>
        <p style="font-size:12px; color:#aaa; margin:10px 0;">Name: <strong id="tp-name" style="color:#fff;">User</strong></p>
        <p style="font-size:12px; color:#aaa; margin:10px 0;">Email: <strong id="tp-email" style="color:#fff;">Email</strong></p>
        <div style="display:flex; gap:10px; margin-top:20px;">
            <button class="main-btn" style="padding:5px; font-size:1rem;" onclick="window.location.reload()">LOGOUT</button>
            <button class="main-btn" style="padding:5px; font-size:1rem; background:#333;" onclick="toggleUserTooltip()">EXIT</button>
        </div>
    </div>

    <script>
        let mode = 'login';
        let selectedCountry = "Sri Lanka";
        const countryTz = {{ "Sri Lanka": "Asia/Colombo", "USA": "America/New_York", "UK": "Europe/London", "India": "Asia/Kolkata", "Australia": "Australia/Sydney", "Canada": "America/Toronto" }};
        const countrySelect = document.getElementById('auth-country');
        Object.keys(countryTz).forEach(c => {{ let opt = document.createElement('option'); opt.value = c; opt.innerText = c; countrySelect.appendChild(opt); }});

        function handleAuth() {{
            const email = document.getElementById('auth-email').value;
            const pass = document.getElementById('auth-pass').value;
            selectedCountry = countrySelect.value;
            if (email === "contact.sthanu2009@gmail.com" && pass === "200928001301") {{
                loginSuccess({{ name: "Admin", email: email, isAdmin: true }});
            }} else {{
                let users = JSON.parse(localStorage.getItem('z94_db')) || [];
                let user = users.find(u => u.email === email && u.pass === pass);
                if (user) loginSuccess({{ ...user, isAdmin: false }});
                else if (mode === 'signup') {{
                    const name = document.getElementById('reg-name').value;
                    users.push({{ name, email, pass, country: selectedCountry }});
                    localStorage.setItem('z94_db', JSON.stringify(users));
                    alert("Account Created! Please Login."); toggleAuth('login');
                }} else alert("Access Denied!");
            }}
        }}

        function loginSuccess(user) {{
            document.getElementById('login-overlay').classList.add('hidden');
            document.getElementById('main-site').classList.remove('hidden');
            document.getElementById('user-avatar').innerText = user.name.charAt(0).toUpperCase();
            document.getElementById('tp-name').innerText = user.name;
            document.getElementById('tp-email').innerText = user.email;
            if (user.isAdmin) document.getElementById('nav-admin').classList.remove('hidden');
            let logs = JSON.parse(localStorage.getItem('z94_logs')) || [];
            logs.push({{ email: user.email, country: selectedCountry, time: new Date().toLocaleString() }});
            localStorage.setItem('z94_logs', JSON.stringify(logs));
        }}

        function showMain(type, btn) {{
            document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById('news-container').classList.toggle('hidden', type !== 'news');
            document.getElementById('channels-container').classList.toggle('hidden', type !== 'channels');
            document.getElementById('admin-container').classList.toggle('hidden', type !== 'admin');
            if (type === 'admin') {{
                const tbody = document.getElementById('log-tbody'); tbody.innerHTML = "";
                let logs = JSON.parse(localStorage.getItem('z94_logs')) || [];
                logs.reverse().forEach(l => {{ tbody.innerHTML += `<tr style='border-bottom:1px solid #222; height:40px;'><td>${{l.email}}</td><td>${{l.country}}</td><td>${{l.time}}</td></tr>`; }});
            }}
        }}

        function toggleAuth(m) {{ mode = m; document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active')); document.getElementById('tab-'+m).classList.add('active'); document.getElementById('signup-fields').classList.toggle('hidden', m === 'login'); }}
        function toggleUserTooltip() {{ document.getElementById('user-tooltip').classList.toggle('hidden'); }}
        function showAboutModal() {{ document.getElementById('about-modal').classList.remove('hidden'); }}
        function closeAboutModal() {{ document.getElementById('about-modal').classList.add('hidden'); }}
        setInterval(() => {{ document.getElementById('live-clock').innerText = new Date().toLocaleTimeString('en-US', {{ timeZone: countryTz[selectedCountry] }}); }}, 1000);
    </script>
</body>
</html>
    """
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(full_html)
    print("\n✅ Success! ZONE 94 v4.0 (Global Edition) is Live.")

if __name__ == "__main__":
    create_pro_portal()