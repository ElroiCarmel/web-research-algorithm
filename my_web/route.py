import json
import logging
import random
from flask import render_template, flash, redirect, url_for, request
from my_web import app
from my_web.forms import ValuationForm
from io import StringIO
from fairpyx import Instance, divide
from fairpyx.algorithms import maximally_proportional_allocation
from fairpyx.algorithms.maximally_proportional import logger


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["GET", "POST"])
def submit():
    form = ValuationForm()
    if form.validate_on_submit():
        if form.fill_random.data:
            kids = ["Alice", "Bob", "Charlie"]
            gifts = ["Board Game", "Headphones", "Sketchbook"]
            rand_example = {
                agent: {item: random.randint(20, 60) for item in gifts}
                for agent in kids
            }
            form.valuation.data = json.dumps(rand_example, indent=2)
            return render_template("submit.html", form=form)
        elif form.submit.data and form.validate_on_submit():
            try:
                valuation = json.loads(form.valuation.data)
            except json.decoder.JSONDecodeError as e:
                flash(f"Invalid input format! See examples. {e}", category="danger")
                return redirect(url_for("submit"))
            else:
                instance = Instance(valuations=valuation)
                # Custom the logger
                log_stream = StringIO()
                log_handler = logging.StreamHandler(log_stream)
                logger.addHandler(log_handler)
                log_handler.setFormatter(
                    logging.Formatter(fmt="{levelname} - {message}", style="{")
                )
                logger.setLevel(logging.DEBUG)

                alloc = divide(maximally_proportional_allocation, instance)

                logger.removeHandler(log_handler)
                logs = log_stream.getvalue()

                return render_template(
                    "allocation.html",
                    alloc=alloc,
                    instance=instance_str(instance),
                    logs=logs,
                )
    return render_template("submit.html", form=form)


@app.route("/about")
def about():
    return render_template("about.html")


def instance_str(instance: Instance) -> str:
    atoms = [f"* Agents: {list(instance.agents)}", f"* Items: {list(instance.items)}"]
    for agent in instance.agents:
        agent_valuation_func = dict(
            (item, instance.agent_item_value(agent, item)) for item in instance.items
        )
        atoms.append(f"** Agnet {agent} valuation: {agent_valuation_func}")
    return "\n".join(atoms)
