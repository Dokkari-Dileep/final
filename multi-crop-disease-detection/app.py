# import os
# import json
# from datetime import datetime
# from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
# from werkzeug.utils import secure_filename
# from PIL import Image
# import numpy as np
# import tensorflow as tf
# from tensorflow.keras.preprocessing import image
# from tensorflow.keras.models import load_model
# import cv2

# app = Flask(__name__)
# app.secret_key = 'your-secret-key-here'
# app.config['UPLOAD_FOLDER'] = 'static/uploads'
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# # Allowed file extensions
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# # Load disease information
# with open('disease_info.json', 'r') as f:
#     disease_info = json.load(f)

# # Load the trained model (will be loaded on first request)
# model = None

# def load_disease_model():
#     """Load the trained model"""
#     global model
#     if model is None:
#         model = load_model('model/disease_model.h5')
#     return model

# def allowed_file(filename):
#     """Check if file extension is allowed"""
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def preprocess_image(img_path):
#     """Preprocess image for model prediction"""
#     img = image.load_img(img_path, target_size=(224, 224))
#     img_array = image.img_to_array(img)
#     img_array = np.expand_dims(img_array, axis=0)
#     img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)
#     return img_array

# def predict_disease(img_path):
#     """Predict disease from image"""
#     model = load_disease_model()
#     processed_img = preprocess_image(img_path)
    
#     predictions = model.predict(processed_img)
#     predicted_class = np.argmax(predictions[0])
#     confidence = float(predictions[0][predicted_class])
    
#     # Get disease name from index
#     disease_names = list(disease_info.keys())
#     predicted_disease = disease_names[predicted_class]
    
#     return predicted_disease, confidence

# @app.route('/')
# def index():
#     """Home page"""
#     return render_template('index.html')

# @app.route('/dataset')
# def dataset_page():
#     """Dataset information page"""
#     crops = {
#         'Apple': ['Apple_Scab', 'Apple_Black_Rot', 'Apple_Cedar_apple_rust', 'Apple_Healthy'],
#         'Cherry': ['Cherry_Healthy', 'Cherry_Brightness_Adjusted', 'Cherry_Constrast_Adjusted'],
#         'Corn': ['Corn_Common_rust', 'Corn_Northern_Leaf_Blight', 'Corn_Healthy'],
#         'Grape': ['Grape_Black_rot', 'Grape_Esca', 'Grape_Leaf_blight', 'Grape_Healthy'],
#         'Tomato': ['Tomato_Early_blight', 'Tomato_Late_blight', 'Tomato_Leaf_Mold', 
#                    'Tomato_Septoria_leaf_spot', 'Tomato_Spider_mites', 'Tomato_Healthy'],
#         'Potato': ['Potato_Early_blight', 'Potato_Late_blight', 'Potato_Healthy'],
#         'Strawberry': ['Strawberry_Leaf_scorch', 'Strawberry_Healthy'],
#         'Peach': ['Peach_Bacterial_spot', 'Peach_Healthy'],
#         'Pepper': ['Pepper_bell_Bacterial_spot', 'Pepper_bell_Healthy'],
#         'Watermelon': ['watermelon_Anthraconse', 'watermelon_Downy_mildew', 
#                        'watermelon_Healthy', 'watermelon_Virus'],
#         'Pomegranate': ['Pomegrante_Alternaria', 'Pomegrante_Anthraconse', 
#                         'Pomegrante_Bacterail_Blight', 'Pomegrante_Cercospora', 'Pomegrante_Healthy'],
#         'Eggplant': ['Eggplant_Healthy', 'Eggplant_Insect_Pest', 
#                      'Eggplant_LeafSpot', 'Eggplant_White_Mold'],
#         'Custard Apple': ['Custard_Apple_Anthracnose', 'Custard_Apple_Blank_Canker', 
#                           'Custard_Apple_Diplodia_rot', 'Custard_Apple_Leaf_Spot_on_Leaves', 
#                           'Custard_Apple_Mealy_Bug'],
#         'Lemon': ['Leamon_Healthy', 'Leamon_Spider_Mites', 'Leamon_Sooty_Mould', 
#                   'Leamon_Curl_Virus', 'Leamon_Anthraconse']
#     }
#     return render_template('dataset.html', crops=crops)

# @app.route('/feedback', methods=['GET', 'POST'])
# def feedback():
#     """Feedback form page"""
#     if request.method == 'POST':
#         name = request.form.get('name')
#         email = request.form.get('email')
#         phone = request.form.get('phone')
#         message = request.form.get('message')
        
#         # Here you would integrate with EmailJS
#         # For now, we'll just save to a log file
#         feedback_data = {
#             'name': name,
#             'email': email,
#             'phone': phone,
#             'message': message,
#             'timestamp': datetime.now().isoformat()
#         }
        
#         try:
#             # Save feedback to file
#             with open('feedback_log.json', 'a') as f:
#                 json.dump(feedback_data, f)
#                 f.write('\n')
            
#             # In production, integrate with EmailJS here
#             # Send email to admin
            
#             flash('Thank you for your feedback! We will contact you soon.', 'success')
#             return redirect(url_for('feedback'))
#         except Exception as e:
#             flash('Error sending feedback. Please try again.', 'error')
    
#     return render_template('feedback.html')

# @app.route('/tutorial')
# def tutorial():
#     """Tutorial page with YouTube video"""
#     return render_template('tutorial.html')

# @app.route('/predict', methods=['POST'])
# def predict():
#     """Handle image prediction"""
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file uploaded'}), 400
    
#     file = request.files['file']
    
#     if file.filename == '':
#         return jsonify({'error': 'No file selected'}), 400
    
#     if file and allowed_file(file.filename):
#         # Save the uploaded file
#         filename = secure_filename(file.filename)
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(filepath)
        
#         try:
#             # Predict disease
#             disease, confidence = predict_disease(filepath)
            
#             # Get disease information
#             info = disease_info.get(disease, {})
            
#             # Format the response
#             response = {
#                 'success': True,
#                 'filename': filename,
#                 'disease': disease,
#                 'confidence': round(confidence * 100, 2),
#                 'description': info.get('description', 'No description available'),
#                 'causes': info.get('causes', []),
#                 'preventions': info.get('preventions', []),
#                 'treatments': info.get('treatments', []),
#                 'organic_remedies': info.get('organic_remedies', []),
#                 'chemical_controls': info.get('chemical_controls', [])
#             }
            
#             return jsonify(response)
            
#         except Exception as e:
#             return jsonify({'error': f'Prediction failed: {str(e)}'}), 500
    
#     return jsonify({'error': 'Invalid file type. Please upload an image.'}), 400

# @app.route('/capture', methods=['POST'])
# def capture_image():
#     """Handle image capture from camera"""
#     if 'image' not in request.files:
#         return jsonify({'error': 'No image captured'}), 400
    
#     file = request.files['image']
    
#     if file and allowed_file(file.filename):
#         # Save the captured image
#         filename = f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(filepath)
        
#         try:
#             # Predict disease
#             disease, confidence = predict_disease(filepath)
            
#             # Get disease information
#             info = disease_info.get(disease, {})
            
#             # Format the response
#             response = {
#                 'success': True,
#                 'filename': filename,
#                 'disease': disease,
#                 'confidence': round(confidence * 100, 2),
#                 'description': info.get('description', 'No description available'),
#                 'causes': info.get('causes', []),
#                 'preventions': info.get('preventions', []),
#                 'treatments': info.get('treatments', []),
#                 'organic_remedies': info.get('organic_remedies', []),
#                 'chemical_controls': info.get('chemical_controls', [])
#             }
            
#             return jsonify(response)
            
#         except Exception as e:
#             return jsonify({'error': f'Prediction failed: {str(e)}'}), 500
    
#     return jsonify({'error': 'Invalid image format'}), 400

# if __name__ == '__main__':
#     # Create necessary directories
#     os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
#     os.makedirs('model', exist_ok=True)
    
#     app.run(debug=True, host='0.0.0.0', port=5000)





import os
import json
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from config import Config

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('model', exist_ok=True)

# Load disease information
try:
    with open('disease_info.json', 'r') as f:
        disease_info = json.load(f)
    logger.info(f"Loaded information for {len(disease_info)} diseases")
except FileNotFoundError:
    logger.error("disease_info.json not found. Creating empty database.")
    disease_info = {}

# Load the trained model
model = None
def load_disease_model():
    global model
    if model is None:
        try:
            model = load_model(app.config['MODEL_PATH'])
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            model = None
    return model

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def preprocess_image(img_path):
    """Preprocess image for model prediction"""
    try:
        img = image.load_img(img_path, target_size=app.config['IMG_SIZE'])
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)
        return img_array
    except Exception as e:
        logger.error(f"Error preprocessing image: {str(e)}")
        raise

def predict_disease(img_path):
    """Predict disease from image"""
    try:
        model = load_disease_model()
        if model is None:
            raise Exception("Model not loaded")
        
        processed_img = preprocess_image(img_path)
        predictions = model.predict(processed_img)
        predicted_class = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class])
        
        # Get disease names
        disease_names = list(disease_info.keys())
        if predicted_class < len(disease_names):
            predicted_disease = disease_names[predicted_class]
        else:
            predicted_disease = "Unknown_Disease"
        
        return predicted_disease, confidence
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html', crops=app.config['SUPPORTED_CROPS'])

@app.route('/dataset')
def dataset_page():
    """Dataset information page"""
    crops = {
        'Apple': ['Apple_Scab', 'Apple_Black_Rot', 'Apple_Cedar_apple_rust', 'Apple_Healthy'],
        'Cherry': ['Cherry_Healthy', 'Cherry_Brightness_Adjusted', 'Cherry_Constrast_Adjusted'],
        'Corn': ['Corn_Common_rust', 'Corn_Northern_Leaf_Blight', 'Corn_Healthy'],
        'Grape': ['Grape_Black_rot', 'Grape_Esca', 'Grape_Leaf_blight', 'Grape_Healthy'],
        'Tomato': ['Tomato_Early_blight', 'Tomato_Late_blight', 'Tomato_Leaf_Mold', 
                   'Tomato_Septoria_leaf_spot', 'Tomato_Spider_mites', 'Tomato_Healthy'],
        'Potato': ['Potato_Early_blight', 'Potato_Late_blight', 'Potato_Healthy'],
        'Strawberry': ['Strawberry_Leaf_scorch', 'Strawberry_Healthy'],
        'Peach': ['Peach_Bacterial_spot', 'Peach_Healthy'],
        'Pepper': ['Pepper_bell_Bacterial_spot', 'Pepper_bell_Healthy'],
        'Watermelon': ['watermelon_Anthraconse', 'watermelon_Downy_mildew', 
                       'watermelon_Healthy', 'watermelon_Virus'],
        'Pomegranate': ['Pomegrante_Alternaria', 'Pomegrante_Anthraconse', 
                        'Pomegrante_Bacterail_Blight', 'Pomegrante_Cercospora', 'Pomegrante_Healthy'],
        'Eggplant': ['Eggplant_Healthy', 'Eggplant_Insect_Pest', 
                     'Eggplant_LeafSpot', 'Eggplant_White_Mold'],
        'Custard Apple': ['Custard_Apple_Anthracnose', 'Custard_Apple_Blank_Canker', 
                          'Custard_Apple_Diplodia_rot', 'Custard_Apple_Leaf_Spot_on_Leaves', 
                          'Custard_Apple_Mealy_Bug'],
        'Lemon': ['Leamon_Healthy', 'Leamon_Spider_Mites', 'Leamon_Sooty_Mould', 
                  'Leamon_Curl_Virus', 'Leamon_Anthraconse']
    }
    return render_template('dataset.html', crops=crops)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    """Feedback form page"""
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            phone = request.form.get('phone', '').strip()
            subject = request.form.get('subject', 'general')
            message = request.form.get('message', '').strip()
            
            # Validate required fields
            if not name or not email or not message:
                flash('Please fill in all required fields (name, email, message)', 'error')
                return redirect(url_for('feedback'))
            
            # Create feedback entry
            feedback_entry = {
                'name': name,
                'email': email,
                'phone': phone,
                'subject': subject,
                'message': message,
                'timestamp': datetime.now().isoformat(),
                'ip_address': request.remote_addr
            }
            
            # Save to log file
            try:
                with open('feedback_log.json', 'a') as f:
                    json.dump(feedback_entry, f)
                    f.write('\n')
            except Exception as e:
                logger.error(f"Error saving feedback: {str(e)}")
            
            # Prepare email data for EmailJS
            email_data = {
                'service_id': app.config['EMAILJS_SERVICE_ID'],
                'template_id': app.config['EMAILJS_TEMPLATE_ID'],
                'user_id': app.config['EMAILJS_USER_ID'],
                'template_params': {
                    'from_name': name,
                    'from_email': email,
                    'phone': phone,
                    'subject': subject,
                    'message': message,
                    'to_email': app.config['ADMIN_EMAIL'],
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            }
            
            # Note: EmailJS will be handled by frontend JavaScript
            # This backend just saves the data
            
            flash('Thank you for your feedback! We will contact you soon.', 'success')
            return redirect(url_for('feedback'))
            
        except Exception as e:
            logger.error(f"Feedback error: {str(e)}")
            flash('An error occurred. Please try again.', 'error')
    
    return render_template('feedback.html')

@app.route('/tutorial')
def tutorial():
    """Tutorial page"""
    return render_template('tutorial.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle image prediction"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Invalid file type. Please upload JPG, PNG, or JPEG.'}), 400
    
    try:
        # Save the uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Predict disease
        disease, confidence = predict_disease(filepath)
        
        # Get disease information
        info = disease_info.get(disease, {})
        if not info:
            # Try to find similar disease
            for key in disease_info.keys():
                if disease.replace('_', '').lower() in key.replace('_', '').lower():
                    info = disease_info[key]
                    disease = key
                    break
        
        # Format response
        response = {
            'success': True,
            'filename': filename,
            'disease': disease,
            'confidence': round(confidence * 100, 2),
            'description': info.get('description', 'No description available'),
            'causes': info.get('causes', ['Information not available']),
            'preventions': info.get('preventions', ['Information not available']),
            'treatments': info.get('treatments', ['Information not available']),
            'organic_remedies': info.get('organic_remedies', ['Information not available']),
            'chemical_controls': info.get('chemical_controls', ['Information not available'])
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({'success': False, 'error': f'Prediction failed: {str(e)}'}), 500

@app.route('/capture', methods=['POST'])
def capture_image():
    """Handle image capture from camera"""
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No image captured'}), 400
    
    file = request.files['image']
    
    if file and allowed_file(file.filename):
        try:
            # Save the captured image
            filename = f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Predict disease
            disease, confidence = predict_disease(filepath)
            
            # Get disease information
            info = disease_info.get(disease, {})
            if not info:
                for key in disease_info.keys():
                    if disease.replace('_', '').lower() in key.replace('_', '').lower():
                        info = disease_info[key]
                        disease = key
                        break
            
            response = {
                'success': True,
                'filename': filename,
                'disease': disease,
                'confidence': round(confidence * 100, 2),
                'description': info.get('description', 'No description available'),
                'causes': info.get('causes', ['Information not available']),
                'preventions': info.get('preventions', ['Information not available']),
                'treatments': info.get('treatments', ['Information not available']),
                'organic_remedies': info.get('organic_remedies', ['Information not available']),
                'chemical_controls': info.get('chemical_controls', ['Information not available'])
            }
            
            return jsonify(response)
            
        except Exception as e:
            logger.error(f"Capture prediction error: {str(e)}")
            return jsonify({'success': False, 'error': f'Prediction failed: {str(e)}'}), 500
    
    return jsonify({'success': False, 'error': 'Invalid image format'}), 400

@app.route('/api/diseases', methods=['GET'])
def get_diseases():
    """API endpoint to get all diseases"""
    return jsonify({
        'success': True,
        'diseases': list(disease_info.keys()),
        'count': len(disease_info)
    })

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting application on {host}:{port}")
    app.run(host=host, port=port, debug=debug)