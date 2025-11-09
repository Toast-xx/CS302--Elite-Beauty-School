from flask import Blueprint, render_template
from app.utils import *

main = Blueprint("main", __name__)

@main.route("/")
#@require_clearance(1)
def home():
    items = [{"id": 11232, "date": "22/11/2022", "percentage": 10, "amount": 200, "status": "Completed"},
    {"id": 11233, "date": "23/11/2022", "percentage": 20, "amount": 300, "status": "Cancelled"},
    {"id": 11234, "date": "24/11/2022", "percentage": 15, "amount": 250, "status": "Processing"},
    {"id": 11235, "date": "25/11/2022", "percentage": 12, "amount": 180, "status": "Completed"},
    {"id": 11236, "date": "26/11/2022", "percentage": 25, "amount": 400, "status": "Completed"},
    {"id": 11237, "date": "27/11/2022", "percentage": 8, "amount": 150, "status": "Processing"},
    {"id": 11238, "date": "28/11/2022", "percentage": 18, "amount": 220, "status": "Cancelled"},
    {"id": 11239, "date": "29/11/2022", "percentage": 30, "amount": 500, "status": "Completed"},
    {"id": 11240, "date": "30/11/2022", "percentage": 22, "amount": 350, "status": "Processing"},
    {"id": 11241, "date": "01/12/2022", "percentage": 16, "amount": 280, "status": "Completed"},
    {"id": 11242, "date": "02/12/2022", "percentage": 14, "amount": 260, "status": "Cancelled"},
    {"id": 11243, "date": "03/12/2022", "percentage": 9, "amount": 175, "status": "Completed"},
    {"id": 11244, "date": "04/12/2022", "percentage": 27, "amount": 420, "status": "Processing"},
    {"id": 11245, "date": "05/12/2022", "percentage": 19, "amount": 310, "status": "Completed"},
    {"id": 11246, "date": "06/12/2022", "percentage": 11, "amount": 190, "status": "Cancelled"}
    ]

    return render_template("admin_base.html", items=items)
    #return render_template("store.html")
