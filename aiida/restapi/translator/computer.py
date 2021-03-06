# -*- coding: utf-8 -*-
###########################################################################
# Copyright (c), The AiiDA team. All rights reserved.                     #
# This file is part of the AiiDA code.                                    #
#                                                                         #
# The code is hosted on GitHub at https://github.com/aiidateam/aiida_core #
# For further information on the license, see the LICENSE.txt file        #
# For further information please visit http://www.aiida.net               #
###########################################################################
from aiida.restapi.translator.base import BaseTranslator
from aiida.restapi.common.config import custom_schema

class ComputerTranslator(BaseTranslator):
    """
    Translator relative to resource 'computers' and aiida class Computer
    """

    # A label associated to the present class (coincides with the resource name)
    __label__ = "computers"
    # The AiiDA class one-to-one associated to the present class
    from aiida.orm.computer import Computer
    _aiida_class = Computer
    # The string name of the AiiDA class
    _aiida_type = "computer.Computer"
    # The string associated to the AiiDA class in the query builder lexicon
    _qb_type = 'computer'

    # If True (False) the corresponding AiiDA class has (no) uuid property
    _has_uuid = True

    _result_type = __label__

    # Extract the default projections from custom_schema if they are defined
    if 'columns' in custom_schema:
        _default_projections = custom_schema['columns'][__label__]
    else:
        _default_projections = ['**']

    def __init__(self, **kwargs):
        """
        Initialise the parameters.
        Create the basic query_help
        """
        super(ComputerTranslator, self).__init__(Class=self.__class__,
                                                 **kwargs)

