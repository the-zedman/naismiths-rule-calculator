import re
import datetime
from collections import Counter
import json
import os
import socket

# Log file path
log_file_path = "/var/log/apache2/naismithsrule.com_access.log"

# Read and parse the log file
def parse_log(log_file_path):
    with open(log_file_path, "r") as f:
        logs = f.readlines()
    
    data = []
    for log in logs:
        match = re.match(r'(.*?) - - \[(.*?)\] "(.*?)" (.*?) (.*?)', log)
        if match:
            ip = match.group(1)
            datetime_str = match.group(2)
            request = match.group(3)
            date_obj = datetime.datetime.strptime(datetime_str.split(':')[0], "%d/%b/%Y")
            path = re.search(r'GET /(.*?) HTTP', request)
            if path:
                page = path.group(1) or "index.html"  # Treat / as index.html
                data.append({
                    "ip": ip,
                    "datetime": date_obj,
                    "page": page
                })
    return data

# Process data
def process_data(data):
    # Define the pages to track
    relevant_pages = {"index.html", "privacy-policy.html", "about.html"}

    # Filter the data to include only relevant pages
    filtered_data = [entry for entry in data if entry['page'] in relevant_pages]

    total_visits = len(filtered_data)
    unique_visitors = len(set(entry['ip'] for entry in filtered_data))
    visits_per_page = Counter(entry['page'] for entry in filtered_data)
    visits_by_hour = Counter(entry['datetime'].hour for entry in filtered_data if entry['datetime'].date() == datetime.datetime.today().date())
    visits_by_day = Counter(entry['datetime'].date() for entry in filtered_data if (datetime.datetime.today().date() - entry['datetime'].date()).days < 7)
    visits_by_day_month = Counter(entry['datetime'].day for entry in filtered_data if entry['datetime'].month == datetime.datetime.today().month)
    visits_by_month = Counter(entry['datetime'].month for entry in filtered_data if entry['datetime'].year == datetime.datetime.today().year)

    return {
        "total_visits": total_visits,
        "unique_visitors": unique_visitors,
        "visits_per_page": visits_per_page,
        "visits_by_hour": visits_by_hour,
        "visits_by_day": visits_by_day,
        "visits_by_day_month": visits_by_day_month,
        "visits_by_month": visits_by_month,
        "ip_visits": Counter(entry['ip'] for entry in filtered_data)
    }

# Generate HTML
def generate_html(data):
    # Get the current date and time for the timestamp
    generated_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Resolve IPs to domains where possible and count visits per IP
    resolved_ips = {}
    for ip in data['ip_visits'].keys():
        try:
            resolved_ips[ip] = socket.gethostbyaddr(ip)[0]  # Resolve to domain
        except socket.herror:
            resolved_ips[ip] = ip  # Fallback to IP if resolution fails

    # Sort IP visits by highest number of visits
    sorted_ip_visits = sorted(data['ip_visits'].items(), key=lambda x: x[1], reverse=True)

    # Convert keys to strings for JSON serialization
    visits_by_day_keys = [str(k) for k in sorted(data['visits_by_day'].keys())]
    visits_by_day_month_keys = [str(k) for k in sorted(data['visits_by_day_month'].keys())]
    visits_by_month_keys = [str(k) for k in sorted(data['visits_by_month'].keys())]
    visits_by_hour_keys = sorted(data['visits_by_hour'].keys())
    visits_by_hour_values = [data['visits_by_hour'][hour] for hour in visits_by_hour_keys]

    # Begin HTML
    html = f"""
    <html>
    <head>
        <title>Web Logs</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body>
        <h1>Web Logs</h1>
        <p><em>Generated on: {generated_time}</em></p>
        <p>Total Visitors: {data['total_visits']}</p>
        <p>Unique Visitors: {data['unique_visitors']}</p>
        <h2>Visits per Page</h2>
        <ul>
    """
    for page, count in data['visits_per_page'].items():
        percentage = (count / data['total_visits']) * 100
        html += f"<li>{page}: {count} visits ({percentage:.2f}%)</li>"

    # Add the charts
    html += """
        </ul>
        <h2>Visits by Hour (Today)</h2>
        <canvas id="hourChart"></canvas>
        <script>
            new Chart(document.getElementById('hourChart'), {
                type: 'bar',
                data: {
                    labels: """ + json.dumps(visits_by_hour_keys) + """,
                    datasets: [{
                        label: 'Visits',
                        data: """ + json.dumps(visits_by_hour_values) + """,
                    }]
                },
                options: {
                    scales: {
                        x: { title: { display: true, text: 'Hour of Day' } },
                        y: { title: { display: true, text: 'Number of Visits' } }
                    }
                }
            });
        </script>
        <h2>Visits by IP Address</h2>
        <table border="1">
            <tr>
                <th>IP Address / Domain</th>
                <th>Number of Visits</th>
            </tr>
    """
    for ip, visits in sorted_ip_visits:
        resolved = resolved_ips[ip]
        html += f"<tr><td>{resolved}</td><td>{visits}</td></tr>"

    html += """
        </table>
    </body>
    </html>
    """
    return html

# Main execution
log_data = parse_log(log_file_path)
processed_data = process_data(log_data)
html_content = generate_html(processed_data)

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
output_file_path = os.path.join(script_dir, "weblogs.html")

# Save the HTML file
with open(output_file_path, "w") as f:
    f.write(html_content)

# Set the correct permissions for the file
os.chmod(output_file_path, 0o755)

print(f"weblogs.html has been successfully created in: {output_file_path}")
