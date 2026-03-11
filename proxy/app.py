from flask import Flask, request, jsonify
import redis
import requests
import os
import yaml

config_path = os.getenv("CONFIG_PATH", "/etc/cache-api/config.yaml")

try:
    with open(config_path, "r") as f:
        config = yaml.safe_load(f) or {}
except FileNotFoundError:
    config = {}

REDIS_HOST = os.getenv("REDIS_HOST", config.get("redis", {}).get("host", "127.0.0.1"))
REDIS_PORT = int(os.getenv("REDIS_PORT", config.get("redis", {}).get("port", 6379)))

BACKEND_HOST = os.getenv("BACKEND_HOST", config.get("backend", {}).get("host", "46.247.41.229"))
BACKEND_PORT = int(os.getenv("BACKEND_PORT", config.get("backend", {}).get("port", 8080)))

APP_PORT = int(os.getenv("APP_PORT", config.get("app", {}).get("port", 5000)))

app = Flask(__name__)
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

@app.route("/user")
def get_user():
    user_id = request.args.get("id")

    if not user_id:
        return jsonify({"error": "id is required"}), 400

    cached = r.get(user_id)
    if cached:
        return jsonify({"cached": True, "user": eval(cached)})

    resp = requests.get(f"http://{BACKEND_HOST}:{BACKEND_PORT}/user?id={user_id}")

    if resp.status_code == 200:
        r.set(user_id, resp.text, ex=60)
        return jsonify({"cached": False, "user": resp.json()})

    return resp.text, resp.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=APP_PORT)