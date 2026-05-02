from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from api import phone

app = FastAPI(docs_url=None, redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(phone.router, prefix="/phone", tags=["phone"])

API_DOCS = [
    {
        "category": "Phone",
        "prefix": "/phone",
        "description": "手机设备信息接口，随机返回一个手机型号及完整硬件参数。",
        "endpoints": [
            {
                "method": "GET",
                "path": "/phone/",
                "description": "随机返回一个手机型号",
                "example": "https://api.shuoweb.com/phone/"
            },
            {
                "method": "GET",
                "path": "/phone/search?brand=Apple",
                "description": "从指定品牌或系统中随机返回一个，支持 brand 和 os 参数",
                "example": "https://api.shuoweb.com/phone/search?brand=Apple"
            },
            {
                "method": "GET",
                "path": "/phone/{model}",
                "description": "按型号查询指定设备详情",
                "example": "https://api.shuoweb.com/phone/iPhone 15 Pro"
            }
        ]
    }
]

HTML = """
<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>ShuoWeb API</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg: #080c10;
    --surface: #0e1318;
    --border: #1a2230;
    --accent: #00d4ff;
    --accent2: #7b61ff;
    --text: #e8f0fe;
    --muted: #556070;
    --get: #00c9a7;
    --post: #f7b731;
  }

  html { scroll-behavior: smooth; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Syne', sans-serif;
    min-height: 100vh;
    overflow-x: hidden;
  }

  /* Background grid */
  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
      linear-gradient(rgba(0,212,255,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(0,212,255,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
  }

  /* Glow orbs */
  .orb {
    position: fixed;
    border-radius: 50%;
    filter: blur(120px);
    pointer-events: none;
    z-index: 0;
  }
  .orb1 {
    width: 600px; height: 600px;
    background: rgba(0,212,255,0.06);
    top: -200px; left: -200px;
  }
  .orb2 {
    width: 500px; height: 500px;
    background: rgba(123,97,255,0.06);
    bottom: -100px; right: -100px;
  }

  .container {
    position: relative;
    z-index: 1;
    max-width: 960px;
    margin: 0 auto;
    padding: 0 24px;
  }

  /* Header */
  header {
    padding: 80px 0 60px;
    border-bottom: 1px solid var(--border);
  }

  .logo-row {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 32px;
  }

  .logo-icon {
    width: 42px; height: 42px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
    font-weight: 800;
    color: #080c10;
    letter-spacing: -1px;
    flex-shrink: 0;
  }

  .logo-text {
    font-size: 15px;
    font-weight: 600;
    color: var(--muted);
    letter-spacing: 3px;
    text-transform: uppercase;
  }

  h1 {
    font-size: clamp(42px, 7vw, 72px);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -2px;
    background: linear-gradient(135deg, #fff 30%, var(--accent) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 20px;
  }

  .subtitle {
    font-size: 17px;
    color: var(--muted);
    font-weight: 400;
    max-width: 520px;
    line-height: 1.7;
  }

  .base-url-box {
    margin-top: 36px;
    display: inline-flex;
    align-items: center;
    gap: 12px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px 20px;
  }

  .base-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--muted);
  }

  .base-url {
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px;
    color: var(--accent);
  }

  /* Stats */
  .stats {
    display: flex;
    gap: 40px;
    margin-top: 48px;
    padding-top: 40px;
    border-top: 1px solid var(--border);
  }

  .stat-item { }
  .stat-num {
    font-size: 32px;
    font-weight: 800;
    color: #fff;
    letter-spacing: -1px;
  }
  .stat-label {
    font-size: 12px;
    color: var(--muted);
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-top: 2px;
  }

  /* Section */
  .section {
    padding: 64px 0;
    border-bottom: 1px solid var(--border);
    animation: fadeUp 0.6s ease both;
  }

  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .category-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 32px;
    gap: 20px;
  }

  .category-tag {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(0,212,255,0.08);
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 6px;
    padding: 4px 12px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 12px;
  }

  .category-tag .dot {
    width: 6px; height: 6px;
    background: var(--accent);
    border-radius: 50%;
    animation: pulse 2s infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
  }

  .category-title {
    font-size: 26px;
    font-weight: 700;
    letter-spacing: -0.5px;
    color: #fff;
  }

  .category-desc {
    font-size: 14px;
    color: var(--muted);
    line-height: 1.7;
    max-width: 500px;
    margin-top: 8px;
  }

  /* Endpoint card */
  .endpoint-list { display: flex; flex-direction: column; gap: 12px; }

  .endpoint-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
    transition: border-color 0.2s, transform 0.2s;
  }

  .endpoint-card:hover {
    border-color: rgba(0,212,255,0.3);
    transform: translateX(4px);
  }

  .endpoint-top {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 18px 22px;
    cursor: pointer;
    user-select: none;
  }

  .method-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 500;
    padding: 3px 10px;
    border-radius: 5px;
    flex-shrink: 0;
    letter-spacing: 0.5px;
  }

  .method-get {
    background: rgba(0,201,167,0.12);
    color: var(--get);
    border: 1px solid rgba(0,201,167,0.25);
  }

  .endpoint-path {
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px;
    color: var(--text);
    flex: 1;
  }

  .endpoint-desc {
    font-size: 13px;
    color: var(--muted);
    margin-left: auto;
    text-align: right;
  }

  .endpoint-detail {
    border-top: 1px solid var(--border);
    padding: 18px 22px;
    display: none;
  }

  .endpoint-detail.open { display: block; }

  .detail-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 8px;
  }

  .example-url {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    color: var(--accent);
    background: rgba(0,212,255,0.05);
    border: 1px solid rgba(0,212,255,0.15);
    border-radius: 7px;
    padding: 10px 14px;
    word-break: break-all;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
  }

  .copy-btn {
    background: none;
    border: none;
    cursor: pointer;
    color: var(--muted);
    font-size: 12px;
    font-family: 'Syne', sans-serif;
    padding: 2px 8px;
    border-radius: 4px;
    transition: color 0.2s, background 0.2s;
    flex-shrink: 0;
    letter-spacing: 1px;
    text-transform: uppercase;
  }

  .copy-btn:hover { color: var(--accent); background: rgba(0,212,255,0.08); }

  /* Footer */
  footer {
    padding: 48px 0;
    text-align: center;
    color: var(--muted);
    font-size: 13px;
  }

  footer a { color: var(--accent); text-decoration: none; }

  @media (max-width: 600px) {
    .stats { gap: 24px; flex-wrap: wrap; }
    .endpoint-desc { display: none; }
    .category-header { flex-direction: column; }
  }
</style>
</head>
<body>
<div class="orb orb1"></div>
<div class="orb orb2"></div>

<div class="container">
  <header>
    <div class="logo-row">
      <div class="logo-icon">SW</div>
      <div class="logo-text">ShuoWeb API</div>
    </div>
    <h1>Open API<br>Platform</h1>
    <p class="subtitle">稳定、开放、免费的数据接口平台，支持跨域请求，所有接口返回标准 JSON 格式。</p>
    <div class="base-url-box">
      <span class="base-label">Base URL</span>
      <span class="base-url">https://api.shuoweb.com</span>
    </div>
    <div class="stats" id="stats">
      <!-- filled by JS -->
    </div>
  </header>

  <main id="main">
    <!-- filled by JS -->
  </main>

  <footer>
    <p>© 2024 <a href="https://shuoweb.com">ShuoWeb</a> · 所有接口免费开放 · 支持跨域</p>
  </footer>
</div>

<script>
const API_DOCS = __API_DOCS__;

// Stats
const totalEndpoints = API_DOCS.reduce((s, c) => s + c.endpoints.length, 0);
document.getElementById('stats').innerHTML = `
  <div class="stat-item">
    <div class="stat-num">${API_DOCS.length}</div>
    <div class="stat-label">接口分类</div>
  </div>
  <div class="stat-item">
    <div class="stat-num">${totalEndpoints}</div>
    <div class="stat-label">接口数量</div>
  </div>
  <div class="stat-item">
    <div class="stat-num">∞</div>
    <div class="stat-label">免费无限制</div>
  </div>
`;

// Render sections
const main = document.getElementById('main');
API_DOCS.forEach((cat, ci) => {
  const section = document.createElement('div');
  section.className = 'section';
  section.style.animationDelay = `${ci * 0.1}s`;

  const endpoints = cat.endpoints.map((ep, ei) => `
    <div class="endpoint-card">
      <div class="endpoint-top" onclick="toggle(${ci},${ei})">
        <span class="method-badge method-${ep.method.toLowerCase()}">${ep.method}</span>
        <span class="endpoint-path">${ep.path}</span>
        <span class="endpoint-desc">${ep.description}</span>
      </div>
      <div class="endpoint-detail" id="detail-${ci}-${ei}">
        <div class="detail-label">示例请求</div>
        <div class="example-url">
          <span>${ep.example}</span>
          <button class="copy-btn" onclick="copy(event,'${ep.example}')">复制</button>
        </div>
      </div>
    </div>
  `).join('');

  section.innerHTML = `
    <div class="category-header">
      <div>
        <div class="category-tag"><span class="dot"></span>${cat.category}</div>
        <div class="category-title">${cat.prefix}</div>
        <div class="category-desc">${cat.description}</div>
      </div>
    </div>
    <div class="endpoint-list">${endpoints}</div>
  `;
  main.appendChild(section);
});

function toggle(ci, ei) {
  const el = document.getElementById(`detail-${ci}-${ei}`);
  el.classList.toggle('open');
}

function copy(e, text) {
  e.stopPropagation();
  navigator.clipboard.writeText(text).then(() => {
    const btn = e.target;
    btn.textContent = '已复制';
    setTimeout(() => btn.textContent = '复制', 1500);
  });
}
</script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def index():
    import json
    html = HTML.replace("__API_DOCS__", json.dumps(API_DOCS, ensure_ascii=False))
    return HTMLResponse(content=html)
