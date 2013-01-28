#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Tivion
## Copyright (C) 2009 Ángel Guzmán Maeso
## http://shakaran.net
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.

import time
import os
import platform

# Constants
VERSION_NUMBER     = '0.0.4'
VERSION_NAME       = 'Tivion'
VERSION            = VERSION_NAME + ' ' + VERSION_NUMBER

# Tree model
(
    COLUMN_ID,
    COLUMN_COUNTRY,
    COLUMN_TYPE,
    COLUMN_NAME,
    COLUMN_URL,
    COLUMN_FORMAT_TYPE
) = range(6)

# Channel Type
(
    TV,
    RADIO,
    SOPCAST,
) = range(3)

# Format Type
(
    PLS,
    ASX,
    RM,
    UNKNOWN,
    M3U,
    MP3,
) = range(6)

lastProcess = None
