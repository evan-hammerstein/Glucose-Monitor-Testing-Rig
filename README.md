# Design and Development of a Test Rig for Continuous Glucose Monitors (CGM)

**Associated Presentations and Full Project Report (Release):
https://github.com/evan-hammerstein/Glucose-Monitor-Testing-Rig/releases/tag/Release
https://prezi.com/p/qimv-nsshvhj/?present=1**

Imperial College London
MEng Bioengineering Final Year Project
Supervisors: Dr. Anil Bharath, Dr. Anna Bird

This repository contains all code, CAD models, control algorithms, circuit schematics, and supporting files for the design and validation of a cost-effective automated CGM test rig.

The full academic report is included in this repository and documents the complete design process and validation results .

---

# Project Overview

Continuous Glucose Monitors are increasingly used in diabetes management. However, early-stage CGM validation often relies on manual in-vitro testing with limited dynamic capability.

This project designed and implemented:

• A low-cost automated CGM test rig
• Programmable glucose concentration control
• Two fluid delivery architectures
• Custom passive mixing solutions
• A CGM-compatible fluid interface
• An Arduino-based control system
• A desktop user interface for simulation and automation

Two complete systems were developed:

1. Binary system
   Alternates between two fixed glucose concentrations.

2. Dynamic system
   Recreates physiologically realistic glucose trajectories using real-time flow rate control based on the Padova model.

---

# Key Features

• Fully automated glucose profile generation
• Real-time pump control via Arduino
• Open-source peristaltic pump integration
• Custom 3D-printed passive mixers
• CGM interface designed for leak-free operation
• Electron-based desktop UI
• Integration with FreeStyle Libre 2 CGM
• Modular design using Luer-lock fluidics

---

# Repository Structure

/3D-Models
• Passive mixer designs
• CGM interface designs
• Peristaltic pump customizations
• STL and CAD files

/arduino
• Binary valve control code
• Dynamic dual-pump control algorithm
• RPM mapping implementation
• Delay synchronization logic

/electron-ui
• User interface for profile selection
• Parameter configuration
• Glucose trajectory visualization

/python
• Padova model integration
• Example glucose profiles
• CSV generation for simulation

/circuits
• Valve control schematics
• Dual pump A4988 driver circuit
• Wiring diagrams

/report
• Final project report (PDF)

---

# System Architecture

Binary System

Syringe Pump → Solenoid Valves → CGM Interface → CGM Reader

Dynamic System

Peristaltic Pump 1
Peristaltic Pump 2
→ Y-junction → Passive Mixer → CGM Interface → CGM Reader

The dynamic system adjusts the ratio of high and low glucose reservoirs in real time to match a target glucose concentration trajectory.

---

# Control Algorithm Summary

Inputs:

• Composite flow rate
• Tubing geometry
• Reservoir concentrations
• Target glucose profile

Outputs:

• Individual pump flow rates
• Stepper motor RPM
• Pump activation delay

The algorithm ensures:

• Constant total flow rate
• Complementary pump behavior
• Synchronized arrival at mixing junction

Edge cases such as zero-flow conditions are handled explicitly.

---

# Hardware Components

• Arduino Uno
• A4988 stepper motor drivers
• NEMA 17 stepper motors
• Open-source peristaltic pump
• Solenoid valves
• Silicone tubing
• Luer connectors
• 3D-printed CGM interface
• FreeStyle Libre 2 CGM

Full bill of materials is included in the repository.

---

# Mixer Designs

Four passive mixer iterations were evaluated:

• Stepwise geometry
• Sinusoidal channel
• Helical in-line mixer
• Self-constructed multi-loop mixer

The self-constructed multi-loop mixer provided:

• Effective mixing
• Ease of fabrication
• Leak-free integration
• Compatibility with standard lab printers

---

# Validation Highlights

• Pump RPM vs flow rate linear correlation: R = 0.9998
• Mixer absorbance matched magnetically stirred control
• Open-channel CGM interface demonstrated leak-free operation
• Binary system successfully reproduced square-wave profiles
• Dynamic system tracked programmed glucose trajectories

Observed deviations were attributed to:

• CGM internal processing
• Diffusion delays
• Environmental effects
• Delay amplification under certain parameter combinations

---

# How to Use

1. Assemble hardware using provided CAD and material lists
2. Upload Arduino firmware
3. Connect pumps and drivers per circuit diagrams
4. Launch Electron UI
5. Select or generate glucose profile
6. Run system
7. Monitor CGM output via xDrip+

---

# Applications

• Early-stage CGM validation
• Sensor accuracy testing
• Interference testing
• Algorithm verification
• Closed-loop system research
• CGM cybersecurity testing
• Hybrid closed loop simulation

---

# Future Improvements

• Improved delay minimization algorithm
• Automatic optimization of reservoir concentrations
• Environmental control integration
• Expanded flow rate characterization
• Diffusion vs advection quantification
• Closed-loop insulin simulation support

---

# Acknowledgements

Imperial College London
Department of Bioengineering

Supervisors:
Dr. Anil Bharath
Dr. Anna Bird

IN-CYPHER Programme
