from flask import Flask, request
from flask import render_template
from hashlib import md5
import pymongo_func

app = Flask(__name__)


def check_hashes(hashes):
    res = []
    for h in hashes:
        error = True
        ha = h.split('-', maxsplit=1)
        if len(ha) == 2:
            if md5(ha[1].encode('utf8')).hexdigest()[:3] == '666':
                uid, rest = ha[0], ha[1]
                if uid.isdigit() and not pymongo_func.check(rest):
                    pymongo_func.add_coin(uid, rest)
                else:
                    error = False
            else:
                error = False
        res.append((h, error))
    return res


@app.route("/", methods=["GET", "POST"])
def index():
    result = []
    if request.method == "POST":
        hashes = request.form["hashes"].strip().split()
        result = check_hashes(hashes)
    return render_template("index.html", res=result)


@app.route("/wallet")
def wallet():
    result = None
    balance = request.args.get("wallet")
    if balance:
        if balance.strip().isdigit():
            result = pymongo_func.get_balance(balance)
        else:
            result = "Вы ввели неверный id"
    return render_template("wallet.html", res=result)


@app.route("/send", methods=["GET", "POST"])
def send():
    result = None
    if request.method == "POST":
        from_id = request.form["from_id"].strip().split()
        to_id = request.form["to_id"].strip().split()
        coin_id = request.form["money"].strip().split()
        result = pymongo_func.transfer(from_id, to_id, coin_id)
    return render_template("send.html", res=result)


@app.route("/top")
def top():
    result = pymongo_func.get_top()
    return render_template("top.html", res=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

