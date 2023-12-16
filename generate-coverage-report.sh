#!/bin/bash


coverage run --source='.' manage.py test

coverage html
coverage report -m


