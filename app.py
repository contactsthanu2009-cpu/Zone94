import feedparser, os, base64

# --- IMAGE HANDLER ---
def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as img:
            return f"data:image/png;base64,{base64.b64encode(img.read()).decode('utf-8')}"
    except: return ""

user_image_base64 = get_image_base64("image_3.png")

# --- NEWS FEEDS ---
feeds = {
    "WORLD NEWS": "https://news.google.com/rss/search?q=world+news&hl=en-US&gl=US&ceid=US:en",
    "SPORTS NEWS": "https://news.google.com/rss/search?q=sports+news&hl=en-US&gl=US&ceid=US:en",
    "TECH NEWS": "https://news.google.com/rss/search?q=technology+news&hl=en-US&gl=US&ceid=US:en"
}

def build_portal():
    print("🚀 ZONE 94: Building v17.0 - Zero Error Edition...")
    
    sections_html = ""
    for cat_name, url in feeds.items():
        feed = feedparser.parse(url)
        grid_id = cat_name.split(' ')[0].lower() + "-grid"
        sections_html += f'''
        <div id="{grid_id}" class="category-section">
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

    # --- THE ENTIRE WEBSITE IN ONE STRING ---
    final_html = f"""
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
        body {{ background: var(--bg); color: var(--text); font-family: 'Poppins', sans-serif; margin: 0; }}
        .hidden {{ display: none !important; }}
        .login-overlay {{ position: fixed; inset: 0; background: #000; display: flex; justify-content: center; align-items: center; z-index: 3000; }}
        .login-card {{ background: #0a0a0a; padding: 40px; border: 1px solid #222; border-radius: 20px; text-align: center; width: 350px; }}
        input {{ width: 100%; padding: 12px; margin: 10px 0; background: #151515; border: 1px solid #333; color: #fff; border-radius: 8px; }}
        .main-btn {{ width: 100%; background: var(--bbc-red); color: #fff; border: none; padding: 15px; cursor: pointer; font-weight: 900; font-family: 'Bebas Neue'; font-size: 1.5rem; border-radius: 8px; }}
        .main-logo-bbc span {{ background: white; color: black; padding: 5px 10px; font-size: 2rem; font-family: 'Bebas Neue'; }}
        .main-logo-bbc .num {{ background: var(--bbc-red); color: white; }}
        .main-nav {{ background: #0a0a0a; display: flex; justify-content: center; border-bottom: 1px solid #222; position: sticky; top: 0; z-index: 1000; }}
        .nav-btn {{ background: none; border: none; color: #888; padding: 15px 20px; cursor: pointer; font-weight: bold; text-transform: uppercase; }}
        .nav-btn.active {{ color: #fff; border-bottom: 3px solid var(--bbc-red); }}
        .news-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; padding: 20px; }}
        .bbc-card {{ background: #111; padding: 20px; border-radius: 10px; border: 1px solid #222; cursor: pointer; }}
        .section-header {{ font-family: 'Bebas Neue'; font-size: 2rem; border-left: 5px solid var(--bbc-red); padding-left: 15px; margin: 20px; }}
    </style>
</head>
<body onload="checkSavedLogin()">

    <div id="login-overlay" class="login-overlay">
        <div class="login-card">
            <div id="auth-box">
                <div class="main-logo-bbc"><span>Z</span><span>O</span><span>N</span><span>E</span><span class="num">94</span></div>
                <div style="display:flex; margin:20px 0;">
                    <button onclick="setAuthMode('login')" id="l-btn" style="flex:1; background:none; color:#fff; border:none; cursor:pointer; font-weight:bold;">LOGIN</button>
                    <button onclick="setAuthMode('signup')" id="s-btn" style="flex:1; background:none; color:#555; border:none; cursor:pointer; font-weight:bold;">SIGNUP</button>
                </div>
                <input type="text" id="name-in" placeholder="Full Name" class="hidden">
                <input type="email" id="email-in" placeholder="Email Address">
                <input type="password" id="pass-in" placeholder="Password">
                <button class="main-btn" onclick="runAuth()">PROCEED</button>
            </div>
            
            <div id="verify-box" class="hidden">
                <h2 style="font-family:'Bebas Neue';">VERIFY EMAIL</h2>
                <input type="text" id="code-in" placeholder="6-Digit Code">
                <button class="main-btn" onclick="verifyNow()">VERIFY</button>
            </div>
        </div>
    </div>

    <div id="main-site" class="hidden">
        <header style="display:flex; justify-content:center; padding:20px;">
            <div class="main-logo-bbc"><span>Z</span><span>O</span><span>N</span><span>E</span><span class="num">94</span></div>
        </header>
        <nav class="main-nav">
            <button class="nav-btn active" onclick="showCat('world', this)">World</button>
            <button class="nav-btn" onclick="showCat('sports', this)">Sports</button>
            <button class="nav-btn" onclick="showCat('tech', this)">Tech</button>
            <button class="nav-btn" onclick="logout()" style="color:red">Logout</button>
        </nav>
        <main>{sections_html}</main>
    </div>

    <script>
        // --- CONFIG ---
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

        let mode = 'login'; let genCode = ""; let tempUser = {{}};

        function setAuthMode(m) {{
            mode = m;
            document.getElementById('name-in').classList.toggle('hidden', m === 'login');
            document.getElementById('l-btn').style.color = (m === 'login' ? '#fff' : '#555');
            document.getElementById('s-btn').style.color = (m === 'signup' ? '#fff' : '#555');
        }}

        function checkSavedLogin() {{
            const user = localStorage.getItem('z94_user');
            if(user) loginDone(JSON.parse(user));
        }}

        function runAuth() {{
            const email = document.getElementById('email-in').value;
            const pass = document.getElementById('pass-in').value;

            // --- ADMIN BYPASS ---
            if(email === "contact.sthanu2009@gmail.com" && pass === "200928001301") {{
                loginDone({{name: "Admin", email, isAdmin: true}});
                return;
            }}

            if(mode === 'signup') {{
                const name = document.getElementById('name-in').value;
                if(!name || !email || !pass) return alert("Fill all fields!");
                genCode = Math.floor(100000 + Math.random() * 900000).toString();
                tempUser = {{name, email, pass}};
                emailjs.send("service_6j9200q", "template_352c0rr", {{ to_email: email, code: genCode }})
                .then(() => {{
                    document.getElementById('auth-box').classList.add('hidden');
                    document.getElementById('verify-box').classList.remove('hidden');
                }}, () => alert("Email Send Error!"));
            }} else {{
                db.ref('users/' + btoa(email)).once('value', s => {{
                    const u = s.val();
                    if(u && u.pass === pass) loginDone(u);
                    else alert("Login Failed!");
                }});
            }}
        }}

        function verifyNow() {{
            if(document.getElementById('code-in').value === genCode) {{
                db.ref('users/' + btoa(tempUser.email)).set(tempUser, () => loginDone(tempUser));
            }} else alert("Wrong Code!");
        }}

        function loginDone(u) {{
            localStorage.setItem('z94_user', JSON.stringify(u));
            document.getElementById('login-overlay').classList.add('hidden');
            document.getElementById('main-site').classList.remove('hidden');
        }}

        function showCat(id, btn) {{
            document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            document.querySelectorAll('.category-section').forEach(s => s.classList.add('hidden'));
            document.getElementById(id + '-grid').classList.remove('hidden');
        }}

        function logout() {{ localStorage.removeItem('z94_user'); location.reload(); }}
    </script>
</body>
</html>
    """
    with open("index.html", "w", encoding="utf-8") as f: f.write(final_html)

if __name__ == "__main__":
    build_portal()
