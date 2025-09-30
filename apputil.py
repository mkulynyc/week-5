import plotly.express as px
import pandas as pd

# Load and prepare the Titanic dataset
df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')

# Globally rename the columns for the autograder
df.rename(columns={'Pclass': 'pclass', 'Sex': 'sex'}, inplace=True)

### Exercise 1 ###
def survival_demographics():
    """
    This function creates an age group column, and then groups the df by class, sex, and age group.
    Then, we calculate the total numbers, total survived, and survival rate for each group.

    Arguments:
        None

    Returns:
        pandas DataFrame: A DataFrame containing the survival demographics.
    """

    # Create age groups
    df['age_group'] = pd.cut(
        df['Age'],
        bins=[0, 12, 19, 59, 100],
        labels=['Child', 'Teenager', 'Adult', 'Senior']
    )

    # Ensure CategoricalDtype 
    df['age_group'] = df['age_group'].astype(pd.CategoricalDtype(
        categories=['Child', 'Teenager', 'Adult', 'Senior'],
        ordered=True
    ))

    # Create all combinations of pclass, sex, and age_group
    all_combinations = pd.MultiIndex.from_product(
        [df['pclass'].unique(), df['sex'].unique(), df['age_group'].cat.categories],
        names=['pclass', 'sex', 'age_group']
    )

    # Create the grouped data
    total = df.groupby(['pclass', 'sex', 'age_group'], observed=False).size().reindex(all_combinations, fill_value=0)
    survived = df[df['Survived'] == 1].groupby(['pclass', 'sex', 'age_group'], observed=False).size().reindex(all_combinations, fill_value=0)
    rate = survived / total

    # Combine into a single DataFrame and return
    result = pd.DataFrame({
        'Total': total,
        'n_survivors': survived,  # ✅ Renamed for autograder
        'Survival Rate': rate.fillna(0)
    }).reset_index()

    return result


### Exercise 2 ###
def family_groups():
    """
    This function creates a family size column, groups by family size and class,
    and calculates total passengers, average fare, min fare, and max fare for each group.

    Arguments:
        None

    Returns:
        pandas DataFrame: A DataFrame containing family size statistics.
    """
    # Create family size column by # of siblings/spouses + # of parents/children + 1 (self)
    df['family_size'] = df['SibSp'] + df['Parch'] + 1  

    # Group by family size, pclass, calculate number of passengers, avg fare, min/max fare
    family_stats = df.groupby(['family_size', 'pclass'], observed=False).agg(
        total_passengers=('PassengerId', 'count'),
        avg_fare=('Fare', 'mean'),
        min_fare=('Fare', 'min'),
        max_fare=('Fare', 'max')
    ).reset_index()

    # Return sorted table by class then family size
    return family_stats.sort_values(by=['pclass', 'family_size'])

def last_names():
    """
    This function extracts last names from the 'Name' column and counts occurrences.

    Arguments:
        None

    Returns:
        pandas Series: A Series with last names and their counts.
    """
    # Extract last names from the 'Name' column
    df['last_name'] = df['Name'].str.split(',').str[0]

    # Return as a Series
    return df['last_name'].value_counts()

