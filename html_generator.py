import os
from datetime import datetime

async def generate_transcript(channel):
    messages = []
    async for message in channel.history(limit=None, oldest_first=True):
        messages.append({
            "author": str(message.author),
            "content": message.content,
            "timestamp": message.created_at.isoformat()
        })

    os.makedirs("transcripts", exist_ok=True)
    ticket_id = channel.name.split("-")[-1]

    html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Transcription Ticket #{ticket_id}</title>
<style>
body {{ font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px; }}
.message {{ margin-bottom: 15px; padding: 10px; border-bottom: 1px solid #ccc; }}
.author {{ font-weight: bold; color: #333; }}
.timestamp {{ color: #888; font-size: 0.9em; }}
.content {{ margin-top: 5px; }}
</style>
</head>
<body>
<h2>Transcription du ticket #{ticket_id}</h2>
<hr />
"""

    for msg in messages:
        if not msg["content"]:
            continue
        timestamp = datetime.fromisoformat(msg["timestamp"]).strftime('%d/%m/%Y %H:%M:%S')
        author = msg["author"]
        content = msg["content"].replace("\n", "<br>")
        html_content += f"""
<div class="message">
<div class="author">{author}</div>
<div class="timestamp">{timestamp}</div>
<div class="content">{content}</div>
</div>
"""

    html_content += "</body></html>"

    filepath = f"transcripts/ticket_{ticket_id}.html"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)

    return filepath
