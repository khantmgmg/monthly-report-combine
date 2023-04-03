from flask import Flask
import script
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(func=script.main, trigger='interval', minutes=10)
scheduler.start()

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()
