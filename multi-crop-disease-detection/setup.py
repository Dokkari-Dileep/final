#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_banner():
    print("=" * 60)
    print("🌿 Multi-Crop Disease Detection System - Setup")
    print("=" * 60)

def check_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 8):
        print(f"❌ Python 3.8 or higher is required. Current: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version}")

def create_directory_structure():
    """Create project directory structure"""
    print("\n📁 Creating directory structure...")
    
    directories = [
        'static/images',
        'static/css',
        'static/js',
        'static/uploads',
        'templates',
        'model',
        'dataset'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {directory}")
    
    # Create .gitkeep in uploads
    (Path('static/uploads') / '.gitkeep').touch()

def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        print("   Trying alternative method...")
        
        # Try installing individually
        packages = [
            'Flask==2.3.3',
            'tensorflow==2.13.0',
            'numpy==1.24.3',
            'pillow==10.0.0',
            'opencv-python==4.8.0.74',
            'python-dotenv==1.0.0',
            'requests==2.31.0',
            'matplotlib==3.7.2'
        ]
        
        for package in packages:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"   ✅ {package}")
            except:
                print(f"   ⚠️  Failed to install {package}")

def create_env_file():
    """Create .env file if it doesn't exist"""
    print("\n⚙️  Creating environment file...")
    
    env_file = Path('.env')
    if not env_file.exists():
        env_content = """# Flask Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production-123456

# EmailJS Configuration (Sign up at https://www.emailjs.com/)
EMAILJS_USER_ID=your_user_id_here
EMAILJS_SERVICE_ID=your_service_id_here
EMAILJS_TEMPLATE_ID=your_template_id_here

# Admin Email
ADMIN_EMAIL=admin@example.com

# Application Settings
DEBUG=True
PORT=5000
HOST=0.0.0.0
"""
        env_file.write_text(env_content)
        print("✅ Created .env file")
        print("   ⚠️  Remember to update EMAILJS credentials")
    else:
        print("✅ .env file already exists")

def create_disease_info():
    """Create disease_info.json if it doesn't exist"""
    print("\n🏥 Creating disease database...")
    
    disease_file = Path('disease_info.json')
    if not disease_file.exists():
        # Basic template - will be expanded during training
        basic_info = {
            "Apple_Scab": {
                "description": "A fungal disease affecting apple leaves and fruit",
                "causes": ["Fungus Venturia inaequalis", "Wet spring weather", "Poor air circulation"],
                "preventions": ["Plant resistant varieties", "Proper pruning for air flow", "Remove fallen leaves"],
                "treatments": ["Apply fungicides early spring", "Copper-based sprays", "Sulfur-based treatments"],
                "organic_remedies": ["Neem oil spray", "Baking soda solution", "Garlic extract"],
                "chemical_controls": ["Myclobutanil", "Trifloxystrobin", "Captan"]
            }
        }
        
        with open('disease_info.json', 'w') as f:
            json.dump(basic_info, f, indent=2)
        print("✅ Created disease_info.json")
    else:
        print("✅ disease_info.json already exists")

def create_feedback_log():
    """Create feedback_log.json if it doesn't exist"""
    print("\n📝 Creating feedback log...")
    
    feedback_file = Path('feedback_log.json')
    if not feedback_file.exists():
        with open('feedback_log.json', 'w') as f:
            json.dump([], f)
        print("✅ Created feedback_log.json")
    else:
        print("✅ feedback_log.json already exists")

def create_placeholder_images():
    """Create placeholder images"""
    print("\n🖼️  Creating placeholder images...")
    
    images_dir = Path('static/images')
    
    # Create a simple placeholder image using PIL if available
    try:
        from PIL import Image, ImageDraw, ImageFont
        import numpy as np
        
        # Create placeholder images
        sizes = {
            'background.jpg': (1920, 1080),
            'dataset-bg.jpg': (1920, 1080),
            'feedback-bg.jpg': (1920, 1080),
            'tutorial-bg.jpg': (1920, 1080),
            'logo.png': (512, 512)
        }
        
        for filename, size in sizes.items():
            if not (images_dir / filename).exists():
                # Create gradient background
                img = Image.new('RGB', size, color='white')
                draw = ImageDraw.Draw(img)
                
                # Draw gradient
                for i in range(size[1]):
                    r = int(40 + (215 * i / size[1]))
                    g = int(167 + (88 * i / size[1]))
                    b = int(69 + (186 * i / size[1]))
                    draw.line([(0, i), (size[0], i)], fill=(r, g, b))
                
                # Add text
                try:
                    font = ImageFont.truetype("arial.ttf", 60)
                except:
                    font = ImageFont.load_default()
                
                text = filename.replace('.', ' ').upper()
                text_width = draw.textlength(text, font=font)
                position = ((size[0] - text_width) // 2, size[1] // 2)
                draw.text(position, text, fill='white', font=font)
                
                img.save(images_dir / filename)
                print(f"   ✅ Created {filename}")
                
    except ImportError:
        print("   ⚠️  PIL not installed, skipping image creation")

def create_sample_dataset():
    """Create sample dataset structure"""
    print("\n📊 Creating sample dataset structure...")
    
    diseases = [
        'Apple_Scab',
        'Apple_Black_Rot',
        'Apple_Cedar_apple_rust',
        'Apple_Healthy',
        'Tomato_Early_blight',
        'Tomato_Late_blight',
        'Tomato_Healthy',
        'Potato_Early_blight',
        'Potato_Late_blight',
        'Potato_Healthy'
    ]
    
    dataset_dir = Path('dataset')
    for disease in diseases:
        disease_dir = dataset_dir / disease
        disease_dir.mkdir(parents=True, exist_ok=True)
        
        # Create README file in each folder
        readme = disease_dir / 'README.md'
        if not readme.exists():
            readme.write_text(f"# {disease}\n\nPlace your images for {disease} in this folder.")
    
    print(f"✅ Created {len(diseases)} disease folders")
    print("   ⚠️  Add your images to these folders before training")

def create_templates():
    """Create HTML templates"""
    print("\n📄 Creating HTML templates...")
    
    templates_dir = Path('templates')
    
    # Create base.html
    base_html = templates_dir / 'base.html'
    if not base_html.exists():
        base_html.write_text("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}AgriDetect{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>""")
        print("   ✅ Created base.html")
    
    # Create other templates
    for template in ['index.html', 'dataset.html', 'feedback.html', 'tutorial.html']:
        template_file = templates_dir / template
        if not template_file.exists():
            template_file.write_text(f"""{{% extends "base.html" %}}

{{% block title %}}{template.replace('.html', '') | title}{{% endblock %}}

{{% block content %}}
<h1>{template.replace('.html', '') | title} Page</h1>
<p>This is the {template.replace('.html', '')} page.</p>
{{% endblock %}}""")
            print(f"   ✅ Created {template}")

def create_css_file():
    """Create CSS file"""
    print("\n🎨 Creating CSS file...")
    
    css_file = Path('static/css/style.css')
    if not css_file.exists():
        css_file.write_text("""/* Basic styles - will be updated */
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}""")
        print("   ✅ Created style.css")

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    check_python_version()
    
    # Create directory structure
    create_directory_structure()
    
    # Install dependencies
    install_dependencies()
    
    # Create configuration files
    create_env_file()
    create_disease_info()
    create_feedback_log()
    
    # Create assets
    create_placeholder_images()
    create_sample_dataset()
    create_templates()
    create_css_file()
    
    # Final instructions
    print("\n" + "=" * 60)
    print("🎉 Setup Complete!")
    print("=" * 60)
    print("\n📋 Next Steps:")
    print("1. Update .env file with your EmailJS credentials")
    print("2. Add your dataset images to the 'dataset/' folder")
    print("3. Train the model: python train_model.py")
    print("4. Run the application: python app.py")
    print("5. Access at: http://localhost:5000")
    print("\n📧 EmailJS Setup:")
    print("   - Sign up at https://www.emailjs.com/")
    print("   - Create a service (Gmail recommended)")
    print("   - Create a template with variables:")
    print("     {{from_name}}, {{from_email}}, {{phone}},")
    print("     {{subject}}, {{message}}, {{to_email}}")
    print("   - Get your User ID, Service ID, and Template ID")
    print("\n🌿 Happy Farming! 🚜")

if __name__ == '__main__':
    main()