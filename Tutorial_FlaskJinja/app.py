from flask import Flask, render_template, url_for, redirect, request

app = Flask(__name__)

grades_lst = ["A", "B", "C", "D", "E", "S", "U"]
rp_lst = [20.00, 17.50, 15.00, 12.50, 10.00, 5.00, 0.00]
subject_lst = ["H2 Subject 1", "H2 Subject 2", "H2 Subject 3", "H1 Subject", "General Paper", "Project Work", "Mother Tongue"]

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/rp_calc/", methods=["GET", "POST"])
def rp_calc():
    if request.method == "GET":
        return render_template("rp_calc1.html")
    else:
        temp_subject_lst = subject_lst[:5]
        pw, mt = request.form["pw"], request.form["mt"]
        # checking if mother tounge and project work are included
        if pw == "Yes":
            temp_subject_lst.append(subject_lst[5])
        if mt == "Yes":
            temp_subject_lst.append(subject_lst[6])
        posted_subject_lst = temp_subject_lst
        return render_template("rp_calc2.html", grades_lst=grades_lst, subject_lst = posted_subject_lst)

@app.route("/rp_display/", methods=["POST"])
def rp_display():
    responses = dict(request.form)
    subjects = list(responses.keys())
    grades = list(responses.values())
    rp_calc = []
    final_rp = []

    # calculating rp for the subjects
    for i in range(len(subjects)):
        if subjects[i] in subject_lst[3:7]:
            # if subject is h1, half the rank points
            rp_calc.append(0.5 * rp_lst[grades_lst.index(grades[i][:1])])
        else:
            rp_calc.append(rp_lst[grades_lst.index(grades[i][:1])])
    
    # adding total
    if len(subjects) > 5:
        final_rp.append("{:.2f}".format(90.00))
        if len(subjects) == 7:
            # if there are 7 subjects (aka mother tongue is included)
            rp_without_mt = sum(rp_calc[:6])
            rp_with_mt = sum(rp_calc) * 0.9
            final_rp.append("{:.2f}".format(max([rp_without_mt, rp_with_mt])))
        else:
            final_rp.append("{:.2f}".format(sum(rp_calc)))
    else:
        final_rp.append("{:.2f}".format(80.00))
        final_rp.append("{:.2f}".format(sum(rp_calc)))
    
    # formatting the rps
    for i in range(len(rp_calc)):
        rp_calc[i] = "{:.2f}".format(rp_calc[i])
    
    return render_template("rp_display.html", subjects = subjects, grades = grades, rp_calc = rp_calc, final_rp = final_rp)
    

@app.route("/display/<page>")
def display(page):
    if page == 'about':
        return redirect(url_for('about'))
    elif page == 'rp_calc':
        return redirect(url_for('rp_calc'))
    elif page == 'rp_display':
        return redirect(url_for('rp_display'))
    else:
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(port=5001, debug=True)