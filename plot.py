import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# # make data:
# eigen = ['eigenfaces correct:', 'eigenfaces incorrect:', 'eigenfaces none det:']
# face =  ['facenet correct:', 'facenet incorrect:', 'facenet none det:',]
# eigeny = np.array([4, 12, 12])
# facey = np.array([12, 0, 16])
#
# # plot
# fig, ax = plt.subplots()
#
# eigenplot, = ax.bar(eigen, eigeny, width=1, edgecolor="white", linewidth=0.7, label='Eigenfaces')
# faceplot, = ax.bar(face, facey, width=1, edgecolor="white", linewidth=0.7, label='Facenet')
# ax.legend(handles=[eigenplot, faceplot])
#
# ax.set(xlim=(0, 6), xticks=np.arange(1, 8),
#        ylim=(0, 29), yticks=np.arange(1, 29))

data = [['correct', 'eigenfaces', 4], ['correct ', 'facenet', 12],
        ['incorrect', 'eigenfaces', 12], ['incorrect ', 'facenet', 0],
        ['none', 'eigenfaces', 12], ['none ', 'facenet', 16]]
data = pd.DataFrame(data, columns = ['Object', 'Type', 'Value'])

colors = {'eigenfaces':'red', 'facenet':'green'}
c = data['Type'].apply(lambda x: colors[x])

bars = plt.bar(data['Object'], data['Value'], color=c, label=colors)
plt.legend()
plt.show()
