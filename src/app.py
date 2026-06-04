from flask import Flask
from src.models import Base, engine

app = Flask(__name__)

Base.metadata.create_all(engine)

if __name__ == '__main__':  
    app.run(debug=True)