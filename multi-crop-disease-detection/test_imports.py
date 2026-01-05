try:
    print('Testing imports...')
    
    # Basic Python
    import os
    import json
    import traceback
    
    # Flask and web
    from flask import Flask, render_template, request, jsonify, send_from_directory
    from flask_cors import CORS
    from werkzeug.utils import secure_filename
    
    # Environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Image processing
    from PIL import Image
    import numpy as np
    
    # ML/AI
    import tensorflow as tf
    import cv2
    
    print('✓ All imports successful!')
    
except ImportError as e:
    print(f'✗ Missing module: {e.name}')
    print(f'  Install with: pip install {e.name}')
except Exception as e:
    print(f'✗ Error: {e}')
