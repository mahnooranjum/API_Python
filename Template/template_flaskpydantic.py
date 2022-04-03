"""
Created on Sun Apr  3 05:04:41 2022

@author: MAQ
"""
'''
    Install pydantic, Flask-Pydantic, Flask
'''
from flask import Flask
from pydantic import BaseModel
from pydantic.typing import Optional
from flask_pydantic import validate

app = Flask(__name__)


class Paths(BaseModel):
    path_ref: str
    cuts: Optional[int] = 30
    # rating: Optional[int] = None


@app.route("/api/func", methods=["POST"])
@validate()
def call_func(body: Paths):
    return func(body.path_ref)


if __name__ == "__main__":
    app.run(port=5500)