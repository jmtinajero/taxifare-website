import requests
import streamlit as st

from datetime import datetime


st.set_page_config(
    page_title="TaxiFare Predictor",
    page_icon="🚕",
    layout="centered",
)


st.title("🚕 TaxiFare Predictor")

st.markdown(
    """
    Enter the details of your taxi ride in New York City
    and get an estimated fare using our Machine Learning model.
    """
)


st.subheader("📍 Ride information")


pickup_date = st.date_input(
    "Pickup date"
)

pickup_time = st.time_input(
    "Pickup time"
)


pickup_longitude = st.number_input(
    "Pickup longitude",
    value=-73.950655,
    format="%.6f",
)

pickup_latitude = st.number_input(
    "Pickup latitude",
    value=40.783282,
    format="%.6f",
)


dropoff_longitude = st.number_input(
    "Dropoff longitude",
    value=-73.984365,
    format="%.6f",
)

dropoff_latitude = st.number_input(
    "Dropoff latitude",
    value=40.769802,
    format="%.6f",
)


passenger_count = st.number_input(
    "Passenger count",
    min_value=1,
    max_value=8,
    value=2,
    step=1,
)


pickup_datetime = datetime.combine(
    pickup_date,
    pickup_time,
).strftime("%Y-%m-%d %H:%M:%S")


url = (
    "https://taxifare-api-198781780479.europe-west1.run.app"
    "/predict"
)


params = {
    "pickup_datetime": pickup_datetime,
    "pickup_longitude": pickup_longitude,
    "pickup_latitude": pickup_latitude,
    "dropoff_longitude": dropoff_longitude,
    "dropoff_latitude": dropoff_latitude,
    "passenger_count": passenger_count,
}


st.subheader("🗺 Ride map")

map_data = {
    "lat": [
        pickup_latitude,
        dropoff_latitude,
    ],
    "lon": [
        pickup_longitude,
        dropoff_longitude,
    ],
}

st.map(map_data)


st.subheader("💰 Fare prediction")


if st.button(
    "Predict fare",
    type="primary",
):

    try:

        response = requests.get(
            url,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        prediction = response.json()

        fare = prediction["fare"]

        st.success(
            f"Estimated fare: ${fare:.2f}"
        )

    except requests.exceptions.RequestException as error:

        st.error(
            f"Could not reach the prediction API: {error}"
        )

    except KeyError:

        st.error(
            "The API response did not contain a fare prediction."
        )


st.markdown("---")

st.caption(
    "Prediction powered by FastAPI, Cloud Run and Machine Learning."
)
