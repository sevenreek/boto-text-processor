from aws_setup import delete_all, App, smart_setup


app = smart_setup()
delete_all(app)