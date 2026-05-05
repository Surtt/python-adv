from abc import ABC, abstractmethod
from collections import defaultdict
from collections.abc import Sequence
import statistics


class StatisticsCalculator(ABC):
    @abstractmethod
    def calculate(self, grades: list[int]) -> float: ...


class Notifier(ABC):
    @abstractmethod
    def notify(self, student: str, value: float) -> None: ...


class AverageCalculator(StatisticsCalculator):
    def calculate(self, grades: list[int]) -> float:
        return sum(grades) / len(grades) if grades else 0.0


class MedianCalculator(StatisticsCalculator):
    def calculate(self, grades: list[int]) -> float:
        return statistics.median(grades) if grades else 0.0


class ConsoleNotifier(Notifier):
    def notify(self, student: str, value: float) -> None:
        print(f"  ⚠ ВНИМАНИЕ: {student} — средний балл {value:.2f} (ниже порога)")


class FileNotifier(Notifier):
    def __init__(self, path: str):
        self._path = path

    def notify(self, student: str, value: float) -> None:
        with open(self._path, "a") as f:
            f.write(f"{student}: средний {value:.2f}\n")


class GradeJournal:
    def __init__(self):
        self._data: dict[str, dict[str, list[int]]] = defaultdict(
            lambda: defaultdict(list)
        )

    def add_grade(self, student: str, subject: str, grade: int) -> None:
        self._data[student][subject].append(grade)

    def get_student_grades(self, student: str) -> list[int]:
        result = []
        for grades in self._data[student].values():
            result.extend(grades)
        return result

    def get_subject_grades(self, subject: str) -> list[int]:
        result = []
        for subjects in self._data.values():
            if subject in subjects:
                result.extend(subjects[subject])
        return result

    def all_students(self) -> list[str]:
        return list(self._data.keys())


class GradeMonitor:
    def __init__(
        self,
        journal: GradeJournal,
        calculator: StatisticsCalculator,
        notifiers: Sequence[Notifier],
        threshold: float = 3.5,
    ):
        self._journal = journal
        self._calculator = calculator
        self._notifiers = notifiers
        self._threshold = threshold

    def on_grade_added(self, student: str, subject: str, grade: int) -> None:
        self._journal.add_grade(student, subject, grade)
        all_grades = self._journal.get_student_grades(student)
        avg = self._calculator.calculate(all_grades)
        if avg < self._threshold:
            for notifier in self._notifiers:
                notifier.notify(student, avg)

    def student_report(self, student: str) -> float:
        return self._calculator.calculate(self._journal.get_student_grades(student))

    def subject_report(self, subject: str) -> float:
        return self._calculator.calculate(self._journal.get_subject_grades(subject))


journal = GradeJournal()
calculator = AverageCalculator()
notifiers = [ConsoleNotifier()]
monitor = GradeMonitor(journal, calculator, notifiers)

print("=== Добавляем оценки ===\n")

monitor.on_grade_added("Иванов", "Математика", 5)
print("Иванов: Математика 5")

monitor.on_grade_added("Иванов", "Физика", 4)
print("Иванов: Физика 4")

monitor.on_grade_added("Иванов", "Русский", 2)
print("Иванов: Русский 2")

monitor.on_grade_added("Иванов", "История", 2)
print("Иванов: История 2")

monitor.on_grade_added("Петрова", "Математика", 5)
print("Петрова: Математика 5")

monitor.on_grade_added("Петрова", "Физика", 5)
print("Петрова: Физика 5")

print("\n=== Отчёты ===\n")
print(f"Иванов, средний балл:    {monitor.student_report('Иванов'):.2f}")
print(f"Петрова, средний балл:   {monitor.student_report('Петрова'):.2f}")
print(f"Математика, средний:     {monitor.subject_report('Математика'):.2f}")
print(f"Физика, средний:         {monitor.subject_report('Физика'):.2f}")
