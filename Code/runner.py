from moduless.LJ_API import API



def main():
    SERVER_PARAMS ={
        "time_end" : 300,
        "num_particles":4900,
        "distance" :2.5,
        "cellList" : True
    }
    GRAPHER_PARAMS = {
        "print_every" : 100,
        "Dimension" :"2d"

    }
    api = API(SERVER_PARAMS,GRAPHER_PARAMS)
    api.run()


main()
