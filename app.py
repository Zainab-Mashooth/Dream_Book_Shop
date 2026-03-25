
# ============================================================
# DREAM BOOK SHOP - ADVANCED OOP ANALYSIS SYSTEM

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod




# ============================================================
# SmartColumnLocator - Auto-detects column names
# ============================================================
class SmartColumnLocator:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def locate(self, keywords):
        for col in self.df.columns:
            if any(key.lower() in col.lower() for key in keywords):
                return col
        return None


# ============================================================
# BookDataManager - Loads and preprocesses dataset
# ============================================================
class BookDataManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None

        self.col_year = None
        self.col_author = None
        self.col_language = None
        self.col_publisher = None
        self.col_isbn = None

    def load_books(self):
        self.df = pd.read_csv(self.file_path)
        self.df.columns = self.df.columns.str.strip()
        self.df.replace(" ", np.nan, inplace=True)

        column_finder = SmartColumnLocator(self.df)

        self.col_year = column_finder.locate(["year", "publication", "publish", "published"])
        self.col_author = column_finder.locate(["author", "writer"])
        self.col_language = column_finder.locate(["lang", "language"])
        self.col_publisher = column_finder.locate(["publisher", "publishing"])
        self.col_isbn = column_finder.locate(["isbn"])

        return self.df

    def prepare_data(self):
        if self.col_year:
            self.df[self.col_year] = pd.to_numeric(self.df[self.col_year], errors="coerce")
            self.df.dropna(subset=[self.col_year], inplace=True)

        for col in [self.col_author, self.col_language, self.col_publisher, self.col_isbn]:
            if col:
                self.df[col] = self.df[col].astype(str).replace("nan", "")

        return self.df


# ============================================================
# Abstract Analyzer Definition
# ============================================================
class AbstractBookAnalyzer(ABC):

    @abstractmethod
    def show_publication_timeline(self): ...
    @abstractmethod
    def show_top_authors(self): ...
    @abstractmethod
    def show_language_mix(self): ...
    @abstractmethod
    def show_publisher_output(self): ...
    @abstractmethod
    def show_missing_isbn_stats(self): ...
    @abstractmethod
    def show_yearly_language_breakdown(self): ...


# ============================================================
# BookInsightsAnalyzer - Concrete Implementation
# ============================================================
class BookInsightsAnalyzer(AbstractBookAnalyzer):

    def __init__(self, df, manager: BookDataManager):
        self.df = df
        self.manager = manager

    # --------------------------------------------------------

    def show_publication_timeline(self):
        year = self.manager.col_year

        trends = self.df.groupby(year).size()

        print("\n== Publication Timeline ==")
        print (trends)

        plt.figure(figsize=(10,4))
        plt.plot(trends.index, trends.values, marker='o', color="#2E86C1")
        plt.title("Publication Timeline (Books per Year)")
        plt.xlabel("Year")
        plt.ylabel("Number of Books")
        plt.grid(True)
        plt.show()

    # --------------------------------------------------------
    def show_top_authors(self):
        author = self.manager.col_author
        counts = self.df[author].value_counts().head(5)

        print("\n== Leading Authors ==")
        print(counts)

        plt.figure(figsize=(8,4))
        plt.barh(counts.index, counts.values, color="#AF7AC5")
        plt.title("Top 5 Authors")
        plt.xlabel("Books")
        plt.gca().invert_yaxis()
        plt.show()

    # --------------------------------------------------------
    def show_language_mix(self):
        lang = self.manager.col_language
        dist = self.df[lang].value_counts()

        print("\n== Language Mix Distribution ==")
        print(dist)

        plt.figure(figsize=(6,6))
        plt.pie(
            dist.values,
            labels=dist.index,
            autopct="%1.1f%%",
            startangle=90,
            colors=["#1ABC9C", "#F1C40F", "#E67E22", "#5DADE2", "#BB8FCE"]
        )
        plt.title("Language Distribution")
        plt.show()

    # --------------------------------------------------------
    def show_publisher_output(self):
        pub = self.manager.col_publisher
        counts = self.df[pub].value_counts()

        print("\n== Publisher Output ==")
        print(counts)

        plt.figure(figsize=(10,5))
        plt.bar(
            counts.index[:15],
            counts.values[:15],
            color="#3498DB"
        )
        plt.xticks(rotation=90)
        plt.title("Books by Publisher")
        plt.xlabel("Publisher")
        plt.ylabel("Book Count")
        plt.show()

    # --------------------------------------------------------
    def show_missing_isbn_stats(self):
        isbn = self.manager.col_isbn

        missing = self.df[isbn].isna().sum()
        total = len(self.df)
        pct = (missing / total) * 100

        print("\n== ISBN Completeness Check ==")
        print(f"Missing: {missing} / Total: {total}  ({pct:.2f}%)")

        plt.figure(figsize=(5,5))
        plt.pie(
            [missing, total - missing],
            labels=["Missing", "Present"],
            autopct="%1.1f%%",
            startangle=90,
            colors=["#E74C3C", "#2ECC71"]
        )
        plt.title("Missing ISBN Percentage")
        plt.show()

    # --------------------------------------------------------
    def show_yearly_language_breakdown(self):
        year = self.manager.col_year
        lang = self.manager.col_language

        table = self.df.groupby([year, lang]).size().unstack(fill_value=0)

        print("\n== Yearly Language Breakdown ==")
        print(table)

        table.plot(
            kind='bar',
            stacked=True,
            figsize=(12,6),
            color=["#1ABC9C", "#2E86C1", "#AF7AC5", "#E67E22", "#E74C3C"]
        )
        plt.title("Books per Year (Category: Language)")
        plt.xlabel("Year")
        plt.ylabel("Book Count")
        plt.show()


# ============================================================
# Main System Controller
# ============================================================
class BookShopAnalysisApp:
    def __init__(self, file_path):
        self.file_path = file_path

    def execute(self):
        manager = BookDataManager(self.file_path)
        df = manager.load_books()
        df = manager.prepare_data()

        analyzer = BookInsightsAnalyzer(df, manager)

        analyzer.show_publication_timeline()
        analyzer.show_top_authors()
        analyzer.show_language_mix()
        analyzer.show_publisher_output()
        analyzer.show_missing_isbn_stats()
        analyzer.show_yearly_language_breakdown()


# ============================================================
# RUN PROGRAM
# ============================================================
file_path = "dataset.csv"
app = BookShopAnalysisApp(file_path)
app.execute()
