from flask import Flask, request
from flask import render_template
from hashlib import md5
from blockchain import pymongo_func

app = Flask(__name__)


def check_hashes(hashes):
    res = []
    for h in hashes:
        error = False
        if md5(h.encode('utf8')).hexdigest()[:4] == '1008':
            uid, rest = h.split('-', maxsplit=1)
            if not uid.isdigit() or not pymongo_func.check(rest):
                error = True
            pymongo_func.add_coin(uid, rest)
        else:
            error = True
        res.append((h, error))
    return res


@app.route("/", methods=["GET", "POST"])
def index():
    result = []
    if request.method == "POST":
        hashes = request.form["hashes"].strip().split()
        result = check_hashes(hashes)
    return render_template("index.html", res=result)


if __name__ == "__main__":
    app.run(host="localhost", port=8080)

