from flask import Flask, Response, jsonify
import psutil
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Prometheus metrics
cpu_gauge = Gauge('cpu_percent', 'CPU usage percent')
memory_gauge = Gauge('memory_percent', 'Memory usage percent')
disk_gauge = Gauge('disk_percent', 'Disk usage percent')
net_sent_gauge = Gauge('network_bytes_sent', 'Total network bytes sent (KB)')
net_recv_gauge = Gauge('network_bytes_recv', 'Total network bytes received (KB)')
health_gauge = Gauge('container_health', '1=Healthy, 0=Unhealthy')

@app.route("/")
def home():
    return jsonify({"message": "System Monitor Running"})

@app.route("/metrics")
def metrics():

    # Create Percentages
    cpu = psutil.cpu_percent(interval=0)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    net_io = psutil.net_io_counters()

    # Update gauges
    cpu_gauge.set(cpu)
    memory_gauge.set(memory)
    disk_gauge.set(disk)
    net_sent_gauge.set(net_io.bytes_sent / 1024)   
    net_recv_gauge.set(net_io.bytes_recv / 1024)

    # Define conditions for a Healthy System
    if cpu >= 80 or memory >= 80 or disk >= 80:
        health_gauge.set(0)  # Poor
    elif cpu >= 60 or memory >= 60 or disk >= 60:
        health_gauge.set(1)  # Okay
    else:
        health_gauge.set(2)  # Good
    
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)