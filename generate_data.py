import pandas as pd
import random

data = pd.read_csv("placement.csv")

genders = ["M","F"]
workex = ["Yes","No"]
branches = ["CS","IT","ECE","ME"]

data["gender"] = [random.choice(genders) for _ in range(len(data))]
data["ssc_p"] = [random.randint(50,90) for _ in range(len(data))]
data["hsc_p"] = [random.randint(50,90) for _ in range(len(data))]
data["degree_p"] = [random.randint(50,90) for _ in range(len(data))]
data["etest_p"] = [random.randint(50,90) for _ in range(len(data))]
data["workex"] = [random.choice(workex) for _ in range(len(data))]
data["branch"] = [random.choice(branches) for _ in range(len(data))]

data.to_csv("placement_updated.csv", index=False)

print("✅ New dataset created: placement_updated.csv")
