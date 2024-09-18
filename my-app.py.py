import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as graph_objects
import matplotlib.pyplot as plt 
import seaborn as sns

path = "https://linked.aub.edu.lb/pkgcube/data/b49644dfb203975571146f1ff8d4fee1_20240907_152325.csv"
df = pd.read_csv(path)

# Clean up the column names by stripping any leading or trailing spaces
df.columns = df.columns.str.strip()

# Select the number of towns to display (Slider)
num_towns = st.slider('Number of towns to display', min_value=10, max_value=70, value=70, step=10)

# Extract relevant columns for plotting
town = df['Town']
percentage_women = df['Percentage of Women']
percentage_men = df['Percentage of Men']

# Create the bar plot using Matplotlib
fig, ax = plt.subplots(figsize=(14, 8))
ax.bar(town[:num_towns], percentage_women[:num_towns], color='pink', label='Women')
ax.bar(town[:num_towns], percentage_men[:num_towns], color='blue', label='Men')

# Add title, labels, and formatting
ax.set_title('Gender by Town')
ax.set_xlabel('Town')
ax.set_ylabel('Percentage')
plt.xticks(rotation=90, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Display the plot using Streamlit
st.pyplot(fig)

# Strip any leading or trailing spaces in column names
df.columns = df.columns.str.strip()

# Calculate the average family size using weighted sums
df['Average family size'] = (
    1.5 * df['Average family size - 1 to 3 members'] + 
    5 * df['Average family size - 4 to 6 members'] + 
    7 * df['Average family size - 7 or more members']
    ) / (
        df['Average family size - 1 to 3 members'] +
        df['Average family size - 4 to 6 members'] +
        df['Average family size - 7 or more members']
    )

# Allow the user to select specific towns
selected_towns = st.multiselect(
    'Select towns to annotate on the scatter plot:', 
    options=df['Town'].unique(),
    default=['Aain El Saydeh', 'Aabadiyeh', 'Aachqout', 'Khreibet Baabda', 'Aabdine', 'Fourzol']
)

# Extract relevant columns for the plot
town_names = df['Town']
average_family_size = df['Average family size']
percentage_eldelry = df['Percentage of Eldelry - 65 or more years']

# Create the scatter plot using Matplotlib
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(average_family_size, percentage_eldelry, color='blue', alpha=0.4, edgecolor='pink', s=100)

# Add plot titles and labels
ax.set_title('Scatter Plot of Average Family Size vs. Percentage of Eldelry', fontsize=12)
ax.set_xlabel('Average Family Size')
ax.set_ylabel('Percentage of Eldelry (65 or more years)')

# Annotate the selected towns
for i, town in enumerate(town_names):
    if town in selected_towns:
        ax.annotate(town, (average_family_size[i], percentage_eldelry[i]), fontsize=9, alpha=0.8)

# Add gridlines
plt.grid(True, linestyle='--', alpha=0.1)

# Display the plot in Streamlit
st.pyplot(fig)

# Sample data (replace this with your actual data or file uploader)
data = {
    'Town': ['Town A', 'Town B', 'Town C'],
    'Percentage of Women': [55, 60, 65],
    'Percentage of Men': [45, 40, 35]
}
df = pd.DataFrame(data)

# Streamlit form for selecting a row
with st.form(key='my_form'):
    st.write("Select a town to view gender distribution:")
    
    # Dropdown to select the town (row)
    selected_town = st.selectbox("Select Town", df['Town'])

    # Submit button
    submit_button = st.form_submit_button(label='Show Distribution')

# Action when the form is submitted
if submit_button:
    # Get the selected row based on the town name
    selected_row = df[df['Town'] == selected_town].iloc[0]
    
    # Labels and sizes for the pie chart
    labels = ['Women', 'Men']
    sizes = [selected_row['Percentage of Women'], selected_row['Percentage of Men']]
    colors = ['pink', 'blue']

    # Plot the pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'white'})
    plt.title(f"Gender Distribution in {selected_row['Town']}")
    
    # Display the plot in Streamlit
    st.pyplot(plt)
