import os
import requests
import psycopg2
from datetime import time
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
def get_conn():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    print(conn)
    return conn
