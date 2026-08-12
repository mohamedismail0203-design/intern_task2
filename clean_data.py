import os
import pandas as pd


def clean_amazon_data(input_path: str, output_path: str) -> pd.DataFrame:
    """
    Cleans raw Amazon sales dataset:
    - Removes currency symbols (₹) and commas from price columns.
    - Converts prices, ratings, and review counts into numeric formats.
    - Extracts primary product category.
    """
    print(f"Loading raw data from: {input_path}")
    df = pd.read_csv(input_path)

    # 1. Clean monetary fields
    df['discounted_price_clean'] = pd.to_numeric(
        df['discounted_price'].astype(str).str.replace('₹', '').str.replace(',', '').str.strip(), errors='coerce'
    )
    df['actual_price_clean'] = pd.to_numeric(
        df['actual_price'].astype(str).str.replace('₹', '').str.replace(',', '').str.strip(), errors='coerce'
    )

    # 2. Clean percentage and numeric rating fields
    df['discount_percentage_clean'] = pd.to_numeric(
        df['discount_percentage'].astype(str).str.replace('%', '').str.strip(), errors='coerce'
    )
    df['rating_clean'] = pd.to_numeric(
        df['rating'].astype(str).str.replace('|', '', regex=False), errors='coerce'
    )
    df['rating_count_clean'] = pd.to_numeric(
        df['rating_count'].astype(str).str.replace(',', '').str.strip(), errors='coerce'
    )

    # 3. Categorical Extraction
    df['main_category'] = df['category'].astype(str).str.split('|').str[0]
    df['main_category'] = df['main_category'].replace({
        'Computers&Accessories': 'Computers & Accessories',
        'Home&Kitchen': 'Home & Kitchen',
        'OfficeProducts': 'Office Products',
        'MusicalInstruments': 'Musical Instruments',
        'HomeImprovement': 'Home Improvement',
        'Toys&Games': 'Toys & Games',
        'Car&Motorbike': 'Car & Motorbike',
        'Health&PersonalCare': 'Health & Personal Care'
    })

    # Export cleaned dataset
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Cleaned dataset successfully exported to: {output_path}")
    return df


if __name__ == "__main__":
    clean_amazon_data('data/amazon.csv', 'data/cleaned_amazon_sales.csv')