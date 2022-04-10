#!/usr/bin/env bash

exec docker run --rm -it -v "${PWD}:/local" peter /local/$1 

