





# import os
# import json
# import logging
# from datetime import datetime
# from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
# from werkzeug.utils import secure_filename
# from PIL import Image
# import numpy as np
# import tensorflow as tf
# from tensorflow.keras.preprocessing import image
# from tensorflow.keras.models import load_model
# from config import Config

# # Setup logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

# app = Flask(__name__)
# app.config.from_object(Config)

# # Create necessary directories
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
# os.makedirs('model', exist_ok=True)

# # Load disease information
# try:
#     with open('disease_info.json', 'r') as f:
#         disease_info = json.load(f)
#     logger.info(f"Loaded information for {len(disease_info)} diseases")
# except FileNotFoundError:
#     logger.error("disease_info.json not found. Creating empty database.")
#     disease_info = {}

# # Load the trained model
# model = None
# def load_disease_model():
#     global model
#     if model is None:
#         try:
#             model = load_model(app.config['MODEL_PATH'])
#             logger.info("Model loaded successfully")
#         except Exception as e:
#             logger.error(f"Failed to load model: {str(e)}")
#             model = None
#     return model

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# def preprocess_image(img_path):
#     """Preprocess image for model prediction"""
#     try:
#         img = image.load_img(img_path, target_size=app.config['IMG_SIZE'])
#         img_array = image.img_to_array(img)
#         img_array = np.expand_dims(img_array, axis=0)
#         img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)
#         return img_array
#     except Exception as e:
#         logger.error(f"Error preprocessing image: {str(e)}")
#         raise

# def predict_disease(img_path):
#     """Predict disease from image"""
#     try:
#         model = load_disease_model()
#         if model is None:
#             raise Exception("Model not loaded")
        
#         processed_img = preprocess_image(img_path)
#         predictions = model.predict(processed_img)
#         predicted_class = np.argmax(predictions[0])
#         confidence = float(predictions[0][predicted_class])
        
#         # Get disease names
#         disease_names = list(disease_info.keys())
#         if predicted_class < len(disease_names):
#             predicted_disease = disease_names[predicted_class]
#         else:
#             predicted_disease = "Unknown_Disease"
        
#         return predicted_disease, confidence
#     except Exception as e:
#         logger.error(f"Prediction error: {str(e)}")
#         raise

# @app.route('/')
# def index():
#     """Home page"""
#     return render_template('index.html', crops=app.config['SUPPORTED_CROPS'])

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
#         try:
#             name = request.form.get('name', '').strip()
#             email = request.form.get('email', '').strip()
#             phone = request.form.get('phone', '').strip()
#             subject = request.form.get('subject', 'general')
#             message = request.form.get('message', '').strip()
            
#             # Validate required fields
#             if not name or not email or not message:
#                 flash('Please fill in all required fields (name, email, message)', 'error')
#                 return redirect(url_for('feedback'))
            
#             # Create feedback entry
#             feedback_entry = {
#                 'name': name,
#                 'email': email,
#                 'phone': phone,
#                 'subject': subject,
#                 'message': message,
#                 'timestamp': datetime.now().isoformat(),
#                 'ip_address': request.remote_addr
#             }
            
#             # Save to log file
#             try:
#                 with open('feedback_log.json', 'a') as f:
#                     json.dump(feedback_entry, f)
#                     f.write('\n')
#             except Exception as e:
#                 logger.error(f"Error saving feedback: {str(e)}")
            
#             # Prepare email data for EmailJS
#             email_data = {
#                 'service_id': app.config['EMAILJS_SERVICE_ID'],
#                 'template_id': app.config['EMAILJS_TEMPLATE_ID'],
#                 'user_id': app.config['EMAILJS_USER_ID'],
#                 'template_params': {
#                     'from_name': name,
#                     'from_email': email,
#                     'phone': phone,
#                     'subject': subject,
#                     'message': message,
#                     'to_email': app.config['ADMIN_EMAIL'],
#                     'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#                 }
#             }
            
#             # Note: EmailJS will be handled by frontend JavaScript
#             # This backend just saves the data
            
#             flash('Thank you for your feedback! We will contact you soon.', 'success')
#             return redirect(url_for('feedback'))
            
#         except Exception as e:
#             logger.error(f"Feedback error: {str(e)}")
#             flash('An error occurred. Please try again.', 'error')
    
#     return render_template('feedback.html')

# @app.route('/tutorial')
# def tutorial():
#     """Tutorial page"""
#     return render_template('tutorial.html')

# @app.route('/predict', methods=['POST'])
# def predict():
#     """Handle image prediction"""
#     if 'file' not in request.files:
#         return jsonify({'success': False, 'error': 'No file uploaded'}), 400
    
#     file = request.files['file']
    
#     if file.filename == '':
#         return jsonify({'success': False, 'error': 'No file selected'}), 400
    
#     if not allowed_file(file.filename):
#         return jsonify({'success': False, 'error': 'Invalid file type. Please upload JPG, PNG, or JPEG.'}), 400
    
#     try:
#         # Save the uploaded file
#         filename = secure_filename(file.filename)
#         timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#         filename = f"{timestamp}_{filename}"
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(filepath)
        
#         # Predict disease
#         disease, confidence = predict_disease(filepath)
        
#         # Get disease information
#         info = disease_info.get(disease, {})
#         if not info:
#             # Try to find similar disease
#             for key in disease_info.keys():
#                 if disease.replace('_', '').lower() in key.replace('_', '').lower():
#                     info = disease_info[key]
#                     disease = key
#                     break
        
#         # Format response
#         response = {
#             'success': True,
#             'filename': filename,
#             'disease': disease,
#             'confidence': round(confidence * 100, 2),
#             'description': info.get('description', 'No description available'),
#             'causes': info.get('causes', ['Information not available']),
#             'preventions': info.get('preventions', ['Information not available']),
#             'treatments': info.get('treatments', ['Information not available']),
#             'organic_remedies': info.get('organic_remedies', ['Information not available']),
#             'chemical_controls': info.get('chemical_controls', ['Information not available'])
#         }
        
#         return jsonify(response)
        
#     except Exception as e:
#         logger.error(f"Prediction error: {str(e)}")
#         return jsonify({'success': False, 'error': f'Prediction failed: {str(e)}'}), 500

# @app.route('/capture', methods=['POST'])
# def capture_image():
#     """Handle image capture from camera"""
#     if 'image' not in request.files:
#         return jsonify({'success': False, 'error': 'No image captured'}), 400
    
#     file = request.files['image']
    
#     if file and allowed_file(file.filename):
#         try:
#             # Save the captured image
#             filename = f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
#             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(filepath)
            
#             # Predict disease
#             disease, confidence = predict_disease(filepath)
            
#             # Get disease information
#             info = disease_info.get(disease, {})
#             if not info:
#                 for key in disease_info.keys():
#                     if disease.replace('_', '').lower() in key.replace('_', '').lower():
#                         info = disease_info[key]
#                         disease = key
#                         break
            
#             response = {
#                 'success': True,
#                 'filename': filename,
#                 'disease': disease,
#                 'confidence': round(confidence * 100, 2),
#                 'description': info.get('description', 'No description available'),
#                 'causes': info.get('causes', ['Information not available']),
#                 'preventions': info.get('preventions', ['Information not available']),
#                 'treatments': info.get('treatments', ['Information not available']),
#                 'organic_remedies': info.get('organic_remedies', ['Information not available']),
#                 'chemical_controls': info.get('chemical_controls', ['Information not available'])
#             }
            
#             return jsonify(response)
            
#         except Exception as e:
#             logger.error(f"Capture prediction error: {str(e)}")
#             return jsonify({'success': False, 'error': f'Prediction failed: {str(e)}'}), 500
    
#     return jsonify({'success': False, 'error': 'Invalid image format'}), 400

# @app.route('/api/diseases', methods=['GET'])
# def get_diseases():
#     """API endpoint to get all diseases"""
#     return jsonify({
#         'success': True,
#         'diseases': list(disease_info.keys()),
#         'count': len(disease_info)
#     })

# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404

# @app.errorhandler(500)
# def internal_error(e):
#     return render_template('500.html'), 500

# if __name__ == '__main__':
#     port = int(os.getenv('PORT', 5000))
#     host = os.getenv('HOST', '0.0.0.0')
#     debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
#     logger.info(f"Starting application on {host}:{port}")

#     app.run(host=host, port=port, debug=debug)































import os
import json
import smtplib
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

import smtplib
from email.message import EmailMessage

def send_feedback_email(name, email, contact, category, subject, message, rating):
    admin_email = "dokkaridileep02@gmail.com"

    msg = EmailMessage()
    msg["Subject"] = f"New Feedback: {subject}"
    msg["From"] = email
    msg["To"] = admin_email

    msg.set_content(f"""
Name: {name}
Email: {email}
Contact: {contact}
Category: {category}
Rating: {rating}

Message:
{message}
""")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login("dokkaridileep02@gmail.com", "wtgnntcqksxsipdb")
        server.send_message(msg)


# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'aJPsrKrxlGlGEXb0jFSNY')

# Email Configuration - REMOVED SPACE from password!
GMAIL_USER = os.getenv('GMAIL_USER', 'dokkaridileep02@gmail.com')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD', 'wtgnntcqksxsipdb')  # NO SPACE at beginning!
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'dokkaridileep02@gmail.com')

# Ensure logs directory exists
if not os.path.exists('logs'):
    os.makedirs('logs')

def send_simple_email(form_data):
    """Send email using SMTP"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = ADMIN_EMAIL
        msg['Subject'] = f"New Feedback: {form_data.get('subject', 'No Subject')}"
        
        # Create email body
        body = f"""
        NEW FEEDBACK RECEIVED
        
        Name: {form_data.get('name', 'Not provided')}
        Email: {form_data.get('email', 'Not provided')}
        Phone: {form_data.get('contact', 'Not provided')}
        
        Feedback Type: {form_data.get('category', 'Not specified')}
        Rating: {form_data.get('rating', 'Not rated')}/5
        Subject: {form_data.get('subject', 'No subject')}
        
        Message:
        {form_data.get('message', 'No message')}
        
        Subscribe to updates: {'Yes' if form_data.get('subscribe') else 'No'}
        
        Submitted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        return True, "Email sent successfully"
        
    except smtplib.SMTPAuthenticationError:
        return False, "SMTP Authentication failed. Check your App Password."
    except Exception as e:
        return False, f"Email error: {str(e)}"

def save_feedback(form_data):
    """Save feedback to JSON file"""
    try:
        log_file = 'logs/feedback.json'
        
        # Read existing data
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                try:
                    data = json.load(f)
                except:
                    data = []
        else:
            data = []
        
        # Add new feedback
        form_data['timestamp'] = datetime.now().isoformat()
        form_data['id'] = len(data) + 1
        data.append(form_data)
        
        # Save back
        with open(log_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        return True, f"Feedback saved (ID: {form_data['id']})"
    except Exception as e:
        return False, f"Save error: {str(e)}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        contact = request.form.get("contact")
        category = request.form.get("category")
        subject = request.form.get("subject")
        message = request.form.get("message")
        rating = request.form.get("rating")

        # Save feedback locally
        # Inside your /feedback POST route
        success, message = send_simple_email({
            "name": name,
            "email": email,
            "contact": contact,
            "category": category,
            "subject": subject,
            "message": message,
            "rating": rating,
            "subscribe": request.form.get("subscribe")
        })
        print(f"📧 Email sent? {success} - {message}")


        # Send email
        try:
            email_success, email_message = send_simple_email({
                "name": name,
                "email": email,
                "contact": contact,
                "category": category,
                "subject": subject,
                "message": message,
                "rating": rating,
                "subscribe": request.form.get("subscribe")
            })
        except Exception as e:
            email_success, email_message = False, str(e)

        # Provide feedback to user
        if email_success:
            return render_template("feedback.html", msg="✅ Feedback sent successfully!")
        else:
            return render_template("feedback.html", msg=f"⚠️ Feedback saved but email failed: {email_message}")

    return render_template("feedback.html")

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    try:
        # Get form data
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
        
        print("📨 Received feedback:", data)
        
        # Validate required fields
        required = ['name', 'email', 'subject', 'message']
        missing = [field for field in required if not data.get(field)]
        
        if missing:
            return jsonify({
                'success': False,
                'message': f'Missing fields: {", ".join(missing)}'
            }), 400
        
        # Save feedback
        save_success, save_message = save_feedback(data)
        print(f"💾 Save result: {save_success} - {save_message}")
        
        # Try to send email
        if GMAIL_APP_PASSWORD:
            email_success, email_message = send_simple_email(data)
            print(f"📧 Email result: {email_success} - {email_message}")
            
            if email_success:
                return jsonify({
                    'success': True,
                    'message': 'Feedback submitted successfully! Email sent.',
                    'feedback_id': data.get('id')
                })
            else:
                # Email failed but data saved
                return jsonify({
                    'success': True,
                    'message': 'Feedback saved but email failed.',
                    'warning': email_message,
                    'feedback_id': data.get('id')
                })
        else:
            # No email password configured
            return jsonify({
                'success': True,
                'message': 'Feedback saved. Email not configured.',
                'feedback_id': data.get('id')
            })
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

@app.route('/test-email')
def test_email():
    """Test email endpoint"""
    try:
        test_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Email',
            'message': 'This is a test email from the system.',
            'category': 'test',
            'rating': '5'
        }
        
        if not GMAIL_APP_PASSWORD:
            return jsonify({
                'success': False,
                'message': 'GMAIL_APP_PASSWORD not configured in .env file'
            })
        
        success, message = send_simple_email(test_data)
        
        return jsonify({
            'success': success,
            'message': message
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })

@app.route('/check-feedback')
def check_feedback():
    """Check saved feedback"""
    try:
        log_file = 'logs/feedback.json'
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                data = json.load(f)
            return jsonify({
                'success': True,
                'count': len(data),
                'feedback': data
            })
        else:
            return jsonify({
                'success': True,
                'count': 0,
                'feedback': []
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })

# Routes for dataset and tutorial - LOADING FROM TEMPLATES
@app.route('/dataset')
def dataset():
    """Render dataset page from templates"""
    try:
        return render_template('dataset.html')
    except Exception as e:
        return f"""
        <html>
        <head><title>Dataset Page</title></head>
        <body>
            <h1>Dataset Page</h1>
            <p>Error loading dataset.html: {str(e)}</p>
            <p>Make sure dataset.html exists in the templates folder.</p>
        </body>
        </html>
        """

@app.route('/tutorial')
def tutorial():
    """Render tutorial page from templates"""
    try:
        return render_template('tutorial.html')
    except Exception as e:
        return f"""
        <html>
        <head><title>Tutorial Page</title></head>
        <body>
            <h1>Tutorial Page</h1>
            <p>Error loading tutorial.html: {str(e)}</p>
            <p>Make sure tutorial.html exists in the templates folder.</p>
        </body>
        </html>
        """

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')

# Error handlers to avoid TemplateNotFound errors
@app.errorhandler(404)
def page_not_found(e):
    return """
    <html>
    <head><title>404 - Page Not Found</title></head>
    <body>
        <h1>404 - Page Not Found</h1>
        <p>The page you are looking for does not exist.</p>
        <p><a href="/">Go to Home Page</a></p>
    </body>
    </html>
    """, 404

@app.errorhandler(500)
def internal_server_error(e):
    return """
    <html>
    <head><title>500 - Internal Server Error</title></head>
    <body>
        <h1>500 - Internal Server Error</h1>
        <p>Something went wrong on our server.</p>
        <p><a href="/">Go to Home Page</a></p>
    </body>
    </html>
    """, 500

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Starting AgriDetect System")
    print("=" * 60)
    
    # Check email configuration
    if not GMAIL_APP_PASSWORD:
        print("⚠️ WARNING: GMAIL_APP_PASSWORD not set in .env file")
        print("   Emails will NOT be sent without this.")
        print("\n📋 Steps to configure:")
        print("   1. Enable 2-Step Verification on Google")
        print("   2. Generate an App Password")
        print("   3. Add to .env: GMAIL_APP_PASSWORD=your-16-char-password")
    else:
        print(f"✅ Email configured for: {GMAIL_USER}")
    
    # Test the password
    print("\n🔧 Testing email configuration...")
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.quit()
        print("✅ Email authentication successful!")
    except Exception as e:
        print(f"❌ Email authentication failed: {e}")
        print("   Make sure your App Password is correct and 2-Step Verification is enabled.")
    
    print(f"\n🌐 Server running on: http://localhost:5000")
    print(f"📧 Admin email: {ADMIN_EMAIL}")
    print("\n📋 Available routes:")
    print("   /               - Home page")
    print("   /feedback       - Feedback form")
    print("   /submit-feedback - Submit feedback")
    print("   /test-email     - Test email")
    print("   /check-feedback - View saved feedback")
    print("   /dataset        - Dataset page (from templates/dataset.html)")
    print("   /tutorial       - Tutorial page (from templates/tutorial.html)")
    print("\n🔧 Debug: Add ?test=1 to any URL for debug info")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
