#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Iris - A Minimalist Whiteboard Application
#
# Copyright (C) 2025 SparkofPrometheus
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QColorDialog,
    QHBoxLayout, QVBoxLayout, QLabel, QSlider, QFileDialog
)
from PyQt5.QtGui import (
    QPainter, QPen, QColor, QPixmap, QCursor, QImage, QBrush, QLinearGradient
)
from PyQt5.QtCore import Qt, QPoint, QRect


class Canvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StaticContents)
        self.setFixedSize(1500, 700)
        self.image = QPixmap(self.size())
        self.image.fill(Qt.transparent)

        # Load whiteboard paper background
        paper = QPixmap('assets/whiteboardpaper.jpg')
        if not paper.isNull():
            self.image = paper.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        self.drawing = False
        self.lastPoint = QPoint()

        # Default settings
        self.pen_color = QColor('#000000')  # Black
        self.pen_width = 3
        self.eraser_mode = False

    def set_pen_color(self, color):
        self.pen_color = QColor(color)
        self.eraser_mode = False
        self.update_cursor()

    def set_pen_width(self, width):
        self.pen_width = width

    def set_eraser_mode(self, mode=True):
        self.eraser_mode = mode
        self.update_cursor()

    def update_cursor(self):
        if self.eraser_mode:
            cursor_pix = QPixmap('assets/cursor.png')  # Replace with eraser cursor if available
        else:
            cursor_pix = QPixmap('assets/cursor.png')  # Replace with pen cursor if available
        if not cursor_pix.isNull():
            self.setCursor(QCursor(cursor_pix, 16, 16))
        else:
            self.setCursor(Qt.CrossCursor)

    def clear_canvas(self):
        self.image.fill(Qt.transparent)
        # Reload background
        paper = QPixmap('assets/whiteboardpaper.jpg')
        if not paper.isNull():
            self.image = paper.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.update()

    def save_as_png(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG Files (*.png)")
        if file_path:
            self.image.save(file_path, "PNG")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.image)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) and self.drawing:
            painter = QPainter(self.image)
            if self.eraser_mode:
                pen = QPen(Qt.transparent, self.pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
                painter.setCompositionMode(QPainter.CompositionMode_Clear)
            else:
                pen = QPen(self.pen_color, self.pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
                painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
            painter.setPen(pen)
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False


class Toolbar(QWidget):
    def __init__(self, canvas, parent=None):
        super().__init__(parent)
        self.canvas = canvas
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        # Color palette
        self.colors = [
            '#000000', '#ffffff', '#ff0000', '#0000ff',
            '#00ff00', '#ffa500', '#ffff00', '#800080',
            '#ffc0cb', '#a52a2a', '#808080', '#ffd700'
        ]

        colors_container = QHBoxLayout()
        self.color_buttons = []
        for color in self.colors:
            btn = QPushButton()
            btn.setFixedSize(25, 25)
            btn.setStyleSheet(f"background-color: {color}; border: 2px solid #ccc; border-radius: 12px;")
            btn.clicked.connect(lambda checked, col=color, button=btn: self.select_color(col, button))
            colors_container.addWidget(btn)
            self.color_buttons.append(btn)
        layout.addLayout(colors_container)

        # Highlight the first color as active by default
        self.color_buttons[0].setStyleSheet(f"background-color: {self.colors[0]}; border: 2px solid #000; border-radius: 12px;")
        self.canvas.set_pen_color(self.colors[0])

        # Brush size slider
        brush_label = QLabel("Brush Size:")
        layout.addWidget(brush_label)

        self.brush_slider = QSlider(Qt.Horizontal)
        self.brush_slider.setMinimum(1)
        self.brush_slider.setMaximum(13)
        self.brush_slider.setValue(3)
        self.brush_slider.valueChanged.connect(self.change_brush_size)
        layout.addWidget(self.brush_slider)

        # Eraser Button
        self.eraser_btn = QPushButton("Eraser (26px)")
        self.eraser_btn.clicked.connect(self.activate_eraser)
        layout.addWidget(self.eraser_btn)

        # Marker Button
        self.marker_btn = QPushButton("Marker")
        self.marker_btn.clicked.connect(self.deactivate_eraser)
        layout.addWidget(self.marker_btn)

        # Clear Button
        self.clear_btn = QPushButton("Clear All")
        self.clear_btn.clicked.connect(self.canvas.clear_canvas)
        layout.addWidget(self.clear_btn)

        # Save Button
        self.save_btn = QPushButton("Save as PNG")
        self.save_btn.clicked.connect(self.canvas.save_as_png)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

    def select_color(self, color, btn):
        # Reset all buttons
        for button in self.color_buttons:
            current_color = button.styleSheet().split(';')[0].split(':')[1].strip()
            button.setStyleSheet(f"background-color: {current_color}; border: 2px solid #ccc; border-radius: 12px;")
        # Highlight selected button
        btn.setStyleSheet(f"background-color: {color}; border: 2px solid #000; border-radius: 12px;")
        self.canvas.set_pen_color(color)

    def change_brush_size(self, value):
        self.canvas.set_pen_width(value)
        if not self.canvas.eraser_mode:
            self.canvas.pen_width = value

    def activate_eraser(self):
        self.canvas.set_pen_width(26)
        self.canvas.set_eraser_mode(True)
        # Update button styles
        self.eraser_btn.setStyleSheet("background-color: #ddd;")
        self.marker_btn.setStyleSheet("")

    def deactivate_eraser(self):
        self.canvas.set_eraser_mode(False)
        # Reset to current brush size
        self.canvas.set_pen_width(self.brush_slider.value())
        # Update button styles
        self.marker_btn.setStyleSheet("background-color: #ddd;")
        self.eraser_btn.setStyleSheet("")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Iris - Whiteboard")
        self.setGeometry(100, 100, 1520, 800)
        self.init_ui()

    def init_ui(self):
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Set background with gradient and image
        palette = central_widget.palette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(255, 255, 255, 180))  # rgba(255,255,255,0.7)
        gradient.setColorAt(1, QColor(0, 0, 0, 204))        # rgba(0,0,0,0.8)
        brush = QBrush(gradient)
        palette.setBrush(central_widget.backgroundRole(), brush)
        # Overlay sand background
        sand_pix = QPixmap('assets/sand2.jpg')
        if not sand_pix.isNull():
            sand_scaled = sand_pix.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            palette.setBrush(central_widget.backgroundRole(), QBrush(sand_scaled))
        central_widget.setPalette(palette)
        central_widget.setAutoFillBackground(True)

        # Toolbar
        self.canvas = Canvas()
        toolbar = Toolbar(self.canvas)
        main_layout.addWidget(toolbar)

        # Canvas
        main_layout.addWidget(self.canvas, alignment=Qt.AlignCenter)

        # Set margins and spacing
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
