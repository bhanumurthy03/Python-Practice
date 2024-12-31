from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)

CORS(app)

# Define a route to add two numbers
@app.route('/add', methods=['GET'])
def add_numbers():
    try:
        # Get the 'num1' and 'num2' parameters from the query string
        num1 = float(request.args.get('num1'))
        num2 = float(request.args.get('num2'))
        
        # Add the numbers
        result = num1 + num2
        
        # Return the result as a JSON response
        return jsonify({'result': result})
    
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid input. Please provide valid numbers for num1 and num2.'}), 400

# Define the folder where you want to save the uploaded files
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allow only certain types of files to be uploaded (optional)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the request contains a file
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']

    # If no file is selected or filename is empty, return error
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Check if the file has an allowed extension
    if file and allowed_file(file.filename):
        # Save the file to the server
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return jsonify({"message": f"File {file.filename} uploaded successfully!"}), 200
    else:
        return jsonify({"error": "File type not allowed"}), 400
if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
