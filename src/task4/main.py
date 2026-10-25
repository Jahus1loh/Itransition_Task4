import time

from processing.app import render_dashboard


def main() -> None:
    render_dashboard()
    # for iteration in range(1, 6):
    #     start = time.time()
    #     aggreage_data(iteration)
    #     end = time.time()
    #     print(f"Exec time: {(end - start):.2f}")


if __name__ == "__main__":
    main()
