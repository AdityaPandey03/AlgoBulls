#!/bin/bash

set -e
set -o pipefail
black . --check
flake8 --extend-ignore E501 .



# chmod +x filename for excutable scripts