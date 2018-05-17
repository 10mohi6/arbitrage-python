import os
import pypandoc

f = open('README.txt','w+')
f.write(pypandoc.convert('README.md', 'rst'))
f.close()
os.system("python setup.py sdist")
os.system("twine upload dist/*")
os.remove('README.txt')