from pathlib import Path

import joblib
import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent.parent

model = joblib.load(BASE_DIR / "models" / "best_model.pkl")
metadata = joblib.load(BASE_DIR / "models" / "metadata.pkl")


st.set_page_config(
    page_title="Прогноз цены квартиры",
    layout="centered"
)


st.title("Прогноз цены квартиры в Москве")
st.write("Введите параметры квартиры и нажмите кнопку расчёта.")


col1, col2 = st.columns(2)

with col1:
    apartment_type = st.selectbox(
        "Тип квартиры",
        metadata["apartment_types"]
    )

with col2:
    metro_station = st.selectbox(
        "Ближайшая станция метро",
        metadata["metro_stations"]
    )


col3, col4 = st.columns(2)

with col3:
    minutes_to_metro = st.number_input(
        "Минут до метро",
        min_value=0,
        max_value=120,
        value=10,
        step=1
    )

with col4:
    renovation_translation = {
        "Without renovation": "Без ремонта",
        "Cosmetic": "Косметический",
        "Designer": "Дизайнерский",
        "European-style renovation": "Евроремонт"
    }

    renovation_options = metadata["renovations"]

    renovation_display_options = [
        renovation_translation.get(option, option)
        for option in renovation_options
    ]

    selected_renovation_display = st.selectbox(
        "Ремонт",
        renovation_display_options
    )

    renovation = renovation_options[
        renovation_display_options.index(selected_renovation_display)
    ]


col5, col6 = st.columns(2)

with col5:
    rooms = st.selectbox(
        "Количество комнат",
        [0, 1, 2, 3, 4, 5, 6],
        index=2
    )

with col6:
    area = st.number_input(
        "Общая площадь, м²",
        min_value=10.0,
        max_value=300.0,
        value=50.0,
        step=1.0
    )


col7, col8 = st.columns(2)

with col7:
    use_living_area = st.checkbox("Указать жилую площадь")

    if use_living_area:
        living_area = st.number_input(
            "Жилая площадь, м²",
            min_value=5.0,
            max_value=250.0,
            value=30.0,
            step=1.0
        )
    else:
        living_area = round(area * 0.6, 1)
        st.caption(f"Автоматически: {living_area} м²")

with col8:
    use_kitchen_area = st.checkbox("Указать площадь кухни")

    if use_kitchen_area:
        kitchen_area = st.number_input(
            "Площадь кухни, м²",
            min_value=3.0,
            max_value=80.0,
            value=10.0,
            step=1.0
        )
    else:
        kitchen_area = round(area * 0.18, 1)
        st.caption(f"Автоматически: {kitchen_area} м²")


col9, col10 = st.columns(2)

with col9:
    floor = st.number_input(
        "Этаж",
        min_value=1,
        max_value=100,
        value=5,
        step=1
    )

with col10:
    total_floors = st.number_input(
        "Всего этажей в доме",
        min_value=1,
        max_value=100,
        value=12,
        step=1
    )


st.markdown("---")

if st.button("Рассчитать стоимость", use_container_width=True):

    if floor > total_floors:
        st.error("Этаж квартиры не может быть больше количества этажей в доме.")

    elif living_area > area:
        st.error("Жилая площадь не может быть больше общей площади.")

    elif kitchen_area > area:
        st.error("Площадь кухни не может быть больше общей площади.")

    elif living_area + kitchen_area > area:
        st.error("Жилая площадь и кухня вместе не должны превышать общую площадь.")

    else:
        input_data = pd.DataFrame([{
            "apartment_type": apartment_type,
            "metro_station": metro_station,
            "minutes_to_metro": minutes_to_metro,
            "rooms": rooms,
            "area": area,
            "living_area": living_area,
            "kitchen_area": kitchen_area,
            "floor": floor,
            "total_floors": total_floors,
            "renovation": renovation
        }])

        predicted_price = model.predict(input_data)[0]
        price_per_m2 = predicted_price / area

        st.success("Прогноз готов!")

        result_col1, result_col2 = st.columns(2)

        with result_col1:
            st.metric(
                "Цена квартиры",
                f"{predicted_price:,.0f} ₽".replace(",", " ")
            )

        with result_col2:
            st.metric(
                "Цена за м²",
                f"{price_per_m2:,.0f} ₽/м²".replace(",", " ")
            )