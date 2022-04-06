from nerv.routes import create_app
from nerv.app1 import test
from flask import Flask

# app = create_app(r"C:\Users\Arman\Desktop\nerv\nerv\data\exp1")
app = test(r"C:\Users\Arman\Desktop\nerv\nerv\data", Flask(__name__))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
