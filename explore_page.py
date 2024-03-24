import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def shorten_categories(categories, cutoff):
    category_map = {}
    for i in range(len(categories)):
      if categories.values[i] >= cutoff:
        category_map[categories.index[i]] = categories.index[i]
      else:
        category_map[categories.index[i]] = "Other"

    return category_map

def clean_experience(x):
  if x == "Less than 1 year":
    return 0.5
  elif x == "More than 50 years":
    return 50
  else:
    return x
  

def clean_education(x):
  if "Bachelor’s degree" in x:
    return "Bachelor’s degree"
  if "Master’s degree" in x:
    return "Master’s degree"
  if "Professional degree" in x or "Other doctoral degree" in x:
    return "Post grad"
  return "Less than a Bachelor's degree"

@st.cache_data
@st.cache_resource

def load_data():
  df = pd.read_csv("survey_results_public_new.csv")

  df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedComp"]]
  df = df.rename({"ConvertedComp": "Salary"}, axis=1)
  df = df.dropna()

  df = df[df["Employment"] == "Employed full-time"]
  df = df.drop("Employment", axis=1)

  country_map = shorten_categories(df["Country"].value_counts(), 400)
  df["Country"] = df["Country"].map(country_map)
  df = df[df["Salary"] <= 250000]
  df = df[df["Salary"] >= 10000]
  df = df[df["Country"] != 'Other']

  df["YearsCodepPro"] = df["YearsCodePro"].apply(clean_experience)
  df["EdLevel"] = df["EdLevel"].apply(clean_education)
  return df

df = load_data()

def show_explore_page():
   st.title("Software Developer Salary Prediction")

   st.write("""### Stack Overflow Developer Survey 2020""")

   data = df["Country"].value_counts()

   fig1, ax1 = plt.subplots()
   ax1.pie(data, labels=data.index, autopct="%1.1f%%", startangle=90)
   ax1.axis("equal")

   st.write(""" #### Number of Data from different countries""")
   st.pyplot(fig1)

   st.write("Mean Salary Based On Country")
   data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
   st.bar_chart(data)

   st.write("Mean Salary Based On Experience")
   data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
   st.line_chart(data)
   return data