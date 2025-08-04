def generate_html_transcript(messages: list, filename: str):
    html_content = "<html><body><h1>Transcript</h1><ul>"
    for msg in messages:
        html_content += f"<li><strong>{msg.author.display_name}:</strong> {msg.content}</li>"
    html_content += "</ul></body></html>"

    with open(f"data/{filename}", "w", encoding="utf-8") as f:
        f.write(html_content)
