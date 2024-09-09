# Imports
import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
from itertools import combinations
import math
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors as nn
from matplotlib.backends.backend_pdf import PdfPages
from sklearn.preprocessing import StandardScaler as ss

def IQR_plots(data, filename, export_pdf):
     plt.figure()
     plt.boxplot(data)
     plt.ylabel(filename.split("-")[1].replace("_", " "))
     plt.title("Book " + filename.split("-")[1].replace("_", " ") + " Distribution")
     export_pdf.savefig()
     plt.close()

def DBSCAN_clust(data, export_pdf):
     #scale data
     data_norm = ss().fit_transform(data)
     
     #choose min_pts + eps
     min_pts = math.ceil(np.log(len(data)))
     eps = 20
      
     #cluster
     db = DBSCAN(eps = eps, min_samples = min_pts).fit(data)

     #find outliers
     clusters = pd.DataFrame(data = db.labels_, columns = ["Cluster"]).merge(data, left_index=True, right_index=True)
     outliers = clusters[clusters['Cluster'] == -1] 
     
     #visualization
     fig = plt.figure()
     axes_labels = data.columns.tolist()
     if len(data.columns) == 2:
         y_pred = db.fit_predict(data)
         plt.scatter(data.iloc[:, 0], data.iloc[:,1], c=y_pred, cmap='Paired')
         plt.xlabel(axes_labels[0])
         plt.ylabel(axes_labels[1])
         plt.title("DBSCAN of " + str(axes_labels[0]) + ' and ' +  str(axes_labels[1]))
     else:
         ax = fig.add_subplot(111, projection = '3d')
         y_pred = db.fit_predict(data)
         ax.scatter(data.iloc[:, 0], data.iloc[:,1], data.iloc[:,2], c=y_pred, cmap='Paired')
         ax.set_xlabel(str(axes_labels[0]))
         ax.set_ylabel(str(axes_labels[1]))
         ax.set_zlabel(str(axes_labels[2]))
         plt.title("DBSCAN of " + str(axes_labels[0]) + ', ' +  str(axes_labels[1]) + ', and ' + str(axes_labels[2]))
     export_pdf.savefig()
     plt.close()
     if (len(outliers) > 0):
         ax2 = plt.subplot()
         ax2.axis('off')
         ax2.table(cellText = outliers.values, colLabels = outliers.columns, loc='best')
         export_pdf.savefig()
         plt.close()

def main():
     """
     Main function
     
     :return: None
     """
     #import file
     reviews_raw = pd.read_csv("prog_book.csv")

     #change book type to numerical value
     Type_key = np.array(reviews_raw.Type.unique())
     reviews_raw.Type = reviews_raw.Type.apply(lambda x: x.replace(x, str(np.where(Type_key == x)[0][0])))
     reviews_raw.Type = reviews_raw.Type.apply(lambda x: int(x))
          
     #clean up data (included numerical Types in part 1 for consistency)
     reviews_raw.Reviews = reviews_raw.Reviews.apply(lambda x:x.replace(",",""))
     reviews_raw.Reviews = reviews_raw.Reviews.apply(lambda x: int(x))
     reviews = reviews_raw.select_dtypes(include=np.number)

     with PdfPages(r'Charts.pdf') as export_pdf:
          #univariate outlier detection: send numerical features to boxplot module   
          IQR_plots(reviews.Rating, "Univariate-Rating", export_pdf)
          IQR_plots(reviews.Reviews, "Univariate-Reviews", export_pdf)
          IQR_plots(reviews.Number_Of_Pages, "Univariate-Number_Of_Pages", export_pdf)
          IQR_plots(reviews.Price, "Univariate-Price", export_pdf)
          
          #multivariate outlier detection
          data_col=reviews.columns.tolist()
          doublets_col = list(combinations(data_col, r =2))
          for i in range(len(doublets_col)):     
               doublet = reviews.loc[:, doublets_col[i]]
               DBSCAN_clust(doublet, export_pdf)

          triplets_col = list(combinations(data_col, r =3))
          for i in range(len(triplets_col)):          
               triplet = reviews.loc[:, triplets_col[i]]
               DBSCAN_clust(triplet, export_pdf)
          
if __name__ == "__main__":
     main()
