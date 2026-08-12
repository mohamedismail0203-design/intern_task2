import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_dashboard(data_path: str, output_image_path: str):
    """
    Generates a 2x2 multi-panel Seaborn dashboard visualizing:
    1. Average Discount Rate by Main Category
    2. Customer Rating Distribution across Categories
    3. Mean Actual Price vs. Discounted Price
    4. Top 5 Most Reviewed Products
    """
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Cleaned dataset not found at {data_path}. Please run clean_data.py first.")

    df = pd.read_csv(data_path)

    # Filter top 3 main categories for clean visualization
    top_categories = ['Electronics', 'Computers & Accessories', 'Home & Kitchen']
    df_top = df[df['main_category'].isin(top_categories)].copy()

    # Apply seaborn theme
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({'font.size': 10})

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Amazon Product Sales Analysis: Visual Story & Business Insights', fontsize=16, fontweight='bold')

    # Chart 1: Average Discount Percentage by Main Category
    cat_summary = df_top.groupby('main_category', as_index=False)['discount_percentage_clean'].mean()
    sns.barplot(
        ax=axes[0, 0], x='main_category', y='discount_percentage_clean', hue='main_category',
        data=cat_summary, palette=['#2b5c8f', '#d9534f', '#41b6c4']
    )
    axes[0, 0].set_title('1. Average Discount Rate by Category (%)', fontweight='bold')
    axes[0, 0].set_xlabel('Category')
    axes[0, 0].set_ylabel('Average Discount (%)')
    if axes[0, 0].get_legend(): axes[0, 0].get_legend().remove()

    for p in axes[0, 0].patches:
        if p.get_height() > 0:
            axes[0, 0].annotate(f'{p.get_height():.1f}%', (p.get_x() + p.get_width() / 2., p.get_height()),
                                ha='center', va='center', xytext=(0, 5), textcoords='offset points')

    # Chart 2: Customer Rating Distribution
    sns.boxplot(
        ax=axes[0, 1], x='main_category', y='rating_clean', hue='main_category',
        data=df_top, palette=['#2b5c8f', '#d9534f', '#41b6c4']
    )
    axes[0, 1].set_title('2. Customer Rating Distribution by Category', fontweight='bold')
    axes[0, 1].set_xlabel('Category')
    axes[0, 1].set_ylabel('Rating (Out of 5)')
    if axes[0, 1].get_legend(): axes[0, 1].get_legend().remove()

    # Chart 3: Mean Actual vs. Discounted Price
    price_summary = df_top.groupby('main_category', as_index=False)[['actual_price_clean', 'discounted_price_clean']].mean()
    price_melted = price_summary.melt(id_vars='main_category', var_name='Price Type', value_name='Price')
    price_melted['Price Type'] = price_melted['Price Type'].map({
        'actual_price_clean': 'Actual Price', 'discounted_price_clean': 'Discounted Price'
    })

    sns.barplot(ax=axes[1, 0], x='main_category', y='Price', hue='Price Type', data=price_melted, palette=['#e41a1c', '#377eb8'])
    axes[1, 0].set_title('3. Mean Actual vs. Discounted Price (₹)', fontweight='bold')
    axes[1, 0].set_xlabel('Category')
    axes[1, 0].set_ylabel('Price in INR (₹)')

    for p in axes[1, 0].patches:
        height = p.get_height()
        if height > 0:
            axes[1, 0].annotate(f'₹{int(height):,}', (p.get_x() + p.get_width() / 2., height),
                                ha='center', va='center', xytext=(0, 5), textcoords='offset points')

    # Chart 4: Top 5 Most Reviewed Products
    top_reviewed = df.nlargest(5, 'rating_count_clean').copy()
    top_reviewed['short_name'] = top_reviewed['product_name'].str.slice(0, 28) + "..."
    sns.barplot(
        ax=axes[1, 1], y='short_name', x='rating_count_clean', hue='short_name',
        data=top_reviewed, palette='Reds_r'
    )
    axes[1, 1].set_title('4. Top 5 Most Reviewed Products (Review Count)', fontweight='bold')
    axes[1, 1].set_xlabel('Total Rating Count')
    axes[1, 1].set_ylabel('Product Name')
    if axes[1, 1].get_legend(): axes[1, 1].get_legend().remove()

    for p in axes[1, 1].patches:
        width = p.get_width()
        if width > 0:
            axes[1, 1].annotate(f'{int(width):,}', (width, p.get_y() + p.get_height() / 2.),
                                ha='center', va='center', xytext=(24, 0), textcoords='offset points')

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
    plt.savefig(output_image_path, dpi=300)
    plt.close()
    print(f"Dashboard saved successfully to: {output_image_path}")

if __name__ == "__main__":
    generate_dashboard('data/cleaned_amazon_sales.csv', 'output/amazon_sales_dashboard.png')