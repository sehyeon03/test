import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("부채꼴 호의 길이를 이용해 넓이 구하기! 🥧")
st.write("부채꼴을 잘게 나눈 뒤 재배치하여 직사각형에 가까워지는 과정을 시각적으로 확인합니다.")

# --- Sidebar Controls ---

st.sidebar.header("⚙️ 설정")

# Logic for the reset button
if st.sidebar.button("초기값으로", key='reset'):
    st.session_state.angle = 180
    st.session_state.segments = 12
    st.session_state.radius = 5.0

# Use Streamlit widgets to get user input
# st.session_state is used to store and maintain the state of the widgets.
angle = st.sidebar.slider(
    '각도 (θ):', 
    min_value=10, 
    max_value=360, 
    value=st.session_state.get('angle', 180), 
    step=1,
    key='angle'
)
segments = st.sidebar.slider(
    '나누는 개수:', 
    min_value=2, 
    max_value=100, 
    value=st.session_state.get('segments', 12), 
    step=1,
    key='segments'
)
radius = st.sidebar.slider(
    '반지름 (r):', 
    min_value=1.0, 
    max_value=10.0, 
    value=st.session_state.get('radius', 5.0), 
    step=0.5,
    key='radius'
)

# --- Main Plotting Logic ---

def create_plots(angle, segments, radius):
    """
    Generates the two plots based on the user's input values.
    Returns a matplotlib figure object.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5), constrained_layout=True)
    theta_rad_total = np.deg2rad(angle)

    # --- Left Plot: Original Sector ---
    ax1.set_aspect('equal')
    for i in range(segments):
        theta_start = theta_rad_total * (i / segments)
        theta_end = theta_rad_total * ((i + 1) / segments)
        theta_slice = np.linspace(theta_start, theta_end, 30)
        x_slice = np.concatenate(([0], radius * np.cos(theta_slice)))
        y_slice = np.concatenate(([0], radius * np.sin(theta_slice)))
        color = plt.cm.viridis(i / segments)
        ax1.fill(x_slice, y_slice, color=color, alpha=0.9)
    
    ax1.set_title("1. origin", fontsize=12)
    ax1.set_xlim(-radius * 1.1, radius * 1.1)
    ax1.set_ylim(-radius * 1.1, radius * 1.1)
    ax1.grid(True)

    # --- Right Plot: Rearranged Segments ---
    angle_per_segment = theta_rad_total / segments if segments > 0 else 0
    
    # Calculate the shape of a single base wedge
    theta_base = np.linspace(-angle_per_segment / 2, angle_per_segment / 2, 30)
    x_base_coords = np.concatenate(([0], radius * np.cos(theta_base)))
    y_base_coords = np.concatenate(([0], radius * np.sin(theta_base)))
    
    # Rotate the wedge by 90 degrees
    x_wedge_base = -y_base_coords
    y_wedge_base = x_base_coords
    
    right_corner = np.array([radius * np.sin(angle_per_segment / 2), radius * np.cos(angle_per_segment / 2)])
    half_base_width = radius * np.sin(angle_per_segment / 2)
    current_tip_pos = np.array([half_base_width, half_base_width / 2])
    
    for i in range(segments):
        color = plt.cm.viridis(i / segments)
        
        if i % 2 == 0:  # Even segments
            x_transformed = x_wedge_base + current_tip_pos[0]
            y_transformed = y_wedge_base + current_tip_pos[1]
        else:  # Odd segments (flipped)
            x_transformed = x_wedge_base + current_tip_pos[0]
            y_transformed = -y_wedge_base + current_tip_pos[1]
        
        ax2.fill(x_transformed, y_transformed, color=color, alpha=0.9)

        # Move the position for the next wedge
        if i % 2 == 0:
            current_tip_pos += right_corner
        else:
            current_tip_pos += np.array([right_corner[0], -right_corner[1]])
            
    final_width = current_tip_pos[0] + half_base_width
    ax2.set_title("2. repositioned", fontsize=12)
    ax2.set_aspect('equal')
    ax2.set_ylim(-0.5, radius * 1.5)
    ax2.set_xlim(-0.5, final_width + 0.5 if final_width > 0 else 1)
    ax2.grid(True)
    
    return fig

# --- Run the App ---
# Generate the plot with the values from the widgets and display it in Streamlit
fig = create_plots(angle, segments, radius)
st.pyplot(fig)

st.info("""
**관찰 포인트:**
- **분할 개수**를 늘릴수록 재배치된 도형이 점점 더 직사각형에 가까워집니다.
- 이 원리를 통해 부채꼴의 넓이 공식 $(Area = \\frac{1}{2}r^2\\theta)$ 이 유도되는 과정을 이해할 수 있습니다.
  - 재배치된 도형의 가로 길이는 호의 길이($l=r\\theta$)의 절반인 $\\frac{1}{2}r\\theta$ 에 가까워지고,
  - 세로 길이는 반지름 $r$에 가까워지기 때문입니다.
""")

