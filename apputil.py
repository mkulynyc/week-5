import plotly.express as px
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')

### Exercise 1 ###
def survival_demographics():
    """
    This function takes the Titanic DF and groups by class, sex, and age group.
    It then calculates the total passengers, survived, and survival rate for each group combination.

    Arguments:
        None

    Returns:
        pandas DataFrame with total passengers, survived, and survival rate for each group combination.
    """
    # 1. Create a new column called 'age_group' based on the 'age' column
    df['age_group'] = pd.cut(df['Age'], bins=[0, 12, 19, 59, 100], labels=['Child', 'Teenager', 'Adult', 'Senior']) 

    # 2. Group by Pclass, Sex, age_group
    grouped = df.groupby(['Pclass', 'Sex', 'age_group'], observed=False).size().unstack(fill_value=0)

    # 3. Calculate total passengers, survived, and survival rate for each group
    total_passengers = df.groupby(['Pclass', 'Sex', 'age_group'], observed=False).size().unstack(fill_value=0)
    survived = df[df['Survived'] == 1].groupby(['Pclass', 'Sex', 'age_group'], observed=False).size().unstack(fill_value=0)
    survival_rate = survived / total_passengers

    # 4. Create DF with total, survived, and survival rate for each group
    groups_df = pd.concat([total_passengers, survived, survival_rate], axis=1, keys=['Total', 'Survived', 'Survival Rate'])

    # 5. Order the Data
    groups_df = groups_df.sort_index()
    
    # 6. Return the DataFrame
    return groups_df


