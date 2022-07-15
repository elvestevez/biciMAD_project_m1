import os


def remove_file(f):
    if os.path.isfile(f):
        os.remove(f)

def save_file(df, f):
    df.to_csv(f, index=False)
