from app import create_app#, db
#from app.models import UserModel

app = create_app()

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)

# @app.shell_context_processor
# def make_shell_context():
#     return {'db': db, "UserModel": UserModel, ""}