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








