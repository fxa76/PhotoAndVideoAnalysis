from flask import Flask


class HealthCheckServer :

    app = Flask(__name__,)

    @app.route('/')
    def index(self):
        return "Analysis engine console"

    @app.route('/health')
    def health(self):
        return ''

    def server_start(self):
        self.app.run(debug=True, host="0.0.0.0", port=6000)
