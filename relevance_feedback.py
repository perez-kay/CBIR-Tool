import collections
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
    The histogram data used is the data in Professor Chen's excel sheets;
    'colorCode.xlsx' and 'intensity.xlsx'.

    Returns
    -------
    pandas.DataFrame
        A Dataframe containing the feature data. The rows are the images
        and the columns are the features. Has shape 100 x 89
    """
    
    color = pd.read_excel('colorCode.xlsx', header=None, index_col=0).T
    intens = pd.read_excel('intensity.xlsx', header=None, index_col=0).T
    
    color = color.to_dict(orient='list')
    intens = intens.to_dict(orient='list')
    combined = dict()

    for i in range(1, 101, 1):
        color_img_size = color[i][0]
        intens_img_size = intens[i][0]
        color_features = list()
        intens_features = list()

        for j in range(1, len(color[i]), 1):
            color_features.append(color[i][j] / color_img_size)
        for j in range(1, len(intens[i]), 1):
            intens_features.append(intens[i][j] / intens_img_size)
        
        combined[i] = np.concatenate((np.array(color_features), np.array(intens_features)))

    combined = collections.OrderedDict(sorted(combined.items()))
    df = pd.DataFrame(combined).T.fillna(0)
    return df


def get_normalized_matrix(feature_matrix):
    """
    Creates the normalized matrix and saves it into a CSV file.

    Parameters
    ----------
    feature_matrix : pandas.DataFrame
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

    with open('normalized_matrix.csv', 'w') as file:
        df.to_csv(path_or_buf=file)

def calculate_weighted_dist(query, retrieved, weight):
    """
    Calculates the weighted Manhattan Distance between the query image and the
    retrieved image.

    Parameters
    ----------
    query : pandas.Series
        Contains the 89 features for the query image
    retrieved : pandas.Series
        Contains the 89 features for the retrieved image
    weight : float or pandas.Series
        The weight used in the calculation
        The original weight, 1/N is passed in as a float, whereas the
        normalized weights are passed in as a pandas.Series

    Returns
    -------
    float
        The distance computed
    """
    
    if type(weight) == float:
        return (weight * abs((query - retrieved))).sum()
    else:
        query = query.tolist()
        weight = weight.tolist()
        retrieved = retrieved.tolist()
        
        distance = 0
        for i in range(len(query)):
            distance += (weight[i] * abs(query[i] - retrieved[i]))
        return distance



def calculate_distance(normalized_matrix, query_num, weight):
    """
    Calculates the weighted Manhattan Distance between the query image and all
    images in the database.

    Parameters
    ----------
    normalized_matrix : pandas.DataFrame
        The normalization matrix for all images
    query_num : int
        The number of the query image (1-100)
    weight : float or pandas.Series
        The weight used in the distance calculation
        The original weight, 1/N is passed in as a float, whereas the
        normalized weights are passed in as a pandas.Series

    Returns
    --------
    list
        A sorted list of tuples containing all of the distances. The first
        value in each tuple is the distance. The second is the image path.
        The list is sorted in ascending order based on distance.
    """
    
    query_features = normalized_matrix[query_num]
    results = list()

    for retrieved_num, retrieved_features in normalized_matrix.iteritems():
        distance = calculate_weighted_dist(query_features,
                                           retrieved_features, weight)
        retrieved_path = 'images/' + str(retrieved_num) + '.jpg'
        results.append((distance, retrieved_path))
    return sorted(results)



def calculate_updated_weight(relevant_imgs, normalized_matrix, query_num):
    """
    Calculates the normalized weights based on the relevant images and returns
    the new distances.

    Parameters
    ----------
    relevant_imgs : set
        Contains the image paths of each relevant image chosen by the user
    normalized_matrix : pandas.DataFrame
        The normalization matrix for all images
    query_num : int
        The number of the query image (1-100) 
    """
    
    rf_features = dict()
    for img_path in relevant_imgs:
        img_num = get_img_num(img_path)
        img_features = normalized_matrix[img_num]
        rf_features[img_num] = img_features
    rf_matrix = pd.DataFrame(rf_features)
    
    std = rf_matrix.T.std()
    avg = rf_matrix.T.mean()
    std = check_std(std, avg)

    updated_weights = compute_new_weights(std)
    normalized_weights = compute_normalized_weights(updated_weights)

    return calculate_distance(normalized_matrix, query_num, normalized_weights)

def check_std(std, avg):
    """
    Checks if any standard deviation values are 0 and updates them accordingly.

    Parameters
    ----------
    std : pandas.Series
        The standard deviation values computed from relevant image features
    avg : pandas.Series
        The average values computed from relevant image features

    Returns
    --------
    list
        Contains the previous standard deviations and any updated ones
    """
    
    std_vals = std.tolist()
    avg_vals = avg.tolist()
    for i in range(len(std_vals)):
        if std_vals[i] == 0:
            if avg_vals[i] != 0:
                std_vals[i] = 0.5 * (min(filter(None, std_vals)))
    return std_vals

def compute_new_weights(std):
    """
    Computes the updated weights based on the standard deviation values of
    the relevant features.

    Parameters
    ----------
    std : list
        The updated standard deviation values
    
    Returns
    -------
    list
        The updated weights
    """
    
    new_weights = list()
    for i in range(len(std)):
        new_weights.append((1 / std[i]) if std[i] != 0 else 0)
    return new_weights

def compute_normalized_weights(weights):
    """
    Computes the normalized weights based on the updated weights.

    Parameters
    ----------
    weights : list
        The updated weights

    Returns
    -------
    pandas.Series
        The normalized weights
    """

    weights = pd.Series(weights)
    sum_weights = weights.sum()
    normalized_weights = weights / sum_weights
    return normalized_weights
