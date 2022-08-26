import glob
import json

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

from utils.convert_to_csv import csv_convert, pd_convert_csv


def extract_kv(config_file):
    # load configuration info from config.json file
    with open(config_file) as f:
        config = json.load(f)
    endpoint = config["endpoint"]
    key = config["key"]
    file_type = config["file_type"]
    model_id = config["model_id"]

    # call the Form recogniser client on azure api
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    # list of the files in the input directory
    all_files = glob.glob("input\\" + file_type + r"\*pdf")
    data_dict_list = list()
    n = 1
    # iterate through all files in the directory
    for testData in all_files:
        input_file = open(testData, "rb")
        # analyze each file using the model mentioned in the config file
        poller = document_analysis_client.begin_analyze_document(model_id, input_file)
        result = poller.result()

        output = dict()
        # Extract key value pairs from the analyzed output of each file
        for idx, document in enumerate(result.documents):
            print("--------Analyzing document #{}--------".format(idx + n))
            # print("Document has type {}".format(document.doc_type))
            print("Document was analyzed by model with ID {}".format(result.model_id))
            print("Document has confidence {}".format(document.confidence))

            for name, field in document.fields.items():
                field_value = field.value if field.value else field.content
                output[name] = field_value
            output["Document confidence"] = document.confidence
            n += 1
        if file_type == "invoice":
            del (output["BankDetails"])
        else:
            del (output["Skills"])
        # add the key value pair output of each file to a list of dictionaries
        data_dict_list.append(output)
    print("Total Documents analyzed:", len(data_dict_list))
    # convert the list of dictionaries to csv
    pd_convert_csv(data_dict_list, file_type)


if __name__ == "__main__":
    extract_kv("resources/config.json")
