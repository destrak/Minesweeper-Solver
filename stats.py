class SolverStats:
    def __init__(self, threshold=0.05):
        self.total_moves = 0
        self.safe_moves = 0
        self.total_games = 0
        self.victories = 0
        self.threshold = threshold
   

    def register_move(self, prob):
        self.total_moves += 1
        if prob <= self.threshold:
            self.safe_moves += 1

    def register_game(self, won):
        self.total_games += 1
        if won:
            self.victories += 1

    def get_summary(self):
        precision = (self.safe_moves / self.total_moves) * 100 if self.total_moves > 0 else 0
        winrate = (self.victories / self.total_games) * 100 if self.total_games > 0 else 0
        return {
            "Total Moves": self.total_moves,
            "Safe Moves": self.safe_moves,
            "Precision (%)": round(precision, 2),
            "Total Games": self.total_games,
            "Victories": self.victories,
            "Win Rate (%)": round(winrate, 2)
        }

    def print_summary(self):
        summary = self.get_summary()
        print("\n===== Solver Statistics =====")
        for key, value in summary.items():
            print(f"{key}: {value}")

    def save_to_csv(self, filename="solver_stats.csv"):
        import csv
        summary = self.get_summary()
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Métrica", "Valor"])
            for key, value in summary.items():
                writer.writerow([key, value])
