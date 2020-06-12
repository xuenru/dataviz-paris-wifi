import numpy as np
import plotly.graph_objects as go
r, theta = np.mgrid[0.6:1:7j, 0:(360/8*7):7j]
color = np.random.random(r.shape)
whitecolor=np.zeros(14)

#color=[90, 51, 126, 164, 203, 232, 218, 182, 156, 121, 126, 45, 129, 117, 70, 66, 72, 93, 17, 10, 21, 20, 38, 72, 73, 44, 101, 88, 40, 18]
color=[16, 49, 85, 52, 75, 114, 22, 8, 55, 38, 61, 54, 50, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0]

color=np.asarray(color)
color=np.append(whitecolor,color)

fig = go.Figure(go.Barpolar(
    r=r.ravel(),
    theta=theta.ravel(),
    marker_color=color.ravel()),)
fig.update_layout(polar_bargap=0,showlegend=False

                  )
fig.show()