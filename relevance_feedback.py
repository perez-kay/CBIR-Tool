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

def feature_mtx():
    """
    Creates the feature matrix for all images in the 'images/' folder.

    Returns
    -------
    DataFrame
        A pandas Dataframe containing the feature data. The rows are the images
        and the columns are the features. Has shape 100 x 89
    """
    # FIRST COL = IMG SIZE
    color = pd.read_excel('colorCode.xlsx', header=None, index_col=0).T
    intens = pd.read_excel('intensity.xlsx', header=None, index_col=0).T
    
    color = color.to_dict(orient='list')
    intens = intens.to_dict(orient='list')

    # dict like: {img_num : [bins]}
    all = dict()

    # for each image 1-100
    for i in range(1, 101, 1):
        color_img_size = color[i][0]
        intens_img_size = intens[i][0]
        color_features = list()
        intens_features = list()
        for j in range(1, len(color[i]), 1):
            color_features.append(color[i][j] / color_img_size)

        for j in range(1, len(intens[i]), 1):
            intens_features.append(intens[i][j] / intens_img_size)
        
        all[i] = np.concatenate((np.array(color_features), np.array(intens_features)))
    all = collections.OrderedDict(sorted(all.items()))
    df = pd.DataFrame(all).T.fillna(0)
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
    df = pd.DataFrame(normalized).fillna(0)
    with open('normalized_matrix2.csv', 'w') as file:
        df.to_csv(path_or_buf=file)

def calculate_weighted_dist(query, retrieved, weight):
    if type(weight) == float:
        return (weight * abs((query - retrieved))).sum()
    else:
    #print(query)
        query = query.tolist()
        weight = weight.tolist()
        retrieved = retrieved.tolist()
        
        distance = 0
        for i in range(len(query)):
            distance += (weight[i] * abs(query[i] - retrieved[i]))
        return distance



def calculate_distance(normalized_matrix, query_num, weight):
    # query img should be the img num
    # this gives the series with the query img's features
    query_features = normalized_matrix[query_num]

    results = list()
    for retrieved_num, retrieved_features in normalized_matrix.iteritems():
        distance = calculate_weighted_dist(query_features,
                                           retrieved_features, weight)
        retrieved_path = 'images/' + str(retrieved_num) + '.jpg'
        results.append((distance, retrieved_path))
    return sorted(results)


# assuming that if the user switches from I+CC to something else, app does NOT
# nee d
def calculate_updated_weight(relevant_imgs, normalized_matrix, query_num):
    # loop through set and pull out all img features from matrix
    rf_features = dict()
    for img_path in relevant_imgs:
        img_num = get_img_num(img_path)
        img_features = normalized_matrix[img_num]
        rf_features[img_num] = img_features
    rf_matrix = pd.DataFrame(rf_features)
    
    std = rf_matrix.T.std()
    avg = rf_matrix.T.mean()
    #print(rf_matrix.T.std())
    #print(normalized_matrix)
    
    # checks std vals and removes 0s based on condition
    std = check_std(std, avg)
    #print('len std:', len(std))
    
    updated_weights = compute_new_weights(std)
    normalized_weights = compute_normalized_weights(updated_weights)

    return calculate_distance(normalized_matrix, query_num, normalized_weights)

def check_std(std, avg):
    std_vals = std.tolist()
    avg_vals = avg.tolist()
    for i in range(len(std_vals)):
        if std_vals[i] == 0:
            if avg_vals[i] != 0:
                std_vals[i] = 0.5 * (min(filter(None, std_vals)))
    return std_vals

def compute_new_weights(std):
    new_weights = list()
    for i in range(len(std)):
        new_weights.append((1 / std[i]) if std[i] != 0 else 0)
    return new_weights

def compute_normalized_weights(weights):
    weights = pd.Series(weights)
    sum_weights = weights.sum()
    #print(sum_weights)
    normalized_weights = weights / sum_weights
    return normalized_weights
        

def feature_mtx():
    # FIRST COL = IMG SIZE
    color = pd.read_excel('colorCode.xlsx', header=None, index_col=0).T
    intens = pd.read_excel('intensity.xlsx', header=None, index_col=0).T
    
    color = color.to_dict(orient='list')
    intens = intens.to_dict(orient='list')

    # dict like: {img_num : [bins]}
    all = dict()

    # for each image 1-100
    for i in range(1, 101, 1):
        color_img_size = color[i][0]
        intens_img_size = intens[i][0]
        color_features = list()
        intens_features = list()
        for j in range(1, len(color[i]), 1):
            color_features.append(color[i][j] / color_img_size)

        for j in range(1, len(intens[i]), 1):
            intens_features.append(intens[i][j] / intens_img_size)
        
        all[i] = np.concatenate((np.array(color_features), np.array(intens_features)))
    all = collections.OrderedDict(sorted(all.items()))
    df = pd.DataFrame(all).T.fillna(0)
    return df

get_normalized_matrix(feature_mtx())



