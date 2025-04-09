# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 15:43:06 2025

@author: ahmed
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr 9 (Year updated based on current date)

@author: ahmed (or your name)
Description: A PyQt5 GUI application for calculating statistical sample sizes.
"""

import sys
import math
import numpy as np
from scipy.stats import norm # Needed for Z-scores in calculations

from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QFormLayout,
                            QSpinBox, QDoubleSpinBox, QLabel, QPushButton, QVBoxLayout,
                            QHBoxLayout, QComboBox, QGroupBox, QScrollArea, QLineEdit,
                            QTextEdit, QSizePolicy, QFrame, QGridLayout, QCheckBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor # QIcon, QPalette, QColor are currently unused

class SampleSizeCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Statistical Sample Size Calculator")
        self.setMinimumSize(950, 750) # Slightly increased size for better layout

        # Set application style
        self.set_application_style()

        # Create main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget) # Directly pass parent widget
        # main_widget.setLayout(main_layout) # Not needed if passed in constructor
        self.setCentralWidget(main_widget)

        # Add header with title
        header = QLabel("Statistical Sample Size Calculator")
        header.setFont(QFont("Arial", 16, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("color: #2c3e50; margin: 10px;")
        main_layout.addWidget(header)

        # Add description
        description = QLabel("Calculate required sample sizes for various statistical analyses")
        description.setFont(QFont("Arial", 10))
        description.setAlignment(Qt.AlignCenter)
        description.setStyleSheet("color: #7f8c8d; margin-bottom: 20px;")
        main_layout.addWidget(description)

        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.setFont(QFont("Arial", 9))
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                background: #f5f5f5;
                border: 1px solid #ddd;
                border-bottom: none;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #3498db;
                color: white;
                border: 1px solid #2980b9;
                border-bottom: none;
            }
            QTabWidget::pane {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 15px; /* Increased padding */
                background-color: #ffffff; /* Ensure pane background is distinct */
            }
        """)

        # Create tabs
        self.create_basic_tab()
        self.create_intermediate_tab()
        self.create_advanced_tab()

        main_layout.addWidget(self.tabs)

        # Add footer
        # Update year dynamically or set manually
        from datetime import datetime
        current_year = datetime.now().year
        footer = QLabel(f"© {current_year} Sample Size Calculator | Created with PyQt5")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: #95a5a6; margin-top: 15px; margin-bottom: 5px;")
        main_layout.addWidget(footer)

    def set_application_style(self):
        """Set the global application style"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0; /* Slightly different background */
            }
            QLabel {
                color: #2c3e50;
                padding: 2px; /* Add slight padding to labels */
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #ccc; /* Lighter border */
                border-radius: 6px;
                margin-top: 15px; /* Increased top margin */
                padding-top: 15px; /* Increased top padding */
                background-color: #f9f9f9; /* Background for groupbox */
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left; /* Position title correctly */
                left: 10px;
                padding: 0 5px 0 5px;
                background-color: #f0f0f0; /* Match main window bg */
                color: #34495e;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                margin: 5px;
                font-weight: bold;
                min-width: 150px; /* Give buttons a minimum width */
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1c6ea4;
            }
            QSpinBox, QDoubleSpinBox, QComboBox, QLineEdit {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
                background: white;
                min-width: 80px; /* Ensure minimum width */
            }
            QScrollArea {
                border: none;
                background-color: transparent; /* Make scroll area background transparent */
            }
            QTextEdit {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
                background: white;
            }
            QLabel#resultLabel { /* Style for result labels */
               font-weight: bold;
               padding: 10px;
               background-color: #e8f6fd; /* Light blue background */
               border-radius: 4px;
               border: 1px solid #d0eafa;
               color: #2980b9;
               min-height: 30px; /* Ensure minimum height */
               margin-top: 5px;
            }
        """)

    def create_scroll_area(self, widget_with_layout):
        """Create a scrollable area for a given widget"""
        # The widget passed should already have a layout set
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(widget_with_layout)
        scroll.setStyleSheet("background-color: transparent;") # Ensure scroll area bg is transparent
        return scroll

    def create_basic_tab(self):
        """Create tab for basic statistical analyses (T-Tests, ANOVA)"""
        basic_tab_widget = QWidget() # Create a container widget for the layout
        basic_layout = QVBoxLayout(basic_tab_widget) # Set layout on the widget
        basic_layout.setSpacing(20) # Add spacing between group boxes

        # --- T-tests section ---
        t_test_group = QGroupBox("T-Tests")
        t_test_layout = QVBoxLayout() # Main layout for T-tests group

        t_tests_grid = QGridLayout() # Grid to arrange different T-tests
        t_tests_grid.setSpacing(15)

        # Independent samples t-test
        indep_t_container = QGroupBox("Independent Samples")
        indep_t_container_layout = QVBoxLayout()
        indep_t_form = QFormLayout()

        self.indep_t_alpha = QDoubleSpinBox(decimals=3, value=0.05, minimum=0.001, maximum=0.5, singleStep=0.01)
        self.indep_t_power = QDoubleSpinBox(decimals=2, value=0.80, minimum=0.50, maximum=0.99, singleStep=0.05)
        self.indep_t_effect = QDoubleSpinBox(decimals=2, value=0.50, minimum=0.10, maximum=3.00, singleStep=0.05)

        indep_t_form.addRow("Significance Level (α):", self.indep_t_alpha)
        indep_t_form.addRow("Power (1-β):", self.indep_t_power)
        indep_t_form.addRow("Effect Size (Cohen's d):", self.indep_t_effect)

        indep_t_calc_btn = QPushButton("Calculate")
        indep_t_calc_btn.clicked.connect(self.calc_indep_t_sample)

        self.indep_t_result = QLabel("Sample size per group: N/A")
        self.indep_t_result.setObjectName("resultLabel") # Assign object name for specific styling
        self.indep_t_result.setAlignment(Qt.AlignCenter)

        indep_t_container_layout.addLayout(indep_t_form)
        indep_t_container_layout.addWidget(indep_t_calc_btn, 0, Qt.AlignCenter)
        indep_t_container_layout.addWidget(self.indep_t_result)
        indep_t_container.setLayout(indep_t_container_layout)
        t_tests_grid.addWidget(indep_t_container, 0, 0)

        # Paired samples t-test
        paired_t_container = QGroupBox("Paired Samples")
        paired_t_container_layout = QVBoxLayout()
        paired_t_form = QFormLayout()

        self.paired_t_alpha = QDoubleSpinBox(decimals=3, value=0.05, minimum=0.001, maximum=0.5, singleStep=0.01)
        self.paired_t_power = QDoubleSpinBox(decimals=2, value=0.80, minimum=0.50, maximum=0.99, singleStep=0.05)
        self.paired_t_effect = QDoubleSpinBox(decimals=2, value=0.50, minimum=0.10, maximum=3.00, singleStep=0.05)

        paired_t_form.addRow("Significance Level (α):", self.paired_t_alpha)
        paired_t_form.addRow("Power (1-β):", self.paired_t_power)
        paired_t_form.addRow("Effect Size (Cohen's dz):", self.paired_t_effect)

        paired_t_calc_btn = QPushButton("Calculate")
        paired_t_calc_btn.clicked.connect(self.calc_paired_t_sample)

        self.paired_t_result = QLabel("Number of pairs: N/A")
        self.paired_t_result.setObjectName("resultLabel")
        self.paired_t_result.setAlignment(Qt.AlignCenter)

        paired_t_container_layout.addLayout(paired_t_form)
        paired_t_container_layout.addWidget(paired_t_calc_btn, 0, Qt.AlignCenter)
        paired_t_container_layout.addWidget(self.paired_t_result)
        paired_t_container.setLayout(paired_t_container_layout)
        t_tests_grid.addWidget(paired_t_container, 0, 1)

        # One-sample t-test
        one_t_container = QGroupBox("One Sample")
        one_t_container_layout = QVBoxLayout()
        one_t_form = QFormLayout()

        self.one_t_alpha = QDoubleSpinBox(decimals=3, value=0.05, minimum=0.001, maximum=0.5, singleStep=0.01)
        self.one_t_power = QDoubleSpinBox(decimals=2, value=0.80, minimum=0.50, maximum=0.99, singleStep=0.05)
        self.one_t_effect = QDoubleSpinBox(decimals=2, value=0.50, minimum=0.10, maximum=3.00, singleStep=0.05)

        one_t_form.addRow("Significance Level (α):", self.one_t_alpha)
        one_t_form.addRow("Power (1-β):", self.one_t_power)
        one_t_form.addRow("Effect Size (Cohen's d):", self.one_t_effect)

        one_t_calc_btn = QPushButton("Calculate")
        one_t_calc_btn.clicked.connect(self.calc_one_t_sample)

        self.one_t_result = QLabel("Sample size: N/A")
        self.one_t_result.setObjectName("resultLabel")
        self.one_t_result.setAlignment(Qt.AlignCenter)

        one_t_container_layout.addLayout(one_t_form)
        one_t_container_layout.addWidget(one_t_calc_btn, 0, Qt.AlignCenter)
        one_t_container_layout.addWidget(self.one_t_result)
        one_t_container.setLayout(one_t_container_layout)
        t_tests_grid.addWidget(one_t_container, 1, 0)

        t_test_layout.addLayout(t_tests_grid)
        t_test_group.setLayout(t_test_layout)
        basic_layout.addWidget(t_test_group)


        # --- ANOVA section ---
        anova_group = QGroupBox("Analysis of Variance (ANOVA)")
        anova_layout = QVBoxLayout()

        anova_grid = QGridLayout()
        anova_grid.setSpacing(15)

        # One-way ANOVA
        oneway_container = QGroupBox("One-way ANOVA (Between Subjects)")
        oneway_container_layout = QVBoxLayout()
        oneway_form = QFormLayout()

        self.oneway_alpha = QDoubleSpinBox(decimals=3, value=0.05, minimum=0.001, maximum=0.5, singleStep=0.01)
        self.oneway_power = QDoubleSpinBox(decimals=2, value=0.80, minimum=0.50, maximum=0.99, singleStep=0.05)
        self.oneway_effect = QDoubleSpinBox(decimals=2, value=0.25, minimum=0.05, maximum=1.50, singleStep=0.05) # Cohen's f
        self.oneway_groups = QSpinBox(value=3, minimum=2, maximum=20)

        oneway_form.addRow("Significance Level (α):", self.oneway_alpha)
        oneway_form.addRow("Power (1-β):", self.oneway_power)
        oneway_form.addRow("Effect Size (f):", self.oneway_effect)
        oneway_form.addRow("Number of Groups:", self.oneway_groups)

        oneway_calc_btn = QPushButton("Calculate")
        oneway_calc_btn.clicked.connect(self.calc_oneway_sample)

        self.oneway_result = QLabel("Sample size per group: N/A")
        self.oneway_result.setObjectName("resultLabel")
        self.oneway_result.setAlignment(Qt.AlignCenter)

        oneway_container_layout.addLayout(oneway_form)
        oneway_container_layout.addWidget(oneway_calc_btn, 0, Qt.AlignCenter)
        oneway_container_layout.addWidget(self.oneway_result)
        oneway_container.setLayout(oneway_container_layout)
        anova_grid.addWidget(oneway_container, 0, 0)

        # Factorial ANOVA (Placeholder - more complex)
        factorial_container = QGroupBox("Factorial ANOVA (Example: 2x2)") # Simplified example
        factorial_container_layout = QVBoxLayout()
        factorial_form = QFormLayout()

        self.factorial_alpha = QDoubleSpinBox(decimals=3, value=0.05, minimum=0.001, maximum=0.5, singleStep=0.01)
        self.factorial_power = QDoubleSpinBox(decimals=2, value=0.80, minimum=0.50, maximum=0.99, singleStep=0.05)
        self.factorial_effect = QDoubleSpinBox(decimals=2, value=0.25, minimum=0.05, maximum=1.50, singleStep=0.05) # Cohen's f
        # Example: For a 2x2 ANOVA, numerator df for interaction = (2-1)*(2-1) = 1
        # Numerator df for main effects = (2-1) = 1
        # Need specific inputs based on which effect size (main/interaction) is targeted.
        # This is a simplified placeholder.
        self.factorial_num_df = QSpinBox(value=1, minimum=1, maximum=50, toolTip="Numerator degrees of freedom for the effect of interest")

        factorial_form.addRow("Significance Level (α):", self.factorial_alpha)
        factorial_form.addRow("Power (1-β):", self.factorial_power)
        factorial_form.addRow("Effect Size (f):", self.factorial_effect)
        factorial_form.addRow("Numerator df:", self.factorial_num_df)


        factorial_calc_btn = QPushButton("Calculate")
        factorial_calc_btn.clicked.connect(self.calc_factorial_sample) # Placeholder function

        self.factorial_result = QLabel("Total sample size: N/A")
        self.factorial_result.setObjectName("resultLabel")
        self.factorial_result.setAlignment(Qt.AlignCenter)

        factorial_container_layout.addLayout(factorial_form)
        factorial_container_layout.addWidget(QLabel("Note: Factorial ANOVA calculation is complex.\nThis is a simplified interface assuming known numerator df."))
        factorial_container_layout.addWidget(factorial_calc_btn, 0, Qt.AlignCenter)
        factorial_container_layout.addWidget(self.factorial_result)
        factorial_container.setLayout(factorial_container_layout)
        anova_grid.addWidget(factorial_container, 0, 1)


        anova_layout.addLayout(anova_grid)
        anova_group.setLayout(anova_layout)
        basic_layout.addWidget(anova_group)

        basic_layout.addStretch(1) # Add stretch to push content upwards

        # Set layout to a scrollable area
        # basic_tab_widget.setLayout(basic_layout) # Layout already set
        scroll = self.create_scroll_area(basic_tab_widget)

        # Add tab
        self.tabs.addTab(scroll, "Basic Analyses")

    def create_intermediate_tab(self):
        """Create tab for intermediate analyses (Correlation, Regression, Chi-Square)"""
        intermediate_tab_widget = QWidget()
        intermediate_layout = QVBoxLayout(intermediate_tab_widget)
        intermediate_layout.setSpacing(20)

        # --- Correlation section ---
        corr_group = QGroupBox("Correlation Analysis")
        corr_layout = QVBoxLayout()
        corr_grid = QGridLayout()
        corr_grid.setSpacing(15)

        # Pearson correlation
        pearson_container = QGroupBox("Pearson Correlation")
        pearson_container_layout = QVBoxLayout()
        pearson_form = QFormLayout()

        self.pearson_alpha = QDoubleSpinBox(decimals=3, value=0.05, minimum=0.001, maximum=0.5, singleStep=0.01)
        self.pearson_power = QDoubleSpinBox(decimals=2, value=0.80, minimum=0.50, maximum=0.99, singleStep=0.05)
        self.pearson_effect = QDoubleSpinBox(decimals=2, value=0.30, minimum=0.01, maximum=0.99, singleStep=0.05) # Correlation coeff (r)
        self.pearson_tails = QComboBox()
        self.pearson_tails.addItems(["Two-tailed", "One-tailed"])

        pearson_form.addRow("Significance Level (α):", self.pearson_alpha)
        pearson_form.addRow("Power (1-β):", self.pearson_power)
        pearson_form.addRow("Expected Correlation (r):", self.pearson_effect)
        pearson_form.addRow("Test Tails:", self.pearson_tails)

        pearson_calc_btn = QPushButton("Calculate")
        pearson_calc_btn.clicked.connect(self.calc_pearson_sample)

        self.pearson_result = QLabel("Sample size: N/A")
        self.pearson_result.setObjectName("resultLabel")
        self.pearson_result.setAlignment(Qt.AlignCenter)

        pearson_container_layout.addLayout(pearson_form)
        pearson_container_layout.addWidget(pearson_calc_btn, 0, Qt.AlignCenter)
        pearson_container_layout.addWidget(self.pearson_result)
        pearson_container.setLayout(pearson_container_layout)
        corr_grid.addWidget(pearson_container, 0, 0)

        # Add more correlation types here if needed (Spearman, etc.)
        # corr_grid.addWidget(some_other_corr_container, 0, 1)

        corr_layout.addLayout(corr_grid)
        corr_group.setLayout(corr_layout)
        intermediate_layout.addWidget(corr_group)


        # --- Regression section ---
        reg_group = QGroupBox("Regression Analysis")
        reg_layout = QVBoxLayout()
        reg_grid = QGridLayout()
        reg_grid.setSpacing(15)

        # Linear Regression
        linear_reg_container = QGroupBox("Multiple Linear Regression")
        linear_reg_container_layout = QVBoxLayout()
        linear_reg_form = QFormLayout()

        self.linear_reg_alpha = QDoubleSpinBox(decimals=3, value=0.05, minimum=0.001, maximum=0.5, singleStep=0.01)
        self.linear_reg_power = QDoubleSpinBox(decimals=2, value=0.80, minimum=0.50, maximum=0.99, singleStep=0.05)
        self.linear_reg_effect = QDoubleSpinBox(decimals=3, value=0.15, minimum=0.01, maximum=1.00, singleStep=0.01) # Cohen's f^2
        self.linear_reg_predictors = QSpinBox(value=3, minimum=1, maximum=50)

        linear_reg_form.addRow("Significance Level (α):", self.linear_reg_alpha)
        linear_reg_form.addRow("Power (1-β):", self.linear_reg_power)
        linear_reg_form.addRow("Effect Size (f²):", self.linear_reg_effect)
        linear_reg_form.addRow("Number of Predictors:", self.linear_reg_predictors)

        linear_reg_calc_btn = QPushButton("Calculate")
        linear_reg_calc_btn.clicked.connect(self.calc_linear_reg_sample)

        self.linear_reg_result = QLabel("Total sample size: N/A")
        self.linear_reg_result.setObjectName("resultLabel")
        self.linear_reg_result.setAlignment(Qt.AlignCenter)

        linear_reg_container_layout.addLayout(linear_reg_form)
        linear_reg_container_layout.addWidget(linear_reg_calc_btn, 0, Qt.AlignCenter)
        linear_reg_container_layout.addWidget(self.linear_reg_result)
        linear_reg_container.setLayout(linear_reg_container_layout)
        reg_grid.addWidget(linear_reg_container, 0, 0)


        # Logistic Regression (Using the second, more standard version from input)
        logistic_reg_container = QGroupBox("Logistic Regression")
        logistic_reg_container_layout = QVBoxLayout()
        logistic_reg_form = QFormLayout()

        self.logistic_reg_alpha = QDoubleSpinBox(decimals=3, value=0.05, minimum=0.001, maximum=0.5, singleStep=0.01)
        self.logistic_reg_power = QDoubleSpinBox(decimals=2, value=0.80, minimum=0.50, maximum=0.99, singleStep=0.05)
        self.logistic_reg_odds_ratio = QDoubleSpinBox(decimals=2, value=2.0, minimum=1.01, maximum=10.0, singleStep=0.1, toolTip="For a one unit change in the predictor of interest")
        self.logistic_reg_p1 = QDoubleSpinBox(decimals=2, value=0.30, minimum=0.01, maximum=0.99, singleStep=0.05, toolTip="Baseline probability of the event (outcome=1)")
        self.logistic_reg_predictors = QSpinBox(value=1, minimum=1, maximum=20, toolTip="Number of predictors *excluding* the one for the Odds Ratio") # Clarified meaning
        self.logistic_reg_r2_other = QDoubleSpinBox(decimals=2, value=0.10, minimum=0.00, maximum=0.95, singleStep=0.05, toolTip="R-squared between predictor of interest and *other* predictors")


        logistic_reg_form.addRow("Significance Level (α):", self.logistic_reg_alpha)
        logistic_reg_form.addRow("Power (1-β):", self.logistic_reg_power)
        logistic_reg_form.addRow("Odds Ratio (Exp(B)):", self.logistic_reg_odds_ratio)
        logistic_reg_form.addRow("Baseline Probability P(Y=1):", self.logistic_reg_p1)
        logistic_reg_form.addRow("R² (X₁ vs other X's):", self.logistic_reg_r2_other)
        # logistic_reg_form.addRow("Number of Other Predictors:", self.logistic_reg_predictors) # Predictors input might need refinement depending on formula used

        logistic_reg_calc_btn = QPushButton("Calculate")
        logistic_reg_calc_btn.clicked.connect(self.calc_logistic_reg_sample)

        self.logistic_reg_result = QLabel("Sample size: N/A")
        self.logistic_reg_result.setObjectName("resultLabel")
        self.logistic_reg_result.setAlignment(Qt.AlignCenter)
        
        # Add explanatory note for logistic regression complexity
        log_reg_note = QLabel("Note: Logistic regression sample size depends heavily\n on the specific formula used (e.g., Hsieh et al., 1998). \nInputs provided target common approaches.")
        log_reg_note.setStyleSheet("font-size: 8pt; color: #555;")


        logistic_reg_container_layout.addLayout(logistic_reg_form)
        logistic_reg_container_layout.addWidget(log_reg_note)
        logistic_reg_container_layout.addWidget(logistic_reg_calc_btn, 0, Qt.AlignCenter)
        logistic_reg_container_layout.addWidget(self.logistic_reg_result)
        logistic_reg_container.setLayout(logistic_reg_container_layout)
        reg_grid.addWidget(logistic_reg_container, 0, 1)

        reg_layout.addLayout(reg_grid)
        reg_group.setLayout(reg_layout)
        intermediate_layout.addWidget(reg_group)

        # --- Chi-Square Tests ---
        chi_group = QGroupBox("Chi-Square Tests")
        chi_layout = QVBoxLayout()
        chi_grid = QGridLayout()
        chi_grid.setSpacing(15)

        # Chi-Square Test of Independence / Goodness of Fit
        chi_ind_container = QGroupBox("Chi-Square Test")
        chi_ind_container_layout = QVBoxLayout()
        chi_ind_form = QFormLayout()

        self.chi_ind_alpha = QDoubleSpinBox(decimals=3, value=0.05, minimum=0.001, maximum=0.5, singleStep=0.01)
        self.chi_ind_power = QDoubleSpinBox(decimals=2, value=0.80, minimum=0.50, maximum=0.99, singleStep=0.05)
        self.chi_ind_effect = QDoubleSpinBox(decimals=2, value=0.30, minimum=0.05, maximum=1.00, singleStep=0.05) # Effect size (w)
        self.chi_ind_df = QSpinBox(value=4, minimum=1, maximum=50, toolTip="Degrees of Freedom (e.g., (rows-1)*(cols-1))")

        chi_ind_form.addRow("Significance Level (α):", self.chi_ind_alpha)
        chi_ind_form.addRow("Power (1-β):", self.chi_ind_power)
        chi_ind_form.addRow("Effect Size (w):", self.chi_ind_effect)
        chi_ind_form.addRow("Degrees of Freedom (df):", self.chi_ind_df)

        chi_ind_calc_btn = QPushButton("Calculate")
        chi_ind_calc_btn.clicked.connect(self.calc_chi_ind_sample)

        self.chi_ind_result = QLabel("Total sample size: N/A")
        self.chi_ind_result.setObjectName("resultLabel")
        self.chi_ind_result.setAlignment(Qt.AlignCenter)

        chi_ind_container_layout.addLayout(chi_ind_form)
        chi_ind_container_layout.addWidget(chi_ind_calc_btn, 0, Qt.AlignCenter)
        chi_ind_container_layout.addWidget(self.chi_ind_result)
        chi_ind_container.setLayout(chi_ind_container_layout)
        chi_grid.addWidget(chi_ind_container, 0, 0)

        # Add more chi-square related tests here if needed

        chi_layout.addLayout(chi_grid)
        chi_group.setLayout(chi_layout)
        intermediate_layout.addWidget(chi_group)


        intermediate_layout.addStretch(1)

        # Set layout to scrollable area
        # intermediate_tab_widget.setLayout(intermediate_layout) # Layout already set
        scroll = self.create_scroll_area(intermediate_tab_widget)

        # Add tab
        self.tabs.addTab(scroll, "Intermediate Analyses")

    def create_advanced_tab(self):
        """Create tab for advanced analyses (e.g., Power Analysis)"""
        advanced_tab_widget = QWidget()
        advanced_layout = QVBoxLayout(advanced_tab_widget)
        advanced_layout.setSpacing(20)

        # --- Power Analysis section (Post-hoc / Sensitivity) ---
        power_group = QGroupBox("Post-hoc / Sensitivity Power Analysis")
        power_layout = QVBoxLayout()
        power_grid = QGridLayout()
        power_grid.setSpacing(15)

        # Calculate Achieved Power
        power_level_container = QGroupBox("Calculate Achieved Power")
        power_level_container_layout = QVBoxLayout()
        power_level_form = QFormLayout()

        # Common inputs
        self.power_level_test_type = QComboBox()
        self.power_level_test_type.addItems([
            "T-Test (Independent)", "T-Test (Paired)", "ANOVA (One-way)",
            "Correlation (Pearson)", "Linear Regression", "Chi-Square"
            ])
        self.power_level_alpha = QDoubleSpinBox(decimals=3, value=0.05, minimum=0.001, maximum=0.5, singleStep=0.01)
        self.power_level_n = QSpinBox(value=100, minimum=10, maximum=10000, singleStep=10, toolTip="Total N for Regression/Chi2/Corr; N per group for T-Ind/ANOVA; N pairs for T-Paired")
        self.power_level_effect = QDoubleSpinBox(decimals=3, value=0.3, minimum=0.01, maximum=3.0, singleStep=0.01, toolTip="Effect size (d, f, r, f², w)")
        # Add specific inputs needed for certain tests (e.g., df, groups)
        self.power_level_groups = QSpinBox(value=3, minimum=2, maximum=20, toolTip="Num Groups (ANOVA)")
        self.power_level_predictors = QSpinBox(value=3, minimum=1, maximum=50, toolTip="Num Predictors (Regression)")
        self.power_level_df = QSpinBox(value=4, minimum=1, maximum=100, toolTip="df (Chi-Square)")
        # Initially hide specific inputs
        self.power_level_groups.setVisible(False)
        self.power_level_predictors.setVisible(False)
        self.power_level_df.setVisible(False)

        power_level_form.addRow("Statistical Test:", self.power_level_test_type)
        power_level_form.addRow("Significance Level (α):", self.power_level_alpha)
        power_level_form.addRow("Sample Size (N):", self.power_level_n)
        power_level_form.addRow("Effect Size:", self.power_level_effect)
        # Add rows for specific inputs, linking visibility later
        self.power_level_groups_row = power_level_form.addRow("Number of Groups:", self.power_level_groups)
        self.power_level_predictors_row = power_level_form.addRow("Number of Predictors:", self.power_level_predictors)
        self.power_level_df_row = power_level_form.addRow("Degrees of Freedom:", self.power_level_df)
        # Hide rows initially - PyQt doesn't directly hide rows, hide widgets instead
        power_level_form.labelForField(self.power_level_groups).setVisible(False)
        power_level_form.labelForField(self.power_level_predictors).setVisible(False)
        power_level_form.labelForField(self.power_level_df).setVisible(False)
        # Connect signal to update visibility
        self.power_level_test_type.currentIndexChanged.connect(self.update_power_level_inputs)


        power_level_calc_btn = QPushButton("Calculate Power")
        power_level_calc_btn.clicked.connect(self.calc_achieved_power)

        self.power_level_result = QLabel("Achieved Power (1-β): N/A")
        self.power_level_result.setObjectName("resultLabel")
        self.power_level_result.setAlignment(Qt.AlignCenter)

        power_level_container_layout.addLayout(power_level_form)
        power_level_container_layout.addWidget(power_level_calc_btn, 0, Qt.AlignCenter)
        power_level_container_layout.addWidget(self.power_level_result)
        power_level_container.setLayout(power_level_container_layout)
        power_grid.addWidget(power_level_container, 0, 0)

        # Calculate Minimum Detectable Effect Size (MDES)
        power_effect_container = QGroupBox("Minimum Detectable Effect Size (MDES)")
        power_effect_container_layout = QVBoxLayout()
        power_effect_form = QFormLayout()

        self.power_effect_test_type = QComboBox()
        self.power_effect_test_type.addItems([
            "T-Test (Independent)", "T-Test (Paired)", "ANOVA (One-way)",
            "Correlation (Pearson)", "Linear Regression", "Chi-Square"
            ])
        self.power_effect_alpha = QDoubleSpinBox(decimals=3, value=0.05, minimum=0.001, maximum=0.5, singleStep=0.01)
        self.power_effect_power = QDoubleSpinBox(decimals=2, value=0.80, minimum=0.50, maximum=0.99, singleStep=0.05)
        self.power_effect_n = QSpinBox(value=100, minimum=10, maximum=10000, singleStep=10, toolTip="Total N or N per group/pair")
        # Add specific inputs needed for certain tests (e.g., df, groups)
        self.power_effect_groups = QSpinBox(value=3, minimum=2, maximum=20, toolTip="Num Groups (ANOVA)")
        self.power_effect_predictors = QSpinBox(value=3, minimum=1, maximum=50, toolTip="Num Predictors (Regression)")
        self.power_effect_df = QSpinBox(value=4, minimum=1, maximum=100, toolTip="df (Chi-Square)")
        # Initially hide specific inputs
        self.power_effect_groups.setVisible(False)
        self.power_effect_predictors.setVisible(False)
        self.power_effect_df.setVisible(False)

        power_effect_form.addRow("Statistical Test:", self.power_effect_test_type)
        power_effect_form.addRow("Significance Level (α):", self.power_effect_alpha)
        power_effect_form.addRow("Desired Power (1-β):", self.power_effect_power)
        power_effect_form.addRow("Sample Size (N):", self.power_effect_n)
        # Add rows for specific inputs
        self.power_effect_groups_row = power_effect_form.addRow("Number of Groups:", self.power_effect_groups)
        self.power_effect_predictors_row = power_effect_form.addRow("Number of Predictors:", self.power_effect_predictors)
        self.power_effect_df_row = power_effect_form.addRow("Degrees of Freedom:", self.power_effect_df)
        # Hide rows initially
        power_effect_form.labelForField(self.power_effect_groups).setVisible(False)
        power_effect_form.labelForField(self.power_effect_predictors).setVisible(False)
        power_effect_form.labelForField(self.power_effect_df).setVisible(False)
        # Connect signal to update visibility
        self.power_effect_test_type.currentIndexChanged.connect(self.update_power_effect_inputs)


        power_effect_calc_btn = QPushButton("Calculate MDES")
        power_effect_calc_btn.clicked.connect(self.calc_mdes)

        self.power_effect_result = QLabel("Minimum Detectable Effect Size: N/A")
        self.power_effect_result.setObjectName("resultLabel")
        self.power_effect_result.setAlignment(Qt.AlignCenter)

        power_effect_container_layout.addLayout(power_effect_form)
        power_effect_container_layout.addWidget(power_effect_calc_btn, 0, Qt.AlignCenter)
        power_effect_container_layout.addWidget(self.power_effect_result)
        power_effect_container.setLayout(power_effect_container_layout)
        power_grid.addWidget(power_effect_container, 0, 1)


        power_layout.addLayout(power_grid)
        power_group.setLayout(power_layout)
        advanced_layout.addWidget(power_group)

        # Add other advanced sections here (e.g., Factor Analysis if implemented)

        advanced_layout.addStretch(1)

        # Set layout to scrollable area
        # advanced_tab_widget.setLayout(advanced_layout) # Layout already set
        scroll = self.create_scroll_area(advanced_tab_widget)

        # Add tab
        self.tabs.addTab(scroll, "Advanced / Power")

    # --- Helper methods to show/hide relevant inputs for Power Tab ---
    def update_power_level_inputs(self):
        test_type = self.power_level_test_type.currentText()
        is_anova = "ANOVA" in test_type
        is_regr = "Regression" in test_type
        is_chi = "Chi-Square" in test_type

        self.power_level_groups.setVisible(is_anova)
        self.sender().parent().layout().labelForField(self.power_level_groups).setVisible(is_anova) # Show/Hide label too
        self.power_level_predictors.setVisible(is_regr)
        self.sender().parent().layout().labelForField(self.power_level_predictors).setVisible(is_regr)
        self.power_level_df.setVisible(is_chi)
        self.sender().parent().layout().labelForField(self.power_level_df).setVisible(is_chi)

    def update_power_effect_inputs(self):
        test_type = self.power_effect_test_type.currentText()
        is_anova = "ANOVA" in test_type
        is_regr = "Regression" in test_type
        is_chi = "Chi-Square" in test_type

        self.power_effect_groups.setVisible(is_anova)
        self.sender().parent().layout().labelForField(self.power_effect_groups).setVisible(is_anova)
        self.power_effect_predictors.setVisible(is_regr)
        self.sender().parent().layout().labelForField(self.power_effect_predictors).setVisible(is_regr)
        self.power_effect_df.setVisible(is_chi)
        self.sender().parent().layout().labelForField(self.power_effect_df).setVisible(is_chi)


    # --- Placeholder Calculation Methods ---
    # You need to replace the logic within these methods with actual formulas.
    # Consider using libraries like statsmodels.stats.power

    def _get_z_scores(self, alpha, power, tails="Two-tailed"):
        """Helper to get Z scores for alpha and beta."""
        alpha_adjusted = alpha / 2 if tails == "Two-tailed" else alpha
        z_alpha = norm.ppf(1 - alpha_adjusted)
        z_beta = norm.ppf(power)
        return z_alpha, z_beta

    def calc_indep_t_sample(self):
        try:
            alpha = self.indep_t_alpha.value()
            power = self.indep_t_power.value()
            d = self.indep_t_effect.value()
            tails = "Two-tailed" # Assuming two-tailed for t-tests unless specified

            if d == 0:
                self.indep_t_result.setText("Effect size cannot be zero.")
                return

            z_alpha, z_beta = self._get_z_scores(alpha, power, tails)
            n = 2 * ((z_alpha + z_beta) / d) ** 2
            n_rounded = math.ceil(n) # Round up to nearest integer

            self.indep_t_result.setText(f"Sample size per group: {n_rounded} (Total N = {n_rounded * 2})")
        except Exception as e:
            self.indep_t_result.setText(f"Error: {e}")

    def calc_paired_t_sample(self):
        try:
            alpha = self.paired_t_alpha.value()
            power = self.paired_t_power.value()
            dz = self.paired_t_effect.value()
            tails = "Two-tailed"

            if dz == 0:
                self.paired_t_result.setText("Effect size cannot be zero.")
                return

            z_alpha, z_beta = self._get_z_scores(alpha, power, tails)
            n = ((z_alpha + z_beta) / dz) ** 2
            n_rounded = math.ceil(n) + 1 # Common adjustment for t-distribution approximation

            self.paired_t_result.setText(f"Number of pairs: {n_rounded}")
        except Exception as e:
            self.paired_t_result.setText(f"Error: {e}")

    def calc_one_t_sample(self):
        try:
            alpha = self.one_t_alpha.value()
            power = self.one_t_power.value()
            d = self.one_t_effect.value()
            tails = "Two-tailed"

            if d == 0:
                self.one_t_result.setText("Effect size cannot be zero.")
                return

            z_alpha, z_beta = self._get_z_scores(alpha, power, tails)
            n = ((z_alpha + z_beta) / d) ** 2
            n_rounded = math.ceil(n) + 1 # Common adjustment

            self.one_t_result.setText(f"Sample size: {n_rounded}")
        except Exception as e:
            self.one_t_result.setText(f"Error: {e}")

    def calc_oneway_sample(self):
        # Placeholder: ANOVA calculation is more complex, often uses non-central F distribution
        # Consider using statsmodels.stats.power.FTestAnovaPower().solve_power
        try:
            alpha = self.oneway_alpha.value()
            power = self.oneway_power.value()
            f_effect = self.oneway_effect.value()
            groups = self.oneway_groups.value()
            # This is a very rough approximation, replace with proper calculation
            from statsmodels.stats.power import FTestAnovaPower
            power_analyzer = FTestAnovaPower()
            n_per_group = power_analyzer.solve_power(effect_size=f_effect, nobs=None, alpha=alpha, power=power, k_groups=groups)
            n_rounded = math.ceil(n_per_group)
            self.oneway_result.setText(f"Sample size per group: {n_rounded} (Total N = {n_rounded * groups})")
            # self.oneway_result.setText("Calculation pending (use statsmodels)")
        except Exception as e:
            self.oneway_result.setText(f"Error: {e} (Requires statsmodels)")


    def calc_factorial_sample(self):
        # Placeholder: Factorial ANOVA is complex. Requires specific effect (main/interaction), df.
        try:
            alpha = self.factorial_alpha.value()
            power = self.factorial_power.value()
            f_effect = self.factorial_effect.value()
            num_df = self.factorial_num_df.value()
             # Need denominator df (depends on total N and design) - calculation is iterative or uses library
            self.factorial_result.setText("Complex calc - Total N: Pending")
        except Exception as e:
            self.factorial_result.setText(f"Error: {e}")

    def calc_pearson_sample(self):
        try:
            alpha = self.pearson_alpha.value()
            power = self.pearson_power.value()
            r = self.pearson_effect.value()
            tails = self.pearson_tails.currentText()

            if abs(r) >= 1:
                self.pearson_result.setText("Correlation must be between -1 and 1.")
                return

            z_alpha, z_beta = self._get_z_scores(alpha, power, tails)

            # Fisher's Z transformation
            z_r = 0.5 * math.log((1 + r) / (1 - r))
            if z_r == 0:
                 self.pearson_result.setText("Effect size (r) leads to zero z_r.")
                 return
                 
            n = ((z_alpha + z_beta) / z_r) ** 2 + 3
            n_rounded = math.ceil(n)

            self.pearson_result.setText(f"Sample size: {n_rounded}")
        except Exception as e:
            self.pearson_result.setText(f"Error: {e}")

    def calc_linear_reg_sample(self):
        # Placeholder: Uses non-central F distribution.
        # Consider statsmodels.stats.power.FTestPower().solve_power for R² test
        try:
            alpha = self.linear_reg_alpha.value()
            power = self.linear_reg_power.value()
            f2 = self.linear_reg_effect.value()
            predictors = self.linear_reg_predictors.value() # u (numerator df)

            # This requires iteration or specialized function (like G*Power or statsmodels)
            # Rough estimate using formula L = (z_alpha + z_beta)^2 / f2 (noncentrality param)
            # N approx = L + u + 1
            
            # Using statsmodels (simpler for R^2 test)
            # Need to relate f^2 to R^2: R^2 = f^2 / (1 + f^2)
            r2 = f2 / (1.0 + f2)
            
            # We need to calculate for the *increase* in R2 due to predictors of interest
            # Assuming f2 represents the effect for *all* predictors vs intercept-only model.
            # This assumes test of R2 = 0, num_df (u) = predictors
            
            # Placeholder using simplified approach (less accurate)
            z_alpha, z_beta = self._get_z_scores(alpha, power, "Two-tailed") # F-test is one-tailed on R2, but ppf uses cumulative prob
            L = ((z_alpha + z_beta)**2) / f2 # Approximate non-centrality parameter lambda
            n = L + predictors + 1
            n_rounded = math.ceil(n)

            self.linear_reg_result.setText(f"Total sample size (approx): {n_rounded}")
            # self.linear_reg_result.setText("Calc pending (use statsmodels FTestPower)")

        except Exception as e:
            self.linear_reg_result.setText(f"Error: {e}")

    def calc_logistic_reg_sample(self):
        # Placeholder: Various formulas exist (e.g., Hsieh et al., 1998). Very complex.
        try:
            alpha = self.logistic_reg_alpha.value()
            power = self.logistic_reg_power.value()
            odds_ratio = self.logistic_reg_odds_ratio.value()
            p1 = self.logistic_reg_p1.value()
            r2_other = self.logistic_reg_r2_other.value()

            if odds_ratio <= 1.0:
                 self.logistic_reg_result.setText("Odds Ratio must be > 1.")
                 return
            if not (0 < p1 < 1):
                 self.logistic_reg_result.setText("P(Y=1) must be between 0 and 1.")
                 return
            if not (0 <= r2_other < 1):
                 self.logistic_reg_result.setText("R² must be between 0 and < 1.")
                 return

            # Example using Hsieh formula for continuous predictor X1
            # Assumes X1 ~ Normal(0,1)
            z_alpha, z_beta = self._get_z_scores(alpha, power, "Two-tailed")
            beta1 = math.log(odds_ratio) # Log odds ratio
            n = ((z_alpha + z_beta)**2) / (p1 * (1 - p1) * beta1**2 * (1 - r2_other))
            n_rounded = math.ceil(n)

            self.logistic_reg_result.setText(f"Sample size (approx): {n_rounded}")
        except Exception as e:
            self.logistic_reg_result.setText(f"Error: {e}")

    def calc_chi_ind_sample(self):
        # Placeholder: Uses non-central Chi-square distribution.
        # Consider statsmodels.stats.power.ChiSquarePower().solve_power
        try:
            alpha = self.chi_ind_alpha.value()
            power = self.chi_ind_power.value()
            w = self.chi_ind_effect.value() # Cohen's w
            df = self.chi_ind_df.value()

            from statsmodels.stats.power import ChisqTestPower
            power_analyzer = ChisqTestPower()
            n = power_analyzer.solve_power(effect_size=w, nobs=None, alpha=alpha, power=power, ddf=df)
            n_rounded = math.ceil(n)

            self.chi_ind_result.setText(f"Total sample size: {n_rounded}")
            # self.chi_ind_result.setText("Calculation pending (use statsmodels)")
        except Exception as e:
            self.chi_ind_result.setText(f"Error: {e} (Requires statsmodels)")

    def calc_achieved_power(self):
        # Placeholder: Reverse calculation using statsmodels or similar
        try:
            test_type = self.power_level_test_type.currentText()
            alpha = self.power_level_alpha.value()
            n = self.power_level_n.value()
            effect = self.power_level_effect.value()
            # Get specific inputs based on test type
            groups = self.power_level_groups.value()
            predictors = self.power_level_predictors.value()
            df = self.power_level_df.value()

            # Call appropriate statsmodels function based on test_type
            # Example for Chi-Square:
            if "Chi-Square" in test_type:
                 from statsmodels.stats.power import ChisqTestPower
                 power_analyzer = ChisqTestPower()
                 achieved_power = power_analyzer.solve_power(effect_size=effect, nobs=n, alpha=alpha, power=None, ddf=df)
                 self.power_level_result.setText(f"Achieved Power (1-β): {achieved_power:.3f}")
            elif "T-Test (Independent)" in test_type:
                 from statsmodels.stats.power import TTestIndPower
                 power_analyzer = TTestIndPower()
                 # Note: nobs1 is sample size in *one* group
                 achieved_power = power_analyzer.solve_power(effect_size=effect, nobs1=n, alpha=alpha, power=None, ratio=1.0, alternative='two-sided')
                 self.power_level_result.setText(f"Achieved Power (1-β): {achieved_power:.3f}")
            # Add other cases for T-Paired, ANOVA, Corr, Regression
            else:
                self.power_level_result.setText("Power calc pending for this test type")

        except Exception as e:
            self.power_level_result.setText(f"Error: {e} (Requires statsmodels)")

    def calc_mdes(self):
        # Placeholder: Reverse calculation using statsmodels or similar
        try:
            test_type = self.power_effect_test_type.currentText()
            alpha = self.power_effect_alpha.value()
            power = self.power_effect_power.value()
            n = self.power_effect_n.value()
            # Get specific inputs
            groups = self.power_effect_groups.value()
            predictors = self.power_effect_predictors.value()
            df = self.power_effect_df.value()

            # Call appropriate statsmodels function
            # Example for Chi-Square:
            if "Chi-Square" in test_type:
                 from statsmodels.stats.power import ChisqTestPower
                 power_analyzer = ChisqTestPower()
                 mdes = power_analyzer.solve_power(effect_size=None, nobs=n, alpha=alpha, power=power, ddf=df)
                 self.power_effect_result.setText(f"Min Detectable Effect (w): {mdes:.3f}")
            elif "T-Test (Independent)" in test_type:
                 from statsmodels.stats.power import TTestIndPower
                 power_analyzer = TTestIndPower()
                 # Note: nobs1 is sample size in *one* group
                 mdes = power_analyzer.solve_power(effect_size=None, nobs1=n, alpha=alpha, power=power, ratio=1.0, alternative='two-sided')
                 self.power_effect_result.setText(f"Min Detectable Effect (d): {mdes:.3f}")
             # Add other cases
            else:
                 self.power_effect_result.setText("MDES calc pending for this test type")

        except Exception as e:
            self.power_effect_result.setText(f"Error: {e} (Requires statsmodels)")


# --- Main Execution Block ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Optional: Apply a fusion style for more modern look across platforms
    # app.setStyle('Fusion')
    
    calculator = SampleSizeCalculator()
    calculator.show()
    sys.exit(app.exec_())