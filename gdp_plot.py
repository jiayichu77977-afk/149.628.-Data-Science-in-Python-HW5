# Homework 5 Question 1: GDP by country within regions
import pandas as pd
import plotly.express as px
import country_converter as coco


url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"

headers = {"User-Agent": "HW5-GDP-Analysis"}

gdp = pd.read_html(
    url,
    match="IMF",
    storage_options=headers
)[0]

gdp = gdp[["Country/Territory", "IMF (2026)[1]"]].copy()

gdp = gdp.rename(columns={
    "Country/Territory": "country",
    "IMF (2026)[1]": "gdp"
})
gdp["gdp"] = pd.to_numeric(gdp["gdp"], errors="coerce")
gdp = gdp.dropna(subset=["gdp"])
gdp = gdp[gdp["country"] != "World"].copy()
gdp["country"] = gdp["country"].str.replace(
    r"\[.*?\]", "", regex=True
).str.strip()

gdp["region"] = coco.convert(
    names=gdp["country"].tolist(),
    to="continent"
)

fig = px.bar(
    gdp,
    x="region",
    y="gdp",
    color="country",
    barmode="stack",
    title="GDP by Country within Regions",
    labels={
        "region": "Region",
        "gdp": "GDP (million US$)",
        "country": "Country"
    }
)

fig.write_html("stacked_bar.html")
