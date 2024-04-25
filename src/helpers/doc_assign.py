from src.Entities.Doctor import Doctor
from src.Entities.Patient import Patient

def assign_doc_patient(doctors: [Doctor], patients:[Patient], map_sp_sym: dict):
    """
    Doctor is a class. It has a property called specialty. (string)
                       It has a property called max_patients. (int)
    Patient is a class. It has a property called specialties_needed. (dictionary)
          Patient.specialties_needed[specialty] = score (int)
    map_sp_sym is a dictionary. It maps specialties to symptoms
           map_sp_sym[specialty] = {symp1: score, symp2: score, ...}

    This function assigns patients to doctors based on the specialties needed by the patient.
    """
    return []