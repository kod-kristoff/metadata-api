"""Routes for the metadata API."""

# import locale

from flask import Blueprint, current_app, jsonify, request
from . import utils

general = Blueprint("general", __name__)
# locale.setlocale(locale.LC_ALL, "sv_SE.utf8")


@general.route("/doc")
def documentation():
    """Serve API documentation yaml file."""
    return current_app.send_static_file("apidoc.yaml")


@general.route("/")
def metadata():
    """Return corpus and lexicon metadata as a JSON object."""
    corpora, lexicons, models = utils.load_resources()

    resource = request.args.get("resource")
    if resource:
        return utils.get_single_resource(resource, corpora, lexicons, models)

    data = {"corpora": utils.dict_to_list(corpora), "lexicons": utils.dict_to_list(lexicons),
            "models": utils.dict_to_list(models)}

    return jsonify(data)


@general.route("/corpora")
def corpora():
    """Return corpus metadata as a JSON object."""
    json_data = utils.get_resource_type("corpus", "CORPORA_FILE")
    return json_data


@general.route("/lexicons")
def lexicons():
    """Return lexicon metadata as a JSON object."""
    json_data = utils.get_resource_type("lexicon", "LEXICONS_FILE")
    return json_data


@general.route("/models")
def models():
    """Return models metadata as a JSON object."""
    json_data = utils.get_resource_type("model", "MODELS_FILE")
    return json_data


@general.route("/collections")
def collections():
    """Return collections metadata as a JSON object."""
    corpora, lexicons, models = utils.load_resources()

    data = dict([(name, data) for (name, data) in corpora.items() if data.get("collection")])
    lexicons = dict([(name, data) for (name, data) in lexicons.items() if data.get("collection")])
    data.update(lexicons)
    models = dict([(name, data) for (name, data) in models.items() if data.get("collection")])
    data.update(models)

    return jsonify({
        "hits": len(data),
        "resources": utils.dict_to_list(data)
    })


@general.route("/list-ids")
def list_ids():
    """List all existing resource IDs."""
    resource_IDs = [k for res_type in utils.load_resources() for k in list(res_type.keys())]
    return sorted(resource_IDs)


@general.route("/check-id-availability")
def check_id():
    """Check if a given resource ID is available."""
    input_id = request.args.get("id")
    if not input_id:
        return jsonify({
            "id": None,
            "error": "No ID provided"
        })
    resource_IDs = set([k for res_type in utils.load_resources() for k in list(res_type.keys())])
    if input_id in resource_IDs:
        return jsonify({
            "id": input_id,
            "available": False
        })
    else:
        return jsonify({
            "id": input_id,
            "available": True
        })


@general.route("/renew-cache")
def renew_cache():
    """Flush cache and re-read json files."""
    try:
        if not current_app.config.get("NO_CACHE"):
            mc = current_app.config.get("cache_client")
            mc.flush_all()
        utils.load_resources()
        utils.load_json(current_app.config.get("RESOURCE_TEXTS_FILE"), prefix="res_desc")
        success = True
        error = None
    except Exception:
        success = False
    return jsonify({"cache_renewed": success,
                    "error": error})
