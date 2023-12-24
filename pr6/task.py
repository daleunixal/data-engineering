import os

import pandas as pd
import numpy as np
import json

def analyze_dataset(file_path, prefix):
    # Загрузка набора данных из файла
    df = pd.read_csv(file_path, usecols=lambda column: column != 'Unnamed: 0')

    # Анализ параметров
    memory_usage = df.memory_usage(index=True).sum()
    columns_info = []

    for col in df.columns:
        col_info = {
            "column": col,
            "memory_usage": df[col].memory_usage(deep=True),
            "memory_share": df[col].memory_usage(deep=True) / memory_usage,
            "data_type": df[col].dtype.name
        }
        columns_info.append(col_info)

    # Сортировка по занимаемому объему памяти
    sorted_columns_info = sorted(columns_info, key=lambda x: x["memory_usage"], reverse=True)

    # Вывод статистики в JSON
    with open(prefix + " dataset_statistics_noopt.json", "w") as json_file:
        json.dump(sorted_columns_info, json_file, indent=2)

    # Преобразование типов данных
    for col in df.select_dtypes(include='object').columns:
        if df[col].nunique() < 50:
            df[col] = df[col].astype('category')

    df[df.select_dtypes(include='int').columns] = df.select_dtypes(include='int').apply(pd.to_numeric, downcast='integer')
    df[df.select_dtypes(include='float').columns] = df.select_dtypes(include='float').apply(pd.to_numeric, downcast='float')

    columns_info = []

    for col in df.columns:
        col_info = {
            "column": col,
            "memory_usage": df[col].memory_usage(deep=True),
            "memory_share": df[col].memory_usage(deep=True) / memory_usage,
            "data_type": df[col].dtype.name
        }
        columns_info.append(col_info)

    # Сортировка по занимаемому объему памяти
    sorted_columns_info = sorted(columns_info, key=lambda x: x["memory_usage"], reverse=True)

    # Вывод статистики в JSON
    with open(prefix + " dataset_statistics_opt.json", "w") as json_file:
        json.dump(sorted_columns_info, json_file, indent=2)

    # Повторный анализ после оптимизации
    memory_usage_optimized = df.memory_usage(index=True).sum()

    # Выбор 10 колонок и сохранение в отдельном файле
    selected_columns = df.columns[:10]
    df[selected_columns].to_csv(f"{prefix}selected_dataset.csv", index=False)

    return memory_usage, memory_usage_optimized

for i, file in enumerate(os.listdir('./data/dataset_6')):
    if file == '[6]spotify.csv':
        memory_usage, memory_usage_optimized = analyze_dataset(f"./data/dataset_6/{file}", f"[{i}]")

        print(f"Memory usage before optimization: {memory_usage} bytes")
        print(f"Memory usage after optimization: {memory_usage_optimized} bytes")

