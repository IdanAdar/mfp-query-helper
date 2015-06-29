python setup.py install --record files.txt
cat files.txt | xargs rm -rf
rm files.txt