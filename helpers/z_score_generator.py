
import numpy as np
import bisect
import multiprocessing
import time as t
import pprint

'''
Dictionary has the following structure:
list_length (1 through n) : {1 : [associated values] 
                through n : [associated values]}
'''
#values_lists = {} # this dictionary will contain the k-th highest observation for a sample of size n
#final_scores = {} # this dictionary will be structured the same way as the values lists, except that the final contained value will not be a list but instead be the observed value
#                   with the average of the 1 000 samples

def z_score_generator(num_samples: int) -> dict[int, dict[int,float]]:
    '''
    This function returns a dictionary containing the z-score of the k-th largest item from n-samples for all k and n up to n
    params:
        num_samples : Integer
    returns
        dictionary : dict[int, dict[int, float]]
    '''
    sample_list = []
    return_dictionary = {}

    for i in range(1,num_samples):
        # create the inner dictionary
        return_dictionary[i] = {}

        # take a sample so our length is i
        sample = np.random.standard_normal()

        # insert in such a way to keep sorted nature of list
        bisect.insort_left(sample_list, sample)

        #print(sample_list)
        for j in range(1,i+1):
            #print(sample_list[-j])
            return_dictionary[i][j] = sample_list[-j]
    
    #print(sample_list)
    #print()

    return return_dictionary

def process_final(dictionary: dict[int,dict[int,list]]):
    '''
    This function process our final dictionary from the generation into a dictionary with the same structure but using a mean value instead of an array
    params:
        dictionary : dict[int,dict[int,list]]; our final dictionary from the generation process
    returns
        mean_dict : dict[int, dict[int, float]]; the dictionary used to get good estimates
        std_dict : dict[int, dict[int,float]]; the dictionary used to get the standard deviations
    '''
    mean_dict = {}
    std_dict = {}
    for num_samples in dictionary.keys():
        
        # create key if not present
        if not num_samples in mean_dict:
            mean_dict[num_samples] = {}
            std_dict[num_samples] = {}

        for k_th in dictionary[num_samples].keys():
            
            # find the mean value of the samples
            mean_dict[num_samples][k_th] = np.mean(dictionary[num_samples][k_th])
            std_dict[num_samples][k_th] = np.std(dictionary[num_samples][k_th])

    return mean_dict, std_dict


if __name__ == "__main__":



    n = 250
    precision = 10000 # this controls the confidence interval around our estimate for the z-scores

    iter_array = [n] * precision
    st = t.time()
    
    with multiprocessing.Pool(processes=20) as pool:
        dictionaries = pool.map(z_score_generator, iter_array)
    pool.close()

    en = t.time()
    print("Took", en-st, "seconds to process information")

    # now we're going to do some stuff with dictionaries
    print("Size of dictionaries", len(dictionaries))
    #print(dictionaries)

    ''' Now we need to process these intermediary dictionaries into our final z score dictionary
    This final dictionary will have the same structure
    {
        num_samples : {k_th_largest : z_score value, ...},
        ...
    }
    Where the z_score value will be the mean of the 1000 runs
    '''
    final = {}
    for i in range(len(dictionaries)):
        # dictionaries[i] retrieves one particular dictionary
        one_dict = dictionaries[i]
        for num_samples in one_dict.keys():

            # initialize sub-dictionary if not present
            if not num_samples in final:
                final[num_samples] = {}

            for k_th in one_dict[num_samples].keys():

                # initialize sub-array if not present
                if not k_th in final[num_samples]:
                    final[num_samples][k_th] = []
                
                # append the result from this dictionary into final
                final[num_samples][k_th].append(one_dict[num_samples][k_th])
        
        if i%50==0:
            print(i/len(dictionaries)*100, "\%\ done")

    # now we have a dictionary that we can process how we like :)
    mean_dict, std_dict = process_final(final)
    #pprint.pprint(processed)

    import csv


    # Define the CSV file path
    csv_file_path = 'mean_dict.csv'

    # Flatten the nested dictionary to a list of dictionaries
    final_list = []

    # write the maximum field names
    field_names = ["num_samples"] + [str(i+1)+"th largest" for i in range(n)]

    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow(field_names)

        for num_samples, inner_dict in mean_dict.items():
            row = [str(num_samples)] + list(map(str, inner_dict.values()))
            writer.writerow(row)

    print(f"CSV file '{csv_file_path}' has been created successfully.")

    csv_file_path = 'std_dict.csv'
    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow(field_names)

        for num_samples, inner_dict in std_dict.items():
            row = [str(num_samples)] + list(map(str, inner_dict.values()))
            writer.writerow(row)





    



