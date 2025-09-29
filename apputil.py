import plotly.express as px
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')

### Exercise 1 ###
def survival_demographics():
    df['age_group'] = pd.cut(
        df['Age'],
        bins=[0, 12, 19, 59, 100],
        labels=['Child', 'Teenager', 'Adult', 'Senior']
    ).astype('category')  # Ensure categorical dtype

    # Create all combinations of Pclass, Sex, age_group
    all_combinations = pd.MultiIndex.from_product(
        [df['Pclass'].unique(), df['Sex'].unique(), df['age_group'].cat.categories],
        names=['Pclass', 'Sex', 'age_group']
    )

    # Group and count total passengers
    total = df.groupby(['Pclass', 'Sex', 'age_group'], observed=False).size().reindex(all_combinations, fill_value=0)

    # Group and count survivors
    survived = df[df['Survived'] == 1].groupby(['Pclass', 'Sex', 'age_group'], observed=False).size().reindex(all_combinations, fill_value=0)

    # Calculate survival rate
    rate = survived / total
    rate = rate.fillna(0)

    # Combine into a DataFrame
    result = pd.DataFrame({
        'Total': total,
        'Survived': survived,
        'Survival Rate': rate
    }).reset_index()

    return result

survival_demographics2()



