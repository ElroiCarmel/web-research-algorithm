import json
import logging
import random
from flask import render_template, flash, redirect, url_for, request
from my_web import app
from my_web.forms import ValuationForm, FillRandomForm
from io import StringIO
from fairpyx import Instance, divide
from fairpyx.algorithms.maximally_proportional import maximally_proportional_allocation
from fairpyx.algorithms.maximally_proportional import logger
from functools import reduce


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["GET", "POST"])
def submit():
    form = ValuationForm()
    fill_rand_form = FillRandomForm()

    if fill_rand_form.validate_on_submit():
        nagents, nitems = fill_rand_form.num_agents.data, fill_rand_form.num_items.data
        rand_instance = Instance.random_uniform(
            num_of_agents=nagents,
            num_of_items=nitems,
            item_capacity_bounds=(1, 1),
            agent_capacity_bounds=(nitems, nitems),
            item_base_value_bounds=(50, 100),
            item_subjective_ratio_bounds=(0.2, 2.0),
            normalized_sum_of_values=100,
        )
        form.valuation.data = str(rand_instance._valuations).replace("'", '"')
        return render_template("submit.html", form=form, fill_rand_form=fill_rand_form)
    elif form.validate_on_submit():
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
            score_by_agent = {}
            for agent, bundle in alloc.items():
                bundle_value = instance.agent_bundle_value(agent, bundle)
                agent_total_value = instance.agent_bundle_value(agent, instance.items)
                score_by_agent[agent] = {
                    "bundle_value": bundle_value,
                    "proportional_value": round(bundle_value / agent_total_value, 4),
                    "threshold": round(agent_total_value / instance.num_of_agents, 4),
                    "prop_threshold": round(1 / instance.num_of_agents, 4),
                }
            items_given = reduce(set.union, alloc.values(), set())
            items = set(instance.items)
            items_not_given = items - items_given
            return render_template(
                "allocation.html",
                alloc=alloc,
                score=score_by_agent,
                instance=instance_str(instance),
                logs=logs,
                items_not_given=items_not_given
            )
    return render_template("submit.html", form=form, fill_rand_form=fill_rand_form)


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
