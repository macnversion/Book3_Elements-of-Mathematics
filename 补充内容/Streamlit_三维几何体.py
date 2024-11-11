import streamlit as st
import numpy as np
import plotly.graph_objects as go
from math import cos, sin, pi

def rotate_points(points, angles):
    """根据欧拉角旋转点"""
    alpha, beta, gamma = angles
    
    # 绕X轴旋转
    Rx = np.array([
        [1, 0, 0],
        [0, cos(alpha), -sin(alpha)],
        [0, sin(alpha), cos(alpha)]
    ])
    
    # 绕Y轴旋转
    Ry = np.array([
        [cos(beta), 0, sin(beta)],
        [0, 1, 0],
        [-sin(beta), 0, cos(beta)]
    ])
    
    # 绕Z轴旋转
    Rz = np.array([
        [cos(gamma), -sin(gamma), 0],
        [sin(gamma), cos(gamma), 0],
        [0, 0, 1]
    ])
    
    # 组合旋转矩阵
    R = Rz @ Ry @ Rx
    
    # 应用旋转
    return points @ R.T

def create_tetrahedron():
    vertices = np.array([
        [1.0, 1.0, 1.0],
        [-1.0, -1.0, 1.0],
        [-1.0, 1.0, -1.0],
        [1.0, -1.0, -1.0]
    ]) / np.sqrt(3)
    
    faces = [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]]
    
    edges = [
        [0, 1], [0, 2], [0, 3],
        [1, 2], [1, 3], [2, 3]
    ]
    
    return vertices, faces, edges

def create_cube():
    vertices = np.array([
        [1, 1, 1], [1, 1, -1], [1, -1, 1], [1, -1, -1],
        [-1, 1, 1], [-1, 1, -1], [-1, -1, 1], [-1, -1, -1]
    ]) / np.sqrt(3)
    
    faces = [
        [0,1,3,2], [4,5,7,6], [0,1,5,4],
        [2,3,7,6], [0,2,6,4], [1,3,7,5]
    ]
    
    edges = [
        [0,1], [1,3], [3,2], [2,0],
        [4,5], [5,7], [7,6], [6,4],
        [0,4], [1,5], [2,6], [3,7]
    ]
    
    return vertices, faces, edges

def create_octahedron():
    vertices = np.array([
        [1, 0, 0], [-1, 0, 0],
        [0, 1, 0], [0, -1, 0],
        [0, 0, 1], [0, 0, -1]
    ])
    
    faces = [
        [0,2,4], [0,4,3], [0,3,5], [0,5,2],
        [1,2,4], [1,4,3], [1,3,5], [1,5,2]
    ]
    
    edges = [
        [0,2], [0,3], [0,4], [0,5],
        [1,2], [1,3], [1,4], [1,5],
        [2,4], [4,3], [3,5], [5,2]
    ]
    
    return vertices, faces, edges

def plot_polyhedron(vertices, faces, edges, angles, show_vertices=True, show_edges=True):
    # 应用旋转
    rotated_vertices = rotate_points(vertices, angles)
    x, y, z = rotated_vertices.T
    
    # 创建图形
    fig = go.Figure()
    
    # 添加面
    fig.add_trace(go.Mesh3d(
        x=x, y=y, z=z,
        i=[f[0] for f in faces],
        j=[f[1] for f in faces],
        k=[f[2] for f in faces],
        opacity=0.7,
        color='lightblue',
        name='faces'
    ))
    
    # 添加边
    if show_edges:
        for edge in edges:
            fig.add_trace(go.Scatter3d(
                x=[x[edge[0]], x[edge[1]]],
                y=[y[edge[0]], y[edge[1]]],
                z=[z[edge[0]], z[edge[1]]],
                mode='lines',
                line=dict(color='black', width=2),
                name='edges'
            ))
    
    # 添加顶点
    if show_vertices:
        fig.add_trace(go.Scatter3d(
            x=x, y=y, z=z,
            mode='markers',
            marker=dict(size=5, color='red'),
            name='vertices'
        ))
    
    # 设置布局
    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[-2, 2]),
            yaxis=dict(range=[-2, 2]),
            zaxis=dict(range=[-2, 2]),
            aspectmode='cube'
        ),
        width=700,
        height=700,
        showlegend=False
    )
    
    return fig

def main():
    st.title("交互式正多面体可视化")
    
    # 侧边栏控制
    st.sidebar.header("控制面板")
    
    # 选择正多面体类型
    polyhedron_type = st.sidebar.selectbox(
        "选择正多面体类型",
        ["正四面体", "正六面体（立方体）", "正八面体"]
    )
    
    # 旋转控制
    st.sidebar.subheader("旋转控制")
    alpha = st.sidebar.slider("绕X轴旋转", 0.0, 2*pi, 0.0)
    beta = st.sidebar.slider("绕Y轴旋转", 0.0, 2*pi, 0.0)
    gamma = st.sidebar.slider("绕Z轴旋转", 0.0, 2*pi, 0.0)
    
    # 显示选项
    st.sidebar.subheader("显示选项")
    show_vertices = st.sidebar.checkbox("显示顶点", True)
    show_edges = st.sidebar.checkbox("显示边", True)
    
    # 创建选中的正多面体
    if polyhedron_type == "正四面体":
        vertices, faces, edges = create_tetrahedron()
    elif polyhedron_type == "正六面体（立方体）":
        vertices, faces, edges = create_cube()
    else:  # 正八面体
        vertices, faces, edges = create_octahedron()
    
    # 绘制图形
    fig = plot_polyhedron(
        vertices, faces, edges, 
        (alpha, beta, gamma),
        show_vertices,
        show_edges
    )
    
    # 显示图形
    st.plotly_chart(fig)
    
    # 显示数据
    if st.sidebar.checkbox("显示数据"):
        col1, col2 = st.columns(2)
        with col1:
            st.write("顶点坐标：")
            st.write(vertices)
        with col2:
            st.write("面的定义：")
            st.write(faces)

if __name__ == "__main__":
    main()