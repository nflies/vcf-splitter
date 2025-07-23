#!/usr/bin/env python3

import os
from pathlib import Path
import re
import sys

from typing import List


class VcfSplitter:
    __pattern_split_cvf: re.Pattern = re.compile(r"(?<=END:VCARD)\s*\n")
    __pattern_read_name: re.Pattern = re.compile(r"\nNICKNAME:(.+)")
    
    def __init__(self, input_file_path: str, output_dir_path: str):
        self.__input_file_path: str = input_file_path
        self.__output_dir_path: str = output_dir_path
    
    def split_vcf_file(self):
        contacts: List[str] = []
        
        with open(self.__input_file_path, "r") as input:
            print("Opened " + self.__input_file_path + " as input file.")
            contacts: List[str] = self.__split_vcf_string(input.read())
            
            if not contacts:
                raise Exception("No contacts found in input file!")
            
            for contact in contacts:
                self.__write_vcf_file(contact)

    def __split_vcf_string(self, contacts: str) -> List[str]:
        return self.__pattern_split_cvf.split(contacts.strip())
    
    def __write_vcf_file(self, contact: str) -> None:
        self.__create_output_dir_if_not_exists()
        output_file_path_vcf: str = self.__create_output_file_path(self.__output_dir_path, contact)
        
        with open(output_file_path_vcf, "w") as output:
            print("Create " + output_file_path_vcf + " as output file.")
            output.write(contact + "\n")
    
    def __create_output_dir_if_not_exists(self) -> None:
        if not os.path.exists(self.__output_dir_path):
            os.makedirs(self.__output_dir_path)
    
    def __create_output_file_path(self, output_dir: str, filename: str) -> str:
        file_path: str = os.path.join(output_dir, self.__read_name(filename)) + ".vcf"

        if os.path.exists(file_path):
            i: int = 1
            while os.path.exists(self.__append_id_to_filename(file_path, i)):
                i += 1
            
            file_path = self.__append_id_to_filename(file_path, i)
        
        return file_path
    
    def __read_name(self, contact: str) -> str:
        try:
            return self.__pattern_read_name.search(contact).group(1).strip()
        except AttributeError:
            raise IndexError("Contact has no nickname:\n\n" + contact)
    
    def __append_id_to_filename(self, file_path: str, id: int):
        # Reference: https://stackoverflow.com/questions/37487758/how-to-add-an-id-to-filename-before-extension
        path: Path = Path(file_path)
        return str(path.with_stem(f"{path.stem}_{id}"))

if __name__ == '__main__':
    input_file: str = os.path.abspath(sys.argv[1])
    output_dir: str = os.path.abspath(sys.argv[2])
    
    splitter: VcfSplitter = VcfSplitter(input_file, output_dir)
    splitter.split_vcf_file()
