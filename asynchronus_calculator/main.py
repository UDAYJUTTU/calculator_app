from flask import Flask
from flask_socketio import SocketIO, send
from flask import render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'calappsecret_key'
socketio = SocketIO(app, cors_allowed_origins='*')

def eval_math_expr(expr):
	try:
		result=eval(expr)
		return result
	except ZeroDivisionError:
		return "cannot be divided"

queue=[]
@socketio.on('message')
def handleMessage(msg):
    if msg != 'User has connected!':
        queue.append(msg + ' = ' + str(eval_math_expr(msg))+" ")
        if len(queue) >10:
            queue.pop(0)
        send(queue, broadcast=True)

@app.route('/')
def index():
	if queue:
		return render_template('index.html',value=queue)
	return render_template('index.html')

if __name__ == '__main__':
	socketio.run(app)