from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import html


# =========================
# FINDER DATABASE
# =========================

ITEMS = [
    {
        "name": "GTA V",
        "type": "Game",
        "platform": ["PC"],
        "tags": ["gta", "open world", "action"],
        "price": "paid",
        "link": "https://store.rockstargames.com/game/buy-gta-v"
    },

    {
        "name": "GTA San Andreas",
        "type": "Game",
        "platform": ["Mobile", "PC"],
        "tags": ["gta", "open world", "action"],
        "price": "paid",
        "link": "https://www.rockstargames.com/games/sanandreas"
    },

    {
        "name": "Gangstar Vegas",
        "type": "Game",
        "platform": ["Mobile"],
        "tags": ["gta", "open world", "action"],
        "price": "free",
        "link": "https://play.google.com/store/apps/details?id=com.gameloft.android.ANMP.GloftGGHM"
    },

    {
        "name": "Payback 2",
        "type": "Game",
        "platform": ["Mobile"],
        "tags": ["gta", "open world", "action"],
        "price": "free",
        "link": "https://play.google.com/store/apps/details?id=net.apex_designs.payback2"
    },

    {
        "name": "CapCut",
        "type": "App",
        "platform": ["Mobile", "PC"],
        "tags": ["video", "editing"],
        "price": "free",
        "link": "https://www.capcut.com/tools/video-editor-download"
    },

    {
        "name": "VN Video Editor",
        "type": "App",
        "platform": ["Mobile"],
        "tags": ["video", "editing"],
        "price": "free",
        "link": "https://www.vlognow.me/"
    },

    {
        "name": "DaVinci Resolve",
        "type": "Software",
        "platform": ["PC"],
        "tags": ["video", "editing"],
        "price": "free",
        "link": "https://www.blackmagicdesign.com/products/davinciresolve"
    },

    {
        "name": "Canva",
        "type": "Website",
        "platform": ["Web", "Mobile", "PC"],
        "tags": ["design", "thumbnail", "editing"],
        "price": "free",
        "link": "https://www.canva.com/"
    }
]


# =========================
# SEARCH
# =========================

def find_items(query):

    q = query.lower().strip()

    platform = None
    price = None
    category = None

    # PLATFORM
    if any(word in q for word in [
        "mobile", "android", "phone"
    ]):
        platform = "Mobile"

    elif any(word in q for word in [
        "pc", "computer", "windows", "laptop"
    ]):
        platform = "PC"

    elif any(word in q for word in [
        "website", "web", "browser"
    ]):
        platform = "Web"

    # PRICE
    if any(word in q for word in [
        "free", "muft"
    ]):
        price = "free"

    elif any(word in q for word in [
        "paid", "buy", "purchase"
    ]):
        price = "paid"

    # CATEGORY
    if any(word in q for word in [
        "game", "games", "gta", "minecraft", "gaming"
    ]):
        category = "Game"

    elif any(word in q for word in [
        "app", "application"
    ]):
        category = "App"

    elif any(word in q for word in [
        "software", "program"
    ]):
        category = "Software"

    elif any(word in q for word in [
        "website", "site"
    ]):
        category = "Website"

    results = []

    for item in ITEMS:

        # Category filter
        if category:
            if item["type"] != category:
                continue

        # Platform filter
        if platform:
            if platform not in item["platform"]:
                continue

        # Price filter
        if price:
            if item["price"] != price:
                continue

        score = 0

        # Matching tags
        for tag in item["tags"]:
            if tag in q:
                score += 2

        # Special searches
        if "gta" in q and "gta" in item["tags"]:
            score += 5

        if "open world" in q and "open world" in item["tags"]:
            score += 5

        if "editing" in q and "editing" in item["tags"]:
            score += 3

        if "video" in q and "video" in item["tags"]:
            score += 3

        # If no specific filter, still allow matching items
        if category or platform or price or score > 0:
            results.append((score, item))

    results.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [item for score, item in results]


# =========================
# RESULTS
# =========================

def make_results(query):

    results = find_items(query)

    if not results:

        return """
        <div class="noresult">
            ❌ No matching result found.
            <br><br>
            Try:
            <br>
            • GTA jaisi open world game mobile pe free
            <br>
            • PC ke liye free video editing
            <br>
            • Mobile video editing app
        </div>
        """

    output = """
    <h2>✨ Found for you</h2>
    """

    for item in results:

        name = html.escape(item["name"])
        typ = html.escape(item["type"])
        price = html.escape(item["price"])
        platforms = html.escape(
            ", ".join(item["platform"])
        )
        link = html.escape(
            item["link"],
            quote=True
        )

        output += f"""
        <div class="card">

            <h3>🔹 {name}</h3>

            <p>
                <b>Type:</b> {typ}
            </p>

            <p>
                <b>Platform:</b> {platforms}
            </p>

            <p>
                <b>Price:</b> {price}
            </p>

            <a
                href="{link}"
                target="_blank"
                class="download"
            >
                ⬇️ Download / Open
            </a>

        </div>
        """

    return output


# =========================
# WEBSITE
# =========================

def make_page(results=""):

    return f"""
<!DOCTYPE html>

<html>

<head>

<meta name="viewport"
content="width=device-width, initial-scale=1">

<title>Best Finder Tool</title>

<style>

* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    background: #09090f;
    color: white;
    font-family: Arial, sans-serif;
}}

.container {{
    width: 92%;
    max-width: 700px;
    margin: 45px auto;
}}

.logo {{
    text-align: center;
    font-size: 34px;
    font-weight: bold;
}}

.subtitle {{
    text-align: center;
    color: #999;
    margin-top: 10px;
    margin-bottom: 28px;
}}

.searchbox {{
    background: #171720;
    border: 1px solid #30303d;
    padding: 8px;
    border-radius: 16px;
}}

textarea {{
    width: 100%;
    height: 110px;
    background: transparent;
    color: white;
    border: none;
    outline: none;
    resize: none;
    padding: 12px;
    font-size: 17px;
}}

textarea::placeholder {{
    color: #777;
}}

button {{
    width: 100%;
    border: none;
    border-radius: 12px;
    padding: 15px;
    background: #6c5ce7;
    color: white;
    font-size: 17px;
    font-weight: bold;
}}

.card {{
    background: #171720;
    border: 1px solid #292936;
    border-radius: 16px;
    padding: 18px;
    margin-top: 15px;
}}

.card h3 {{
    margin-top: 0;
    font-size: 21px;
}}

.card p {{
    color: #aaa;
}}

.download {{
    display: block;
    text-align: center;
    background: #6c5ce7;
    color: white;
    padding: 13px;
    border-radius: 10px;
    text-decoration: none;
    font-weight: bold;
    margin-top: 15px;
}}

.noresult {{
    background: #171720;
    padding: 20px;
    border-radius: 15px;
    margin-top: 20px;
    color: #aaa;
}}

</style>

</head>

<body>

<div class="container">

<div class="logo">
🔎 Find your tool
</div>

<div class="subtitle">
Describe what you need
</div>

<form method="POST">

<div class="searchbox">

<textarea
name="query"
placeholder="Find your tool..."
></textarea>

<button type="submit">
🔍 Find
</button>

</div>

</form>

{results}

</div>

</body>

</html>
"""


# =========================
# SERVER
# =========================

class FinderHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        self.send_page(
            make_page()
        )

    def do_POST(self):

        length = int(
            self.headers.get(
                "Content-Length",
                0
            )
        )

        body = self.rfile.read(
            length
        ).decode("utf-8")

        form = parse_qs(body)

        query = form.get(
            "query",
            [""]
        )[0]

        results = make_results(query)

        self.send_page(
            make_page(results)
        )

    def send_page(self, content):

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "text/html; charset=utf-8"
        )

        self.end_headers()

        self.wfile.write(
            content.encode("utf-8")
        )


# =========================
# START
# =========================

print("================================")
print("🔎 BEST FINDER TOOL")
print("================================")
print("Server started!")
print("Open this:")
print("http://127.0.0.1:8080")
print("================================")


import os

port = int(os.environ.get("PORT", 8080))

server = HTTPServer(
    ("0.0.0.0", port),
    FinderHandler
)

server.serve_forever()