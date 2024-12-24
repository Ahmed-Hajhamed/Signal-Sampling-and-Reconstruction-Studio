import csv
def save_signal(time_data, amplitude_data):
    file_path = "file_of_signal\synthetic_ecg_data.csv"
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["List1", "List2"])
        for item1, item2 in zip(time_data, amplitude_data):
            writer.writerow([item1, item2])