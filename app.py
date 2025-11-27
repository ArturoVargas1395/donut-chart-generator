from flask import Flask, render_template, request
import json

app = Flask(__name__)

# ===== CONFIGURATION VARIABLES =====
# Change these values to customize your donut chart
CURRENT_VALUE = 4.3  # Current completion value
MAX_VALUE = 5.0      # Maximum value (denominator)
COMPLETED_COLOR = "#00D2FF"  # Color for completed portion (cyan/blue)
INCOMPLETE_COLOR = "#FF6E64"  # Color for incomplete portion (coral/red)
TEXT_COLOR = "#2d3748"  # Color for center text (dark gray, change to #FFFFFF for white)
CHART_TYPE = "donut"  # Chart type: "donut" or "battery"
# ===================================

@app.route('/')
def index():
    """Render the main page with the donut chart"""
    completion_percentage = (CURRENT_VALUE / MAX_VALUE) * 100
    completed_degrees = (CURRENT_VALUE / MAX_VALUE) * 360
    
    chart_data = {
        'current': CURRENT_VALUE,
        'max': MAX_VALUE,
        'percentage': completion_percentage,
        'completed_degrees': completed_degrees,
        'completed_color': COMPLETED_COLOR,
        'incomplete_color': INCOMPLETE_COLOR,
        'text_color': TEXT_COLOR,
        'chart_type': CHART_TYPE
    }
    
    return render_template('index.html', data=chart_data)

@app.route('/update', methods=['POST'])
def update():
    """Update chart values via form submission"""
    global CURRENT_VALUE, MAX_VALUE, COMPLETED_COLOR, INCOMPLETE_COLOR, TEXT_COLOR, CHART_TYPE
    
    CURRENT_VALUE = float(request.form.get('current', CURRENT_VALUE))
    MAX_VALUE = float(request.form.get('max', MAX_VALUE))
    COMPLETED_COLOR = request.form.get('completed_color', COMPLETED_COLOR)
    INCOMPLETE_COLOR = request.form.get('incomplete_color', INCOMPLETE_COLOR)
    TEXT_COLOR = request.form.get('text_color', TEXT_COLOR)
    CHART_TYPE = request.form.get('chart_type', CHART_TYPE)
    
    return index()

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

