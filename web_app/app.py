from flask import Flask, request, jsonify
# allow cross domain
from flask_cors import CORS
import json
import lib.Bayesian_Bandit as bay_band
import sys
port = 8080

app = Flask(__name__)
CORS(app)

# set this by default to allow cross domain calls to work
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/', methods=['POST', 'GET'])
def test():
    """
    Sanity check for flask application
    ---
    get:
        responses:
            200:
                description: html page
    post:
        responses:
            200:
                description: html page
    """
    print("some debugging information for you", file=sys.stderr)
    html = "<h3>Hello world! </h3>"
    return html


BETA_MATRIX = bay_band.Bayes_Bandit()


@app.route('/update_bandit', methods=['POST', 'GET'])
def update_beta_function_from_json():
    """
    Update the bandit based on a JSON string that looks like:
        [{"game_key_1": {"number_successes": 50, "number_failures": 400}},
             {"game_key_2": {"number_successes": 30, "number_trials": 33}},
             {"id3": {"number_failures": 30, "number_trials": 33}}
        ]
    or just a single dictionaries
    {"game_key_1": {"number_successes": 50, "number_failures": 400}
    ---
    get:
        parameters:
              - name: someParam
                in: formData
                type: integer
                required: true
        responses:
            200:
                description: item updated
    """

    # process using bandit_function functions, to generate gsme keys in Beta Matrix they don't exist
    # update your BetaMatix['game_key']

    json_list = request.get_json()

    if isinstance(json_list, list) is False:
        json_list = [json_list]

    for game_beta_info in json_list:

        game_id = list(game_beta_info.keys())[0]

        BETA_MATRIX.update(game_id, game_beta_info[game_id][
            'number_successes'], game_beta_info[game_id]['number_trials'])

    output = {"message": f"{len(json_list)} records appended"}
    print(output, file=sys.stderr)
    return json.dumps(output), 200, {'Content-Type': 'text/plain; charset=utf-8'}


@app.route('/pull_lever', methods=['POST', 'GET'])
def pull_lever():
    """
    Pull the lever on the bandit
    ---
    post:
        parameters:
            - in: body
                name items list of ids to be drawn from
                type list of str
                required false
        responses:
            200:
                description: Jsonified dict of predictions, including the most likely id, and the corresponding probability
    """

    # pull from the beta matric, BetaMatix get the probabilities
    # probs = BETAMATRIX.pull()
    #

    best_item = BETA_MATRIX.pull_lever()
    output = {"item": best_item}

    return json.dumps(output), 200, {'Content-Type': 'text/plain; charset=utf-8'}


@app.route('/dump_beta_matrix_parameters', methods=['POST', 'GET'])
def dump_beta_matrix():
    """
    Return all the current beta-matrix parameter, with their ids/game keys
    ---
    get:
        parameters:
              - name: someParam
                in: formData
                type: integer
                required: true
        responses:
            200:
                description: Jsonified dict of predictions
    """

    bm_list = []
    for i, item in enumerate(BETA_MATRIX.items):
        bm_list.append({
            f"{item}": {"success": int(BETA_MATRIX.current_beta_matrix[i][0]) - 1,
                        "failures": int(BETA_MATRIX.current_beta_matrix[i][1] - 1),
                        "number_trials": int(BETA_MATRIX.current_beta_matrix[i][0] + BETA_MATRIX.current_beta_matrix[i][1] - 2)
                        }
        })

    output = {"beta_matrix_parameters": bm_list}

    return json.dumps(output), 200, {'Content-Type': 'text/plain; charset=utf-8'}


def create_app():
    """ Constructor
    Returns
    -------
    app : flask app
    """
    return app

if __name__ == "__main__":
    # app = create_app(config=None)
    # , use_reloader=False) # remember to set debug to False
    app.run(host='0.0.0.0', port=port, debug=True)


"""
# to do.

-- add a reset api endpoint

-- perform error handeling on inputs

-- 

-- add unit tests directory tests/, 
use pytest to run some unit tests

"""
