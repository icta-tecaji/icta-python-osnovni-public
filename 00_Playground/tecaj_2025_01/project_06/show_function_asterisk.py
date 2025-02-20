def run_parsing_process(url: str, *, number_of_threads: int, skip_duplicates: bool, run_daemon_mode: bool) -> None:
    """Run parsing process."""
    print("Parsing process started")
    print(f"URL: {url} | Threads: {number_of_threads} | Skip duplicates: {skip_duplicates} | Daemon mode: {run_daemon_mode}")


def sum_all_numbers(*args, **kwargs) -> None:
    """Run parsing process."""
    print(f"*args: {args}, type: {type(args)}")
    print(f"**kwargs: {kwargs}, type: {type(kwargs)}")
    print(f"Sum of all numbers: {sum(args)}")


if __name__ == "__main__":
    run_parsing_process("https://www.google.com", number_of_threads=5, skip_duplicates=True, run_daemon_mode=False)

    sum_all_numbers(1, 2, 3, 4, 7, 8, 8, 8, mode="sum", skip_duplicates=True)
