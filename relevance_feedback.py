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
        bins = np.concatenate((intens[1], color[1])) / img_size
        data[img_num] = bins
    data = collections.OrderedDict(sorted(data.items()))
    df = pd.DataFrame(data).T
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
