from flask import Flask, request, redirect
import redis

app = Flask(__name__)
r = redis.StrictRedis(host='redis', port=6379, decode_responses=True)

@app.route('/', methods=['GET', 'POST'])
def guestbook():
    if request.method == 'POST':
        message = request.form.get('message')
        if message:
            r.rpush("messages", message)
        return redirect('/')  # Refresh page after POST

    # Get last 10 messages
    messages = r.lrange("messages", -10, -1)
    messages.reverse()  # Show newest first

    html = "<h2>💬 Guestbook</h2><form method='POST'>"
    html += "<input name='message' placeholder='Type a message' required>"
    html += "<button type='submit'>Submit</button></form><br>"

    for msg in messages:
        html += f"<p>• {msg}</p>"

    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

