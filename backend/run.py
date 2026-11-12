from app import create_app
from app.extensions import socketio

app = create_app()

if __name__ == "__main__":
    # 用 socketio.run 才能处理 /socket.io 的轮询与 WebSocket 协商；
    # 关闭 reloader 保持单进程，避免长连接在进程重启时被断开。
    socketio.run(
        app,
        host="127.0.0.1",
        port=5000,
        debug=True,
        use_reloader=False,
        allow_unsafe_werkzeug=True,
    )
