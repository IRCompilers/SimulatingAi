import csv

# Define column names
column_names = ['name', 'id', 'description']

# Define data rows
data_rows = [
    ['Med1', '1', 'Cures headache. Side effects: dizziness, nausea.'],
    ['Med2', '2', 'Cures fever. Side effects: fatigue, dry mouth.'],
    ['Med3', '3', 'Cures cold. Side effects: drowsiness, dry eyes.'],
    ['Med4', '4', 'Cures flu. Side effects: muscle pain, fever.'],
    ['Med5', '5', 'Cures cough. Side effects: dizziness, dry mouth.'],
    ['Med6', '6', 'Cures sore throat. Side effects: fatigue, nausea.'],
    ['Med7', '7', 'Cures sinusitis. Side effects: drowsiness, dry eyes.'],
    ['Med8', '8', 'Cures asthma. Side effects: muscle pain, fever.'],
    ['Med9', '9', 'Cures bronchitis. Side effects: dizziness, dry mouth.'],
    ['Med10', '10', 'Cures pneumonia. Side effects: fatigue, nausea.'],
    ['Med11', '11', 'Cures tuberculosis. Side effects: drowsiness, dry eyes.'],
    ['Med12', '12', 'Cures arthritis. Side effects: muscle pain, fever.'],
    ['Med13', '13', 'Cures osteoporosis. Side effects: dizziness, dry mouth.'],
    ['Med14', '14', 'Cures hypertension. Side effects: fatigue, nausea.'],
    ['Med15', '15', 'Cures diabetes. Side effects: drowsiness, dry eyes.'],
]

# Open file in write mode
with open('medications.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    # Write column names
    writer.writerow(column_names)

    # Write data rows
    writer.writerows(data_rows)