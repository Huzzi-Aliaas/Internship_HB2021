# py-gnse


##  Current structure of the package

```
.
├── README.md
├── gnse
│   ├── config.py
│   ├── propagation_constant.py
│   ├── solver.py
│   ├── spectrogram.py
│   ├── tools.py
│   └── version.py
└── results
    ├── numExp00_NSE
    │   ├── main_NSE_test.py
    │   ├── main_NSE_test_InteractionPictureMethod.py
    │   └── main_NSE_test_SySSM.py
    ├── numExp01_analyze_beta
    │   ├── main_analyze_prop_const.py
    │   └── plot_beta2_-1.000000_beta3_0.100000.png
    ├── numExp02_event_horizon
    │   ├── main_event_horizon_v1.py
    │   ├── main_event_horizon_v1b.py
    │   └── res_t0_0.500000_w0_0.000000_t1_4.000000_w1_18.000000_tsep_30.000000_sfac_0.050000.png
    ├── numExp03_cleaned_up_soliton
    │   ├── main_event_horizon_clean.py
    │   ├── res_S_DW_collision.npz
    │   └── res_cleaned_up_t0_0.500000_w0_0.000000_t1_4.000000_w1_18.000000_tsep_30.000000_sfac_0.050000.png
    └── numExp04_spectrogram
        ├── figs
        ├── generate_animation.sh
        ├── main_spectrogram.py
        └── spec.gif
```

List of folders:
* gnse: folder containing all our "library" modules. 
* results: project-specific scripts.
  - numExp00: test of solvers using the standard NSE for benchmarking
  - numExp01: demonstration of how to analyze a propagation constant
  - numExp02: demonstration of an optical event horizon 
  - numExp03: demonstration of how to get a "cleaned up" a soliton + DW initial condition
  - numExp04: demonstration of how to compute spectrograms


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


### Meeting 06 -- 2021-06-07

* Analysis of propagation constant
  - Discussed PropConst convenience class
  - Considered b2=-1 and b3=0.1 and determined parameters of a soliton and 
    a group-velocity matched dispersive wave as basis for a numerical 
    simulation study of an optical event horizon
  - see folder numExp01

* Optical event horizon propagation scenario
  - We set up a preliminary propagation scenario using a soliton and a 
    dispersive wave (slightly faster than the soltion), demonstrating
    an optical event horizon.
  - Needs to be optimized so that computational grid is adequate and 
    total reflection is supported.
  - see folder numExp02


### Meeting 07 -- 2021-06-15

* Discussed how to obtain a cleaned up initial condition 
  - We set up an NSE soliton and propagate it subject to nonzero beta3. We then
    propagate until the soliton sheds off its radiative dress and filter out
    the localized state. We use this localized state to represent a "cleaned
    up" soliton in subsequently designed initial conditions.
  - see folder numExp03


### Meeting 08 -- 2021-06-18

* Discussed how to obtain spectrograms
  - We discussed spectograms as Fourier transforms of localized signals
  - We used the "convert" tool of the imagemagick library to assemble
    many png-files into an animated gif
  - see folder numExp04


