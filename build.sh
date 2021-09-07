source venv/bin/activate;

python3.9 setup.py bdist_wheel;
python3.9 setup.py sdist --format=gztar;
