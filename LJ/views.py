from LJ import app

from LJ.application import runner
from flask import render_template,request,Response,redirect, url_for,jsonify , stream_with_context
import json


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

#old version
@app.route('/run', methods=['POST'])
def get_run():
    if request.method == 'GET':
        content = request.get_json(silent=True)
        # print (content)
    return render_template("index.html",response = run())


def stream_template(template_name, **context):
    # http://flask.pocoo.org/docs/patterns/streaming/#streaming-from-templates
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    # uncomment if you don't need immediate reaction
    ##rv.enable_buffering(5)
    return rv


@app.route('/submit',methods = ['GET','POST'])
def submit():
    print(request.form.get("springDisplay"))
    run_params = {
        "time_end" : 3000 if request.form['time_end']=='' else int(request.form['time_end']),
        "dt" : 0.0005 if request.form['dt']=='' else float(request.form['dt']),
        "num_particles": 100 if request.form['num_particle']=='' else int(request.form['num_particle']),
        "distance" :2.5,
        "cellList" : True,
        "print_every" : 100 if request.form['print_every']=='' else int(request.form['print_every']),
        "Dimension" :"2d",
        "k": 0.05 if request.form['k']=='' else float(request.form['k']),
        "r0": 1.12 if request.form['r0']=='' else float(request.form['r0']),
        "epsilon" : 5 if request.form['epsilon']=='' else float(request.form['epsilon']),
        "ljcutoff" : 2.5 if request.form['ljcutoff']=='' else float(request.form['ljcutoff']), #might be same as the cell  size
        "moveafter": 500 if request.form['moveafter']=='' else int(request.form['moveafter']),
        "moveevery": 20 if request.form['moveevery']=='' else int(request.form['moveevery']),
        "movedisplacement": 1.5 if request.form['movedisplacement']=='' else float(request.form['movedisplacement']),
        "spring_viz" : True if request.form.get("springDisplay")=='true' else False

    }
    run_params["rc"] = run_params['r0'] * 1.2
    return run(run_params)

# @app.route('/run',methods = ['GET','POST'])
def run(run_params):
    # x = runner.main(run_params)
    # runner.main(run_params)
    return Response(stream_template("index.html",data = runner.main(run_params),iter_inc = run_params["print_every"],v_spring=run_params["spring_viz"]))

    # return Response(stream_with_context(runner.main(run_params)),mimetype='application/json')
    # return redirect('index.html')
