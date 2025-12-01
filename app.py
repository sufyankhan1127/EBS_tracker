import os
import json
import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, Response, jsonify
from bson.objectid import ObjectId
from db_helper import init_db, get_db
from file_handler import log_error, generate_csv, generate_pdf, backup_data

app = Flask(__name__)
app.secret_key = "super_secret_key_for_dev"

# Cloud Connection (Render)
app.config["MONGO_URI"] = os.environ.get("MONGO_URI", "mongodb://localhost:27017/finance_tracker")

init_db(app)

def load_config():
    try:
        with open("user_config.json", "r") as f:
            return json.load(f)
    except:
        return {"theme": "light", "currency_symbol": "$"}

@app.context_processor
def inject_config():
    return dict(config=load_config())

@app.route("/")
def dashboard():
    try:
        db = get_db()
        if db is None:
            # If DB is not connected, show empty dashboard instead of crashing
            raise Exception("Database not connected")

        month_filter = request.args.get("month", datetime.datetime.now().strftime("%Y-%m"))
        
        pipeline = [
            {"$match": {"date": {"$regex": f"^{month_filter}"}}},
            {"$group": {"_id": "$type", "total": {"$sum": "$amount"}}}
        ]
        totals = list(db.transactions.aggregate(pipeline))
        
        income = next((item["total"] for item in totals if item["_id"] == "income"), 0)
        expense = next((item["total"] for item in totals if item["_id"] == "expense"), 0)
        balance = income - expense

        budget_obj = db.budgets.find_one({"month": month_filter})
        budget_limit = float(budget_obj["amount"]) if budget_obj else 0
        budget_pct = (expense / budget_limit * 100) if budget_limit > 0 else 0

        cat_pipeline = [
            {"$match": {"type": "expense", "date": {"$regex": f"^{month_filter}"}}},
            {"$group": {"_id": "$category", "total": {"$sum": "$amount"}}}
        ]
        chart_data = list(db.transactions.aggregate(cat_pipeline))
        
        goals = list(db.goals.find())

        return render_template("dashboard.html", 
                               income=income, expense=expense, balance=balance, 
                               month=month_filter, budget_limit=budget_limit, 
                               budget_pct=budget_pct, chart_data=chart_data, goals=goals)
    except Exception as e:
        log_error(str(e))
        # Return a working page with zeros if DB fails
        return render_template("dashboard.html", 
                               income=0, expense=0, balance=0, 
                               budget_limit=0, budget_pct=0, 
                               chart_data=[], goals=[])

@app.route("/transactions", methods=["GET", "POST"])
def transactions():
    db = get_db()
    
    if request.method == "POST":
        try:
            data = {
                "date": request.form["date"],
                "type": request.form["type"],
                "category": request.form["category"],
                "amount": float(request.form["amount"]),
                "notes": request.form["notes"]
            }
            if request.form.get("transaction_id"):
                db.transactions.update_one({"_id": ObjectId(request.form["transaction_id"])}, {"$set": data})
                flash("Transaction Updated!", "success")
            else:
                db.transactions.insert_one(data)
                flash("Transaction Added!", "success")
        except Exception as e:
            log_error(str(e))
            flash("Error saving transaction.", "danger")
        return redirect(url_for("transactions"))

    query = {}
    search = request.args.get("search")
    if search:
        query["notes"] = {"$regex": search, "$options": "i"}
    
    sort_by = request.args.get("sort", "date")
    
    try:
        txs = list(db.transactions.find(query).sort(sort_by, -1))
        categories = list(db.categories.find())
    except:
        txs = []
        categories = []
    
    return render_template("transactions.html", transactions=txs, categories=categories)

@app.route("/delete_transaction/<id>")
def delete_transaction(id):
    get_db().transactions.delete_one({"_id": ObjectId(id)})
    flash("Transaction deleted", "warning")
    return redirect(url_for("transactions"))

@app.route("/manage_data", methods=["GET", "POST"])
def manage_data():
    db = get_db()
    if request.method == "POST":
        type_ = request.form.get("form_type")
        try:
            if type_ == "category":
                db.categories.insert_one({"name": request.form["name"]})
            elif type_ == "budget":
                db.budgets.update_one(
                    {"month": request.form["month"]}, 
                    {"$set": {"amount": float(request.form["amount"])}}, 
                    upsert=True
                )
            elif type_ == "goal":
                db.goals.insert_one({
                    "name": request.form["name"],
                    "target": float(request.form["target"]),
                    "current": float(request.form["current"])
                })
            flash(f"{type_.capitalize()} saved!", "success")
        except Exception as e:
            log_error(str(e))
            flash("Error saving data", "danger")
            
    return render_template("manage_data.html")

@app.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        conf = {
            "theme": request.form["theme"],
            "currency_symbol": request.form["currency"]
        }
        with open("user_config.json", "w") as f:
            json.dump(conf, f)
        return redirect(url_for("settings"))
    return render_template("settings.html")

@app.route("/export/csv")
def export_csv():
    try:
        txs = list(get_db().transactions.find())
        csv_data = generate_csv(txs)
        return Response(
            csv_data,
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=transactions.csv"}
        )
    except Exception as e:
        log_error(str(e))
        return "Error exporting CSV"

@app.route("/export/pdf")
def export_pdf():
    try:
        month = datetime.datetime.now().strftime("%Y-%m")
        txs = list(get_db().transactions.find({"date": {"$regex": f"^{month}"}}))
        pdf_bytes = generate_pdf(txs, month)
        return Response(
            pdf_bytes,
            mimetype="application/pdf",
            headers={"Content-disposition": f"attachment; filename=report_{month}.pdf"}
        )
    except Exception as e:
        log_error(str(e))
        return f"Error exporting PDF: {e}"

@app.route("/backup")
def download_backup():
    try:
        json_data = backup_data(get_db())
        return Response(
            json_data,
            mimetype="application/json",
            headers={"Content-disposition": "attachment; filename=backup.json"}
        )
    except Exception as e:
        log_error(str(e))
        return "Backup failed"

@app.route("/restore", methods=["POST"])
def restore_backup():
    try:
        if "file" not in request.files:
            flash("No file uploaded", "danger")
            return redirect(url_for("manage_data"))
            
        file = request.files["file"]
        data = json.load(file)
        db = get_db()
        
        for col in ["transactions", "categories", "budgets", "goals"]:
            if col in data:
                db[col].delete_many({})
                for item in data[col]:
                    if "_id" in item: del item["_id"]
                if data[col]:
                    db[col].insert_many(data[col])
                    
        flash("Data restored successfully!", "success")
    except Exception as e:
        log_error(str(e))
        flash("Restore failed. Check logs.", "danger")
        
    return redirect(url_for("manage_data"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
    