import sympy
import sympy as sp
from typing import Optional


class BisectionProcessor:
    def __init__(self, func: callable, epsilon: float, a: Optional[float] = None, b: Optional[float] = None, interval_find_step: float = 1, interval_max_iterations: int = 100000, interval_start_iterations: Optional[int] = None):
        """
        :param func: The function whose root needs to be found
        :param a: Start number changing signs on an interval (if known)
        :param b: End number changing signs on an interval (if known)
        :param epsilon: Calculation accuracy float value, e.g. 10**-4 (The smaller the more accurate, but at the same time there are more iterations to solve)
        :param interval_find_step: Step value for searching intervals a, b. (it is advisable to use integers for more “human” calculations)
        :param interval_max_iterations: Maximum number of the end of iterations for searching intervals a, b
        :param interval_start_iterations: Minimum number of the start of iterations for searching intervals a, b (by default = -1interval_max_iterations)
        """
        self.x = sp.symbols('x')
        self.equations: list[str] = []

        self.function: callable = func
        self.a: Optional[float] = a
        self.b: Optional[float] = b
        self.epsilon: float = epsilon

        self.step: float = interval_find_step
        self.max_iters: int = interval_max_iterations
        self.start_iters: int = interval_start_iterations if interval_start_iterations is not None else -interval_max_iterations

        self.solutions: list[float] = []
        self.intervals: Optional[list] = None

    @staticmethod
    def _get_signs(integers: list[int | float]) -> str:
        return f'({", ".join(["-" if sign < 0 else "+" if sign != 0 else "" for sign in integers])})'

    def find_intervals(self):
        intervals = []

        while self.start_iters < self.max_iters:
            if self.function(self.start_iters) * self.function(self.start_iters + self.step) < 0:
                a = self.start_iters
                b = self.start_iters + self.step
                intervals.append((a, b))
            self.start_iters += self.step
        return intervals

    def find_solutions(self, extra: bool = False) -> list[int | float]:
        """
        :param extra: Parameter indicating whether to solve the equation using the instant method without intermediate steps
        :return: List of possible solutions
        """
        self.equations = []
        self.intervals = [(self.a, self.b)]

        if extra:
            self.solutions = sp.solve(self.function(self.x), self.x)

            return self.solutions

        if self.a is None or self.b is None:
            self.intervals = self.find_intervals()

        for a, b in self.intervals:
            equation = []
            self.a = a
            self.b = b

            if self.function(self.a) * self.function(self.b) >= 0:
                raise ValueError("Функция должна иметь разные знаки на концах интервала [a, b].")

            while (self.b - self.a) >= self.epsilon:
                statuses = [["\033[9m", "\033[0m"], ["\033[9m", "\033[0m"]]

                c = (self.a + self.b) / 2.0
                eq = f"({self.a} + {self.b}) / 2 = {c}"

                if self.function(c) == 0.0:
                    self.solutions.append(c)

                old_a, old_b = float(self.a), float(self.b)

                if self.function(c) * self.function(self.a) < 0:
                    statuses[1] = ["", ""]
                    self.b = c
                else:
                    statuses[0] = ["", ""]
                    self.a = c

                eq += f"\n\t\t{self._get_signs([f(old_a), f(c)])} {statuses[1][0]}{[old_a, c]}{statuses[1][1]} " \
                      f"| {self._get_signs([f(c), f(old_b)])} {statuses[0][0]}{[c, old_b]}{statuses[0][1]}\n"
                equation.append(eq)

            self.equations.append(equation)

            self.solutions.append((self.a + self.b) / 2)

        return self.solutions

    def print_last_equations(self) -> None:
        print(f"Всего решений: {len(self.equations)}")
        for solution_index, solution in enumerate(self.equations):
            print(f"Решение {solution_index+1}:")
            for step_index, step in enumerate(solution):
                print(f"\t{step_index+1}. {step}")




def f(x: int | float) -> int | float:
    return x**3-12*x+10


epsilon = 10 ** -4

processor = BisectionProcessor(f, epsilon=epsilon)
processor.find_solutions(extra=False)

processor.print_last_equations()




