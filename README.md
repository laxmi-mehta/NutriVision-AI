## **Overview**  
NutriVision is an AI-powered **Food Nutritional Analysis System** that helps users analyze their food intake by simply uploading images. The platform identifies the food item and provides its **caloric and nutritional breakdown**, making it easier for users to track their diet.  

🔹 **Image Recognition:** Automatically detects food items from images.  
🔹 **Nutritional Analysis:** Displays calories, protein, carbs, and fats.  
🔹 **Recipe Recommendations:** Suggests healthy meal options.  
🔹 **Community Forum:** Users can share food experiences and recipes.  
🔹 **User Profiles:** Stores past analyses for easy tracking.  

---

## **Tech Stack**  

| Technology        | Purpose |
|------------------|---------|
| **Python (Django)** | Backend Development |
| **MongoDB** | Database for storing user and food data |
| **TensorFlow & OpenCV** | Machine Learning Model for food detection |
| **HTML** | Frontend UI |
| **Tailwind CSS** | Styling |

---

## **Features**  

### 1️⃣ **User Authentication**  
- Secure login & registration  
- Profile management
![NutriVision-7](https://github.com/user-attachments/assets/914c56fe-1dc7-47f2-ab39-4f2121b24f34)
![NutriVision-8](https://github.com/user-attachments/assets/12c63ac2-7087-482d-9755-d91eda12bede)

### 2️⃣ **Food Image Analysis**  
- Upload an image of food  
- AI model detects the food type  
- Retrieves calorie, protein, fat, and carbohydrate data  
![NutriVision-1](https://github.com/user-attachments/assets/759ee10f-e817-44e2-a1af-3ece6fda5d37)
![NutriVision-5](https://github.com/user-attachments/assets/1bb4c08e-31ee-46ac-aff8-3b7091910070)

### 3️⃣ **Barcode Scanner**  
- Scan food packaging to retrieve nutritional details
   ![NutriVision-2](https://github.com/user-attachments/assets/88551759-8303-4355-97b3-c010fc16d48f)


### 4️⃣ **Recipe Recommendations**  
- Personalized meal suggestions based on user preferences  
  ![NutriVision-3](https://github.com/user-attachments/assets/f4d3a090-3cc3-4309-b771-7d3facbea289)


### 5️⃣ **Community Forum**  
- Users can post food experiences & discuss diets  
![NutriVision-4](https://github.com/user-attachments/assets/da0ebc39-13b9-47b6-8591-8b8b42dfdd0d)

### 5️⃣ **NutriBot - Customize Chatbot**  
- This is NutriBot which gives answers to health related questions.
  
![NutriVision-6](https://github.com/user-attachments/assets/4742d8fc-7833-4d51-86d6-14c3d03e3367)


### 6️⃣ **Admin Dashboard**  
- Manage users
 
![NutriVision-9](https://github.com/user-attachments/assets/85375dc4-bafd-49bb-bd06-cf80ef20375e)

---

## **Project Setup (Installation Guide)**  

### **1️⃣ Clone the Repository**  
```sh
git clone https://github.com/yourusername/NutriVision.git
cd NutriVision
```
2️⃣ Setup Backend (Django & MongoDB)
Install Dependencies
```sh
pip install -r backend/requirements.txt
Set Up MongoDB
Install MongoDB.
```

Run MongoDB server:

```sh
mongod --dbpath=<your_database_path>
Update backend/settings.py with your MongoDB connection.
```

Run Django Server
```sh
python manage.py runserver
```

Future Enhancements

✅ Mobile App Version 📱

✅ Wearable Device Integration ⌚

✅ Multi-Language Support 🌍

✅ Voice Commands 🎙️
