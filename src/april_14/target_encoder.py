import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Load the dataset
df = pd.read_csv("../../data/april_14/filtered_April.csv")

# Define categorical variables for target encoding
categorical_vars = ['actor_0_name', 'actor_1_name',
                    'actor_2_name', 'director', 'production_company_name']

# Split data into train and validation sets
train_df, val_df = train_test_split(df, test_size=0.2, random_state=42)

# Function to calculate target encoding for categorical variables


def target_encode(train, val, cat_vars, target):
    for var in cat_vars:
        target_map = train.groupby(var)[target].mean()
        val[var + '_encoded'] = val[var].map(target_map)
        # Replace NaN values with mean revenue (overall mean)
        val[var + '_encoded'].fillna(train[target].mean(), inplace=True)


# Calculate target encoding for categorical variables
target_encode(train_df, val_df, categorical_vars, 'revenue')

# Concatenate the train and validation sets back together
encoded_df = pd.concat([train_df, val_df])

# Save the updated dataset to a new CSV file
encoded_df.to_csv("your_dataset_encoded.csv", index=False)
