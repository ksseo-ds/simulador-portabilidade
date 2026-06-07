from flask import Blueprint, render_template

investments_bp = Blueprint("investments", __name__, url_prefix="/investments")

@investments_bp.route("/comparador")
def comparador():
    
    return render_template("investments/comparador.html")