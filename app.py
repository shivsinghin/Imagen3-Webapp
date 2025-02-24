# app.py
# Import required libraries and modules
from flask import Flask, render_template, request, jsonify, url_for
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
import base64

# Initialize Flask application
app = Flask(__name__, static_folder='static')

# Google Cloud Project ID
PROJECT_ID = "your-googlecloud-project-id-here"

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route for image generation API endpoint
@app.route('/generate', methods=['POST'])
def generate_image():
    try:
        # Extract parameters from the request JSON
        data = request.json
        prompt = data.get('prompt')
        negative_prompt = data.get('negative_prompt')
        seed = int(data.get('seed', 100))
        number_of_images = int(data.get('number_of_images', 1))
        aspect_ratio = data.get('aspect_ratio', '1:1')

        # Initialize Vertex AI with project settings
        vertexai.init(project=PROJECT_ID, location="us-central1")
        
        # Load the Imagen 3.0 model
        model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")

        # Generate images using the model
        images = model.generate_images(
            prompt=prompt,
            negative_prompt=negative_prompt,
            number_of_images=number_of_images,
            language="en",
            add_watermark=False,
            seed=seed,
            aspect_ratio=aspect_ratio,
            safety_filter_level="off",
            person_generation="allow_adult",
        )

        # Convert generated images to base64 format
        image_data = []
        for img in images:
            base64_image = base64.b64encode(img._image_bytes).decode('utf-8')
            image_data.append(base64_image)

        # Return success response with encoded images
        return jsonify({'success': True, 'images': image_data})
    except Exception as e:
        # Return error response if generation fails
        return jsonify({'success': False, 'error': str(e)})
    
# Run the Flask application in debug mode if executed directly
if __name__ == '__main__':
    app.run(debug=True)