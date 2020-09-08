from flask import Flask, render_template, request, send_file
from scrapper import stackoverflow_scrapper, wework_scrapper, remoteok_scrapper
from export import save_to_file

stack_db = {}
wework_db = {}
remoteok_db = {}
keyword_db = {}

app = Flask("Remote_Job_Scrapper")


@app.route("/")
def home():

    return render_template("home.html")


@app.route("/result")
def result():
    # stack_result=stack_result, total=len(stack_result)
    search_input = request.args.get('search_input')
    search_input = search_input.lower()
    if search_input:
        fromdb = keyword_db.get(search_input)
        if fromdb:
            stack_result = stack_db.get(search_input)
            wework_result = wework_db.get(search_input)
            remoteok_result = remoteok_db.get(search_input)
        else:
            stack_result = stackoverflow_scrapper(search_input)
            stack_db[search_input] = stack_result

            wework_result = wework_scrapper(search_input)
            wework_db[search_input] = wework_result

            remoteok_result = remoteok_scrapper(search_input)
            remoteok_db[search_input] = remoteok_result

            keyword_db[search_input] = "searched"

    total = len(stack_result) + len(wework_result) + len(remoteok_result)
    total = format(total, ",")

    return render_template("result.html", search_input=search_input, stack_result=stack_result, wework_result=wework_result, remoteok_result=remoteok_result, total=total)


@app.route("/export")
def export():
    search_input = request.args.get('search_input')
    if keyword_db.get(search_input):
        stack_result = stack_db.get(search_input)
        wework_result = wework_db.get(search_input)
        remoteok_result = remoteok_db.get(search_input)
        save_to_file(stack_result, wework_result, remoteok_result)
    else:
        raise Exception

    return send_file(filename_or_fp=f'Magic_Report.csv', mimetype='text/x-csv', attachment_filename=f'Magic_{search_input}_Report.csv', as_attachment=True)


app.run(host="192.168.0.4")
