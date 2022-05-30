"""
Reference: I:\_T.H.U\MLSys\Projects\qiskit-terra\test\python\transpiler\test_sabre_layout.py
Compares our definition of Tokyo and Qiskit's.
"""

from qiskit.test.mock import FakeTokyo


def main():
    """
    our tokyo:
    00 ↔ 01 ↔ 02 ↔ 03 ↔ 04
     ↕    ↕ x ↕    ↕ ⤫  ↕
    05 ↔ 06 ↔ 07 ↔ 08 ↔ 09
     ↕ ⤫ ↕    ↕ ⤫ ↕     ↕
    10 ↔ 11 ↔ 12 ↔ 13 ↔ 14
     ↕    ↕ ⤫ ↕     ↕ ⤫  ↕
    15 ↔ 16 ↔ 17 ↔ 18 ↔ 19
    """
    our_tokyo = [
        # rows
        [0, 1], [1, 2], [2, 3], [3, 4],
        [5, 6], [6, 7], [7, 8], [8, 9],
        [10, 11], [11, 12], [12, 13], [13, 14],
        [15, 16], [16, 17], [17, 18], [18, 19],
        # cols
        [0, 5], [5, 10], [10, 15],
        [1, 6], [6, 11], [11, 16],
        [2, 7], [7, 12], [12, 17],
        [3, 8], [8, 13], [13, 18],
        [4, 9], [9, 14], [14, 19],
        # crossings
        [1, 7], [2, 6],
        [3, 9], [4, 8],
        [5, 11], [6, 10],
        [8, 12], [7, 13],
        [11, 17], [12, 16],
        [13, 19], [14, 18]
    ]
    """
    qiskit tokyo:
    00 ↔ 01 ↔ 02   03   04
     ↕   ↕  x      ↕  /  ↕
    05 ↔ 06 ↔ 07 ↔ 08 ↔ 09
     ↕ ⤫ ↕    ↕  / ↕     
    10 ↔ 11 ↔ 12 ↔ 13 ↔ 14
     ↕    ↕ ⤫       ↕ ⤫ ↕
    15 ↔ 16 ↔ 17 ↔ 18   19
    """
    qiskit_tokyo = FakeTokyo().configuration().coupling_map

    # check which pairs are different
    print("Edges in our device but not in theirs:")
    for pair in our_tokyo:
        if pair not in qiskit_tokyo and [pair[1], pair[0]] not in qiskit_tokyo:
            print(pair)
    print("Edges in their device but not in ours:")
    for pair in qiskit_tokyo:
        if pair not in our_tokyo and [pair[1], pair[0]] not in our_tokyo:
            print(pair)


if __name__ == '__main__':
    main()
