"""Read-only portfolio dashboard (fictional demo app)."""

import os

import boto3
import requests
from flask import Flask, jsonify

app = Flask(__name__)
s3 = boto3.client("s3")

REPORT_BUCKET = os.environ.get("REPORT_BUCKET", "demo-portfolio-reports")
PORTFOLIO_API = os.environ.get("PORTFOLIO_API_URL", "https://portfolio.internal.example.com/v1")


@app.get("/summary")
def summary():
    obj = s3.get_object(Bucket=REPORT_BUCKET, Key="summary.json")
    return jsonify(obj["Body"].read().decode())


@app.get("/positions")
def positions():
    resp = requests.get(f"{PORTFOLIO_API}/positions", timeout=10)
    return jsonify(resp.json())


@app.get("/reports")
def reports():
    listing = s3.list_objects_v2(Bucket=REPORT_BUCKET)
    return jsonify([o["Key"] for o in listing.get("Contents", [])])
