import jedi
import sys
from Jedi.read_py_files import ReadPyFiles
from Enums.jedi_error_enum import JediErrorEnum
from Utils.json_writer import JsonWriter
from Models.inference import Inference

#TODO mudar o nome dessa classe
class Skywalker(object):

    def __init__(self, project_root_folder):
        self.project_root_folder = project_root_folder
        self.files = None
        self.inferences = {}
    
    def run_jedi(self):
        #Lê os arquivos
        self.__search_project_folder()
        #Faz a inferência
        self.__make_inference()
        #Entrega arquivos de uma maneira legível
    
    def __search_project_folder(self):
        read_py_files = ReadPyFiles(self.project_root_folder)
        read_py_files.find_pys()
        self.files = read_py_files.get_files_dictionary()
    
    #TODO tratar quando tiver mais de dois arquivos em uma classe
    #TODO pegar o método que está chamando
    #TODO pegar o arquivo que está chamando
    def __make_inference(self):
        if self.files == None:
            raise Exception(JediErrorEnum.NO_FILES_FOUND.value)

        for key in self.files:
            file = self.files[key]

            # script_names = jedi.Script(path=file.file_path).get_names(all_scopes=True)
            jedai = jedi.Script(path=file.file_path)

            script_names = jedi.Script(path=file.file_path).get_names(all_scopes=True, definitions=True)

            for definition in script_names:

                if not self.__should_ignore_definition(definition, file):
                    inferences = definition.infer()

                    file_name = definition.module_name
                    variable_name = definition.name
                    inference_key = definition.full_name if definition.full_name != None else definition.desc_with_module

                    self.inferences[inference_key] = Inference(file_name, variable_name)

                    for inference in inferences:
                        self.inferences[inference_key].add_type(inference.name)
            pass

    
    def __should_ignore_definition(self, inference, file):
        if inference.type == "statement" or inference.type == "param":
            return False
        return True
    
    def get_jedi_results(self):
        for index in self.files:
            print(self.files[index].get_as_dict())
    
    def register_jedi_results(self):
        list_of_files_as_dict = []
        for index in self.files:
            list_of_files_as_dict.append(self.files[index].get_as_dict())
        JsonWriter.write_json(list_of_files_as_dict)


# if __name__ == "__main__":
#     project_root_folder = "/home/eduardol/UFLA/tcc/arquivos-arthur/dataset/sistema0"

#     for key in files:
#         file_dict = files[key]

#         # script_names = jedi.Script(path=file_dict['path']).get_names(all_scopes=True, definitions=True, references=True)
#         script_names = jedi.Script(path=file_dict['path']).get_names()


#         for definition in script_names:
#             inferences = definition.infer()
#             for inference in inferences:
#                 files[key]['types'].add(inference.name)

#             # inference = definition.infer()[0].name
#             # files[key]['types'].append(inference)
        

#     a = 2



