import requests
from datetime import datetime, timedelta
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
        date = datetime.now().strftime("%d-%m-%Y")
        centers_response = requests.get(
            url+"/v2/appointment/sessions/public/findByPin", params={"pincode": pincode, "date": date})
        if "error" in centers_response.json().keys():
            return "Invalid Pin Code"
        else:
            sessions = centers_response.json()["sessions"]
            return render_template("centers.djhtml", sessions=sessions, date=date)
    else:
        return redirect(url_for('get_pin_code'))


@app.route("/findByDistrict/select_state", methods=["GET", "POST"])
def select_state():
    if request.method == "POST":
        return redirect(f"/findByDistrict/select_district/{request.form['state_id']}")
    else:
        state_response = requests.get(url+"/v2/admin/location/states")
        states = state_response.json()["states"]
        return render_template("select_state.djhtml", states=states)


@app.route("/findByDistrict/select_district/<int:state_id>", methods=["GET", "POST"])
def select_district(state_id):
    if request.method == "POST":
        return redirect(f"/findByDistrict/centers/{request.form['district_id']}/{datetime.today().strftime('%d-%m-%Y')}")
    else:
        district_response = requests.get(
            url+f"/v2/admin/location/districts/{state_id}")
        districts = district_response.json()["districts"]
        return render_template("select_district.djhtml", districts=districts)


@app.route("/findByDistrict/centers/<int:district_id>/<string:date>")
def centers_by_district(district_id, date):
    datetime_object = datetime.strptime(date, "%d-%m-%Y")
    dates = [
        datetime_object.strftime("%d-%m-%Y"),
        (datetime_object + timedelta(days=1)).strftime("%d-%m-%Y"),
        (datetime_object + timedelta(days=2)).strftime("%d-%m-%Y"),
        (datetime_object + timedelta(days=3)).strftime("%d-%m-%Y"),
        (datetime_object + timedelta(days=4)).strftime("%d-%m-%Y"),
    ]
    if date:
        centers_response = requests.get(
            url+"/v2/appointment/sessions/public/findByDistrict", params={"district_id": district_id, "date": date})
    else:
        centers_response = requests.get(
            url+"/v2/appointment/sessions/public/findByDistrict", params={"district_id": district_id, "date": dates[0]})
    sessions = centers_response.json()["sessions"]
    return render_template("centers.djhtml", district_id=district_id, sessions=sessions, date_selected=date, todays_date=datetime.today().strftime("%d-%m-%Y"), dates=dates)


if __name__ == "__main__":
    app.run(debug=True)
