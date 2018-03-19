from moduless.LJ_API import API



def main():
    SERVER_PARAMS ={
        "time_end" : 3000,
        "num_particles":100,
        "distance" :2.5,
        "cellList" : False,

    }
    GRAPHER_PARAMS = {
        "print_every" : 100,
        "Dimension" :"2d"

    }

    STRESS_PARAM = {
        "k": 0.05,
        "rc" : 1.12 *1.2,
        "r0": 1.12
    }

    api = API(SERVER_PARAMS,GRAPHER_PARAMS,STRESS_PARAM)
    api.run()


main()
