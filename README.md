# py-gnse
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)


1. The python script ```solver.py``` provided in the repository contain algorithms to solve normal and generalized nonliear Schrödinger equation in object oriented programming. The algorithms include split step Fourier method, symmetric split step Fourier method and forth-order Runge-kutta in interation picture mmethod. The aim of employing different numerical schemes is to test the performance of each method by checking the global error. In order to compare the performance of different numerical schemes, the aroot mean square intensity error after one soliton period is used. The graph below generated by ```Quality_control.py``` shows that the fourth-order Runge-Kutta method clearly outperforms other numerical schemes.

![alt text](https://github.com/omelchert/Internship_HB2021/blob/main/results/numExp07_quality_controll/Quality_control.png)

2. The script ```main_event_horizon_v1.py``` provided in this repository depicts the optical event horizon. It aims to show the nonlinear interation of light in an optical fiber which mimics the physics at an event horizon of astrophysical black hole. The figure showm below is generated by ```main_event_horizon_clean.py``` where a soliton in anomalous dispersion regime interacts with a dispersive wave in normal dispersion regime at a different velocity. The dispersive wave is reflected off the soliton in time domain and in frequency domain the frequency of the dispersive wave appears to have been blue shifted. Here the dispersive waves from soliton itself is cleared out in order to make the figure more clean.

![alt text](https://github.com/omelchert/Internship_HB2021/blob/main/results/numExp05_energy_conservation/res_cleaned_up_t0_0.500000_w0_0.000000_t1_4.000000_w1_19.500000_tsep_30.000000_sfac_0.200000.png)


3. The preliminary condition to depict an event horizon in an optical fiber is that the soliton and the dispersive wave should lie in anomalous and normal dispersion regime respectively. The python script ```main_analyze_prop_const.py```  shows the group velocity matching frequency in anomalous and normal dispersion regime. The figure below shows the group velociy matching frequency when ```\beta_2 = -1 fs^2 / m``` and ```\beta_3 = 0.1 fs^3 / m```.

![alt text](https://github.com/omelchert/Internship_HB2021/blob/main/results/numExp01_analyze_beta/plot_beta2_-1.000000_beta3_0.100000.png)

Brief description of what the provided code does



## Prerequisites

The scripts in the ```internship_HB2021``` repository requires a working ```Python3``` environement with the functionality of ```numpy, scipy``` and ```matplotlib```. 

## Availability of the software

The repository can be clone by running the following in the command line: 

```$ git clone https://github.com/omelchert/Internship_HB2021.git```


##  Structure of the software repository

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
    ├── numExp04_spectrogram
    │   ├── figs
    │   ├── generate_animation.sh
    │   ├── main_spectrogram.py
    │   └── spec.gif
    ├── numExp05_energy_conservation
    │   ├── main_event_horizon_clean.py
    │   ├── res_S_DW_collision.npz
    │   ├── res_cleaned_up_t0_0.500000_w0_0.000000_t1_4.000000_w1_19.500000_tsep_30.000000_sfac_0.200000.png
    │   └── test.dat
    ├── numExp06_supercontinuum_generation
    │   ├── fig_SC_generation.png
    │   ├── main_sc_generation.py
    │   ├── pp_spectrogram
    │   └── res_SC_generation.npz
    └── numExp07_quality_controll
        ├── Quality_control.png
        └── Quality_control.py

```

List of folders:
* gnse: folder containing all our "library" modules. 
* results: project-specific scripts.
  - numExp00: test of solvers using the standard NSE for benchmarking
  - numExp01: demonstration of how to analyze a propagation constant
  - numExp02: demonstration of an optical event horizon 
  - numExp03: demonstration of how to get a "cleaned up" a soliton + DW initial condition
  - numExp04: demonstration of how to compute spectrograms
  - numExp05: demonstration of energy conservation (NSE) for each pulse 
  - numExp06: demonstration that supercontinuum generation gives conditions for an optical event horizon
  - numExp07: demonstration of the scaling behavior of the global error for decreasing stepsize for the implemented algorithms

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
  - See folder numExp01

* Optical event horizon propagation scenario
  - We set up a preliminary propagation scenario using a soliton and a 
    dispersive wave (slightly faster than the soltion), demonstrating
    an optical event horizon.
  - Needs to be optimized so that computational grid is adequate and 
    total reflection is supported.
  - See folder numExp02


### Meeting 07 -- 2021-06-15

* Discussed how to obtain a cleaned up initial condition 
  - We set up an NSE soliton and propagate it subject to nonzero beta3. We then
    propagate until the soliton sheds off its radiative dress and filter out
    the localized state. We use this localized state to represent a "cleaned
    up" soliton in subsequently designed initial conditions.
  - See folder numExp03


### Meeting 08 -- 2021-06-18

* Discussed how to obtain spectrograms
  - We discussed spectograms as Fourier transforms of localized signals
  - We used the "convert" tool of the imagemagick library to assemble
    many png-files into an animated gif
  - See folder numExp04


### Meeting 09 -- 2021-06-28

* Talk rehearsal where we discussed "optical event horizon" simulations
  - We verified that the energies of both pulses are conserved when considering 
    the NSE for modeling
  - See folder numExp5


### Meeting 10 -- 2021-07-01

* Discussed supercontinuum example
  - We had a look at a supercontinuum generation scenario to demonstrate
    that the conditions for an optical event horizon are realized during 
    supercontinuum generation
  - See folder numExp06

* Quality controll
  - Final task for Huzefa was to prepare a plot, showing how the global error
    of the three different z-propagation algorithms scales for decreasing
    stepsize
  - See folder numExp07


### Meeting 11 -- 2021-07-05

* Wrap up of the internship work
  - We discussed how to amend this README file in order to better document the 
    project folder


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.


## Acknowledgements

Throughout my internship I have received a great deal of support and assistance. I would first like to thank my supervisor, Dr. Oliver Melchert, whose expertise was invaluable in formulating the questions and methodology. His insightful feedback pushed me to sharpen my thinking and brought my work to a higher level. I would like to acknowledge and thanks Prof. Dr. Ayhan Demircan for his constant support and for all of the opportunities I was given to further enhance my skills.
