from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from openai import OpenAI

app = Flask(__name__)
app.secret_key = "hospital_ai_final_system_2026"

# =========================
# OPENAI CLIENT
# =========================
client = OpenAI(
    api_key="YOUR_API_KEY_HERE"
)

# =========================
# GPT DOCTOR
# =========================
def gpt_doctor(question):

    try:

        response = client.chat.completions.create(

            model="gpt-4o-mini",

            messages=[

                {
                    "role": "system",
                    "content": """
                    You are a safe AI medical assistant.
                    Give short medical advice.
                    Recommend hospital for dangerous symptoms.
                    """
                },

                {
                    "role": "user",
                    "content": question
                }

            ]

        )

        return response.choices[0].message.content

    except Exception as e:

        return f"""
        <div class='glass-card'>
            ❌ AI Error:
            <br><br>
            {e}
        </div>
        """

# =========================
# DATABASE
# =========================
def init_db():

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    # USERS TABLE
    c.execute("""

        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT

        )

    """)

    # HISTORY TABLE
    c.execute("""

        CREATE TABLE IF NOT EXISTS diagnosis_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            symptoms TEXT,
            result TEXT

        )

    """)

    conn.commit()
    conn.close()

init_db()

# =========================
# SYMPTOMS
# =========================
ALL_SYMPTOMS = [

    "fever",
    "high fever",
    "chills",
    "fatigue",
    "weakness",
    "headache",
    "cough",
    "dry cough",
    "wet cough",
    "shortness of breath",
    "difficulty breathing",
    "chest pain",
    "runny nose",
    "blocked nose",
    "sneezing",
    "sore throat",
    "stomach pain",
    "vomiting",
    "diarrhea",
    "nausea",
    "loss of appetite",
    "body pain",
    "joint pain",
    "back pain",
    "dizziness",
    "blurred vision",
    "confusion",
    "sweating",
    "rash",
    "itching",
    "ear pain",
    "red eyes",
    "watery eyes",
    "frequent urination",
    "painful urination",
    "dark urine",
    "paralysis",
    "loss of consciousness",
    "severe bleeding"
"high fever",
"dry cough",
"wet cough",
"difficulty breathing",
"dark urine",
"loss of consciousness",
"severe bleeding",
"high fever",
"dry cough",
"wet cough",
"difficulty breathing",
"dark urine",
"loss of consciousness",
"severe bleeding",
"weight loss",
"dehydration",
"stiff neck",
"burning urination",
"swollen joints",
"muscle pain",
"abdominal pain",
"yellow eyes",
"yellow skin",
"fainting",
"rapid heartbeat",
"night sweats",
"difficulty walking",
"loss of balance",
"swollen glands",
"skin peeling",
"mouth sores",
"loss of smell",
"loss of taste",
"chest tightness",
"bloated stomach",
"cold hands",
"cold feet",
"face swelling",
"leg swelling",
"memory loss",
"hallucinations",
"shivering",
"blood in urine",
"blood in stool",
"constipation",
"dry mouth",
"burning chest",
"excess thirst",
"swollen eyes",
"pain behind eyes",
"sleeping problems",
"restlessness",
"fast breathing"
]

# =========================
# SYMPTOM KEYWORDS
# =========================
SYMPTOM_KEYWORDS = {

    "fever": [
        "fever",
        "hot body",
        "burning body",
        "body hot"
    ],

    "cough": [
        "cough",
        "dry cough",
        "wet cough"
    ],

    "headache": [
        "headache",
        "migraine",
        "head pain"
    ],

    "fatigue": [
        "fatigue",
        "tired",
        "weak",
        "no energy"
    ],

    "stomach pain": [
        "stomach pain",
        "belly pain",
        "cramps"
    ],

    "vomiting": [
        "vomiting",
        "throwing up",
        "puking"
    ],

    "diarrhea": [
        "diarrhea",
        "loose stool"
    ],

    "shortness of breath": [
        "shortness of breath",
        "breathless",
        "cannot breathe"
    ],

    "chest pain": [
        "chest pain",
        "tight chest"
    ],

    "runny nose": [
        "runny nose",
        "blocked nose"
    ],

    "sneezing": [
        "sneezing"
    ],

    "loss of appetite": [
        "loss of appetite",
        "not hungry"
    ],

    "dizziness": [
        "dizziness",
        "light headed"
    ],

    "rash": [
        "rash",
        "skin rash"
    ],
    "high fever": [
    "high fever",
    "very hot body",
    "extreme fever"
],

"dry cough": [
    "dry cough",
    "persistent dry cough"
],

"wet cough": [
    "wet cough",
    "cough with mucus",
    "phlegm cough"
],

"difficulty breathing": [
    "difficulty breathing",
    "cant breathe",
    "hard to breathe",
    "breathing problem"
],

"dark urine": [
    "dark urine",
    "brown urine",
    "deep yellow urine"
],

"loss of consciousness": [
    "loss of consciousness",
    "passed out",
    "fainted",
    "unconscious"
],

"severe bleeding": [
    "severe bleeding",
    "heavy bleeding",
    "bleeding badly"
],

"joint pain": [
    "joint pain",
    "painful joints"
],

"back pain": [
    "back pain",
    "waist pain",
    "spine pain"
],

"body pain": [
    "body pain",
    "muscle pain",
    "body aches"
],

"fatigue": [
    "fatigue",
    "tired",
    "weak",
    "no energy"
],

"weakness": [
    "weakness",
    "weak body",
    "low strength"
],

"runny nose": [
    "runny nose",
    "running nose"
],

"blocked nose": [
    "blocked nose",
    "stuffy nose"
],

"sore throat": [
    "sore throat",
    "throat pain"
],

"stomach pain": [
    "stomach pain",
    "abdominal pain",
    "belly pain"
],

"vomiting": [
    "vomiting",
    "throwing up",
    "puking"
],

"diarrhea": [
    "diarrhea",
    "running stomach",
    "loose stool"
],

"nausea": [
    "nausea",
    "feeling sick"
],

"loss of appetite": [
    "loss of appetite",
    "not hungry"
],

"dizziness": [
    "dizziness",
    "light headed",
    "spinning head"
],

"blurred vision": [
    "blurred vision",
    "cannot see clearly"
],

"confusion": [
    "confusion",
    "disoriented",
    "mental confusion"
],

"rash": [
    "rash",
    "skin rash",
    "skin spots"
],

"itching": [
    "itching",
    "itchy skin"
],

"ear pain": [
    "ear pain",
    "pain in ear"
],

"red eyes": [
    "red eyes",
    "reddish eyes"
],

"watery eyes": [
    "watery eyes",
    "tearing eyes"
],

"frequent urination": [
    "frequent urination",
    "urinating often"
],

"painful urination": [
    "painful urination",
    "burning urination",
    "pain when urinating"
],

"paralysis": [
    "paralysis",
    "cannot move",
    "body not moving"
]

}

# =========================
# NORMALIZE SYMPTOMS
# =========================
def normalize_symptoms(text_list):

    result = set()

    for text in text_list:

        text = text.lower()

        for key, values in SYMPTOM_KEYWORDS.items():

            for v in values:

                if v in text:

                    result.add(key)

    return list(result)

# =========================
# DISEASE DATABASE
# =========================
DISEASES = {

    "Malaria": {
        "fever": 3,
        "high fever": 3,
        "chills": 3,
        "headache": 2,
        "fatigue": 2,
        "sweating": 2,
        "body pain": 2,
        "vomiting": 1
    },

    "Typhoid": {
        "fever": 3,
        "high fever": 3,
        "stomach pain": 3,
        "diarrhea": 3,
        "weakness": 2,
        "loss of appetite": 2,
        "headache": 2
    },

    "COVID-19": {
        "fever": 3,
        "dry cough": 3,
        "fatigue": 2,
        "shortness of breath": 3,
        "difficulty breathing": 3,
        "sore throat": 2,
        "body pain": 2
    },

    "Common Cold": {
        "runny nose": 3,
        "blocked nose": 3,
        "sneezing": 3,
        "cough": 2,
        "sore throat": 2
    },

    "Asthma": {
        "shortness of breath": 3,
        "difficulty breathing": 3,
        "chest pain": 2,
        "cough": 2,
        "wet cough": 1
    },

    "Pneumonia": {
        "fever": 3,
        "wet cough": 3,
        "difficulty breathing": 3,
        "chest pain": 2,
        "fatigue": 2
    },

    "Tuberculosis": {
        "wet cough": 3,
        "fatigue": 2,
        "chest pain": 2,
        "high fever": 2,
        "loss of appetite": 2
    },

    "Diabetes": {
        "frequent urination": 3,
        "fatigue": 2,
        "weakness": 2,
        "blurred vision": 2
    },

    "Migraine": {
        "headache": 3,
        "blurred vision": 2,
        "dizziness": 2,
        "nausea": 2
    },

    "Food Poisoning": {
        "vomiting": 3,
        "diarrhea": 3,
        "stomach pain": 3,
        "nausea": 2,
        "weakness": 2
    },

    "Cholera": {
        "diarrhea": 3,
        "vomiting": 3,
        "weakness": 3,
        "dark urine": 2
    },

    "Meningitis": {
        "high fever": 3,
        "headache": 3,
        "confusion": 3,
        "vomiting": 2,
        "loss of consciousness": 3
    },

    "Flu": {
        "fever": 3,
        "cough": 2,
        "body pain": 3,
        "fatigue": 2,
        "headache": 2,
        "sore throat": 2
    },

    "Bronchitis": {
        "wet cough": 3,
        "chest pain": 2,
        "fatigue": 2,
        "difficulty breathing": 2
    },

    "Sinusitis": {
        "headache": 2,
        "blocked nose": 3,
        "runny nose": 2,
        "fever": 1
    },

    "Anemia": {
        "fatigue": 3,
        "weakness": 3,
        "dizziness": 2,
        "shortness of breath": 2
    },

    "Hypertension": {
        "headache": 2,
        "dizziness": 2,
        "blurred vision": 2,
        "chest pain": 2
    },

    "Appendicitis": {
        "stomach pain": 3,
        "vomiting": 2,
        "loss of appetite": 2,
        "fever": 2
    },

    "Dengue": {
        "high fever": 3,
        "joint pain": 3,
        "rash": 2,
        "vomiting": 2,
        "body pain": 2
    },

    "Eye Infection": {
        "red eyes": 3,
        "watery eyes": 3,
        "itching": 2
    },

    "Ear Infection": {
        "ear pain": 3,
        "fever": 1,
        "headache": 1
    },

    "UTI": {
        "painful urination": 3,
        "frequent urination": 3,
        "dark urine": 2,
        "fever": 1
    },

    "Stroke": {
        "paralysis": 3,
        "confusion": 3,
        "loss of consciousness": 3,
        "blurred vision": 2
    },

    "Internal Bleeding": {
        "severe bleeding": 3,
        "loss of consciousness": 3,
        "weakness": 2,
        "dizziness": 2
    },
    "Yellow Fever": {
    "high fever": 3,
    "vomiting": 2,
    "body pain": 2,
    "dark urine": 2,
    "fatigue": 2
},

"Rabies": {
    "fever": 2,
    "confusion": 3,
    "difficulty breathing": 2,
    "paralysis": 3
},

"Hepatitis": {
    "fatigue": 2,
    "vomiting": 2,
    "loss of appetite": 3,
    "dark urine": 3
},

"Kidney Infection": {
    "painful urination": 3,
    "frequent urination": 3,
    "back pain": 2,
    "fever": 2
},

"Kidney Stones": {
    "back pain": 3,
    "painful urination": 2,
    "dark urine": 2,
    "vomiting": 1
},

"Heart Attack": {
    "chest pain": 3,
    "shortness of breath": 3,
    "sweating": 2,
    "loss of consciousness": 2
},

"Heart Failure": {
    "shortness of breath": 3,
    "fatigue": 2,
    "chest pain": 2,
    "weakness": 2
},

"Allergy": {
    "itching": 3,
    "rash": 3,
    "sneezing": 2,
    "watery eyes": 2
},

"Chickenpox": {
    "rash": 3,
    "fever": 2,
    "itching": 3,
    "fatigue": 1
},

"Measles": {
    "rash": 3,
    "high fever": 3,
    "red eyes": 2,
    "cough": 2
},

"Mumps": {
    "fever": 2,
    "headache": 2,
    "fatigue": 2,
    "ear pain": 3
},

"Polio": {
    "paralysis": 3,
    "fever": 2,
    "fatigue": 2,
    "body pain": 2
},

"Epilepsy": {
    "loss of consciousness": 3,
    "confusion": 2,
    "headache": 1
},

"Gastritis": {
    "stomach pain": 3,
    "nausea": 2,
    "vomiting": 2,
    "loss of appetite": 2
},

"Ulcer": {
    "stomach pain": 3,
    "vomiting": 2,
    "loss of appetite": 2,
    "nausea": 2
},

"Arthritis": {
    "joint pain": 3,
    "body pain": 2,
    "fatigue": 1
},

"Sciatica": {
    "back pain": 3,
    "weakness": 2,
    "joint pain": 1
},

"Conjunctivitis": {
    "red eyes": 3,
    "watery eyes": 3,
    "itching": 2
},

"Dehydration": {
    "dark urine": 3,
    "weakness": 2,
    "dizziness": 2,
    "fatigue": 2
},

"Sepsis": {
    "high fever": 3,
    "confusion": 3,
    "difficulty breathing": 3,
    "loss of consciousness": 3
}
  
}

# =========================
# TREATMENT DATABASE
# =========================
TREATMENT = {

    "Malaria":
    "Visit clinic immediately and take prescribed antimalarial medication.",

    "Typhoid":
    "Seek medical attention and use antibiotics prescribed by a doctor.",

    "COVID-19":
    "Rest, hydrate, isolate and seek hospital care if breathing worsens.",

    "Common Cold":
    "Drink fluids, rest and monitor symptoms.",

    "Asthma":
    "Use inhaler immediately and avoid triggers.",

    "Pneumonia":
    "Hospital treatment and antibiotics may be required.",

    "Tuberculosis":
    "Complete TB medication under medical supervision.",

    "Diabetes":
    "Monitor blood sugar levels and consult a doctor.",

    "Migraine":
    "Rest in a quiet dark room and use pain relief medication.",

    "Food Poisoning":
    "Hydrate properly and visit hospital if symptoms continue.",

    "Cholera":
    "Urgent hydration and emergency hospital treatment required.",

    "Meningitis":
    "Seek emergency medical care immediately.",

    "Flu":
    "Rest, drink fluids and use fever reducing medication.",

    "Bronchitis":
    "Rest, fluids and hospital care if breathing worsens.",

    "Sinusitis":
    "Steam inhalation and medical treatment may help.",

    "Anemia":
    "Increase iron-rich foods and seek medical advice.",

    "Hypertension":
    "Reduce salt intake and monitor blood pressure.",

    "Appendicitis":
    "Urgent surgery may be required.",

    "Dengue":
    "Hydrate properly and seek hospital care immediately.",

    "Eye Infection":
    "Use prescribed eye medication and avoid touching eyes.",

    "Ear Infection":
    "Consult doctor for ear medication.",

    "UTI":
    "Drink water and use prescribed antibiotics.",

    "Stroke":
    "Emergency hospital treatment required immediately.",

    "Internal Bleeding":
    "Seek emergency medical attention immediately.",
    "Yellow Fever":
"Seek urgent hospital care and stay hydrated.",

"Rabies":
"Emergency medical treatment required immediately.",

"Hepatitis":
"Rest, avoid alcohol and seek medical care.",

"Kidney Infection":
"Use prescribed antibiotics and drink water.",

"Kidney Stones":
"Drink fluids and seek medical evaluation.",

"Heart Attack":
"Call emergency services immediately.",

"Heart Failure":
"Seek urgent hospital treatment.",

"Allergy":
"Use antihistamines and avoid triggers.",

"Chickenpox":
"Rest, hydrate and avoid scratching rash.",

"Measles":
"Seek medical attention and isolate patient.",

"Mumps":
"Rest, hydrate and monitor symptoms.",

"Polio":
"Seek emergency medical support immediately.",

"Epilepsy":
"Consult neurologist and use prescribed medication.",

"Gastritis":
"Avoid spicy foods and use stomach medication.",

"Ulcer":
"Use ulcer medication and avoid acidic foods.",

"Arthritis":
"Use pain relief treatment and exercise carefully.",

"Sciatica":
"Physical therapy and pain management may help.",

"Conjunctivitis":
"Use eye drops and maintain hygiene.",

"Dehydration":
"Drink fluids immediately and rest.",

"Sepsis":
"Emergency hospital treatment required immediately."

}
# =========================
# EMERGENCY FLAGS
# =========================
EMERGENCY_FLAGS = [

    "loss of consciousness",
    "severe chest pain",
    "difficulty breathing",
    "paralysis",
    "severe bleeding"

]

# =========================
# EMERGENCY CHECK
# =========================
def check_emergency(symptoms):

    for s in symptoms:

        if s in EMERGENCY_FLAGS:

            return True, s

    return False, None

# =========================
# AI ENGINE
# =========================
def ai_engine(symptoms):

    symptoms = normalize_symptoms(symptoms)

    emergency, trigger = check_emergency(symptoms)

    # EMERGENCY RESULT
    if emergency:

        return f"""

        <div class="glass-card">

            <h2 style="color:red;">
                🚨 EMERGENCY DETECTED
            </h2>

            <p>
                <b>{trigger}</b>
            </p>

            <p>
                Go to hospital immediately.
            </p>

        </div>

        """

    results = {}

    for disease, sym_map in DISEASES.items():

        score = 0
        matched = []

        max_score = sum(sym_map.values())

        for symptom, weight in sym_map.items():

            if symptom in symptoms:

                score += weight
                matched.append(symptom)

        if score > 0:

            confidence = round((score / max_score) * 100, 1)

            if confidence >= 75:
                risk = "🔴 CRITICAL"

            elif confidence >= 50:
                risk = "🟠 HIGH"

            elif confidence >= 30:
                risk = "🟡 MODERATE"

            else:
                risk = "🟢 LOW"

            results[disease] = {

                "confidence": confidence,
                "risk": risk,
                "matched": matched

            }

    if not results:

        return """

        <div class="glass-card">

            <h2>
                ❌ No Disease Match Found
            </h2>

            <p>
                Try selecting more symptoms.
            </p>

        </div>

        """

    sorted_results = sorted(

        results.items(),

        key=lambda x: x[1]["confidence"],

        reverse=True

    )

    output = """

    <div>

        <h2 style="margin-bottom:20px;">
            🧠
        </h2>

    """

    for disease, data in sorted_results[:5]:

        output += f"""

        <div class="glass-card">

            <h2 style="color:#1877f2;">
                {disease}
            </h2>

            <p>
                <b>Confidence:</b>
                {data['confidence']}%
            </p>

            <p>
                <b>Risk Level:</b>
                {data['risk']}
            </p>

            <p>
                <b>Matched Symptoms:</b>
                {', '.join(data['matched'])}
            </p>

            <p>
                <b>Treatment:</b>
                {TREATMENT.get(disease, "Consult doctor")}
            </p>

        </div>

        """

    output += "</div>"

    return output

# =========================
# LOGIN
# =========================
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        c.execute(

            "SELECT * FROM users WHERE username=? AND password=?",

            (username, password)

        )

        user = c.fetchone()

        conn.close()

        if user:

            session["user"] = username

            return redirect(url_for("home"))

    return render_template("login.html")

# =========================
# REGISTER
# =========================
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        try:

            c.execute(

                "INSERT INTO users (username, password) VALUES (?, ?)",

                (username, password)

            )

            conn.commit()

        except:

            conn.close()

            return """
            Username already exists.
            """

        conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")

# =========================
# HOME
# =========================
@app.route("/home", methods=["GET", "POST"])
def home():

    if "user" not in session:

        return redirect(url_for("login"))

    result = ""

    if request.method == "POST":

        symptoms = request.form.getlist("symptoms")

        chat_input = request.form.get("chat_input")

        ai_question = request.form.get("ai_question")

        if ai_question:

            result = gpt_doctor(ai_question)

        elif chat_input:

            result = ai_engine([chat_input])

        else:
         
         result = ai_engine(symptoms)

        # SAVE HISTORY
        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        c.execute(

            """

            INSERT INTO diagnosis_history
            (username, symptoms, result)

            VALUES (?, ?, ?)

            """,

            (

                session["user"],
                ", ".join(symptoms),
                result

            )

        )

        conn.commit()
        conn.close()

    return render_template(

        "index.html",

        result=result,

        all_symptoms=ALL_SYMPTOMS,

        user=session["user"]

    )

# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))

# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)