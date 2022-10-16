#!/usr/bin/env bash
npm --prefix app install &&
poetry install &&
echo -e "\n*** Install complete! Run ./start.sh --help to see how to use the program. ***"
exit 0