# py-gnse


##  Current structure of the package

```
├── README.md
├── gnse
│   ├── config.py
│   ├── solver.py
│   ├── tools.py
│   └── version.py
└── results
    ├── numExp00_NSE
    │   ├── main_NSE_test.py
    │   └── main_NSE_test_SySSM.py
    └── numExp01_event_horizon
```

List of folders:
* gnse: folder containing all our "library" modules. 
* results: project-specific scripts.


## Internship meetings

The subsections below give an outling of the topics discussed in the
meetings

### Meeting 01 -- 2021-04-16

* Discussed OOP implentation of the pde-solver in stand-alone python script


### Meeting 02 -- 2021-04-22

* Review "A quick guide to Organizing Computational Biology Projects"
* If you need pars of your code in more than one place: refactor! 
  - organize your code in several independent modules. This then yields a
    "package"
  - You can refactor on many levels. You can refactor scripts into modules (as
    we did today), you can refactor classes, functions, etc.
* Cohesion: 
  - Classes have attributes, and classes have methods
  - "Cohesion" makes a statement of how the method and class are related
  - A method and its class are coupled with high cohesion, 
  - The more attribues a given method manipulates (i.e. uses or alters), the
    higher the cohesion between method and class 
  - aim: when you refactor a class, try do increase cohesion
* Documentation:
  - Clearly document the interface of your classes and functions


### Meeting 03 -- 2021-04-27 

* Versioning:
  - PEP 440 - Version identification
* Documenting software: 
  - Google-style docstrings, https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
* Object oriented implementation of z-propagation algorithm
  - Symmetric split-step Fourier method (you did that already!)
  - Fourth-order "Runge-Kutta in the interaction picture" (RK4IP) method
  - References: Hult_JLT_2007 (fixed stepsize), Balac_CPC_2013 (adaptive stepsize), Numerical Recipes


### Meeting 04 -- 2021-05-14

* Interaction picture method
  - Discussed the article of Hult and Balac


### Meeting 05 -- 2021-05-21

* Research data management recap 
  - Huzefa visited the RDM course of the Hannover School for Nanotechnology

* Discussion of the RK4IP algorithm




