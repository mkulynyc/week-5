import plotly.express as px
import pandas as pd

# Load and prepare the Titanic dataset
df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')

df.rename(columns={'Pclass': 'pclass', 'Sex': 'sex'}, inplace=True)

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
    all_combinations = pd.MultiIndex.from_product(
        [df['pclass'].unique(), df['sex'].unique(), df['age_group'].cat.categories],
        names=['pclass', 'sex', 'age_group']
    )

    total = df.groupby(['pclass', 'sex', 'age_group'], observed=False).size().reindex(all_combinations, fill_value=0)
    survived = df[df['Survived'] == 1].groupby(['pclass', 'sex', 'age_group'], observed=False).size().reindex(all_combinations, fill_value=0)
    rate = survived / total

    result = pd.DataFrame({
        'Total': total,
        'n_survivors': survived,  # ✅ Renamed for autograder
        'Survival Rate': rate.fillna(0)
    }).reset_index()

    return result