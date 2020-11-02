import numpy as np
import os
#from skimage.filters import gaussian
from skimage import io

def load_stack(stack_list):
    z = len(stack_list)
    img_example = io.imread(stack_list[0], as_gray=True)
    h,w = np.shape(img_example)
    tiffarray=np.zeros((h,w,z))
    for n,img in enumerate(stack_list):
        tiffarray[:,:,n]=  (io.imread(stack_list[n], as_gray=True))  #normalize
    return tiffarray    
        

def flatten_dict(*args):
    ret_list = [i for i in range(len(args))]
    for i, ar in enumerate(args):
        ret_list[i] = np.concatenate([*ar.values()], axis=0)
    return ret_list

def createFolder(directory):
    '''
    function to create directories if they dont already exist
    '''
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory

    except OSError:
        print('Error: Creating directory. ' + directory)


def make_iterable(value):
    if not hasattr(value, '__iter__') or isinstance(value,str):
        return [value]
    else:
        return value



def convolution_fitler_with_nan(arr1, function, **kwargs):

    '''
        applies a gaussian to an array with nans, so that nan values are ignored.
    :param arr1:
    :param function: any convloution functio, such as skimage.filters.gaussian or scipy.ndimage.filters.ndimage.uniform_filter
    :param f_args:  kwargs for the convolution function
    :return:
    '''


    arr_zeros = arr1.copy()
    arr_ones = np.zeros(arr1.shape)
    arr_zeros[np.isnan(arr1)] = 0  # array where all nans are replaced by zeros
    arr_ones[~np.isnan(arr1)] = 1  # array where all nans are replaced by zeros and all other values are replaced by ones

    filter_zeros = function(arr_zeros, **kwargs)  # gaussian filter applied to both arrays
    filter_ones = function(arr_ones, **kwargs)
    filter_final = filter_zeros / filter_ones  # devision cancles somehow the effect of nan positions
    filter_final[np.isnan(arr1)] = np.nan  # refilling original nans

    return filter_final

