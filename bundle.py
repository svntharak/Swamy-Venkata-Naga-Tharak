import os, base64

base = os.path.dirname(os.path.abspath(__file__))
out  = os.path.join(base, 'BHARAT_BENEFITS_AI_COMPLETE.html')

# Read text assets
def read(path, enc='utf-8'):
    with open(path, encoding=enc) as f:
        return f.read()

# Read binary assets and convert to base64 data URIs
def img_b64(path, mime='image/jpeg'):
    with open(path, 'rb') as f:
        data = base64.b64encode(f.read()).decode('ascii')
    return f'data:{mime};base64,{data}'

css         = read(os.path.join(base, 'style.css'))
js_app      = read(os.path.join(base, 'app.js'))
js_schemes  = read(os.path.join(base, 'data', 'schemes.js'))
js_support  = read(os.path.join(base, 'data', 'support_data.js'))

assets_dir = os.path.join(base, 'assets')
logo_b64   = img_b64(os.path.join(assets_dir, 'bharat_benefits_logo.jpg'))
robot_b64  = img_b64(os.path.join(assets_dir, 'bharat_mitra_robot.jpg'))
banner_b64 = img_b64(os.path.join(assets_dir, 'bharat_benefits_banner.jpg'))
hero_b64   = img_b64(os.path.join(assets_dir, 'hero_citizen_woman.png'), 'image/png')
prob_b64   = img_b64(os.path.join(assets_dir, 'problem_stressed_citizen.png'), 'image/png')
sol_b64    = img_b64(os.path.join(assets_dir, 'solution_dashboard.png'), 'image/png')
impact_b64 = img_b64(os.path.join(assets_dir, 'impact_happy_family.png'), 'image/png')

# Replace asset paths with base64 data URIs in JS (not needed in HTML)
# Replace in HTML template
html_template = read(os.path.join(base, 'index.html'))

html_template = html_template.replace(
    '<link rel="stylesheet" href="style.css" />', 
    f'<style>\n{css}\n</style>'
)
html_template = html_template.replace(
    '  <!-- Preloaded Offline Data Scripts (Guarantees Instant Execution Anywhere) -->\n  <script src="data/schemes.js"></script>\n  <script src="data/support_data.js"></script>\n  <!-- App Logic Script -->\n  <script src="app.js"></script>',
    f'<script>\n{js_schemes}\n</script>\n<script>\n{js_support}\n</script>\n<script>\n{js_app}\n</script>'
)

# Replace image src paths with base64 embedded data
html_template = html_template.replace('src="assets/bharat_benefits_logo.jpg"', f'src="{logo_b64}"')
html_template = html_template.replace('src="assets/bharat_mitra_robot.jpg"',   f'src="{robot_b64}"')
html_template = html_template.replace('src="assets/bharat_benefits_banner.jpg"', f'src="{banner_b64}"')
html_template = html_template.replace('src="assets/hero_citizen_woman.png"',   f'src="{hero_b64}"')
html_template = html_template.replace('src="assets/problem_stressed_citizen.png"', f'src="{prob_b64}"')
html_template = html_template.replace('src="assets/solution_dashboard.png"',   f'src="{sol_b64}"')
html_template = html_template.replace('src="assets/impact_happy_family.png"',  f'src="{impact_b64}"')

# Remove Google Fonts external dependency (replace with system font fallback)
# Keep fonts if online, add fallback
html_template = html_template.replace(
    '<link rel="preconnect" href="https://fonts.googleapis.com">',
    '<link rel="preconnect" href="https://fonts.googleapis.com" crossorigin>'
)

with open(out, 'w', encoding='utf-8') as f:
    f.write(html_template)

size_mb = os.path.getsize(out) / (1024 * 1024)
print(f'Bundle created: BHARAT_BENEFITS_AI_COMPLETE.html ({size_mb:.2f} MB)')
print(f'Path: {out}')
print('Open this single file in ANY browser — works completely offline!')
