# -*- coding: utf-8 -*-
"""
Implement subclass for a single file in the permanent repository
files = [one_single_file]
jsons = {}

methods:
* get_content
* get_path
* get_aiidaurl (?)
* get_md5
* ...

To discuss: do we also need a simple directory class for full directories
in the perm repo?
"""
import os

from aiida.orm import Data


__author__ = "Giovanni Pizzi, Andrea Cepellotti, Riccardo Sabatini, Nicola Marzari, and Boris Kozinsky"
__copyright__ = u"Copyright (c), 2012-2014, École Polytechnique Fédérale de Lausanne (EPFL), Laboratory of Theory and Simulation of Materials (THEOS), MXC - Station 12, 1015 Lausanne, Switzerland. All rights reserved."
__license__ = "MIT license, see LICENSE.txt file"
__version__ = "0.2.0"

class SinglefileData(Data):
    """
    Pass as input a file parameter with the (absolute) path of a file 
    on the hard drive.
    It will get copied inside the node.

    Internally must have a single file, and stores as internal attribute
    the filename in the 'filename' attribute.
    """
    @property
    def filename(self):
        return self.get_attr('filename')

    def get_file_abs_path(self):
        return os.path.join(self.path_subfolder.abspath,self.filename)

    def set_file(self, filename):
            self.add_path(filename)

    def add_path(self,src_abs,dst_filename=None):
        """
        Add a single file
        """
        old_file_list = self.get_path_list()

        if not os.path.isabs(src_abs):
            raise ValueError("Pass an absolute path for src_abs")

        if not os.path.isfile(src_abs):
            raise ValueError("src_abs must exist and must be a single file")

        if dst_filename is None:
            final_filename = os.path.split(src_abs)[1]
        else:
            final_filename = dst_filename

        try:
            # I remove the 'filename' from the list of old files:
            # if I am overwriting the file, I don't want to delete if afterwards
            old_file_list.remove(dst_filename)
        except ValueError:
            # filename is not there: no problem, it simply means I don't have
            # to delete it
            pass
            
        super(SinglefileData,self).add_path(src_abs,final_filename)

        for delete_me in old_file_list:
            self.remove_path(delete_me)

        self.set_attr('filename', final_filename)

    def remove_path(self,filename):
        if filename == self.get_attr('filename',None):
            try:
                self.del_attr('filename')
            except AttributeError:
                ## There was not file set
                pass

    def validate(self):
        from aiida.common.exceptions import ValidationError

        super(SinglefileData,self).validate()
        
        try:
            filename = self.filename
        except AttributeError:
            raise ValidationError("attribute 'filename' not set.")

        if [filename] != self.get_path_list():
            raise ValidationError("The list of files in the folder does not "
                "match the 'filename' attribute. "
                "_filename='{}', content: {}".format(
                    filename, self.get_path_list()))
        
    
