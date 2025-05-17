import os
from flask import Flask, render_template, redirect, make_response, request, send_from_directory

app = Flask(__name__)

@app.route("/")
def home_page():
    with open("./logs/visitors.txt", "r") as file:
        count = int(file.read())
    count += 1
    with open("./logs/visitors.txt", "w") as file:
        file.write(str(count))
    response = make_response(render_template("home_page.html", count=count))
    cookie_value = request.cookies.get("seen")
    if cookie_value != "true":
        response.set_cookie(key="seen", value="true")
    else:
        pass
    return response

@app.route("/redirect")
def redirect_to_website():
    return redirect("https://www.ntu.edu.tw/")

@app.route("/download")
def download():
    files = sorted(os.listdir("download"))
    return f"""<h1>可下載檔案</h1>
    <ul>{''.join(f'<li>{file}</li>' for file in files)}</ul>
    """

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory('download', filename, as_attachment=True)

@app.route("/get_tracker")
def get_tracker():
    with open("./logs/id.txt", "r") as file:
        id_ = int(file.read())
    with open("./logs/read_log.txt", "r") as file:
            log = [line.strip() for line in file]
    id_ += 1
    while str(id_) in log:
        id_ += 1
    with open("./logs/id.txt", "w") as file:
        file.write(str(id_))
    response = make_response(f"Your ID is:{id_}")
    response.set_cookie(key="admin", value=str(id_))
    return response

@app.route("/tracker")
def tracker():
    id_ = request.args.get("id")
    if request.cookies.get("admin") == id_:
        pass
    else:
        with open("./logs/read_log.txt", "a") as file:
            file.write(str(id_)+"\n")
    return render_template("image.html")

@app.route("/read")
def read_check():
    id_ = request.args.get("id")
    with open("./logs/read_log.txt", "r") as file:
            log = [line.strip() for line in file]
    if id_ in log:
        return "Yes"
    else:
        return "No"

'''
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5522)
'''