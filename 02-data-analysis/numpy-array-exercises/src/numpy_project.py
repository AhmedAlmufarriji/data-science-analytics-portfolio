# -*- coding: utf-8 -*-
"""NumPy course project - arrays, indexing, reshaping, merging, and splitting."""

import numpy as np


def main():
    # 1) Create 15 floating-point values using linspace.
    numbers = np.linspace(1, 15, 15, dtype=float)
    print("1) Linspace (15 floats):")
    print(numbers)

    # 2) Create a 3D array of shape (2, 2, 3) from four rows.
    array_3d = np.array([
        [[1.1, 2.1, 3.1], [4.1, 5.1, 6.1]],
        [[7.1, 8.1, 9.1], [10.1, 11.1, 12.1]]
    ])
    print("\n2) Original 3D array:")
    print(array_3d)

    # 3) Display all required array properties.
    print("\n3) Properties:")
    print("type:", type(array_3d))
    print("datatype:", array_3d.dtype)
    print("shape:", array_3d.shape)
    print("size:", array_3d.size)
    print("dimension:", array_3d.ndim)

    # 4) Convert the array into a four-dimensional array.
    array_4d = array_3d.reshape(1, 2, 2, 3)
    print("\n4) Four-dimensional array:")
    print("dimension:", array_4d.ndim)
    print("shape:", array_4d.shape)

    # 5) Convert its values to integers.
    array_int = array_4d.astype(int)
    print("\n5) Integer array:")
    print(array_int)
    print("datatype:", array_int.dtype)

    # 6) Print every value using nditer.
    print("\n6) All elements using nditer:")
    for value in np.nditer(array_int):
        print(int(value), end=" ")
    print()

    # 7) Print the eighth element (counting from one).
    print("\n7) Eighth element:", array_int.flat[7])

    # 8) Print the fifth and sixth elements (counting from one).
    print("\n8) Fifth and sixth elements:", array_int.flat[4:6])

    # 9) Find the value 8 using where.
    locations = np.where(array_int == 8)
    coordinates = list(zip(*(axis.tolist() for axis in locations)))
    print("\n9) Coordinates of value 8 (where):", coordinates)

    # 10) Reshape into a (2, 3, 2) array.
    reshaped = array_int.reshape(2, 3, 2)
    print("\n10) Reshaped array (2, 3, 2):")
    print(reshaped)

    # 11) Concatenate two string arrays using the default axis (0).
    arr1 = np.array([['A', 'B'], ['E', 'F']])
    arr2 = np.array([['C', 'D'], ['G', 'H']])
    combined_default = np.concatenate((arr1, arr2))
    print("\n11) Concatenation (default axis=0):")
    print(combined_default)

    # 12) Concatenate the same arrays along columns (axis=1).
    combined_columns = np.concatenate((arr1, arr2), axis=1)
    print("\n12) Concatenation (axis=1):")
    print(combined_columns)

    # 13) Split the previous result into two 2x2 arrays (4 values each).
    first, second = np.split(combined_columns, 2, axis=1)
    print("\n13) Split into two arrays (axis=1):")
    print("First array (4 elements):\n", first, sep="")
    print("Second array (4 elements):\n", second, sep="")


if __name__ == "__main__":
    main()