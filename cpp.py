from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit
from PySide6.QtCore import Qt
import sys

class MatrixBuilder:
    @staticmethod
    def build(N: int) -> list[list[str]]:
        return [['0' for _ in range(N)] for _ in range(N)]

class PieceMoves:
    @staticmethod
    def get_moves(x, y):
        return {
            (x - 1, y), (x + 1, y),
            (x, y + 1), (x, y - 1),
            (x - 1, y + 2), (x + 1, y + 2),
            (x - 2, y + 1), (x + 2, y + 1),
            (x - 2, y - 1), (x - 2, y - 1),
            (x - 1, y - 2), (x + 1, y - 2)
        }

class Board:
    def __init__(self, N):
        self.matrix = MatrixBuilder.build(N)

    def pose_figure(self, x: int, y: int):
        dragon_moves = PieceMoves.get_moves(x, y)
        self.matrix[x][y] = '#'
        for m, n in dragon_moves:
            if 0 <= m < len(self.matrix) and 0 <= n < len(self.matrix):
                self.matrix[m][n] = '*'

    def create_board(self, posed_figures: list[tuple[int, int]]):
        for x, y in posed_figures:
            self.pose_figure(x, y)

    def print_board(self):
        for row in self.matrix:
            print(" ".join(row))

class SolutionFinder:
    def __init__(self, N, L, posed_figures):
        self.N = N
        self.L = L
        self.posed_figures = posed_figures
        self.solutions = set()

    def find_solutions(self):
        self._recursion_for_all_arrangements(self.N, self.L, self.solutions, set(self.posed_figures), 0, 0, 0)

    def _recursion_for_all_arrangements(self, N, L, solutions, solution, cnt, last_x, last_y):
        if cnt == L:
            unique_solution = tuple(solution)
            solutions.add(unique_solution)

            # Вывод первого решения
            if len(solutions) == 1:
                print("First solution:")
                board = Board(N)
                board.create_board(list(unique_solution))
                board.print_board()
            return

        for i in range(last_x, N):
            start_y = last_y if i == last_x else 0
            for j in range(start_y, N):
                if (i, j) not in solution and not PieceMoves.get_moves(i, j).intersection(solution):
                    solution.add((i, j))
                    self._recursion_for_all_arrangements(N, L, solutions, solution, cnt + 1, i, j)
                    solution.remove((i, j))

    def print_number_of_solutions(self):
        print(f"Number of solutions: {len(self.solutions)}")
        if self.solutions:
            solutions_str = [" ".join(map(str, solution)) + "\n" for solution in self.solutions]
            with open("output.txt", "w") as output_file:
                output_file.writelines(solutions_str)
        else:
            print('no solutions')

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Board Solutions")
        self.setGeometry(100, 100, 800, 600)
        self.layout = QVBoxLayout()

        self.instructions = QLabel("Размер доски, количество фигур, количество расставленных фигур")
        self.layout.addWidget(self.instructions)

        self.input_text = QTextEdit()
        self.layout.addWidget(self.input_text)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.layout.addWidget(self.result_text)

        self.setLayout(self.layout)
        self._run()

    def _run(self):
        # Пример входных данных
        input_data = "5 3 2\n1 1\n2 3\n"
        self.input_text.setPlainText(input_data)
        self._process_input()

    def _process_input(self):
        data = self.input_text.toPlainText().strip().split('\n')
        N, L, K = map(int, data[0].split())
        posed_figures = set(tuple(map(int, line.split())) for line in data[1:])

        solution_finder = SolutionFinder(N, L, posed_figures)
        solution_finder.find_solutions()
        solution_finder.print_number_of_solutions()

        result_str = f"Number of solutions: {len(solution_finder.solutions)}\n"
        if solution_finder.solutions:
            for solution in solution_finder.solutions:
                board = Board(N)
                board.create_board(list(solution))
                result_str += "\n".join(" ".join(row) for row in board.matrix) + "\n\n"
        else:
            result_str += 'No solutions\n'

        self.result_text.setPlainText(result_str)

if __name__ == "__main__": # Запуск приложения
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())