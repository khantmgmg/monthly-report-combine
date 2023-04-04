from flask import Flask
import script
import time
import threading

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

def run_script():
    while True:
        script.main()
        time.sleep(1800)  # sleep for 10 minutes

if __name__ == '__main__':
    bg_thread = threading.Thread(target=run_script, daemon=True)
    bg_thread.start()

    app.run(host='0.0.0.0', port=8080)
