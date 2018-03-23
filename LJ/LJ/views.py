from LJ import app

from LJ.application import runner
from flask import render_template,request,Response,redirect, url_for,jsonify
import json


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/run', methods=['POST'])
def get_run():
    if request.method == 'GET':
        content = request.get_json(silent=True)
        print (content)
    return render_template("index.html",response = run())


def stream_template(template_name, **context):
    # http://flask.pocoo.org/docs/patterns/streaming/#streaming-from-templates
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    # uncomment if you don't need immediate reaction
    ##rv.enable_buffering(5)
    return rv

@app.route('/run',methods = ['GET'])
def run():
    run_params = {
        "time_end" : 3000,
        "num_particles":100,
        "distance" :2.5,
        "cellList" : True,
        "print_every" : 100,
        "Dimension" :"2d",
        "k": 0.05,
        "rc" : 1.12 *1.2,
        "r0": 1.12

    }
    # x = runner.main(run_params)
    # runner.main(run_params)
    return Response(stream_template("index.html",data = runner.main(run_params)))

        # return app.response_class(response=x,mimetype='application/json')
    # return redirect('index.html')
