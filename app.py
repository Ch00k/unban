from flask import Flask, request, render_template, redirect

from f2b_client import unban_ip, find_banned_ip


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def unban():
    if request.method == 'GET':
        ip = request.remote_addr
        ip = '149.154.157.239'
        banned_in_jails = find_banned_ip(ip)
        if banned_in_jails:
            return render_template('unban.html', ip=ip, jails=banned_in_jails)
        else:
            return "{0} is not banned".format(ip), 200
    elif request.method == 'POST':
        unban_ip(request.form['jails'], request.form['ip'])
        return redirect('/')


if __name__ == '__main__':
    app.run()
