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
from flask import Flask, render_template, request, redirect, url_for
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
FONT_SIZE = 48  # Default font size in pixels
# ===================================

@app.route('/')
def index():
    """Render the main page with the donut chart"""
    
    chart_data = {
        'current': CURRENT_VALUE,
        'max': MAX_VALUE,
        'percentage': (CURRENT_VALUE / MAX_VALUE) * 100 if MAX_VALUE > 0 else 0,
        'completed_degrees': (CURRENT_VALUE / MAX_VALUE) * 360 if MAX_VALUE > 0 else 0,
        'completed_color': COMPLETED_COLOR,
        'incomplete_color': INCOMPLETE_COLOR,
        'text_color': TEXT_COLOR,
        'chart_type': CHART_TYPE,
        'font_size': FONT_SIZE
    }
    
    return render_template('index.html', data=chart_data)

@app.route('/update', methods=['POST'])
def update():
    """Update chart values via form submission"""
    global CURRENT_VALUE, MAX_VALUE, COMPLETED_COLOR, INCOMPLETE_COLOR, TEXT_COLOR, CHART_TYPE, FONT_SIZE
    
    try:
        CURRENT_VALUE = float(request.form.get('current', CURRENT_VALUE))
        MAX_VALUE = float(request.form.get('max', MAX_VALUE))
        COMPLETED_COLOR = request.form.get('completed_color', COMPLETED_COLOR)
        INCOMPLETE_COLOR = request.form.get('incomplete_color', INCOMPLETE_COLOR)
        TEXT_COLOR = request.form.get('text_color', TEXT_COLOR)
        CHART_TYPE = request.form.get('chart_type', CHART_TYPE)
        FONT_SIZE = int(request.form.get('font_size', FONT_SIZE))
    except ValueError:
        pass  # Keep old values if conversion fails
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
