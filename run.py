import locale
from app import FitnessApp

if __name__ == "__main__":
    locale.setlocale(locale.LC_TIME, "fr_CH.UTF-8")
    app = FitnessApp()
    app.run()