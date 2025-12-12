# Donut Chart Generator

A simple web application to create customizable donut charts for completion ratios.

## Features

- ✅ Customizable completion values (supports 2 decimal places)
- ✅ Adjustable colors for completed and incomplete portions
- ✅ Editable text color for center numbers
- ✅ Download as transparent PNG (perfect for PowerPoint)
- ✅ Vertical orientation (starts from top)

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
python app.py
```

3. Open your browser to: `http://localhost:5000`

## Usage

1. Enter your current value and maximum value
2. Choose your colors (completed, incomplete, and text)
3. Click "Update Chart"
4. Download as PNG for use in presentations

## Project structure

- `app.py`: Minimal Flask server with two routes (`/` to render the chart UI, `/update` to accept form submissions and refresh the page).
- `static/style.css`: Styling for the chart, form controls, and layout.
- `templates/`: Expected location for `index.html`; currently empty (see Known gaps).
- `requirements.txt`: Python dependencies (only Flask).

## How it works

- **Configuration**: The top of `app.py` defines defaults for the current value, max value, colors, chart type (`donut` or `battery`), and font size. These globals are read on every request.
- **Rendering**: The `/` route builds a `chart_data` dictionary with the computed percentage and degrees for the completed arc, then passes it to `templates/index.html` as `data`.
- **Updating**: The `/update` POST route reads values from an HTML form, updates the globals (falling back to previous values on conversion errors), and redirects to `/` so the new chart renders.
- **Styling**: `static/style.css` defines the gradient background, glassmorphism container, SVG sizing, typography, inputs, and button states to keep the chart visually centered on the page.
- **Serving**: When run directly (`python app.py`), Flask starts on `0.0.0.0` using the `PORT` env var or default `5000`, with debug disabled.

## Extending or customizing

- Adjust the defaults in `app.py` to change initial values or color presets before starting the server.
- Add validation in `/update` if you want to reject invalid ranges instead of silently keeping the prior values.
- Implement a JSON API (e.g., a `/data` route) if you want to drive the chart from other services instead of HTML form posts.
- Swap the font or color scheme by editing `static/style.css`; layout is responsive down to ~320px widths.

## Known gaps / issues

- `templates/index.html` is missing. The Flask app will 500 on `/` without a template; add it under `templates/` with the form fields expected by `/update` (`current`, `max`, `completed_color`, `incomplete_color`, `text_color`, `chart_type`, `font_size`).
- `app.py` repeats imports and configuration variables at the top; cleaning that duplication will make the file clearer.

## Deployment

This app is ready to deploy to Render, Railway, or any Python hosting platform.

See `DEPLOYMENT_GUIDE.md` for detailed instructions.

## License

Free to use for your team!
