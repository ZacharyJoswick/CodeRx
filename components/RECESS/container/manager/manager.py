# Three parts to the recess system
    #Central manager
        #Keeps track of managers across the system
            #Number total
            #Where they are running
            #Max number of workers per
            #Currently running jobs
        #Accepts jobs from the main application
        #Tasks jobs to individual managers
        #Accepts responses and sends back to the user
    #Computer Manager
        #One or per computer
        #Accepts jobs from central manager
        #Starts one worker container per job
        #Captures container stream and forwards to the user
        #Stops and removes container when job complete
    #Worker script
        #Takes in a job
        #Creates file
        #Compiles file
            #Subprocess
            #Stream output to stdout
            #Append a designator to each line
        #Runs tests
            #