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
        "is_graph" : True,
        "print_every" : runner_params["print_every"],
        "Dimension" : runner_params["Dimension"]

    }

    STRESS_PARAM = {
        "k": runner_params["k"],
        "rc" : runner_params["rc"],
        "r0": runner_params["r0"]
    }

    DISPLACEMENT_PARAMS = {
        "move_after" : runner_params["moveafter"],
        "move_every" : runner_params["moveevery"],
        "displacement" : runner_params["movedisplacement"]
    }

    LJ_PARAMS = {
        "epsilon" : runner_params["epsilon"],
        "ljcutoff": runner_params["ljcutoff"]
    }

    api = API(SERVER_PARAMS,GRAPHER_PARAMS,STRESS_PARAM,DISPLACEMENT_PARAMS,LJ_PARAMS)
    for i in api.run():
        yield i


runner_params = {
    "time_end" : 3000 ,
    "dt" : 0.0005 ,
    "num_particles":100,
    "distance" :2.5,
    "cellList" : True,
    "print_every" : 100,
    "Dimension" :"2d",
    "k": 1,
    "rc" : 1.12 *1.2,
    "r0": 1.12

}
