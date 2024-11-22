import matplotlib.pyplot as plt
from . import db

plt.rcParams['font.family'] = 'DejaVu Sans'


def plot_top_countries(top=10):
    data = db.get_top_countries(top)
    countries = [row['country'] for row in data]
    gold = [row['gold'] for row in data]
    silver = [row['silver'] for row in data]
    bronze = [row['bronze'] for row in data]

    x = range(len(countries))

    plt.bar(x, gold, label='Gold', color='gold')
    plt.bar(x, silver, bottom=gold, label='Silver', color='silver')
    plt.bar(x, bronze, bottom=[g + s for g, s in zip(gold, silver)], label='Bronze', color='#cd7f32')

    plt.xticks(x, countries, rotation=45, ha='right')
    plt.ylabel("Medal Count")
    plt.title(f"Top {top} Countries by Medals")
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_top_collective(top=10):
    data = db.get_top_collective(top)
    countries = [row['country'] for row in data]
    medals = [row['medals'] for row in data]

    plt.bar(countries, medals, color='blue')
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Medal Count")
    plt.title(f"Top {top} Countries by Collective Medals")
    plt.tight_layout()
    plt.show()

def plot_top_individual(top=10):
    data = db.get_top_individual(top)
    athletes = [row['name'] for row in data]
    medals = [row['medals'] for row in data]

    plt.bar(athletes, medals, color='green')
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Medal Count")
    plt.title(f"Top {top} Individual Athletes by Medals")
    plt.tight_layout()
    plt.show()