import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import warnings
warnings.filterwarnings('ignore')

print("Loading RFM data...")
rfm = pd.read_csv(r'C:\Neuralretail\data\features\rfm.csv')

# Scale the data
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm[['Recency', 'Frequency', 'Monetary']])

# Use k=6 which gave best score of 0.5495
kmeans = KMeans(n_clusters=6, random_state=42, n_init=10)
rfm['Segment'] = kmeans.fit_predict(rfm_scaled)

segment_labels = {0:'Champions', 1:'Loyal Customers', 
                  2:'At Risk', 3:'New Customers', 
                  4:'Hibernating', 5:'Lost'}
rfm['SegmentName'] = rfm['Segment'].map(segment_labels)

score = silhouette_score(rfm_scaled, rfm['Segment'])
print(f"Silhouette Score: {score:.4f}")

print("\nSegment distribution:")
print(rfm['SegmentName'].value_counts())

rfm.to_csv(r'C:\Neuralretail\data\features\segments.csv', index=False)
print("\nSegments saved!")
