import re
import os.path 

def load_data (data_folder):
         data_file = os.path.join(data_folder, "RefGenomeOrthologs") 
         # this empty dictionary is for storing the final output 
         d = {}
         # this empty list is for storing the orthologs of the same reference gene
         o = []
         # this empty list stores the common Uniprot_ID temporarily for comparison 
         e = None 
     
         # Define a function that takes the datafile as the sole argument               
         with open(data_file, "r+") as f:# change this to the file name
             # This function is for splitting the line
             for line in f:
                 y = re.split("[\| \t \n]", line)
                 z = re.split("=", y [2])
                 a = re.split("=", y [1])
                 b = re.split("=", y [4])
                 c = re.split("=", y [5])
                 # The above are only intermediates
                 # The below are the important variables
                 ref_gene_uniprot_id = z [1]
                 ref_gene_db_name = a [0]
                 ref_gene_db_id = a[-1]
                 ortholog_db_name = b [0]
                 ortholog_db_id = b [-1]
                 ortholog_uniprot_id = c [1]
                 ortholog_type = y [6]
                 ortholog_family = y [8]
        
                 if e is None: # for the first item
                    e = ref_gene_uniprot_id
                    d = { "id": ref_gene_uniprot_id,
                           "pantherdb": {
                           ref_gene_db_name: ref_gene_db_id,
                           "UniProtKB": ref_gene_uniprot_id,
                           }
                        }
           
                 if ref_gene_uniprot_id != e: # if read up to a different ref. gene 
                      d["ortholog: "] = o
                      yield d  
                      d.clear()
                      e = ref_gene_uniprot_id
                      d = { "id": ref_gene_uniprot_id,
                            "pantherdb": {
                            ref_gene_db_name: ref_gene_db_id,
                            "UniProtKB": ref_gene_uniprot_id
                            }
                          }
                      o = [{ortholog_db_name: ortholog_db_id,
                             "UniProtKB": ortholog_uniprot_id,
                             "Ortholog_type": ortholog_type,
                             "panther_family": ortholog_family
                             }
                          ]
        
                 else: # in this case the ref. gene is the same, just append the ortholog 
                     new = {ortholog_db_name: ortholog_db_id,
                            "UniProtKB": ortholog_uniprot_id,
                            "Ortholog_type": ortholog_type,
                            "panther_family": ortholog_family
                            }
                     o.append(new)
              
             if o:
             # at the last item, the ortholog is created but since it has no next ref_gene_uniprot_id to compare,
             # it does not go to the second if and output the result
             # and thus we need to let it output the result by giving it the condition if o == true. 
                d["ortholog: "] = o
                yield d       


if __name__ == "__main__":
    # The below code is what I used for testing whether my generator is working 
    # I opened the file named Test_folder containing 2 files, one is my test file
    # and the other is a "fake data file" that contains data with the same structure
    # Just to test if my parser can get the right file from the folder
    
    # Then, I feed the function with the directory to the test folder that contains 
    # both the right file and the fake file        
    import pprint
    g = load_data(".")
    pprint.pprint(g)
    for i in g:
         pprint.pprint(i)
