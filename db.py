import threading
import time
import random
import json
import os
from datetime import datetime, timezone
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.management.base import BaseCommand
from django.conf import settings
from django.apps import AppConfig
from django.utils.timezone import now as django_now

# Global variables
live_data_lock = threading.Lock()
buffer_lock = threading.Lock()
monthly_data_lock = threading.Lock()

current_value = 0.0
voltage_value = 0.0
buffer = []

MONTHLY_DATA_FILE = os.path.join(settings.BASE_DIR, 'monthly_data.json')

def load_monthly_data():
    if os.path.exists(MONTHLY_DATA_FILE):
        with open(MONTHLY_DATA_FILE, 'r') as f:
            return json.load(f)
    return {
        'current': {'total_kwh': 0.0, 'month': None, 'year': None},
        'previous': {'total_kwh': 0.0, 'month': None, 'year': None},
        'history': {}
    }

def save_monthly_data():
    try:
        with open(MONTHLY_DATA_FILE, 'w') as f:
            json.dump(monthly_data, f)
    except Exception as e:
        print(f"Error saving data: {str(e)}")

monthly_data = load_monthly_data()

def generate_live_values():
    while True:
        current = random.uniform(0, 30)
        voltage = random.uniform(220, 240)
        with live_data_lock:
            global current_value, voltage_value
            current_value = current
            voltage_value = voltage
        with buffer_lock:
            buffer.append((current, voltage))
        time.sleep(1)

def calculate_monthly_usage():
    while True:
        time.sleep(60)
        now = datetime.now(timezone.utc)
        current_year = now.year
        current_month = now.month
        with buffer_lock:
            if not buffer:
                continue
            readings = buffer.copy()
            buffer.clear()
        if readings:
            avg_current = sum(c for c, _ in readings) / len(readings)
            avg_voltage = sum(v for _, v in readings) / len(readings)
            energy_kwh = (avg_current * avg_voltage) * (1/60) / 1000
            with monthly_data_lock:
                if monthly_data['current']['month'] != current_month:
                    if monthly_data['current']['month']:
                        year_key = str(monthly_data['current']['year'])
                        monthly_data['history'].setdefault(year_key, {})[
                            str(monthly_data['current']['month'])] = monthly_data['current']['total_kwh']
                    monthly_data['previous'] = monthly_data['current'].copy()
                    monthly_data['current'] = {
                        'total_kwh': energy_kwh,
                        'month': current_month,
                        'year': current_year
                    }
                else:
                    monthly_data['current']['total_kwh'] += energy_kwh
                save_monthly_data()

@csrf_exempt
def stream(request):
    def event_stream():
        while True:
            with live_data_lock:
                current = current_value
                voltage = voltage_value
            data = {
                'current': round(current, 2),
                'voltage': round(voltage, 2),
                'power': round(current * voltage, 2),
                'timestamp': django_now().isoformat()
            }
            yield f"data: {json.dumps(data)}\n\n"
            time.sleep(1)
    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')

def monthly_usage(request):
    now = datetime.now(timezone.utc)
    current_month = now.month
    with monthly_data_lock:
        monthly_usage = [
            round(random.uniform(5, 15), 2) if m < current_month-1 else 0.0 
            for m in range(12)
        ]
        monthly_usage[current_month-1] = round(
            monthly_data['current']['total_kwh'], 2
        )
        return JsonResponse({
            "current_month": monthly_data['current'],
            "monthly_usage": monthly_usage,
            "difference": round(monthly_data['current']['total_kwh'] - monthly_data['previous']['total_kwh'], 2)
        })

class BackgroundThreadCommand(BaseCommand):
    def handle(self, *args, **options):
        threading.Thread(target=generate_live_values, daemon=True).start()
        threading.Thread(target=calculate_monthly_usage, daemon=True).start()

class PowerMonitorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'power_monitor'
    def ready(self):
        threading.Thread(target=generate_live_values, daemon=True).start()
        threading.Thread(target=calculate_monthly_usage, daemon=True).start()