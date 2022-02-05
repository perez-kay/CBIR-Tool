import cbir_methods, collections, os
import numpy as np
import pandas as pd

def get_img_num(img_path):
    """
    Returns the number of the image, as an integer.

    Parameters
    ----------
    img_path : str
        The image path, in the format 'images/{number}.jpg'
    
    Returns
    -------
    int
        The image's number
    """
    
    if len(img_path) == 12:
        return int(img_path[7:8])
    elif len(img_path) == 13:
        return int(img_path[7:9])
    else:
        return int(img_path[7:10])

def get_feature_matrix():
    """
    Creates the feature matrix for all images in the 'images/' folder.

    Returns
    -------
    DataFrame
        A pandas Dataframe containing the feature data. The rows are the images
        and the columns are the features.
    """
    data = dict()
    for img in os.listdir('images/'):
        if img == 'Thumbs.db':
            continue
        path = 'images/' + img
        img_num = get_img_num(path)
        intens = cbir_methods.calculate_intensity(path)
        color = cbir_methods.calculate_color_code(path)
        img_size = intens[0]
        intensity_bins = intens[1] / img_size
        color_bins = color[1] / img_size
        intensity_bins = np.around(intensity_bins, 5)
        color_bins = np.around(color_bins, 5)
        bins = np.concatenate((intensity_bins, color_bins))
        data[img_num] = bins
    data = collections.OrderedDict(sorted(data.items()))
    df = pd.DataFrame(data).T.fillna(0)
    return df

def get_normalized_matrix(feature_matrix):
    """
    Creates the normalized matrix and saves it into a CSV file.

    Parameters
    ----------
    feature_matrix : DataFrame
        The feature matrix for all images
    """
    avg = feature_matrix.mean()
    std = feature_matrix.std()

    normalized = dict()
    idx = 0
    for col, feature in feature_matrix.iteritems():
        normalized_data = (feature - avg[idx]) / std[idx]
        normalized[col] = normalized_data
        idx += 1
    df = pd.DataFrame(normalized)
    with open('normalized_matrix.csv', 'w') as file:
        df.to_csv(path_or_buf=file)


#df = pd.read_csv('normalized_matrix.csv', index_col=0).T

# ex = {1:[.25,.375,.375,.25,.25,.25,.25], 2:[.1,.5,.4,0,0,.5,.5], 3:[.4,.4,.2,.4,.4,.2,0], 4:[.4,.4,.2,.2,.2,.2,.4]}
# df = pd.DataFrame(ex).T
# print(df)

# avg = df.mean()
# std = df.std()

# normalized = dict()
# idx = 0
# for col, feature in df.iteritems():
#     normalized_data = (feature - avg[idx]) / std[idx]
#     normalized[col] = normalized_data
#     idx += 1
# df = pd.DataFrame(normalized)
# print(df)



def calculate_weighted_dist(query, retrieved, weight):
    return (weight * abs((query - retrieved))).sum()
    #print(query)
    # query = np.nan_to_num(query.to_numpy())
    
    # retrieved = np.nan_to_num(retrieved.to_numpy())
    # distance = 0
    # for i in range(query.size):
    #     distance += (weight * abs(query[i] - retrieved[i]))
    # return distance



def calculate_no_bias_dist(normalized_matrix, query_num):
    # query img should be the img num
    # this gives the series with the query img's features
    query_features = normalized_matrix[query_num]

    results = list()
    weight = 1/89
    for retrieved_num, retrieved_features in normalized_matrix.iteritems():
        distance = calculate_weighted_dist(query_features,
                                           retrieved_features, weight)
        retrieved_path = 'images/' + str(retrieved_num) + '.jpg'
        results.append((distance, retrieved_path))
    return sorted(results)



# df = pd.read_csv('normalized_matrix.csv', index_col=0).T

#def calculate_updated_weight(relevant_imgs):
    # somehow need to save this list




# print(calculate_no_bias_dist(df, 1))


