from flask import Flask
import script

app = Flask(__name__)

@app.route('/')
def hello():
    script.main()
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()
