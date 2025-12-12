from flask import Flask, render_template, request, redirect, url_for
import math

app = Flask(__name__)

# ===== CONFIGURATION VARIABLES =====
# Change these values to customize your donut chart
CURRENT_VALUE = 4.3  # Current completion value
MAX_VALUE = 5.0  # Maximum value (denominator)
COMPLETED_COLOR = "#00D2FF"  # Color for completed portion (cyan/blue)
INCOMPLETE_COLOR = "#FF6E64"  # Color for incomplete portion (coral/red)
TEXT_COLOR = "#2d3748"  # Color for center text (dark gray, change to #FFFFFF for white)
CHART_TYPE = "donut"  # Chart type: "donut" or "battery"
FONT_SIZE = 48  # Default font size in pixels

# Number formatting defaults
NUMBER_FORMAT = "general"  # one of: general, number, percentage, currency, custom
DECIMAL_PLACES = 1  # clamp between 0-4
USE_THOUSANDS = False
CURRENCY_SYMBOL = "$"
# ===================================


def clamp_decimals(value: int, minimum: int = 0, maximum: int = 4) -> int:
    """Clamp decimal places to a safe range."""
    return max(minimum, min(maximum, value))


def sanitize_currency_symbol(symbol: str, fallback: str = "$") -> str:
    """Use the first 3 printable characters for currency; fallback if empty."""
    clean = (symbol or "").strip()
    return clean[:3] if clean else fallback


def format_number(value, number_format, decimals, use_thousands, currency_symbol, as_percentage=False):
    """Format a numeric value according to the selected number format."""
    try:
        num = float(value)
    except (TypeError, ValueError):
        return str(value)

    decimals = clamp_decimals(decimals)
    base_pattern = f"{{:,.{decimals}f}}" if use_thousands else f"{{:.{decimals}f}}"

    if number_format == "percentage":
        display_value = num * 100 if as_percentage else num
        return f"{base_pattern.format(display_value)}%"
    if number_format == "currency":
        return f"{currency_symbol}{base_pattern.format(num)}"
    # Treat general/custom similarly to number for now
    return base_pattern.format(num)


@app.route('/')
def index():
    """Render the main page with the donut chart."""

    if MAX_VALUE > 0:
        completion_ratio = CURRENT_VALUE / MAX_VALUE
        percentage = completion_ratio * 100
    else:
        completion_ratio = 0
        percentage = 0

    clamped_ratio = max(0, min(completion_ratio, 1))
    radius = 90
    circumference = 2 * math.pi * radius
    completed_length = circumference * clamped_ratio

    formatted_current = format_number(
        CURRENT_VALUE, NUMBER_FORMAT, DECIMAL_PLACES, USE_THOUSANDS, CURRENCY_SYMBOL
    )
    formatted_max = format_number(
        MAX_VALUE, NUMBER_FORMAT, DECIMAL_PLACES, USE_THOUSANDS, CURRENCY_SYMBOL
    )
    formatted_completion = f"{percentage:.{clamp_decimals(DECIMAL_PLACES)}f}%"

    chart_data = {
        "current": CURRENT_VALUE,
        "max": MAX_VALUE,
        "percentage": percentage,
        "completed_length": completed_length,
        "circumference": circumference,
        "completed_color": COMPLETED_COLOR,
        "incomplete_color": INCOMPLETE_COLOR,
        "text_color": TEXT_COLOR,
        "chart_type": CHART_TYPE,
        "font_size": FONT_SIZE,
        "number_format": NUMBER_FORMAT,
        "decimal_places": DECIMAL_PLACES,
        "use_thousands": USE_THOUSANDS,
        "currency_symbol": CURRENCY_SYMBOL,
        "formatted_current": formatted_current,
        "formatted_max": formatted_max,
        "formatted_completion": formatted_completion,
    }

    return render_template("index.html", data=chart_data)


@app.route('/update', methods=['POST'])
def update():
    """Update chart values via form submission."""
    global CURRENT_VALUE, MAX_VALUE, COMPLETED_COLOR, INCOMPLETE_COLOR, TEXT_COLOR
    global CHART_TYPE, FONT_SIZE, NUMBER_FORMAT, DECIMAL_PLACES, USE_THOUSANDS, CURRENCY_SYMBOL

    try:
        CURRENT_VALUE = float(request.form.get("current", CURRENT_VALUE))
        MAX_VALUE = float(request.form.get("max", MAX_VALUE))
        COMPLETED_COLOR = request.form.get("completed_color", COMPLETED_COLOR)
        INCOMPLETE_COLOR = request.form.get("incomplete_color", INCOMPLETE_COLOR)
        TEXT_COLOR = request.form.get("text_color", TEXT_COLOR)
        CHART_TYPE = request.form.get("chart_type", CHART_TYPE)
        FONT_SIZE = int(request.form.get("font_size", FONT_SIZE))
        NUMBER_FORMAT = request.form.get("number_format", NUMBER_FORMAT)
        DECIMAL_PLACES = clamp_decimals(int(request.form.get("decimal_places", DECIMAL_PLACES)))
        USE_THOUSANDS = request.form.get("use_thousands") == "on"
        CURRENCY_SYMBOL = sanitize_currency_symbol(request.form.get("currency_symbol", CURRENCY_SYMBOL))
    except ValueError:
        pass  # Keep old values if conversion fails

    return redirect(url_for("index"))


if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
