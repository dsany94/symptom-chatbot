# 🩺 AI-Powered Symptom Checker Chatbot

A **Streamlit-based healthcare chatbot** that uses **OpenAI's GPT-3.5 model** to analyze user-reported symptoms and recommend possible actions. It also suggests the **appropriate type of doctor** to consult and provides a **location-based map search** to find nearby specialists.

---

## 🚀 Features

- Step-by-step symptom intake
- GPT-3.5 generated insights and recommendations
- Extracts relevant specialist using **regex**
- Real-time doctor map lookup based on user ZIP code
- Clean UI with a two-step form experience
- Privacy protection with environment variable-based API usage

---

## 🧠 Technologies Used

- `streamlit`
- `openai`
- `python-dotenv`
- `re` (for regex-based doctor extraction)

---

## 📦 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/dsany94/symptom-chatbot.git
cd symptom-chatbot

### 2. Create and activate a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate     # Mac/Linux
venv\Scripts\activate        # Windows

### 3. Install the required libraries

```bash
pip install -r requirements.txt


### 4. Set up your .env file securely
- Create a .env file in the root directory and add your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_key_here

## Running the app
- Run the Streamlit app using:

```bash
streamlit run symptom_chatbot.py


---

## 🔐 Privacy & Security

- The API key is never hardcoded. It is loaded securely via python-dotenv.
- The .env file is added to .gitignore to prevent accidental exposure.
- No user data is stored or transmitted beyond the OpenAI API call.
- ZIP code-based location lookup uses Google Maps links, not backend storage.

---

## 📸 Demo
[▶️ Click to watch the demo](https://github.com/dsany94/symptom-chatbot/blob/main/symptom_checker_demo.mp4)


---

🤖 Future Improvements

- Add symptom category auto-detection using embeddings
- Allow multilingual input via translation
- Integrate with public health APIs for more structured data

---

## Acknowledgments

- OpenAI for GPT-3.5 API
- CDC and healthdata.gov for public health data guidelines
- Streamlit for a quick and beautiful front-end

---



