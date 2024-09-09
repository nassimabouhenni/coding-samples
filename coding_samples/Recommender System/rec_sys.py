# Imports
import os
import sys

import pandas as pd 
import numpy as np
from itertools import product

from surprise import SVD
from surprise import Reader
from surprise import Dataset

from collections import defaultdict


#Functions

#Question 1:
def user_user(user_shows):
     alex_shows = user_shows[499][:]
     cs = cos_sim(user_shows, alex_shows, 'uu')
     r_tv = np.matmul(cs, user_shows)

     return r_tv

#Question 2:
def item_item(user_shows):
     cs = cos_sim(user_shows.transpose(), user_shows, 'ii')
     r_tv = np.matmul(user_shows[499][:], cs)
     r_tv = np.squeeze(np.asarray(r_tv.transpose()))
     
     return r_tv

def cos_sim(a, b, rec):

     #create array of dot products for each x
     dot_prod = np.matmul(a, b)

     #0^2 = 0, 1^2 = 1; sum across rows; take square root to obtain norm
     sq_sums = np.sum(a, axis = 1) 
     norms = np.sqrt(sq_sums)
     alex_norm = norms[499]
     
     #multiply norms, obtain cos_sim array for each user against Alex//for each item pairing
     if rec == 'uu':
          norm_prod = alex_norm*norms
     elif rec == 'ii':
          norms = np.asmatrix(norms)
          norm_prod = norms.transpose()*norms

     cs = np.divide(dot_prod, norm_prod)

     return cs

#Question 3:
def latent_factor(user_shows):
     #format ratings matrix for Surprise
     ID_df = pd.DataFrame(list(product(range(np.shape(user_shows)[0]),range(np.shape(user_shows)[1]))), \
     columns=['User_ID', 'Show_ID'])
     ratings = pd.DataFrame(user_shows.flatten(), columns = ['Rating'])
     rate_mat = pd.concat([ID_df, ratings], axis=1).drop(range(280937,281037))
 
     #read data     
     reader = Reader(rating_scale=(0,1))
     data = Dataset.load_from_df(rate_mat[['User_ID', 'Show_ID', 'Rating']], reader)
     trainset = data.build_full_trainset()

     #build algorithm, train on whole set
     algo = SVD(n_factors = 10) 
     algo.fit(trainset)
     
     #predict!
     testset = trainset.build_anti_testset()
     predictions = algo.test(testset)
     
     top_n = get_top_n(predictions)
          
     return top_n
           
def get_top_n(predictions):
     n = 5
     top_n = defaultdict(list)  
     for uid, iid, true_r, est, _ in predictions:
          top_n[uid].append([iid, est])

     # Then sort the predictions for each user and retrieve the k highest ones.
     for uid, user_ratings in top_n.items():
          user_ratings.sort(key=lambda x: x[1], reverse=True)
          top_n[uid] = user_ratings[:n]
      
     return top_n

#All 3 Questions-Write to File:
def match_shows(shows, output, title):
     #match shows
     unknown_shows = pd.Series(output, index = shows).head(100)
     top_shows = unknown_shows.sort_values(ascending = False)[0:5]

     #clean up for output file
     top_shows = pd.DataFrame((top_shows.index.values, top_shows), index = ["TV Show", "Similarity Score"])
     top_shows = top_shows.transpose().to_string().replace(",","").replace("(","").replace(")","")

     write_file(top_shows, title)

     return None

def match_showslf(shows, output, title):
     #clean dataset
     output_df = pd.Series(output.values())
     output_np = np.array([np.array(xi) for xi in output_df]).flatten()
     tv_shows_ID = output_np[::2].astype(int)
     similarity_scores = output_np[1::2]

     #match to shows
     top_shows_titles = shows.iloc[tv_shows_ID].to_numpy().flatten()
     top_shows = pd.DataFrame((top_shows_titles, similarity_scores), index = ['TV Show', 'Similarity Score'])
     top_shows = top_shows.transpose().to_string()
     write_file(top_shows, title)

     return None

def write_file(top_shows, title):
     #save txt file of shows
     ans_file = open("answers.txt", "a")
     ans_file.writelines(title) 
     ans_file.write(top_shows)
     ans_file.close()
     
     return None
       
def main():
     """
     Main function
     """
     #os.remove("answers.txt")

     #Create dataframes/matrices    
     user_shows = np.loadtxt('user-shows.txt', dtype=int)
     shows = pd.read_csv('shows.txt', sep = ' ', header = None)

     #Call recommender systems
     uu_output = user_user(user_shows)
     match_shows(shows, uu_output, "user-user recommender:\n")

     ii_output = item_item(user_shows)
     match_shows(shows, ii_output, "\n\nitem-item recommender:\n")

     lf_output = latent_factor(user_shows)
     match_showslf(shows, lf_output, "\n\nlatent-factor recommender:\n")

if __name__ == '__main__':
     main()
