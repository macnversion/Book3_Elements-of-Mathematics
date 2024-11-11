import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 定义绘制数轴的函数
def plot_number_line(data_dict, x_range=(-3, 4), buffer=0.2):
    x_values = np.arange(x_range[0], x_range[1], 0.1)
    
    # 创建图像
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(x_values, np.zeros_like(x_values), color="blue", lw=2, zorder=1)  # 数轴
    
    # 动态调整标签位置
    y_positions = []
    for label, value in data_dict.items():
        y_pos = 0.5
        for other_y in y_positions:
            if abs(other_y - y_pos) < buffer:
                y_pos += buffer  # 如果重叠，增加垂直距离
        y_positions.append(y_pos)
        
        # 画垂直线和标签
        ax.plot([value, value], [0, y_pos], color="red", lw=1, zorder=2)
        ax.text(value, y_pos + 0.1, label, ha='center', va='bottom', fontsize=10)

    # 添加整数刻度
    for i in range(x_range[0], x_range[1]):
        ax.plot([i, i], [0, 0.1], color="black", lw=1, zorder=2)
        ax.text(i, -0.2, str(i), ha='center', va='top', fontsize=10)

    # 设置图像边界和隐藏坐标轴
    ax.set_xlim(x_range[0] - 0.5, x_range[1] - 0.5)
    ax.set_ylim(-0.5, max(y_positions) + 0.5)
    ax.axis("off")
    
    return fig

# Streamlit界面部分
st.title("数轴生成器")
st.write("输入你想要显示在数轴上的标签和对应的数值")

# 用户输入数据
data_dict = {}
num_entries = st.number_input("输入你想显示的数字数量", min_value=1, max_value=10, value=5)
for i in range(num_entries):
    label = st.text_input(f"标签 {i + 1}", f"Label {i + 1}")
    value = st.number_input(f"数值 {i + 1}", value=0.0)
    data_dict[label] = value

# 用户设置数轴范围
x_min = st.number_input("数轴最小值", value=-3)
x_max = st.number_input("数轴最大值", value=4)
buffer = st.slider("标签之间的间隔调整（避免重叠）", min_value=0.1, max_value=1.0, value=0.2)

# 绘制数轴
if st.button("生成数轴"):
    fig = plot_number_line(data_dict, x_range=(x_min, x_max), buffer=buffer)
    st.pyplot(fig)
