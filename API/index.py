from flask import Flask, request, render_template, redirect, url_for, jsonify
import os

app = Flask(__name__)
# Define the upload folder
app.config['UPLOAD_FOLDER'] = 'uploads'

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# Function to check if the file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # Check if a file was submitted
        if 'file' not in request.files:
            print("file not submitted")
            return redirect(request.url)
        
        file = request.files['file']
        print(file)

        # If the user submits an empty form
        if file.filename == '':
            print("empty form")
            return redirect(request.url)
        
        # If the file is allowed, save it to the upload folder
        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            print("file saved")
            return redirect(url_for('uploaded_file', filename=file.filename))

    return render_template('upload_image.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return f'Image: {filename} has been uploaded successfully.'


# @app.route('/', methods=['GET']) 
# def index():
#     """
#     INPUT -> image
#     OUTPUT -> list of similar items & score
#     """

#     return jsonify({"message": "HELLO WORLD"})
#     # return 'Index Page'



@app.route('/api/hello', methods=['GET'])
def hello_world():
    # Make an API call to "Hello, World"
    return jsonify({"message": "HELLO WORLD"})

if __name__ == '__main__':
     app.run(debug=True)

# if request.method == 'POST':
# f = request.files['the_file']
# f.save('/var/www/uploads/uploaded_file.txt')
