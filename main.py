from random import randint
from timeit import timeit


def insertion_sort_inplace(lst: list):
    for i in range(1, len(lst)):
        key = lst[i]
        j = i-1
        while j >= 0 and key < lst[j]:
            lst[j+1] = lst[j]
            j -= 1
        lst[j+1] = key
    return lst


def insertion_sort(lst: list):
    return insertion_sort_inplace(list(lst))


def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    def merge(left, right):
        merged = []
        left_index = 0
        right_index = 0

        while left_index < len(left) and right_index < len(right):
            if left[left_index] <= right[right_index]:
                merged.append(left[left_index])
                left_index += 1
            else:
                merged.append(right[right_index])
                right_index += 1

        while left_index < len(left):
            merged.append(left[left_index])
            left_index += 1

        while right_index < len(right):
            merged.append(right[right_index])
            right_index += 1

        return merged

    mid = len(arr) // 2
    return merge(merge_sort(arr[:mid]), merge_sort(arr[mid:]))


def measure(
    dataset: dict[str, list],
    algos: dict[str, callable(list)],
    number=10,
    skip_runs: list[tuple[str, str]] = None
):
    if skip_runs is None:
        skip_runs = []
    results = {}
    print('>> start measure')
    for (ds_label, ds) in dataset.items():
        ds_results = {}
        results[ds_label] = ds_results
        print(f'\t>> start dataset `{ds_label}`')
        for (algo_label, algo) in algos.items():
            if (ds_label, algo_label) in skip_runs:
                print(f'\t\t== skip algo `{algo_label}`')
                continue
            print(f'\t\t>> start algo `{algo_label}`')
            ds_results[algo_label] = timeit(
                stmt='algo(lst)',
                globals={'lst': ds, 'algo': algo},
                number=number
            )
            print(f'\t\t<< end algo `{algo_label}`: {ds_results[algo_label]}')
        print(f'\t<< end dataset `{ds_label}`')
    print('<< end measure')
    return results


def main():
    results = measure(
        dataset={
            'small_random': [randint(0, 100) for _ in range(10)],
            'medium_random': [randint(0, 100) for _ in range(1_000)],
            'small_sorted': list(range(10)),
            'medium_sorted': list(range(1_000)),
            'large_random': [randint(0, 100) for _ in range(1_000_000)],
            'large_sorted': list(range(1_000_000)),
        },
        algos={
            'insertion_sort': insertion_sort,
            'merge_sort': merge_sort,
            'sorted': sorted,
        },
        skip_runs=[
            ('large_random', 'insertion_sort'),
        ],
    )
    print(results)


if __name__ == '__main__':
    main()
