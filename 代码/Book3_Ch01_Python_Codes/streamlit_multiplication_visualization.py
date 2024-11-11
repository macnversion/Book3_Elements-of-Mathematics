import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

# Streamlit app title
st.title("乘法是重复加法的可视化")

# Input numbers for multiplication
a = st.number_input("输入第一个数 (被乘数)", min_value=1, step=1, value=2)
b = st.number_input("输入第二个数 (乘数)", min_value=1, step=1, value=4)

# Calculate product
product = a * b
st.write(f"{a} × {b} = {product}")

# Create the number line plot
fig, ax = plt.subplots(figsize=(10, 4))

# Draw the number line
ax.axhline(0, color='blue', linewidth=1)
ax.set_xticks(range(0, product + a + 1, 1))
ax.set_xticklabels(range(0, product + a + 1, 1))
ax.set_xlim(0, product + a)
ax.set_ylim(-1, b * 0.6)

# Draw the repeated addition arcs
for i in range(b):
    start = i * a
    end = start + a
    midpoint = (start + end) / 2
    
    # Draw arc to represent each addition
    arc = Arc(
        xy=(midpoint, 0),     # Center of the arc
        width=a,               # Width of the arc (same as the step 'a')
        height=a * 0.6,        # Adjust height for clear visualization
        angle=0,               # Rotation angle
        theta1=0,              # Start angle of the arc
        theta2=180,            # End angle of the arc
        color="red",           # Arc color
        lw=2
    )
    ax.add_patch(arc)

    # Add the number label for each addition
    ax.text(midpoint, 0.3, f"{a}", ha="center", color="red", fontsize=10)
    
# Final result annotation
ax.text(product, b * 0.3, f"{a} × {b} = {product}", ha="center", color="black", fontsize=12)

# Hide y-axis and spines
ax.get_yaxis().set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Display the plot in Streamlit
st.pyplot(fig)
