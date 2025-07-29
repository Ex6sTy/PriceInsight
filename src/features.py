import pandas as pd

def add_mean_competitor_price(df: pd.DataFrame) -> pd.DataFrame:
    sum_by_product = df.groupby('product')['price'].transform('sum')
    count_by_product = df.groupby('product')['price'].transform('count')
    sum_by_product_company = df.groupby(['product', 'company'])['price'].transform('sum')
    count_by_product_company = df.groupby(['product', 'company'])['price'].transform('count')
    df['mean_competitor_price'] = (
        (sum_by_product - sum_by_product_company) / (count_by_product - count_by_product_company)
    )
    return df

if __name__ == '__main__':
    df = pd.read_csv('data/cleaned.csv')
    df = add_mean_competitor_price(df)
    print(df[['company', 'product', 'price', 'mean_competitor_price']].head(10))
    df.to_csv('data/features.csv', index=False)
    print("\nФайл с фичами сохранён в data/features.csv")

