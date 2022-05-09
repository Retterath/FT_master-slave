# Specifications 
#####  (Vorlage nach Balzert, Lehrbuch der Softwaretechnik (3 Auflage, Kapitel 20.3))

| Version | Autor | Quelle | Status | Datum | Kommentar |
| ------- | ----- | ------ | ------ | ----- | --------- |
|  0.1    |Retterath| none | editing | 09.05.2022 | First description |


## 1. Visions and Goals

Description of the visions and goals to be achieved through the use of the system

The Software is meant to connect one user to a server which is connected to several microcontrollers (Master-Slave). The connection is established via SSH and as such uses keys/passwords. 
Each microcontroller is connected to a interpreter. Since not all microcontrollers use the same architecture and programming language the input to the server would be unequal for different microcontrollers.
The role of an interpreter is to format that unequal data from the microcontroller and to deliver it to the server. In that way we can agree on one convention of formating and delivering data to the server. 


## 2. General conditions

Description of the areas of application and target groups

The area of use of that project is unspecific. This can be used in small projects (e.g. connect microcontrollers at home) or large projects (e.g. measure multiple temperatures inside chambers of industrial areas). 

## 3. Context and Overview
 
Definition of the relevant system environment (context) and overview of the system


## 4. Functional Requirements 

## 5. Quality Requirements

| System quality  | excellent | good | normal | not relevant |
| -------------------  | -------- | --- | ------ | -------------- | 
| Functionality        |     x    |     |        |                |
| Reliability          |          |     |        |                |
| Usability            |     x    |     |        |                |
| Efficiency           |          |     |   x    |                |
| Maintainability      |          |     |   x    |                |
| Portability          |     x    |     |        |                |