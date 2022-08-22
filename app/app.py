import requests
import json
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
url = "https://cdn-api.co-vin.in/api"


@app.route("/")
def home():
    return render_template("home.djhtml")


@app.route("/findByPin", methods=["GET", "POST"])
def get_pin_code():
    if request.method == "POST":
        return redirect(f"/findByPin/centers/{request.form['pincode']}/{datetime.today().strftime('%d-%m-%Y')}")
    else:
        return render_template("pin.djhtml")


@app.route("/findByPin/centers/<int:pin>/<string:date>", methods=["GET", "POST"])
def centers_by_pin(pin, date):
    centers_response = requests.get(
        url+"/v2/appointment/sessions/public/findByPin", params={"pincode": pin, "date": date})
    if "error" in centers_response.json().keys():
        return "Invalid Pin Code"
    else:
        datetime_object = datetime.strptime(date, "%d-%m-%Y")
        dates_coming = [
            (datetime_object + timedelta(days=1)).strftime("%d-%m-%Y"),
            (datetime_object + timedelta(days=2)).strftime("%d-%m-%Y"),
            (datetime_object + timedelta(days=3)).strftime("%d-%m-%Y"),
            (datetime_object + timedelta(days=4)).strftime("%d-%m-%Y"),
        ]
        dates_previous = [
            (datetime_object - timedelta(days=1)).strftime("%d-%m-%Y"),
            (datetime_object - timedelta(days=2)).strftime("%d-%m-%Y"),
            (datetime_object - timedelta(days=3)).strftime("%d-%m-%Y"),
            (datetime_object - timedelta(days=4)).strftime("%d-%m-%Y"),
        ]
        sessions = centers_response.json()["sessions"]
        return render_template("centers_pincode.djhtml", pincode=pin, todays_date=datetime.today().strftime("%d-%m-%Y"), sessions=sessions, date_selected=date, dates_coming=dates_coming, dates_previous=dates_previous)


@app.route("/findByDistrict/select_state", methods=["GET", "POST"])
def select_state():
    if request.method == "POST":
        return redirect(f"/findByDistrict/select_district/{request.form['state_id']}")
    else:
        with open("metadata/states.json") as f:
            states = json.load(f)["states"]
            return render_template("select_state.djhtml", states=states)


@app.route("/findByDistrict/select_district/<int:state_id>", methods=["GET", "POST"])
def select_district(state_id):
    if request.method == "POST":
        return redirect(f"/findByDistrict/centers/{request.form['district_id']}/{datetime.today().strftime('%d-%m-%Y')}")
    else:
        with open(f"metadata/districts/state{state_id}.json") as f:
            districts = json.load(f)["districts"]
            return render_template("select_district.djhtml", districts=districts)


@app.route("/findByDistrict/centers/<int:district_id>/<string:date>")
def centers_by_district(district_id, date):
    datetime_object = datetime.strptime(date, "%d-%m-%Y")
    dates_coming = [
        (datetime_object + timedelta(days=1)).strftime("%d-%m-%Y"),
        (datetime_object + timedelta(days=2)).strftime("%d-%m-%Y"),
        (datetime_object + timedelta(days=3)).strftime("%d-%m-%Y"),
        (datetime_object + timedelta(days=4)).strftime("%d-%m-%Y"),
    ]
    dates_previous = [
        (datetime_object - timedelta(days=1)).strftime("%d-%m-%Y"),
        (datetime_object - timedelta(days=2)).strftime("%d-%m-%Y"),
        (datetime_object - timedelta(days=3)).strftime("%d-%m-%Y"),
        (datetime_object - timedelta(days=4)).strftime("%d-%m-%Y"),
    ]
    centers_response = requests.get(
        url+"/v2/appointment/sessions/public/findByDistrict", params={"district_id": district_id, "date": date})
    sessions = centers_response.json()["sessions"]
    return render_template("centers_district.djhtml", district_id=district_id, sessions=sessions, date_selected=date, todays_date=datetime.today().strftime("%d-%m-%Y"), dates_coming=dates_coming, dates_previous=dates_previous)


if __name__ == "__main__":
    app.run()
