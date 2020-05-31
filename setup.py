from distutils.core import setup
setup(
  name = 'robotframework-impansible',
  packages = ['Impansible'],
  version = '0.6',
  license='MIT',
  description = 'Robotframework library to access all ansible internal modules.',
  author = 'Adam Przybyla',
  author_email = 'adam.przybyla@gmail.com',
  url = 'https://github.com/AdamPrzybyla/impansible',
  download_url = 'https://github.com/AdamPrzybyla/Impansible/archive/v_06.tar.gz',
  keywords = ['robotframework', 'ansible', 'automatisation','nsm'],
  install_requires=[
          'ansible',
          'robotframework',
          'robotframework-nsm',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 2',
  ],
)
