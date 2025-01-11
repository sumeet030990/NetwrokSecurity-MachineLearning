'''
The setup file is an essential part of the packaging and distribution Python project. 
It is used by setuptools(or disutils in older Python versions) to define the configuration of
your projects such as metadata, dependency and more
'''

from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT = '-e .'

'''
import list of pacakges from filepaths
'''
def get_requirement() -> List[str]:
  requirements=[]
  with open('requirements.txt') as file_obj:
    requirements= file_obj.readlines() 

    ## at the end of each lines \n is appended, which we need to remove
    requirements = [requirement.replace('\n', '') for requirement in requirements]

    ## when running packages names from file, we need to avoid "-e ."
    if HYPHEN_E_DOT in requirements:
      requirements.remove(HYPHEN_E_DOT)
    
  return requirements


setup(
  name="Network Security: Machine Learning",
  version='0.0.1',
  author='sumeet',
  author_email='sumeet.030990@gmail.com',
  packages=find_packages(),
  install_requires=get_requirement()
)


