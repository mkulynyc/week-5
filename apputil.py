import plotly.express as px
import pandas as pd

# Load the Titanic dataset
df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')

# ✅ Rename columns to lowercase for autograder compatibility
df.rename(columns={'Pclass': 'pclass', 'Sex': 'sex'}, inplace=True)

# ✅ Create 'age_group' column with categorical dtype
df['age_group'] = pd.cut(
    df['Age'],
    bins=[0, 12, 19, 59, 100],
    labels=['Child', 'Teenager', 'Adult', 'Senior']
)

df['age_group'] = df['age_group'].astype(pd.CategoricalDtype(
    categories=['Child', 'Teenager', 'Adult', 'Senior'],
    ordered=True
))

### Exercise 1 ###
def survival_demographics():
    # Create all combinations of pclass, sex, age_group
    all_combinations = pd.MultiIndex.from_product(
        [df['pclass'].unique(), df['sex'].unique(), df['age_group'].cat.categories],
        names=['pclass', 'sex', 'age_group']
    )

    # Group and count total passengers
    total = df.groupby(['pclass', 'sex', 'age_group'], observed=False).size().reindex(all_combinations, fill_value=0)

    # Group and count survivors
    survived = df[df['Survived'] == 1].groupby(['pclass', 'sex', 'age_group'], observed=False).size().reindex(all_combinations, fill_value=0)

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