import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

np.set_printoptions(suppress=True, precision=4)

X = np.load('clustering_matrix.npy')
#print(X.shape)
x_shose = np.load('shese_for_clus.npy')
x_tennis = np.load('tennis_for_clus.npy')
print(x_shose.shape,x_tennis.shape)

X = np.vstack((x_shose,x_tennis))

print(X.shape)


def standard_scaler(matrix):
    epsilon = 1e-9
    mean_vals = np.mean(matrix, axis=0)
    std_vals = np.std(matrix, axis=0)
    standardized_matrix = (matrix - mean_vals) / (std_vals + epsilon)
    return standardized_matrix

X = standard_scaler(X)




kmeans = KMeans(n_clusters=2, random_state=1)

X[:,0]*=2.5
X[:,1]*=0
X[:,2]*=0
X[:,3]*=0
X[:,4]*=1
X[:,5]*=2.5

# חישוב ממוצע הפיצ'רים לכל סוג כדור


kmeans.fit(X[:, [0,1,2,3,4,5]])

print("Clustering done!")
print(kmeans.labels_)
print(kmeans.cluster_centers_)

from sklearn.metrics import silhouette_score


score = silhouette_score(X, kmeans.labels_)
print(f"Silhouette Score: {score:.2f}")

inertia_values = []
K_range = range(1, 11)



for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X)
    inertia_values.append(kmeans.inertia_) # השגת ה-Inertia מהמודל

# ציור הגרף
plt.figure(figsize=(8, 5))
plt.plot(K_range, inertia_values, 'bx-')
plt.xlabel('Number of clusters (K)')
plt.ylabel('Inertia')
plt.title('The Elbow Method showing the optimal K')
plt.show()

'''
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score # חובה לייבא את זה בנפרד

# 1. הפעלת ה-PCA - צמצום מ-5 ממדים ל-2 כדי שנוכל לצייר
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X) # משתמשים בנתונים המנורמלים!

# 2. חילוץ הליבלים מהמודל שהרצת קודם
# שים לב לסימן ה _ בסוף labels_
cluster_labels = kmeans.labels_ 

# 3. חישוב הציון (Silhouette Score)
# משתמשים ב-X_scaled ובליבלים שהפקנו
s_score = silhouette_score(X, cluster_labels)

# 4. ציור הגרף
plt.figure(figsize=(10, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=cluster_labels, cmap='viridis', edgecolors='k', alpha=0.7)
plt.colorbar(label='Cluster Label') # מוסיף מקרא צבעים
plt.title(f'Cluster Visualization (Silhouette: {s_score:.2f})')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()
'''