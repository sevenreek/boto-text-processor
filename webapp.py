from aws_setup import App, smart_setup, delete_all
from flask import Flask, request, render_template, g, send_from_directory, Response
import os

webapp = Flask(__name__, static_url_path='')

def get_aws():
    if 'aws' not in g:
        g.aws = smart_setup()
    return g.aws

def create_presigned_upload():
    aws = get_aws()
    client = aws.session.client('s3')
    ret = client.generate_presigned_post(
        Bucket=aws.bucket.name, 
        Key="${filename}",
        Fields={"acl": "public-read", "success_action_status":"201"},
        Conditions=[{"acl": "public-read"}, {"success_action_status":"201"}]
    )
    return ret

@webapp.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@webapp.route("/")
def home():
    try:
        aws = get_aws()        
        things = list(aws.bucket.objects.all())
        files = map(lambda el: {
            "path":el.key,
            "name":os.path.basename(el.key), 
            "url":f'https://{aws.bucket.name}.s3.amazonaws.com/{el.key}'
            }, things)
        return render_template('list.html', files=files)
    except Exception as e:    
        return str(e)
    
@webapp.route("/upload")
def request_upload():
    return create_presigned_upload()

@webapp.route("/process", methods=['POST'])
def request_process():
    content = request.get_json(force=True)
    print("Requested process of", content)
    if(len(content)):
        aws = get_aws()
        for f in content:
            aws.queue.send_message(
                MessageBody=f
            )
    return Response(status=200)

if __name__ == "__main__":
    webapp.run(debug=True)