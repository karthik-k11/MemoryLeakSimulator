
from flask import (
    Flask,
    abort,
    redirect,
    render_template,
    request,
    url_for,
)

from config import (
    DEFAULT_MEASUREMENT_INTERVAL,
    MAX_ITERATIONS,
    MAX_MEMORY_MB,
)
from database import (
    get_experiment,
    init_db,
    list_experiments,
    save_experiment,
)
from experiment_runner import run_experiment


def create_app(test_config=None):
    """Create and configure the Flask application."""

    app = Flask(__name__)
    app.config.update(
        DATABASE=None,
        MAX_CONTENT_LENGTH=1024 * 1024,
    )

    if test_config:
        app.config.update(test_config)

    database_path = app.config["DATABASE"]
    init_db(database_path)

    @app.get("/")
    def index():
        return render_template(
            "index.html",
            history=list_experiments(database_path, limit=10),
            max_iterations=MAX_ITERATIONS,
            default_interval=DEFAULT_MEASUREMENT_INTERVAL,
            error=None,
        )

    @app.post("/run")
    def run():
        workload = request.form.get("workload", "list")

        try:
            iterations = int(
                request.form.get("iterations", "10000")
            )
            interval = int(
                request.form.get(
                    "measurement_interval",
                    str(DEFAULT_MEASUREMENT_INTERVAL),
                )
            )

            result = run_experiment(
                workload=workload,
                iterations=iterations,
                measurement_interval=interval,
                max_memory_mb=MAX_MEMORY_MB,
            )

        except (ValueError, TypeError) as exc:
            return render_template(
                "index.html",
                history=list_experiments(database_path, limit=10),
                max_iterations=MAX_ITERATIONS,
                default_interval=DEFAULT_MEASUREMENT_INTERVAL,
                error=str(exc),
            ), 400

        experiment_id = save_experiment(
            result,
            iterations,
            interval,
            database_path,
        )

        return redirect(
            url_for("detail", experiment_id=experiment_id)
        )

    @app.get("/experiments/<int:experiment_id>")
    def detail(experiment_id):
        experiment = get_experiment(
            experiment_id,
            database_path,
        )

        if experiment is None:
            abort(404)

        chart = make_svg_chart(experiment["measurements"])

        return render_template(
            "detail.html",
            experiment=experiment,
            chart=chart,
        )

    return app


def make_svg_chart(measurements):
    """Create an SVG memory chart without an extra plotting dependency."""

    width, height = 760, 260
    left, right, top, bottom = 58, 20, 18, 42

    plot_width = width - left - right
    plot_height = height - top - bottom

    values = [
        float(item["memory_mb"])
        for item in measurements
    ]
    iterations = [
        int(item["iteration"])
        for item in measurements
    ]

    low = min(values)
    high = max(values)

    if high == low:
        high = low + 1.0

    max_iteration = max(iterations) or 1
    points = []

    for iteration, value in zip(iterations, values):
        x = left + (iteration / max_iteration) * plot_width
        y = top + ((high - value) / (high - low)) * plot_height
        points.append((x, y))

    polyline = " ".join(
        f"{x:.1f},{y:.1f}" for x, y in points
    )

    circles = "".join(
        (
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" '
            'fill="#2459d3"/>'
        )
        for x, y in points
    )

    grid_lines = []

    for index in range(3):
        y = top + index * plot_height / 2
        label = high - index * (high - low) / 2

        grid_lines.append(
            f'<line x1="{left}" y1="{y:.1f}" '
            f'x2="{width - right}" y2="{y:.1f}" '
            'stroke="#e4e8ef"/>'
        )
        grid_lines.append(
            f'<text x="{left - 10}" y="{y + 4:.1f}" '
            'text-anchor="end" font-size="11" '
            'fill="#657187">'
            f'{label:.1f}</text>'
        )

    return (
        f'<svg viewBox="0 0 {width} {height}" '
        'role="img" aria-label="Memory usage by iteration" '
        'xmlns="http://www.w3.org/2000/svg">'
        + "".join(grid_lines)
        + (
            f'<polyline points="{polyline}" fill="none" '
            'stroke="#2459d3" stroke-width="2.5" '
            'stroke-linejoin="round"/>'
        )
        + circles
        + (
            f'<text x="{left}" y="{height - 12}" '
            'font-size="11" fill="#657187">0</text>'
        )
        + (
            f'<text x="{width - right}" y="{height - 12}" '
            'text-anchor="end" font-size="11" fill="#657187">'
            f'{max(iterations)}</text>'
        )
        + (
            f'<text x="{width / 2}" y="{height - 1}" '
            'text-anchor="middle" font-size="11" '
            'fill="#657187">Iteration</text>'
        )
        + (
            f'<text x="14" y="{height / 2}" '
            f'transform="rotate(-90 14 {height / 2})" '
            'text-anchor="middle" font-size="11" '
            'fill="#657187">RSS memory (MB)</text>'
        )
        + "</svg>"
    )


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=False)