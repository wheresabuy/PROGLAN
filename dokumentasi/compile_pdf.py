import os
import re
import subprocess
import sys

# List of files in logical order
DOCS_ORDER = [
    "main.md",
    "engine.md",
    "sanctuary_logic.md",
    "shooting_range.md",
    "entities.md",
    "dialogue.md",
    "hud.md",
    "gestures.md",
    "visualisasi_logika_pistol.md",
    "game_architecture_flowchart.md"
]

def compile_docs():
    docs_dir = "/home/abuyyy/PemogramanLanjut/dokumentasi"
    html_output_path = os.path.join(docs_dir, "all_docs.html")
    pdf_output_path = os.path.join(docs_dir, "dokumentasi_lengkap.pdf")
    
    # Check virtual environment Python's markdown library
    try:
        import markdown
    except ImportError:
        print("Error: 'markdown' package is not installed. Installing it now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown"])
        import markdown

    combined_markdown = ""
    
    # 1. Create a beautiful Cover Page in markdown
    cover_page = """
<div class="cover-page">
    <div class="cover-title">DOKUMENTASI LENGKAP</div>
    <div class="cover-subtitle">Gim Sanctuary Defense & Modul Pengenalan Gestur</div>
    <div class="cover-divider"></div>
    <div class="cover-meta">
        <p><strong>Mata Kuliah:</strong> Pemrograman Lanjut</p>
        <p><strong>Bahasa Pemrograman:</strong> Python (Pygame & MediaPipe)</p>
        <p><strong>Tanggal Pembuatan:</strong> Juni 2026</p>
    </div>
</div>

---

"""
    combined_markdown += cover_page
    
    for filename in DOCS_ORDER:
        file_path = os.path.join(docs_dir, filename)
        if not os.path.exists(file_path):
            print(f"Warning: {filename} not found, skipping...")
            continue
            
        print(f"Processing {filename}...")
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Replace relative image links with absolute file paths so LibreOffice can resolve them
        # Example: ![Visualisasi Logika Pistol](./pistol_gesture_logic.png) -> ![Visualisasi Logika Pistol](/home/abuyyy/PemogramanLanjut/dokumentasi/pistol_gesture_logic.png)
        content = re.sub(
            r'!\[(.*?)\]\(\./(.*?)\)', 
            r'![\1](' + docs_dir.replace('\\', '/') + r'/\2)', 
            content
        )
        content = re.sub(
            r'!\[(.*?)\]\((?!http)(.*?)\)', 
            r'![\1](' + docs_dir.replace('\\', '/') + r'/\2)', 
            content
        )
        
        # Add page break marker before each file content (except the first heading in HTML body)
        combined_markdown += f"\n\n<!-- PAGE BREAK -->\n\n"
        combined_markdown += content
        combined_markdown += "\n\n"

    # Convert Markdown to HTML with extensions
    # 'tables' for tables formatting, 'fenced_code' for code blocks
    html_body = markdown.markdown(
        combined_markdown, 
        extensions=['tables', 'fenced_code', 'codehilite']
    )
    
    # Modify PAGE BREAK HTML comments to a div that CSS can break page on
    html_body = html_body.replace("<!-- PAGE BREAK -->", '<div class="page-break"></div>')
    
    # Wrap in full HTML document with styles
    full_html = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Dokumentasi Lengkap Sanctuary Defense</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #1a1a1a;
            background-color: #ffffff;
            margin: 0;
            padding: 0;
            font-size: 11pt;
        }}

        @page {{
            size: A4;
            margin: 2.5cm 2cm 2.5cm 2cm;
        }}

        .page-break {{
            page-break-before: always;
        }}

        /* Cover Page Styling */
        .cover-page {{
            height: 90vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding-top: 4cm;
            page-break-after: always;
        }}

        .cover-title {{
            font-size: 32pt;
            font-weight: 800;
            color: #1e293b;
            margin-bottom: 15px;
            letter-spacing: -0.5px;
        }}

        .cover-subtitle {{
            font-size: 18pt;
            color: #475569;
            margin-bottom: 40px;
            font-weight: 400;
        }}

        .cover-divider {{
            width: 150px;
            height: 4px;
            background: #3b82f6;
            margin: 20px auto;
            border-radius: 2px;
        }}

        .cover-meta {{
            font-size: 12pt;
            color: #64748b;
            margin-top: 5cm;
            line-height: 1.8;
        }}

        .cover-meta p {{
            margin: 5px 0;
            text-align: center;
        }}

        /* Document Body Styling */
        h1 {{
            page-break-before: always;
            font-size: 22pt;
            color: #0f172a;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 8px;
            margin-top: 0;
            margin-bottom: 20px;
            font-weight: 700;
        }}

        /* First h1 after cover shouldn't force extra page break */
        .cover-page + * + h1,
        .cover-page + h1 {{
            page-break-before: avoid;
        }}

        h2 {{
            page-break-after: avoid;
            font-size: 16pt;
            color: #1e293b;
            margin-top: 35px;
            margin-bottom: 15px;
            border-bottom: 1px solid #f1f5f9;
            padding-bottom: 6px;
            font-weight: 600;
        }}

        h3 {{
            page-break-after: avoid;
            font-size: 13pt;
            color: #334155;
            margin-top: 25px;
            margin-bottom: 10px;
            font-weight: 600;
        }}

        p, li {{
            font-size: 11pt;
            color: #334155;
            text-align: justify;
        }}

        li {{
            margin-bottom: 6px;
        }}

        ul, ol {{
            margin-top: 10px;
            margin-bottom: 15px;
            padding-left: 25px;
        }}

        a {{
            color: #2563eb;
            text-decoration: none;
        }}

        pre {{
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 12px 16px;
            font-family: 'Fira Code', 'Courier New', Courier, monospace;
            font-size: 9.5pt;
            overflow-x: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
            page-break-inside: avoid;
            margin-top: 15px;
            margin-bottom: 15px;
        }}

        code {{
            font-family: 'Fira Code', 'Courier New', Courier, monospace;
            background-color: #f1f5f9;
            padding: 2px 5px;
            border-radius: 4px;
            font-size: 9.5pt;
            color: #0f172a;
        }}

        pre code {{
            background-color: transparent;
            padding: 0;
            border-radius: 0;
            color: #334155;
            font-size: 9pt;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            margin-bottom: 20px;
            page-break-inside: avoid;
        }}

        th, td {{
            border: 1px solid #e2e8f0;
            padding: 10px 14px;
            text-align: left;
            font-size: 10pt;
        }}

        th {{
            background-color: #f8fafc;
            font-weight: 600;
            color: #1e293b;
        }}

        tr:nth-child(even) {{
            background-color: #fdfdfd;
        }}

        blockquote {{
            border-left: 4px solid #3b82f6;
            background-color: #f8fafc;
            padding: 12px 20px;
            margin-left: 0;
            margin-right: 0;
            margin-top: 15px;
            margin-bottom: 15px;
            page-break-inside: avoid;
        }}

        blockquote p {{
            margin: 0;
            color: #475569;
            font-style: italic;
        }}

        img {{
            max-width: 90%;
            max-height: 8cm;
            height: auto;
            display: block;
            margin: 25px auto;
            page-break-inside: avoid;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
        }}

        hr {{
            border: 0;
            border-top: 1px solid #e2e8f0;
            margin: 30px 0;
        }}
    </style>
</head>
<body>
    {html_body}
</body>
</html>
"""

    # Save compilation to temporary HTML
    with open(html_output_path, "w", encoding="utf-8") as f:
        f.write(full_html)
        
    print(f"Temporary HTML generated at: {html_output_path}")

    # Convert HTML to PDF using LibreOffice headless
    libreoffice_bin = "/usr/bin/libreoffice"
    if not os.path.exists(libreoffice_bin):
        # Fallback to path lookup
        libreoffice_bin = "libreoffice"
        
    print("Converting HTML to PDF via LibreOffice...")
    import tempfile
    with tempfile.TemporaryDirectory() as temp_profile_dir:
        profile_url = "file://" + temp_profile_dir.replace('\\', '/')
        cmd = [
            libreoffice_bin,
            f"-env:UserInstallation={profile_url}",
            "--headless",
            "--convert-to",
            "pdf",
            html_output_path,
            "--outdir",
            docs_dir
        ]
        
        try:
            result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print("LibreOffice output:", result.stdout)
        except subprocess.CalledProcessError as e:
            print("Error during LibreOffice conversion:")
            print(e.stderr)
            sys.exit(1)
        
    # LibreOffice output filename matches input filename base, i.e., "all_docs.pdf"
    generated_pdf = os.path.join(docs_dir, "all_docs.pdf")
    if os.path.exists(generated_pdf):
        if os.path.exists(pdf_output_path):
            os.remove(pdf_output_path)
        os.rename(generated_pdf, pdf_output_path)
        print(f"Success! PDF created at: {pdf_output_path}")
    else:
        print("Error: Output PDF file not found after conversion.")
        sys.exit(1)

    # Clean up temporary HTML file
    if os.path.exists(html_output_path):
        os.remove(html_output_path)
        print("Cleaned up temporary HTML file.")

if __name__ == "__main__":
    compile_docs()
