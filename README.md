# Moscow Real Estate Price Prediction

Модель предсказывает цену недвижимости в Москве.

Dataset:  
https://www.kaggle.com/datasets/mrdaniilak/russia-real-estate-2021

## Run

1. Скачать датасет
2. Положить файл в `data/data.csv`
3. Запустить `data/eda.ipynb`
4. Запустить `models/models.ipynb`
5. Обученная модель сохранится в `models/model.pkl`
6. Также сохраняется обученный scaler в `models/scaler.pkl`

## Structure

```text
data/
├── data.csv
├── clean_data.csv
├── eda.ipynb

models/
├── models.ipynb
├── model.pkl
├── scaler.pkl
```