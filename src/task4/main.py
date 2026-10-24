import time

from processing.process_data import aggreage_data


def main() -> None:
    start = time.time()
    aggreage_data()
    end = time.time()
    print(f"Exec time: {(end - start):.2f}")


if __name__ == "__main__":
    main()
