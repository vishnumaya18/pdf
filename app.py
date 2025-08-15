from flask import Flask, render_template, request, send_file
from reportlab.pdfgen import canvas
import io
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file_name = request.form.get("filename", f"document_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
        text_content = request.form.get("content", "")

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.setFont("Helvetica", 12)

        y = 800
        for line in text_content.split("\n"):
            p.drawString(50, y, line)
            y -= 20

        p.showPage()
        p.save()
        buffer.seek(0)

        return send_file(buffer, as_attachment=True, download_name=file_name, mimetype="application/pdf")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
