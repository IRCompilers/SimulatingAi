# Hospital Simulation Project

>Authors:
> - [Karen D. Cantero Lopez C411]()
> - [Héctor Miguel Rodríguez Sosa C411]()
> - [Sebastián Suárez Gomez C411]()

## How to run the project
1. Install the required libraries. The libraries are found in the `requirements.txt` file. To install them, run the following command:
```bash
pip install -r requirements.txt
```
2. Execute the `sim.py` file. This file is found in the `Simulation` folder. The project must be run as a project with its root folder as the main folder.

## Summary of the project
This project is a simulation of a hospital that has an initial number of patients and a set amount of ICU (Intensive Care Unit) beds and regular beds. The patients can be in a critical, grave or regular condition. They have a set of symptoms. Using an optimization algorithm, the patients are assigned to the beds in a way that prioritizes the most critical patients. The patients' symptoms are treated with a treatment recommended by a RAG. The treatment is a set of medications. The patients can be discharged from the hospital when they are fully recovered. Once a patient is discharged, that bed is then made available for another patient. The patients can also die if they are not treated in time.

## Optimization Method Used
In this simulation, we have used the Hungarian method for a linear assignment problem. The Hungarian method is an optimization algorithm that finds the optimal assignment of patients to beds. 
The algorithm is based on the cost matrix, which is a matrix that contains the cost of assigning a patient to a specific type of bed. We view it as: the lower the cost, the more beneficial it is to assign the patient to that bed.
The Hungarian method finds the optimal assignment by minimizing the total cost of the assignment. It has the restrictions that each patient can only be assigned to one bed and each bed can only be assigned to one patient.

## RAG & DataBase
> insert 


## Simulation
The simulation is run for a set number of days (30).

The first step is using the Hungarian method to assign the initial patients to the beds.

The patients are then treated with the treatment (medication) recommended by the RAG. Once the patient receives the medication 
for a specific symptom, that symptom has a high probability of being cured and there's a chance that the patient acquires one
or more of that drug's side effects.

Then there's the 'evolution' phase. In this phase the patients get cured, die, get better or get worse; all depending on the
amount of symptoms the patient still has, it's status (critical, grave, regular) and the bed assigned. 

The last step is to generate new patients which will be added to the patients that survived the day. The amount of new patients is decided by a Poisson distribution.
The symptoms are decided randomly from all possible symptoms.

This process is then repeated for the set number of days.

## Results
We ran the simulation 10 times (because of time constraints and computational power), and we have gotten the following mean values:

> Mean Deaths Per Day
> 
> ![Mean Deaths Per Day](   https://i.postimg.cc/zftmf7fM/deaths.png)

> Mean Cured/Discharged Per Day
> 
> ![Mean Cured Per Day](https://i.postimg.cc/vH3ChXrm/cured.png)

>Mean Better Per Day
> 
> ![Mean Better](https://i.postimg.cc/XYv66tjF/better.png)

> Mean Worse Per Day
> 
> ![Mean Worse](https://i.postimg.cc/yx7rXSW9/worse.png)








