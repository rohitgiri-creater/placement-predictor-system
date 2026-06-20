import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix


# ================= LOAD DATA =================
data = pd.read_csv("placementdata.csv")

data.columns = data.columns.str.lower().str.strip()

# FIX COLUMN NAME
if "workshops/certifications" in data.columns:
    data.rename(columns={"workshops/certifications": "workshops"}, inplace=True)

# ================= TARGET =================
data["status"] = data["placementstatus"].astype(str).str.strip().map(
    {"Placed": 1, "Not Placed": 0}
)

# ================= ENCODING =================
data["placementtraining"] = data["placementtraining"].astype(str).str.strip().map({"Yes": 1, "No": 0})
data["extracurricularactivities"] = data["extracurricularactivities"].astype(str).str.strip().map({"Yes": 1, "No": 0})

data = data.dropna()

# ================= FEATURES =================
features = [
    "cgpa",
    "internships",
    "projects",
    "workshops",
    "aptitudetestscore",
    "softskillsrating",
    "extracurricularactivities",
    "placementtraining",
    "ssc_marks",
    "hsc_marks"
]

X = data[features]
y = data["status"]

# ================= TRAIN TEST SPLIT =================
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

# ================= MODEL =================
model = RandomForestClassifier(
    n_estimators=50,
    max_depth=4,
    min_samples_split=10,
    min_samples_leaf=5,
    random_state=42
)

model.fit(X_train, y_train)

# ================= ACCURACY =================
# ================= ACCURACY =================
cv_scores = cross_val_score(model, X, y, cv=5)
acc = cv_scores.mean()

st.title("Student Placement Prediction System")
st.write("This project predicts whether a student will be placed or not.")



# ================= INPUT =================
st.subheader("Enter Student Details")

cgpa = st.slider("CGPA", 0.0, 10.0, 7.0)
internships = st.slider("Internships", 0, 10, 1)
projects = st.slider("Projects", 0, 10, 2)
workshops = st.slider("Workshops", 0, 10, 1)
aptitude = st.slider("Aptitude Score", 0, 100, 70)
softskills = st.slider("Soft Skills Rating", 0, 10, 7)

extra = st.selectbox("Extracurricular Activities", ["Yes", "No"])
training = st.selectbox("Placement Training", ["Yes", "No"])

ssc = st.slider("SSC Marks", 0, 100, 75)
hsc = st.slider("HSC Marks", 0, 100, 75)

# ================= GRAPH =================
st.subheader("Academic Performance Graph")

fig2 = plt.figure()

labels = [
    "SSC",
    "HSC",
    "CGPA",
    "Aptitude",
    "Internships",
    "Projects",
    "Soft Skills"
]

values = [
    ssc,
    hsc,
    cgpa * 10,
    aptitude,
    internships * 10,
    projects * 10,
    softskills * 10
]

plt.bar(labels, values)
plt.xticks(rotation=45)
plt.ylabel("Score")

st.pyplot(fig2)

# ================= PREDICTION =================
# ================= PREDICTION =================
if st.button("Predict"):

    score = (
        (cgpa * 10) +
        aptitude +
        (softskills * 10) +
        (internships * 10) +
        (projects * 10) +
        (ssc + hsc) / 2
    ) / 6

    final_prob = score / 100
    final_prob = max(0, min(final_prob, 1))

    # ================= RESULT =================
    st.subheader("📊 Placement Chance Meter")
    st.progress(int(final_prob * 100))
    st.write(f"{final_prob*100:.2f}% Chance of Placement")

    # ================= BADGE =================
    if final_prob > 0.75:
        st.success("🟢 Excellent Profile")
    elif final_prob > 0.5:
        st.warning("🟡 Average Profile")
    else:
        st.error("🔴 Needs Improvement")

    # ================= DECISION =================
    if final_prob > 0.6:
        st.success("Student will be PLACED")

        if cgpa > 8:
            st.write("Good chances in top companies")
        else:
            st.write("Chances in medium companies")
    else:
        st.error("Student may NOT be placed")

    # ================= 📌 IMPROVEMENT SUGGESTIONS (ADDED) =================
    st.subheader("📌 Improvement Suggestions")

    suggestions = []

    if cgpa < 7:
        suggestions.append("📉 Improve CGPA (Aim 7+ for better placement)")

    if aptitude < 60:
        suggestions.append("🧠 Practice Aptitude daily (Math + Reasoning)")

    if softskills < 6:
        suggestions.append("🗣 Improve Communication & Soft Skills")

    if internships == 0:
        suggestions.append("💼 Do at least 1 internship for experience")

    if projects < 2:
        suggestions.append("📁 Build more real-world projects")

    if extra == "No":
        suggestions.append("🏆 Participate in extracurricular activities")

    if training == "No":
        suggestions.append("🎯 Take placement training seriously")

    if len(suggestions) == 7:
        st.success("🎉 Excellent profile! No improvements needed")
    else:
     for s in suggestions:
      st.write("•", s)
