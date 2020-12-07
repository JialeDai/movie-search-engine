import pymongo
from bson.json_util import dumps
from bson import ObjectId
import numpy as np
from scipy.stats.stats import pearsonr

# check whether the user has ratings
def movie_recommend(user_name):
    client = pymongo.MongoClient("mongodb://Song:a931021@cluster0-shard-00-00-ywxjv.azure.mongodb.net:27017,cluster0-shard-00-01-ywxjv.azure.mongodb.net:27017,cluster0-shard-00-02-ywxjv.azure.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
    movie_db = client.movie_web
    login_user = movie_db.catalog_users.find({'name': user_name})[0]
    login_user_oid = login_user['_id']
    login_user_rated_ids = list(login_user['ratings'].keys())

    # get login user's unrated movies ids (drawback: when user and rated movies get larger, the time cost will grow)
    all_rated_movie_ids = []
    other_user_oids = []
    users = movie_db.catalog_users.find()
    for user in users:
        if 'ratings' in user:
            rated_movie_ids = list(user['ratings'].keys())
            all_rated_movie_ids += rated_movie_ids
            other_user_oids.append(user['_id'])
    all_rated_movie_ids = set(all_rated_movie_ids)
    other_user_oids.remove(login_user_oid)
    unrated_movie_ids = [id for id in all_rated_movie_ids if id not in login_user_rated_ids]

    # loop over all rated movie ids and choose not rated movies for login user
    predict_ratings = {}
    for unrated_movie_id in unrated_movie_ids:

        # peer to peer calculate the correlation value
        denomiator_sum = 0
        nomiator_sum = 0
        sum_login = 0
        count = 0
        for other_user_oid in other_user_oids:
            other_user = movie_db.catalog_users.find({'_id': other_user_oid})[0]
            other_user_rated_ids = list(other_user['ratings'].keys())
            
            # check whether this user has rated this movie
            if unrated_movie_id in other_user_rated_ids:
                count += 1
                join_rated_ids = [id for id in login_user_rated_ids if id in other_user_rated_ids]

                # get the rate value for each user to form each array
                login_user_ratings = []
                other_user_ratings = []
                for join_rated_id in join_rated_ids:
                    login_user_ratings.append(login_user['ratings'][join_rated_id])
                    other_user_ratings.append(other_user['ratings'][join_rated_id])

                # converting list into arrays
                login_user_ratings = np.array(login_user_ratings)
                other_user_ratings = np.array(other_user_ratings)

                # calculating pearsonr correlation
                p = pearsonr(login_user_ratings, other_user_ratings)[0]

                # calculating the average in other_user_ratings
                sum_login += login_user_ratings.sum() / len(login_user_ratings)
                av_other = other_user_ratings.sum() / len(other_user_ratings)

                # calculating the sums for this iteration
                rated_value = other_user['ratings'][unrated_movie_id]
                nomiator_sum += p * (rated_value - av_other)
                denomiator_sum += abs(p)
        predict_rating = nomiator_sum / denomiator_sum + sum_login / count
        predict_ratings[unrated_movie_id] = predict_rating

    # build recommand list for login user
    sorted_ratings = sorted(predict_ratings.items(), key=lambda item:item[1])
    recommand_list = []
    if len(sorted_ratings) < 3:
        recommand_list = sorted_ratings
    else:
        recommand_list = sorted_ratings[-3:]
    recommand_ids = [ObjectId(item[0]) for item in recommand_list]

    return recommand_ids
    
