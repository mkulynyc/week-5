import streamlit as st

from apputil import *


# Load Titanic dataset
df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')

st.write(
'''
What age groups in each passenger class were most likely to survive the Titanic?

'''
)

def visualize_demographic():
    """
    This function visualizes the survival rate for each age group within each passenger class as a bar plot.
    It first has to aggregate across gender, then it recomputes survival rates before plotting.

    Arguments:
        None

    Returns:
        plotly.graph_objs._figure.Figure: A Plotly figure object representing the bar plot
    """
    
    # Get the grouped DataFrame from the previous function
    df_grouped = survival_demographics()

    # Aggregate across gender
    df_agg = (
        df_grouped
        .groupby(['pclass', 'age_group'], observed=False)
        .agg({'Total': 'sum', 'n_survivors': 'sum'})
        .reset_index()
    )

    # Recalculate survival rate
    df_agg['Survival Rate'] = df_agg['n_survivors'] / df_agg['Total']

    # Plot: class on x-axis, age group as color
    fig = px.bar(
        df_agg,
        x='pclass',
        y='Survival Rate',
        color='age_group',
        barmode='group',
        title='Survival Rate by Class and Age Group (Aggregated Across Gender)',
        labels={
            'pclass': 'Passenger Class',
            'age_group': 'Age Group',
            'Survival Rate': 'Survival Rate'
        }
    )

    return fig

# Generate and display the figure
fig1 = visualize_demographic()
st.plotly_chart(fig1, use_container_width=True)

st.write(
'''
# Titanic Visualization 2

There seems to be a discrepancy between the last name counts and family size.
For instance, the largest family size is 11, but the largest last name count is 9 (Andersson).
There are other examples of this as well.

Question:
What is the distribution of family sizes on the Titanic, and how does that relate to fare prices?
'''
)
# Generate the plot
def visualize_families():
    family_stats = family_groups()

    # ✅ Convert pclass to string so Plotly treats it as categorical
    family_stats['pclass'] = family_stats['pclass'].astype(str)

    fig = px.bar(
        family_stats,
        x='family_size',
        y='avg_fare',
        color='pclass',
        barmode='group',  # ensures side-by-side bars
        title='Average Fare by Family Size and Class',
        labels={
            'family_size': 'Family Size',
            'avg_fare': 'Average Fare',
            'pclass': 'Passenger Class'
        }
    )

    return fig

# Display the figure
fig2 = visualize_families()
st.plotly_chart(fig2, use_container_width=True)

'''
st.write(
'''
# Titanic Visualization Bonus
'''
)
# Generate and display the figure
fig3 = visualize_family_size()
st.plotly_chart(fig3, use_container_width=True)
'''