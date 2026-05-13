from flask import Blueprint, request, redirect, render_template

auth_bp = Blueprint("auth", __name__);

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        
        return redirect("/dashboard")  
    return render_template("login.html")  

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        
        return redirect("/login")  
    return render_template("register.html")