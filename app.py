import streamlit as st
import numpy as np

# Given constants
sensitivity = 0.125  # Sensitivity of the model
specificity = 0.95  # Specificity of the model
P_NS = 0.75  # Probability of no storm
P_S = 0.25  # Probability of storm

value_no_storm_no_sugar = 960000
value_no_storm_typical_sugar = 1410000
value_no_storm_high_sugar = 1500000
value_storm_mold = 3300000
value_storm_no_mold = 420000

# Function to calculate expected values
def calculate_expected_value(sensitivity, specificity, P_S, P_NS, value_if_no_storm, value_if_storm):
    P_DNS = specificity * P_NS + (1 - sensitivity) * P_S
    P_NS_given_DNS = (specificity * P_NS) / P_DNS
    P_DS = sensitivity * P_S + (1 - specificity) * P_NS
    P_S_given_DS = (sensitivity * P_S) / P_DS
    
    EV_wait = P_DNS * (P_NS_given_DNS * value_if_no_storm + (1 - P_NS_given_DNS) * value_if_storm) + \
              P_DS * (P_S_given_DS * value_if_storm + (1 - P_S_given_DS) * value_if_no_storm)
    # print(EV_wait)
    return EV_wait

# Streamlit app
st.title('Decision Model for Harvesting')

# Initialize probabilities with default values
default_values = [0.6, 0.3, 0.1]  # Default values for the sugar levels
P_no_sugar, P_typical_sugar, P_high_sugar = default_values

# User inputs for the probabilities
P_botrytis = st.slider('Chance of Botrytis (Mold)', 0.0, 1.0, 0.1)
P_no_sugar = st.slider('Chance of No Sugar Increase', 0.0, 1.0, 0.6)
P_typical_sugar = st.slider('Chance of Typical Sugar Increase', 0.0, 1.0, 0.3)
P_high_sugar = st.slider('Chance of High Sugar Increase', 0.0, 1.0, 0.1)

if (P_no_sugar + P_typical_sugar + P_high_sugar) > 1:
    st.error('The total probability of sugar levels must not exceed 1.')
    st.stop()

# Assuming botrytis affects the chance of storm
P_S = P_botrytis
P_NS = 1 - P_botrytis

def calculate_no_storm(P_no_sugar, P_typical_sugar, P_high_sugar):
    value_if_no_storm = (P_no_sugar * value_no_storm_no_sugar +
                         P_typical_sugar * value_no_storm_typical_sugar +
                         P_high_sugar * value_no_storm_high_sugar)
    return value_if_no_storm

def calculate_storm(P_botrytis):
    value_if_storm = (P_botrytis * value_storm_mold +
                      (1 - P_botrytis) * value_storm_no_mold)
    return value_if_storm

# Calculate the expected values
EV_now = 960000  # Fixed value of harvesting now
# value_if_no_storm = calculate_no_storm(P_no_sugar, P_typical_sugar, P_high_sugar)
# value_if_storm = calculate_storm(P_botrytis)
# print(value_if_no_storm)
# print(value_if_storm)

EV_wait = calculate_expected_value(sensitivity, specificity, P_S, P_NS, calculate_no_storm(P_no_sugar, P_typical_sugar, P_high_sugar), calculate_storm(P_botrytis))

# Display the results
st.write(f'Expected Value of Waiting: {EV_wait}')
st.write(f'Expected Value of Harvesting Now: {EV_now}')

# Recommend the action
if EV_wait > EV_now:
    st.success('Recommended Action: Wait')
else:
    st.error('Recommended Action: Harvest Now')
