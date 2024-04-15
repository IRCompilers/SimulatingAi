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

## RAG

RAG, or Retrieval-Augmented Generation, is a type of model that combines the benefits of both retrieval-based and generative models for natural language processing tasks. The main idea behind RAG is to leverage the vast amount of information available in large text corpora by retrieving relevant documents and conditioning the generation on the retrieved documents. This allows the model to generate more informed and contextually relevant responses.  

In this particular implementation, the RAG model is used to recommend medications based on a list of symptoms. The model is initialized with a dataset of medications, each with a description and potential side effects. If the use_persistence configuration is set to True, the model will use a MongoDB database to persist the medication data. The model also uses a SentenceTransformer to create embeddings for each medication description, which are used to compute cosine similarity with the input symptoms. We use MongoDB because of its easiness to use and setup, and because of the fact that it allows JSON object upserting, ideal for the embedded vector

The query_medications_for_patients method is the main entry point for querying the model. It takes a list of symptoms and returns a list of recommended medications. If the use_llm configuration is set to True, the model will use a Language Model (LLM) to generate a response based on the top documents retrieved from the vector query. The LLM is queried with a context that includes the top documents and the input symptoms, and the response is parsed to extract the medication names. The LLM we use in this latest iteration of the RAG is the Gemini model by Google, via their genai API.

## Database
> insert

## Simulation
The simulation is run for a set number of days (30).

The first step is using the Hungarian method to assign the initial patients to the beds.

The patients are then treated with the treatment (medication) recommended by the RAG. Once the patient receives the medication 
for a specific symptom, that symptom has a high probability of being cured and there's a chance that the patient acquires one
or more of that drug's side effects.

Then there's the 'evolution' phase. In this phase the patients are cured, die, get better or get worse; all depending on the
amount of symptoms the patient still has, it's status (critical, grave, regular) and the bed assigned. 

The last step is to generate new patients which will be added to the patients that survived the day. The amount of new patients is decided by a Poisson distribution.
The symptoms are decided randomly from all possible symptoms.

This process is then repeated for the set number of days.

## Results
We ran the simulation 10 times (because of time constraints and computational power) for each set of parameters, and we have gotten the following mean values:
> Note: The standard deviation, min and max values are the mean values of its respective metric per simulation


___
#### Simulation 1 (Baseline)
#### ICU Beds: 5, Common Beds: 10, Initial Patients: 50, Lambda For Poisson: 50

| Metric                                  |  Mean   |  Std Deviation  |   Min   |   Max   |
|:----------------------------------------|:-------:|:---------------:|:-------:|:-------:|
| Patients Discharged                     |  15.56  |      3.26       |  11.36  |  20.26  |
| Patients Dead                           |  31.75  |      5.09       |  24.8   |  38.83  |
| Patients Cured                          |  0.85   |      0.78       |   0.1   |  2.06   |
| Patients that got better                |  9.90   |      2.31       |   7.0   |  13.46  |
| Patients that got worse                 |  20.63  |      3.83       |  15.53  |  25.9   |
| Regular patients that stayed the same   |  6.94   |      2.09       |  3.93   |  9.73   |
| Grave patients that stayed the same     |  12.33  |      3.01       |  8.36   |  16.56  |
| Critical patients that stayed the same  |  2.93   |      1.61       |  1.03   |  5.36   |

___
#### Simulation 2 (Upping the number of beds)
#### ICU Beds: 20, Common Beds: 20, Initial Patients: 50, Lambda For Poisson: 50

| Metric                                  |  Mean   |  Std Deviation  |   Min   |   Max   |
|:----------------------------------------|:-------:|:---------------:|:-------:|:-------:|
| Patients Discharged                     |  20.96  |      3.62       |  16.1   |  25.96  |
| Patients Dead                           |  26.34  |      5.44       |  19.06  |  34.13  |
| Patients Cured                          |  2.58   |      1.16       |  1.16   |  4.26   |
| Patients that got better                |  19.02  |      2.66       |  15.76  |  23.03  |
| Patients that got worse                 |  25.06  |      4.21       |  18.96  |  30.66  |
| Regular patients that stayed the same   |  8.45   |      2.24       |  5.43   |  11.73  |
| Grave patients that stayed the same     |  13.02  |      3.08       |   8.8   |  17.33  |
| Critical patients that stayed the same  |  3.34   |      1.61       |  1.23   |  5.66   |

___
#### Simulation 3 (Upping the number of initial patients and the number of new patients per day)
#### ICU Beds: 5, Common Beds: 10, Initial Patients: 100, Lambda For Poisson: 100

| Metric                                  | Mean  | Std Deviation |  Min  |  Max  |
|:----------------------------------------|:-----:|:-------------:|:-----:|:-----:|
| Patients Discharged                     | 29.51 |     4.60      | 23.76 | 36.4  |
| Patients Dead                           | 67.34 |     7.03      | 57.8  | 77.0  |
| Patients Cured                          | 0.79  |     0.69      | 0.06  | 1.83  |
| Patients that got better                | 15.10 |     3.33      | 10.96 | 20.03 |
| Patients that got worse                 | 40.89 |     5.38      | 33.86 | 48.7  |
| Regular patients that stayed the same   | 14.83 |     3.02      | 10.93 | 19.2  |
| Grave patients that stayed the same     | 23.05 |     3.66      | 18.13 | 28.06 |
| Critical patients that stayed the same  | 5.00  |     1.78      |  2.7  | 7.73  |


### Interpretation of the results











