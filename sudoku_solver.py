import numpy as np


class SudokuSolver:
    def __init__(self, _matrix):
        self.data = _matrix
        self.rows = 9
        self.columns = 9

    def solve(self):
        """
        Solves sudoku
        :return: solved sudoku
        """
        history = []
        all_history = []

        row = 0
        while row < self.rows:
            column = 0
            while column < self.columns:
                if self.data[row][column] == 0:
                    counter = 0

                    # Try numbers from 1 to 9
                    for number in range(1, 10):
                        counter += 1
                        if self.possible(row, column, number) and [row, column, 0, number] not in all_history:
                            history_item = [row, column, self.data[row][column], number]

                            history.append(history_item)
                            all_history.append(history_item)

                            self.data[row][column] = number
                            counter = 0
                            break

                    # If appropriate number was not found returns to previous change
                    if counter == 9:
                        hist_item = history.pop()

                        self.data[hist_item[0]][hist_item[1]] = hist_item[2]
                        self.revert_history(all_history, hist_item)

                        row = hist_item[0]
                        column = hist_item[1]
                        continue
                column += 1

            row += 1

        return np.matrix(self.data)

    def revert_history(self, history, from_point):
        """
        Removes all history items from given point
        :param history: History data
        :param from_point: Point from which to remove items
        :return: Reverted history array
        """
        items_to_remove = []
        for i in range(len(history)):
            if history[i][0] > from_point[0]:
                items_to_remove.append(i)
            elif history[i][0] == from_point[0] and history[i][1] > from_point[1]:
                items_to_remove.append(i)

        for index in sorted(items_to_remove, reverse=True):
            del history[index]

        return history

    def possible(self, row, column, number):
        """
        Checks if it is possible to write number to the given position
        :param row: Row index
        :param column: Column index
        :param number: Number
        :return: True if possible, false if not
        """
        # Horizontal check
        for cell in self.data[row]:
            if cell == number:
                return False

        # Vertical check
        for _row in self.data:
            if _row[column] == number:
                return False

        # Quadrant check
        quadrant_x = int(np.floor(column / 3))
        quadrant_y = int(np.floor(row / 3))

        quad_x_start = quadrant_x * 3
        quad_x_end = quad_x_start + 3

        quad_y_start = quadrant_y * 3
        quad_y_end = quad_y_start + 3

        for i in range(quad_y_start, quad_y_end):
            for j in range(quad_x_start, quad_x_end):
                if self.data[i][j] == number:
                    return False

        return True


matrix = [
    [5, 0, 0, 0, 0, 7, 1, 4, 0],
    [8, 0, 0, 0, 0, 6, 0, 0, 0],
    [0, 0, 7, 0, 0, 0, 9, 8, 0],
    [0, 0, 1, 0, 0, 5, 6, 0, 0],
    [0, 0, 0, 0, 3, 0, 0, 7, 0],
    [0, 0, 0, 0, 0, 0, 8, 0, 2],
    [0, 1, 0, 0, 8, 3, 0, 2, 0],
    [0, 4, 0, 7, 0, 0, 0, 0, 0],
    [0, 0, 2, 9, 0, 0, 0, 0, 0]
]

solver = SudokuSolver(matrix)
print(solver.solve())
