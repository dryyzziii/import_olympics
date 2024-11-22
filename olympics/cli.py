"""CLI internal functions."""

from rich.console import Console
from rich.table import Table
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from . import db

plt.rcParams['font.family'] = 'DejaVu Sans'



def top_countries(top=10, file=None, plot=False):
    table = Table(title=f"Top {top} countries")

    table.add_column('Country')
    table.add_column('Gold', justify='right')
    table.add_column('Silver', justify='right')
    table.add_column('Bronze', justify='right')
    table.add_column('Total', justify='right')

    get_top = db.get_top_countries(top)
    if plot:
        plot_top_countries(get_top)
    else:
        if get_top:
            for row in get_top:
                table.add_row(
                    row['country'],
                    str(row['gold']),
                    str(row['silver']),
                    str(row['bronze']),
                    str(row['gold'] + row['silver'] + row['bronze']),
                )

    console = Console(file=file)
    console.print(table)


def top_collective(top=10, file=None):
    table = Table(title=f'Top {top} collective events')

    table.add_column('Country')
    table.add_column('Medals', justify='right')

    get_top = db.get_top_collective(top)
    if get_top:
        for row in get_top:
            table.add_row(
                row['country'],
                str(row['medals']),
            )

    console = Console(file=file)
    console.print(table)



def top_individual(top=10, file=None):
    table = Table(title=f'Top {top} individual events')

    table.add_column('Name')
    table.add_column('Gender')
    table.add_column('Country')
    table.add_column('Medals', justify='right')

    get_top = db.get_top_individual(top)
    if get_top:
        for row in get_top:
            table.add_row(
                row['name'],
                row['gender'].capitalize(),
                row['country'],
                str(row['medals']),
            )

    console = Console(file=file)
    console.print(table)


def plot_top_countries_tk(data):
    """Créer un graphique matplotlib pour les médailles par pays."""
    fig, ax = plt.subplots()
    countries = [row['country'] for row in data]
    gold = [row['gold'] for row in data]
    silver = [row['silver'] for row in data]
    bronze = [row['bronze'] for row in data]

    bar_width = 0.25
    indices = range(len(countries))

    ax.bar(indices, gold, width=bar_width, label="Gold", color='gold')
    ax.bar([i + bar_width for i in indices], silver, width=bar_width, label="Silver", color='silver')
    ax.bar([i + 2 * bar_width for i in indices], bronze, width=bar_width, label="Bronze", color='#cd7f32')

    ax.set_xlabel("Countries")
    ax.set_ylabel("Number of Medals")
    ax.set_title("Top Countries by Medal Count")
    ax.set_xticks([i + bar_width for i in indices])
    ax.set_xticklabels(countries, rotation=45)
    ax.legend()

    return fig


def show_plot_in_tk(data):
    """Fenêtre Tkinter pour afficher un graphique."""
    root = tk.Tk()
    root.title("Olympics Data Visualization")

    # Création du graphique
    fig = plot_top_countries_tk(data)

    # Intégration du graphique dans Tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Bouton de fermeture
    btn_close = ttk.Button(root, text="Close", command=root.destroy)
    btn_close.pack(side=tk.BOTTOM)

    root.mainloop()

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