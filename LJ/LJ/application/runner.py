from LJ.application.Modules.LJ_API import API



def main(runner_params):
    SERVER_PARAMS ={
        "time_end" : runner_params["time_end"],
        "num_particles":runner_params["num_particles"],
        "distance" :runner_params["distance"],
        "cellList" : runner_params["cellList"],
        "dt" : runner_params["dt"]

    }
    GRAPHER_PARAMS = {
        "print_every" : runner_params["print_every"],
        "Dimension" : runner_params["Dimension"]

    }

    STRESS_PARAM = {
        "k": runner_params["k"],
        "rc" : runner_params["rc"],
        "r0": runner_params["r0"]
    }

    api = API(SERVER_PARAMS,GRAPHER_PARAMS,STRESS_PARAM)
    for i in api.run():
        yield i
