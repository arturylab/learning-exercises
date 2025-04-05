from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import paramiko

app = Flask(__name__)
socketio = SocketIO(app)

clients = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect_ssh')
def connect_ssh(data):
    """Establece conexión SSH"""
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=data['host'],
            username=data['user'],
            password=data['password'],
            port=22
        )
        clients[request.sid] = ssh
        emit('message', 'Conectado al servidor SSH')
    except Exception as e:
        emit('message', f'Error: {str(e)}')

@socketio.on('execute_command')
def execute_command(data):
    """Ejecuta un comando y envía la salida"""
    ssh = clients.get(request.sid)
    if ssh:
        stdin, stdout, stderr = ssh.exec_command(data['command'])
        output = stdout.read().decode() + stderr.read().decode()
        emit('message', output)

@socketio.on('disconnect_ssh')
def disconnect_ssh():
    """Cierra la conexión SSH del usuario"""
    ssh = clients.pop(request.sid, None)
    if ssh:
        ssh.close()
    emit('message', 'Conexión SSH cerrada.')


if __name__ == '__main__':
    socketio.run(app, debug=True)
