import pandas as pd

def load_dataset(file_path):
    """Loads the dataset from a CSV file."""
    try:
        df = pd.read_csv(file_path)
        print("Dataset loaded successfully!")
        print("Shape:", df.shape)
        print("Columns:", df.columns.tolist())
        return df
    except Exception as e:
        print("Error loading dataset:", e)
        return None

if __name__ == "__main__":
    file_path = "dataset.csv"  
    dataset = load_dataset(file_path)
    if dataset is not None:
        print(dataset.head())
