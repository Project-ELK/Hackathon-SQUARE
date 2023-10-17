from flask import Flask, request, render_template, redirect, url_for, jsonify, send_from_directory
import os

from Scripts.GetItemSummary import getSummary

app = Flask(__name__)
# Define the upload folder
app.config['UPLOAD_FOLDER'] = 'static'


# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# Function to check if the file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Uploads page -
@app.route('/uploads', methods=['GET', 'POST'])
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
            # Gets the current working directory
            current_working_directory = os.getcwd().replace("\\","/")
            filename = current_working_directory+f"/API/{app.config['UPLOAD_FOLDER']}/{file.filename}"
            # Saves image locally
            file.save(filename)
            print("file saved")
            # Redirects user to success message (route)
            return redirect(url_for('uploaded_file', filename=file.filename))

    return render_template('upload_image.html')

@app.route('/', methods=['GET'])
def root_Page():
    return render_template('itemIndex.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    image_url = url_for('static', filename=f'uploads/{filename}')

    #TODO:    
    #summary_data = getSummary()
    summary_data = [["hi", 1, 4], ["hi", 1, 4], ["hi", 1, 4]]

    return render_template('image_display.html', image_url=image_url, summary_data = summary_data)

@app.route('/api/hello', methods=['GET'])
def hello_world():
    # Make an API call to "Hello, World"
    return jsonify({"message": "HELLO WORLD"})

if __name__ == '__main__':
     app.run(debug=False)
