#!/usr/bin/env python
# coding: utf-8

# # Time Series Analysis of Racing Game Input Data
# 
# In this notebook, we will perform a time series analysis on the gameplay input data from a racing car game. The data will be read from a text file, processed, and analyzed to identify patterns in the accelerator, brake, and left/right control inputs.

# In[3]:


# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


# ## Step 1: Read and Parse the Input Log File
# 
# We will read the input log file and parse it to extract timestamps along with the corresponding values for acceleration, braking, and left/right controls.

# In[5]:


# Step 1: Read and parse the input log file
file_path = 'input_log.txt'  # Update with your file path if necessary
data = []

with open(file_path, 'r') as f:
    for line in f:
        parts = line.strip().split(' at ')
        if len(parts) == 2:
            value_info = parts[0]
            timestamp_str = parts[1]
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
            
            if 'Accelerator' in value_info:
                value = float(value_info.split(' moved to ')[1])
                data.append((timestamp, 'Accelerator', value))
            elif 'Brake' in value_info:
                value = float(value_info.split(' moved to ')[1])
                data.append((timestamp, 'Brake', value))
            elif 'Left/Right Control' in value_info:
                value = float(value_info.split(' moved to ')[1])
                data.append((timestamp, 'Left/Right Control', value))


# ## Step 2: Create a DataFrame
# 
# Next, we will create a Pandas DataFrame from the parsed data for easier manipulation and analysis.

# In[7]:


# Step 2: Create a DataFrame
df = pd.DataFrame(data, columns=['Timestamp', 'Control', 'Value'])


# In[8]:


df.head(10)


# In[9]:


# Step 3: Aggregate duplicate entries by taking the mean
df_grouped = df.groupby(['Timestamp', 'Control']).mean().reset_index()


# ## Step 3: Pivot the DataFrame for Easier Plotting
# 
# We will pivot the DataFrame so that each control type becomes a separate column with timestamps as indices.

# In[11]:


pivot_df = df_grouped.pivot(index='Timestamp', columns='Control', values='Value')


# In[12]:


pivot_df.head(10)


# ## Step 4: Plotting the Data
# 
# Now we will plot the values of accelerator, brake, and left/right controls over time to visualize their behavior.

# In[84]:


plt.figure(figsize=(25, 8))
plt.plot(pivot_df.index, pivot_df['Accelerator'], label='Accelerator (Axis 5)', color='g')
plt.plot(pivot_df.index, pivot_df['Brake'], label='Brake (Axis 4)', color='r')
plt.plot(pivot_df.index, pivot_df['Left/Right Control'], label='Left/Right Control (Axis 0)', color='b')
plt.title('Gameplay Input Analysis Over Time')
plt.xlabel('Time')
plt.ylabel('Control Value')
plt.legend()
plt.grid()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ## Step 5: Analyze Patterns (Optional)
# 
# We can also calculate correlations between different controls to examine their relationships.

# In[16]:


# Step 5: Analyze patterns (optional)
correlation_matrix = pivot_df.corr()
print("Correlation Matrix:")
print(correlation_matrix)


# In[17]:


# Optional: Classify patterns based on thresholds or conditions
def classify_patterns(row):
    if row['Accelerator'] > 0.5 and row['Brake'] < -0.5:
        return 'Aggressive Acceleration'
    elif row['Brake'] > 0.5:
        return 'Braking'
    elif row['Left/Right Control'] < -0.5:
        return 'Turning Left'
    elif row['Left/Right Control'] > 0.5:
        return 'Turning Right'
    else:
        return 'Neutral'

pivot_df['Pattern'] = pivot_df.apply(classify_patterns, axis=1)

# Display classified patterns
print(pivot_df[['Pattern']].head(100))


# In[18]:


# Step 6: Visualize patterns over time
plt.figure(figsize=(14, 8))
plt.plot(pivot_df.index, pivot_df['Pattern'].astype('category').cat.codes, label='Driving Pattern', marker='o')

# Customize ticks and labels
plt.yticks(ticks=range(len(pivot_df['Pattern'].unique())), labels=pivot_df['Pattern'].unique())
plt.title('Driving Patterns Over Time')
plt.xlabel('Time Index')
plt.ylabel('Driving Pattern')
plt.grid()
plt.xticks(rotation=45)
plt.tight_layout()
plt.legend()
plt.show()


# ## #5 Advnace 

# In[20]:


import numpy as np
# Step 5: Define a function to analyze patterns within a running window
def analyze_window(data_window):
    features = {
        'mean_accelerator': np.mean(data_window['Accelerator']),
        'mean_brake': np.mean(data_window['Brake']),
        'mean_turning': np.mean(data_window['Left/Right Control']),
        'std_accelerator': np.std(data_window['Accelerator']),
        'std_brake': np.std(data_window['Brake']),
        'std_turning': np.std(data_window['Left/Right Control'])
    }
    return features


# In[21]:


# Step 6: Sliding window parameters
window_size = 5  # Number of rows in each window
step_size = 1    # Number of rows to move for each step


# In[22]:


# Step 7: Analyze each window and classify patterns
results = []
for start in range(0, len(pivot_df) - window_size + 1, step_size):
    end = start + window_size
    window_data = pivot_df.iloc[start:end]
    features = analyze_window(window_data)
    
    # Classify patterns based on features (you can adjust thresholds)
    if features['mean_accelerator'] > 0.5 and features['mean_brake'] < 0:
        pattern = 'Aggressive Acceleration'
    elif features['mean_brake'] > 0.5:
        pattern = 'Braking'
    elif features['mean_turning'] < -0.5:
        pattern = 'Turning Left'
    elif features['mean_turning'] > 0.5:
        pattern = 'Turning Right'
    else:
        pattern = 'Neutral'
    
    results.append((pivot_df.index[start], features, pattern))


# In[23]:


# Convert results to DataFrame for easier analysis
results_df = pd.DataFrame(results, columns=['Start_Index', 'Features', 'Pattern'])

# Display some results
print(results_df[['Start_Index', 'Pattern']].head(50))


# In[ ]:




