🌾 Crop Prediction & Disease Detection Web Application

An AI-powered web application for farmers and agricultural enthusiasts to predict the most suitable crops based on environmental factors and detect plant diseases through image analysis.
Built with Django (backend), React (frontend), and integrated machine learning models for accurate recommendations and early disease detection.

🚀 Features

✅ Crop Recommendation:
Predict the best crop to cultivate based on soil nutrients (N, P, K), temperature, humidity, pH, and rainfall.

🦠 Disease Detection:
Upload plant leaf images to detect common diseases and get actionable treatment advice.

🧠 AI Integration:
Machine learning models trained on real agricultural datasets for high prediction accuracy.

🌐 Responsive Frontend:
Clean and modern UI built with React for seamless user experience.

⚙️ RESTful API:
Backend APIs built with Django REST Framework for smooth communication between frontend and backend.

🛠️ Tech Stack
Frontend: React.js, Tailwind CSS 

Backend: Django, Django REST Framework

AI Models:

Crop Prediction: RandomForest 

Disease Detection: CNN trained on PlantVillage dataset 

Database: SQLite 

Others: TensorFlow / PyTorch, Scikit-learn


🚀 Getting Started
Prerequisites
Python 3.x

Node.js and npm

pip / virtualenv

Backend Setup
bash
Copy
Edit
# Clone the repository
git clone https://github.com/your-username/your-repo.git
cd your-repo/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start backend server
python manage.py runserver
Frontend Setup
bash
Copy
Edit
cd your-repo/frontend

# Install dependencies
npm install

# Start frontend server
npm start
Access the App
Open your browser and navigate to:
http://localhost:3000/ — React frontend
http://localhost:8000/api/ — Django API

🧩 API Endpoints
POST /api/predict-crop/ — Crop prediction

POST /api/detect-disease/ — Disease detection


🧠 Model Training

Collected dataset from PlantVillage Dataset

Preprocessed data using pandas, OpenCV

Trained models using Scikit-learn 

Saved models as .pkl / .h5 files and integrated into Django backend

🤝 Contributing
Contributions are welcome!
Feel free to fork this repo, create a new branch, and submit a pull request.

📄 License
This project is licensed under the MIT License — see the LICENSE file for details.

🙌 Acknowledgements
PlantVillage Dataset

Scikit-learn

TensorFlow

Django

React

🌟 Show Your Support
If you like this project, give it a ⭐️ and share it with others!
