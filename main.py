from flask import Flask, render_template, request
# import ratemyprofessor

app = Flask(__name__)

@app.route('/')
def search_page():
    return render_template('search.html')

@app.route('/results', methods=['POST'])
def results_page():
    interests = []
    weekdays = []
    times = []
    modes = []
    hours = []
    levels = []
    for i in range(1, 8):
        interest = request.form.get("interest"+str(i))
        if (interest != None):
            interests.append(interest)
    if (len(interests)==0):
        pass
    for i in range(1, 6):
        if (request.form.get("hours"+str(i)) != None):
            hours.append(i)
    for i in range(1, 6):
        level = request.form.get("levels"+str(i))
        if (level != None):
            levels.append(level)
    for i in range(1, 8):
        weekday = request.form.get("weekday"+str(i))
        if (weekday != None):
            weekdays.append(weekday)
    for i in range(1, 4):
        time = request.form.get("time"+str(i))
        if (time != None):
            times.append(time)
    for i in range(1, 3):
        mode = request.form.get("mode"+str(i))
        if (mode != None):
            modes.append(mode)

    ## school = ratemyprofessor.get_school_by_name("University of Texas at Dallas")
    ## for 
    ## professor = ratemyprofessor.get_professor_by_school_and_name(school, "Professor Name") 
    ## if professor is not None:
    ##     print(professor.rating)

    return render_template("results.html", results=[{"section": "CS 1337", "description": "This is a course in introductory computer science", "prerequisites": "CS 1336", "title": "Computer Science I", "professor": "Khiem Le"}, {"section": "CS 1337", "description": "Math", "prerequisites": "CS 1336", "whySelected": "Tired"}, {"section": "CS 1337", "description": "Math", "prerequisites": "CS 1336", "whySelected": "Tired"}, {"section": "CS 1337", "description": "Math", "prerequisites": "CS 1336", "whySelected": "Tired"}])

## @app.route('/results')
## def results_page():
##    return render_template("results.html", results=[{"section": "CS 1337", "description": "Math", "prerequisites": "CS 1336", "whySelected": "Tired"}, {"section": "CS 1337", "description": "Math", "prerequisites": "CS 1336", "whySelected": "Tired"}, {"section": "CS 1337", "description": "Math", "prerequisites": "CS 1336", "whySelected": "Tired"}, {"section": "CS 1337", "description": "Math", "prerequisites": "CS 1336", "whySelected": "Tired"}])

if __name__ == '__main__':
    app.run()