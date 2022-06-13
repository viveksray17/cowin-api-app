import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
url = "https://cdn-api.co-vin.in/api"


@app.route("/")
def home():
    return render_template("home.djhtml")


@app.route("/findByPin")
def get_pin_code():
    return render_template("pin.djhtml")


@app.route("/findByPin/centers", methods=["GET", "POST"])
def centers_by_pin():
    if request.method == "POST":
        pincode = request.form["pincode"]
        centers_response = requests.get(
            url+"/v2/appointment/sessions/public/findByPin", params={"pincode": pincode, "date": "13-06-2022"})
        if "error" in centers_response.json().keys():
            return "Invalid Pin Code"
        else:
            sessions = centers_response.json()["sessions"]
            return render_template("centers.djhtml", sessions=sessions)
    else:
        return redirect(url_for('get_pin_code'))


@app.route("/findByDistrict/select_state")
def select_state():
    state_response = requests.get(url+"/v2/admin/location/states")
    states = state_response.json()["states"]
    return render_template("select_state.djhtml", states=states)


@app.route("/findByDistrict/select_district", methods=["GET", "POST"])
def select_district():
    if request.method == "POST":
        selected_state = request.form["state_id"]
        district_response = requests.get(
            url+f"/v2/admin/location/districts/{selected_state}")
        districts = district_response.json()["districts"]
        return render_template("select_district.djhtml", districts=districts)
    else:
        return redirect(url_for('select_state'))


@app.route("/findByDistrict/centers", methods=["GET", "POST"])
def centers_by_district():
    if request.method == "POST":
        selected_district = request.form["district_id"]
        centers_response = requests.get(
            url+"/v2/appointment/sessions/public/findByDistrict", params={"district_id": selected_district, "date": "13-06-2022"})
        sessions = centers_response.json()["sessions"]
        return render_template("centers.djhtml", sessions=sessions)


if __name__ == "__main__":
    app.run()
