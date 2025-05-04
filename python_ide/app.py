import os
import io
import zipfile
import subprocess
from flask import Flask, render_template, request, jsonify, send_file

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run_code():
    code = request.json.get("code", "")
    with open("user_code.py", "w", encoding="utf-8") as f:
        f.write(code)
    proc = subprocess.Popen(["python", "user_code.py"],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             text=True)
    output, _ = proc.communicate(timeout=10)
    return jsonify({"output": output})

@app.route("/download/raw")
def download_raw():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk('.'):
            if any(x in root for x in ("venv", "dist", "__pycache__")):
                continue
            for fn in files:
                z.write(os.path.join(root, fn))
    buf.seek(0)
    return send_file(buf, as_attachment=True, download_name="python_ide.zip")

@app.route("/download/exe")
def download_exe():
    exe_path = os.path.join("dist", "app", "app.exe")
    if not os.path.exists(exe_path):
        return "EXE not found. Run `python package_app.py` first.", 404
    return send_file(exe_path, as_attachment=True, download_name="python_ide.exe")

if __name__ == "__main__":
    app.run(debug=True)
